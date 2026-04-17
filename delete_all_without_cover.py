import os
import pandas as pd

COVERS_DIR = "booksite/public/covers"

def has_cover(book_id: int) -> bool:
    prefix = f"book_{book_id}."
    for fname in os.listdir(COVERS_DIR):
        if fname.startswith(prefix):
            return True
    return False


def filter_books_with_covers(csv_path: str, output_path: str):
    df = pd.read_csv(csv_path)

    keep_rows = []

    for _, row in df.iterrows():
        book_id = row["id"]

        if has_cover(book_id):
            keep_rows.append(row)
            print(f"[KEEP] {book_id} — cover exists")
        else:
            print(f"[REMOVE] {book_id} — no cover")

    new_df = pd.DataFrame(keep_rows)
    new_df.to_csv(output_path, index=False)

    print(f"\nSaved filtered table to: {output_path}")
    print(f"Remaining books: {len(new_df)}")


# Запуск
filter_books_with_covers("books.csv", "books_with_covers.csv")
