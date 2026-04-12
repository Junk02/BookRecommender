import pandas as pd
import re

df = pd.read_csv("books_no_volumes.csv")

# Маска: есть ли скобки в названии
mask_remove = df["title"].astype(str).str.contains(r"\(", regex=True)

df_removed = df[mask_remove]
df_clean   = df[~mask_remove]

df_clean.to_csv("books.csv", index=False)
df_removed.to_csv("books_removed_parentheses.csv", index=False)

print("Всего книг:", len(df))
print("Удалено:", len(df_removed))
print("Осталось:", len(df_clean))
