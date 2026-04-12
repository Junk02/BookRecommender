import pandas as pd
import numpy as np

# Загружаем основной файл
books = pd.read_csv("items_with_desc.csv")  # id, title, authors, year, description, genres

# Загружаем взаимодействия
inter = pd.read_csv("mts_dataset/interactions.csv")  # item_id, rating, user_id, timestamp ...

# Считаем количество читателей (все упоминания item_id)
read_counts = inter.groupby("item_id").size().rename("readers_count")

# Считаем средний рейтинг (rating != 0)
ratings = (
    inter[inter["rating"] != 0]
    .groupby("item_id")["rating"]
    .mean()
    .rename("avg_rating")
)

# Объединяем всё в одну таблицу
books = books.merge(read_counts, how="left", left_on="id", right_on="item_id")
books = books.merge(ratings, how="left", left_on="id", right_on="item_id")

# Удаляем служебные колонки item_id
books = books.drop(columns=["item_id_x", "item_id_y"], errors="ignore")

# Если книги никто не читал → readers_count = 0
books["readers_count"] = books["readers_count"].fillna(0).astype(int)

# Если нет оценок → avg_rating = None
books["avg_rating"] = books["avg_rating"].astype(float)

# Сохраняем
books.to_csv("books_with_stats.csv", index=False)
