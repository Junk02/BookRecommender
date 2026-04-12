import pandas as pd
import re

df = pd.read_csv("books.csv")

# Регулярка для поиска томов/книг/частей
VOLUME_PATTERN = re.compile(
    r'\b(том|книга|часть|volume|vol\.?|book)\s*[0-9IVXLC]+\b',
    flags=re.IGNORECASE
)

def has_volume_info(title: str) -> bool:
    if not isinstance(title, str):
        return False
    return bool(VOLUME_PATTERN.search(title))

# Маска: книги, которые нужно удалить
mask_remove = df["title"].apply(has_volume_info)

df_removed = df[mask_remove]
df_clean   = df[~mask_remove]

df_clean.to_csv("books_no_volumes.csv", index=False)
df_removed.to_csv("books_removed_volumes.csv", index=False)

print("Всего книг:", len(df))
print("Удалено:", len(df_removed))
print("Осталось:", len(df_clean))
