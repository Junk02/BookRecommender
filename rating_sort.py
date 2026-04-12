import pandas as pd

books = pd.read_csv("items_with_desc.csv")

# Сортировка: сначала по рейтингу (по убыванию), потом по количеству читателей
books_sorted = books.sort_values(
    by=["avg_rating", "readers_count"],
    ascending=[False, False]
)

books_sorted.to_csv("items_with_desc.csv", index=False)
