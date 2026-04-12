import pandas as pd

df = pd.read_csv("books.csv")

# Маска: строки, где есть битый символ �
mask_bad_unicode = df["title"].astype(str).str.contains("�")

df_removed = df[mask_bad_unicode]
df_clean   = df[~mask_bad_unicode]

df_clean.to_csv("books.csv", index=False)
df_removed.to_csv("books_removed_broken_unicode.csv", index=False)

print("Удалено из-за битого Unicode:", len(df_removed))
