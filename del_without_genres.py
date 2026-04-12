import pandas as pd

df = pd.read_csv("books_filtered.csv")

# Маска "плохих" жанров: NaN ИЛИ пустая строка/пробелы
mask_bad_genres = df["genres"].isna() | df["genres"].astype(str).str.strip().eq("")

df_bad  = df[mask_bad_genres]
df_good = df[~mask_bad_genres]

df_good.to_csv("books_filtered.csv", index=False)
df_bad.to_csv("books_removed_no_genres.csv", index=False)

print("Всего книг:", len(df))
print("Без жанров (удалено):", len(df_bad))
print("Осталось:", len(df_good))
