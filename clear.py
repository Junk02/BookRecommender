import re
import pandas as pd

def clean_leading_garbage(text):
    if not isinstance(text, str):
        return text

    # 1. Заменяем все нестандартные пробелы на обычные
    text = re.sub(r'[\u00A0\u202F\u2007\u2009\u200A]', ' ', text)

    # 2. Удаляем лидирующие # и пробелы после них
    text = re.sub(r'^\s*#+\s*', '', text)

    # 3. Удаляем просто лидирующие пробелы (если остались)
    text = text.lstrip()

    # 4. Убираем двойные пробелы
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


df = pd.read_csv("books_no_volumes.csv")

df["title"] = df["title"].apply(clean_leading_garbage)

df.to_csv("books_clean.csv", index=False)

