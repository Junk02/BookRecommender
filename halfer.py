import pandas as pd
import random

SELFHELP_KEYWORDS = [
    "научная фантастика"
]

def is_selfhelp(text: str) -> bool:
    if not isinstance(text, str):
        return False
    t = text.lower()
    return any(kw in t for kw in SELFHELP_KEYWORDS)

df = pd.read_csv("books_filtered.csv")

# Находим все книги, которые попадают под фильтр
mask_all = df.apply(
    lambda row: (
        is_selfhelp(str(row.get("title", ""))) or
        is_selfhelp(str(row.get("authors", ""))) or
        is_selfhelp(str(row.get("genres", "")))
    ),
    axis=1
)

df_candidates = df[mask_all]          # книги, которые можно удалить
df_safe = df[~mask_all]               # книги, которые точно оставляем

# Выбираем случайную половину кандидатов
df_to_remove = df_candidates.sample(frac=0.5, random_state=42)
df_to_keep = df_candidates.drop(df_to_remove.index)

# Объединяем оставшиеся книги
df_final = pd.concat([df_safe, df_to_keep], ignore_index=True)

df_final.to_csv("books_filtered.csv", index=False)
df_to_remove.to_csv("books_removed_half.csv", index=False)

print("Всего книг:", len(df))
print("Кандидатов на удаление:", len(df_candidates))
print("Удалено (половина):", len(df_to_remove))
print("Осталось:", len(df_final))
