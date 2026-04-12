import time
import pandas as pd
from llm import get_description

INPUT_CSV = "books.csv"
OUTPUT_CSV = "books.csv"

MAX_TO_PROCESS = 100   # лимит генераций за запуск


def main():
    df = pd.read_csv(INPUT_CSV)

    # если колонки description нет — создаём
    if "description" not in df.columns:
        df["description"] = ""

    total = len(df)

    # ---------- ШАГ 1: считаем уже существующие описания ----------
    def has_desc(x: str) -> bool:
        if not isinstance(x, str):
            return False
        x = x.strip().lower()
        return x not in ("", "nan", "null", "none")

    already_done = df["description"].apply(has_desc).sum()

    print(f"Всего записей: {total}")
    print(f"Уже есть описаний: {already_done}")

    generated = 0  # сколько новых описаний мы создали

    # ---------- ШАГ 2: основной цикл ----------
    for idx, row in df.iterrows():

        # если достигли лимита генераций — стоп
        if generated >= MAX_TO_PROCESS:
            print(f"\n[INFO] Достигнут лимит генераций {MAX_TO_PROCESS}. Останавливаюсь.")
            break

        title = str(row.get("title", "")).strip()
        authors = str(row.get("authors", "")).strip()
        existing = str(row.get("description", "")).strip().lower()

        # пропускаем, если описание уже есть
        if has_desc(existing):
            continue

        if not title:
            print(f"[SKIP] idx={idx}: нет названия")
            continue

        print(f"[{generated+1}/{MAX_TO_PROCESS}] Генерирую: «{title}»")

        # пробуем несколько раз
        desc = None
        for attempt in range(3):
            try:
                desc = get_description(title, authors)
                print("DEBUG DESC:", repr(desc))

                if desc and "Описание недоступно" not in desc:
                    break

            except Exception as e:
                print(f"[WARN] Ошибка LLM: {repr(e)}. Попытка {attempt+1}/3")
                time.sleep(3)

        if not desc:
            print(f"[FAIL] Не удалось получить описание для «{title}»")
            continue

        # записываем описание
        df.at[idx, "description"] = desc
        generated += 1
        print(f"[OK] Описание получено")

        # промежуточное сохранение
        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
        print(f"[SAVE] Промежуточное сохранение ({generated} новых описаний)")

        time.sleep(1)

    # финальное сохранение
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nГотово! Создано новых описаний: {generated}")
    print(f"Файл сохранён: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
