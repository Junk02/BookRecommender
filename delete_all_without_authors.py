import pandas as pd

df = pd.read_csv("books_filtered.csv")

# Маска "плохих" авторов: NaN ИЛИ пустая строка/пробелы
mask_bad_authors = df["authors"].isna() | df["authors"].astype(str).str.strip().eq("")

df_bad  = df[mask_bad_authors]
df_good = df[~mask_bad_authors]

df_good.to_csv("books.csv", index=False)
df_bad.to_csv("books_removed_no_authors.csv", index=False)

print("Всего книг:", len(df))
print("Без авторов (удалено):", len(df_bad))
print("Осталось:", len(df_good))
