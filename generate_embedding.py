import pandas as pd
import json
from sentence_transformers import SentenceTransformer

INPUT_CSV = "books1.csv"
OUTPUT_CSV = "books_with_embeddings.csv"


def normalize_description(desc: str) -> str:
    if not isinstance(desc, str):
        return ""
    return " ".join(desc.split()).strip()


def main():
    print("Загружаю таблицу...")
    df = pd.read_csv(INPUT_CSV)
    total = len(df)
    print(f"Всего книг в исходном CSV: {total}")

    # создаём колонку, если её нет
    if "embedding" not in df.columns:
        df["embedding"] = ""

    # приводим к object, чтобы спокойно класть строки
    df["embedding"] = df["embedding"].astype("object")

    print("Загружаю модель эмбеддингов...")
    model = SentenceTransformer("BAAI/bge-m3")

    empty_desc_count = 0
    skipped_existing = 0
    encoded_count = 0

    for idx in range(total):
        row = df.iloc[idx]

        # если эмбеддинг уже есть — пропускаем
        if isinstance(row["embedding"], str) and row["embedding"].strip():
            skipped_existing += 1
            continue

        desc = normalize_description(row.get("description", ""))

        if not desc:
            empty_desc_count += 1
            continue

        print(f"[{idx + 1}/{total}] Генерирую эмбеддинг...")

        emb = model.encode(desc, normalize_embeddings=True)
        df.at[idx, "embedding"] = json.dumps(emb.tolist())
        encoded_count += 1

        if encoded_count % 100 == 0:
            df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
            print(f"[SAVE] Промежуточное сохранение, сгенерировано {encoded_count} эмбеддингов")

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print("\nГотово!")
    print(f"Всего строк в итоговом CSV: {len(df)}")
    print(f"Сгенерировано эмбеддингов: {encoded_count}")
    print(f"Пропущено (эмбеддинг уже был): {skipped_existing}")
    print(f"Пропущено (пустой description): {empty_desc_count}")


if __name__ == "__main__":
    main()
