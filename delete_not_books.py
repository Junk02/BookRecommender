import re
import pandas as pd

OTHER_TRASH = [
    "каталог", "отчет", "документация", "руководство", "manual",
    "инструкция", "справочник"
]

TECH_KEYWORDS = [
    "windows", "word", "excel", "office", "linux", "ubuntu", "adobe",
    "photoshop", "corel", "autocad", "visual basic", "c#", "c++", "java",
    "python", "sql", "oracle", "1с", "программирование", "it", "сетевое",
    "администрирование", "компьютер", "пк", "интернет"
]

MAGAZINE_KEYWORDS = [
    "vogue", "forbes", "cosmopolitan", "men's health", "playboy",
    "газета", "журнал", "еженедельник", "ежемесячник", "выпуск",
    "№", "номер", "issue", "magazine"
]

EDU_KEYWORDS = [
    "огэ", "егэ", "гдз", "учебник", "пособие", "методичка",
    "тесты", "задания", "подготовка", "шпаргалка"
]


def is_trash(text: str) -> bool:
    if not isinstance(text, str):
        return False

    t = text.lower()

    # Проверка по ключевым словам
    for kw in TECH_KEYWORDS + MAGAZINE_KEYWORDS + EDU_KEYWORDS + OTHER_TRASH:
        if kw in t:
            return True

    # Детектор странного языка (мало букв)
    letters = re.findall(r"[A-Za-zА-Яа-я]", t)
    if len(letters) / max(len(t), 1) < 0.3:
        return True

    # Детектор журналов по датам
    if re.search(r"\b\d{1,2}[-/]\d{4}\b", t):
        return True

    return False


# Загружаем книги
df = pd.read_csv("books_clean.csv")

# Проверяем каждую книгу
df["is_trash"] = df.apply(
    lambda row: is_trash(str(row["title"])) or is_trash(str(row["authors"])),
    axis=1
)

# Разделяем
df_good = df[df["is_trash"] == False].drop(columns=["is_trash"])
df_bad  = df[df["is_trash"] == True].drop(columns=["is_trash"])

# Сохраняем
df_good.to_csv("books_filtered.csv", index=False)
df_bad.to_csv("books_removed.csv", index=False)

print("Всего книг:", len(df))
print("Удалено:", len(df_bad))
print("Оставлено:", len(df_good))
