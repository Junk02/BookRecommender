import pandas as pd

books = pd.read_csv("items_with_desc.csv")

# Округляем avg_rating до 1 знака после запятой
books["avg_rating"] = books["avg_rating"].round(1)

books.to_csv("books_with_stats.csv", index=False)
