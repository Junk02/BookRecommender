import pandas as pd
import re

# Загружаем таблицу
books = pd.read_csv("items_with_desc.csv")

def remove_volume_info(title: str) -> str:
    """
    Удаляет упоминания томов/частей из названия:
    'Том 1', 'Том I', 'Том III', 'Часть 2', 'Книга 3', 'Book One', 'Volume II'
    """
    if not isinstance(title, str):
        return title

    # Удаляем конструкции вида "Том X", "Часть X", "Книга X", "Volume X", "Book X"
    cleaned = re.sub(
        r'(\s*[\.\-–—]?\s*(Том|Часть|Книга|Volume|Vol\.?|Book)\s*[IVXLC0-9]+)',
        '',
        title,
        flags=re.IGNORECASE
    )

    # Удаляем двойные пробелы
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned


# Создаём колонку с нормализованным названием
books["normalized_title"] = books["title"].apply(remove_volume_info)

# Группируем по нормализованному названию
# Оставляем только первую запись (обычно это том 1 или базовое название)
books_unique = books.sort_values("id").groupby("normalized_title").first().reset_index()

# Удаляем служебную колонку
books_unique = books_unique.drop(columns=["normalized_title"])

# Сохраняем результат
books_unique.to_csv("books_no_volumes.csv", index=False)

print("Готово! Количество книг до:", len(books), "после:", len(books_unique))
