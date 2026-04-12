import pandas as pd
from collections import Counter

df = pd.read_csv("books.csv")

# ---------- ШАГ 1: считаем частоту жанров ----------
genre_counter = Counter()

for genres in df["genres"].astype(str):
    parts = genres.split(",")
    for g in parts:
        g = g.strip().lower()
        if g and g != "nan":
            genre_counter[g] += 1

# ---------- ШАГ 2: вычисляем "вес" жанров для каждой книги ----------
def genre_score(genres_str: str) -> int:
    parts = genres_str.split(",")
    scores = []
    for g in parts:
        g = g.strip().lower()
        if g in genre_counter:
            scores.append(genre_counter[g])
    return max(scores) if scores else 0

df["genre_score"] = df["genres"].astype(str).apply(genre_score)

# ---------- ШАГ 3: сортируем книги ----------
df_sorted = df.sort_values("genre_score", ascending=False)

# ---------- ШАГ 4: сохраняем ----------
df_sorted.to_csv("books_sorted_by_genres.csv", index=False)

print("Готово! Книги отсортированы по популярности жанров.")
