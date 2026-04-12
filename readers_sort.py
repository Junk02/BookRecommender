import pandas as pd

books = pd.read_csv("items_with_desc.csv")

# Сортировка по количеству читателей (по убыванию)
books_sorted = books.sort_values(
    by=["readers_count", "avg_rating"],
    ascending=[False, False]
)

books_sorted.to_csv("items_with_desc.csv", index=False)
