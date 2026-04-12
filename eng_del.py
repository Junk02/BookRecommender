import pandas as pd
import re

def is_english_title(title: str) -> bool:
    if not isinstance(title, str):
        return False

    latin = len(re.findall(r"[A-Za-z]", title))
    cyril = len(re.findall(r"[А-Яа-я]", title))

    # Если латиницы намного больше — это английский
    return latin > 0 and latin > cyril * 2

df = pd.read_csv("books.csv")

mask_bad_unicode = df["title"].astype(str).str.contains("�")
mask_english = df["title"].apply(is_english_title)

mask_remove = mask_bad_unicode | mask_english

df_removed = df[mask_remove]
df_clean   = df[~mask_remove]

df_clean.to_csv("books_clean_stage3.csv", index=False)
df_removed.to_csv("books_removed_stage3.csv", index=False)

print("Удалено всего:", len(df_removed))
