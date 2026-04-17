import os
import pandas as pd

COVERS_DIR = "booksite/public/covers"
INPUT_CSV = "books.csv"
OUTPUT_CSV = "books_with_covers.csv"

def has_cover(book_id: int) -> bool:
    prefix = f"book_{book_id}."
    for fname in os.listdir(COVERS_DIR):
        if fname.startswith(prefix):
            return True
    return False

def main():
    df = pd.read_csv(INPUT_CSV)

    keep_rows = []

    for _, row in df.iterrows():
        book_id = row["id"]

        if has_cover(book_id):
            keep_rows.append(row)
        # если нет — просто не добавляем

    new_df = pd.DataFrame(keep_rows)
    new_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print(f"Готово. Сохранено {len(new_df)} книг в {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
