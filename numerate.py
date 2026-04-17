import pandas as pd

INPUT = "books.csv"
OUTPUT = "books.csv"   # можешь поменять, если хочешь сохранить в новый файл

df = pd.read_csv(INPUT)

# создаём колонку id: 0, 1, 2, 3, ...
df["id"] = range(len(df))

df.to_csv(OUTPUT, index=False, encoding="utf-8")

print("Готово! Добавлена колонка id.")
