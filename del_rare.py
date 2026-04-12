import pandas as pd
from collections import Counter

df = pd.read_csv("books_filtered.csv")

# ---------- ШАГ 1: считаем жанры ----------
genre_counter = Counter()

for genres in df["genres"].astype(str):
    parts = genres.split(",")
    for g in parts:
        g = g.strip().lower()
        if g and g != "nan":
            genre_counter[g] += 1

# Жанры, которые встречаются меньше 20 раз
rare_genres = {genre for genre, count in genre_counter.items() if count < 20}

print("Редких жанров (<20 книг):", len(rare_genres))

# ---------- ШАГ 2: удаляем книги с редкими жанрами ----------
def has_rare_genre(genres_str: str) -> bool:
    parts = genres_str.split(",")
    for g in parts:
        g = g.strip().lower()
        if g in rare_genres:
            return True
    return False

mask_remove = df["genres"].astype(str).apply(has_rare_genre)

df_removed = df[mask_remove]
df_clean = df[~mask_remove]

df_clean.to_csv("books_filtered.csv", index=False)
df_removed.to_csv("books_removed_rare_genres.csv", index=False)

print("Всего книг:", len(df))
print("Удалено книг с редкими жанрами:", len(df_removed))
print("Осталось:", len(df_clean))
