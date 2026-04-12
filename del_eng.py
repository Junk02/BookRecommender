import pandas as pd
import re

# Разрешённые символы:
# - кириллица
# - цифры
# - пробелы
# - пунктуация
# - дефисы, кавычки
ALLOWED_PATTERN = re.compile(r"^[а-яёА-ЯЁ0-9\s\.,!?:;\"'«»\-\(\)\[\]…]+$")

def is_not_russian_strict(text: str) -> bool:
    if not isinstance(text, str):
        return True

    text = text.strip()

    # Пустые строки считаем мусором
    if text == "":
        return True

    # Если строка НЕ соответствует разрешённому набору символов → удалить
    return not bool(ALLOWED_PATTERN.match(text))


df = pd.read_csv("books_filtered.csv")

mask_remove = df.apply(
    lambda row: (
        is_not_russian_strict(str(row.get("title", ""))) or
        is_not_russian_strict(str(row.get("authors", ""))) or
        is_not_russian_strict(str(row.get("genres", "")))
    ),
    axis=1
)

df_removed = df[mask_remove]
df_clean = df[~mask_remove]

df_clean.to_csv("books_russian_only_strict.csv", index=False)
df_removed.to_csv("books_removed_non_russian_strict.csv", index=False)

print("Всего книг:", len(df))
print("Удалено:", len(df_removed))
print("Осталось:", len(df_clean))
