import pandas as pd
import re


def clean_spaces(text):
    if not isinstance(text, str):
        return text
    # заменяем все нестандартные пробелы на обычный
    text = re.sub(r'[\u00A0\u202F\u2007\u2009\u200A]', ' ', text)
    # убираем двойные пробелы
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
df = pd.read_csv("books_no_volumes.csv")

for col in ["title", "authors", "description"]:
    df[col] = df[col].apply(clean_spaces)

df.to_csv("books_no_volumes.csv", index=False)
