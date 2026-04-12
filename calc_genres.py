import pandas as pd
from collections import Counter

df = pd.read_csv("books_filtered.csv")

total_books = len(df)

genre_counter = Counter()

for genres in df["genres"].astype(str):
    parts = genres.split(",")
    for g in parts:
        g = g.strip().lower()
        if g and g != "nan":
            genre_counter[g] += 1

# Сортируем по убыванию
sorted_genres = sorted(genre_counter.items(), key=lambda x: x[1], reverse=True)

# Определяем максимальную длину жанра для выравнивания
max_len = max(len(genre) for genre, _ in sorted_genres)

with open("genres_stats.txt", "w", encoding="utf-8") as f:
    for genre, count in sorted_genres:
        percent = (count / total_books) * 100
        f.write(f"{genre.ljust(max_len)}\t— {str(count).rjust(5)}\t({percent:5.2f}%)\n")

print("Готово! Жанры записаны в genres_stats.txt")
