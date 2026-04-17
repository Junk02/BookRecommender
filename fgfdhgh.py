import pandas as pd

INPUT_CSV = "books_with_covers.csv"
OUTPUT_CSV = "books_desc_filtered.csv"

def main():
    df = pd.read_csv(INPUT_CSV)

    # приводим description к строке
    df["description"] = df["description"].astype(str)

    # оставляем только те строки, где description начинается с "жанр"
    mask = df["description"].str.strip().str.lower().str.startswith("жанр")

    df_filtered = df[mask]

    print("Всего книг:", len(df))
    print("Осталось после фильтра:", len(df_filtered))
    print("Удалено:", len(df) - len(df_filtered))

    df_filtered.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print("Готово:", OUTPUT_CSV)


if __name__ == "__main__":
    main()
