import time
import pandas as pd
import winsound  # встроенная библиотека Windows
from llm import get_description

INPUT_CSV = "books_with_covers.csv"
OUTPUT_CSV = "books_with_covers.csv"

MAX_TO_PROCESS = 200


def beep_error():
    # громкий системный звук
    winsound.Beep(1000, 700)
    winsound.Beep(700, 700)


def main():
    df = pd.read_csv(INPUT_CSV)

    if "description" not in df.columns:
        df["description"] = ""

    total = len(df)

    def has_desc(x: str) -> bool:
        if not isinstance(x, str):
            return False
        x = x.strip().lower()
        return x not in ("", "nan", "null", "none")

    already_done = df["description"].apply(has_desc).sum()

    print(f"Всего записей: {total}")
    print(f"Уже есть описаний: {already_done}")

    generated = 0

    for idx, row in df.iterrows():

        if generated >= MAX_TO_PROCESS:
            print(f"\n[INFO] Достигнут лимит генераций {MAX_TO_PROCESS}. Останавливаюсь.")
            break

        title = str(row.get("title", "")).strip()
        authors = str(row.get("authors", "")).strip()
        existing = str(row.get("description", "")).strip().lower()

        if has_desc(existing):
            continue

        if not title:
            print(f"[SKIP] idx={idx}: нет названия")
            continue

        print(f"[{generated+1}/{MAX_TO_PROCESS}] Генерирую: «{title}»")

        desc = None

        for attempt in range(3):
            try:
                desc = get_description(title, authors)
                print("DEBUG DESC:", repr(desc))

                if desc and "Описание недоступно" not in desc:
                    break

            except Exception as e:
                print(f"[ERROR] Ошибка LLM: {repr(e)}")
                print("[STOP] Останавливаю программу.")
                beep_error()
                return  # ← мгновенная остановка программы

            time.sleep(2)

        if not desc:
            print(f"[ERROR] Не удалось получить описание для «{title}»")
            print("[STOP] Останавливаю программу.")
            beep_error()
            return

        df.at[idx, "description"] = desc
        generated += 1
        print(f"[OK] Описание получено")

        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
        print(f"[SAVE] Промежуточное сохранение ({generated} новых описаний)")

        time.sleep(1)

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nГотово! Создано новых описаний: {generated}")
    print(f"Файл сохранён: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
