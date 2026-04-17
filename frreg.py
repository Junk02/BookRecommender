import pandas as pd

df = pd.read_csv("books.csv")

# гарантируем, что колонка существует и строковая
df["book_description"] = df["book_description"].astype(str)

# берём описание первой книги
first_desc = df.loc[0, "book_description"]

print("Описание первой книги:")
print(first_desc)

# копируем всем
df["book_description"] = first_desc

# сохраняем в новый файл
df.to_csv("books_with_copied_descriptions.csv", index=False, encoding="utf-8")

print("Готово! Все описания заменены на описание первой книги.")
