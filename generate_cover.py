import os
import time
import requests
import pandas as pd
import winsound
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.parse
import re

INPUT_CSV = "books.csv"
OUTPUT_CSV = "books.csv"

COVERS_DIR = "booksite/public/covers"
MAX_TO_PROCESS = 500


def beep_error():
    winsound.Beep(1000, 700)
    winsound.Beep(700, 700)


def normalize(s: str) -> str:
    if not s:
        return ""
    s = s.lower().strip()
    s = s.replace("ё", "е")
    s = re.sub(r"[^a-zа-я0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def find_cover_labirint(title: str, author: str = "") -> str | None:
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "ru-RU,ru;q=0.9"
    }

    # Поисковый запрос: только название
    query = urllib.parse.quote(title)
    url = f"https://www.labirint.ru/search/{query}/?stype=0"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] Labirint status {resp.status_code}")
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # Берём первые 5 карточек
        products = soup.find_all("div", class_="product-card", limit=5)
        if not products:
            print("[INFO] Книги не найдены")
            return None

        title_norm = normalize(title)
        author_norm = normalize(author)

        for product in products:
            found_name = normalize(product.get("data-name", ""))

            if title_norm not in found_name:
                continue

            if author_norm:
                author_block = product.find("div", class_="product-card__author")
                found_author = ""

                if author_block:
                    found_author = normalize(author_block.get_text(" ", strip=True))

                author_parts = author_norm.split()

                if not any(part in found_author for part in author_parts):
                    print(f"[SKIP] Автор не совпал: '{found_author}' != '{author_norm}'")
                    continue

            img = product.find("img", class_="book-img-cover")
            if not img:
                continue

            cover_url = img.get("data-src") or img.get("src")
            if not cover_url:
                continue

            if cover_url.startswith("//"):
                cover_url = "https:" + cover_url
            elif cover_url.startswith("/"):
                cover_url = "https://www.labirint.ru" + cover_url

            return cover_url

        print("[SKIP] Нет совпадений по названию/автору")
        return None

    except Exception as e:
        print(f"[ERROR] Ошибка при запросе Лабиринта: {e}")
        return None


def main():
    os.makedirs(COVERS_DIR, exist_ok=True)

    existing_ids = []

    for fname in os.listdir(COVERS_DIR):
        if fname.startswith("book_") and fname.endswith(".jpg"):
            try:
                num = int(fname[5:-4])
                existing_ids.append(num)
            except:
                pass

    max_done_id = max(existing_ids) if existing_ids else -1
    print(f"[INFO] Максимальный обработанный id: {max_done_id}")

    df = pd.read_csv(INPUT_CSV)

    total = len(df)
    print(f"Всего книг: {total}")

    downloaded = 0

    for idx, row in df.iterrows():

        book_id = row.get("id")

        if book_id <= max_done_id:
            continue

        if downloaded >= MAX_TO_PROCESS:
            print(f"\n[INFO] Достигнут лимит {MAX_TO_PROCESS}. Останавливаюсь.")
            break

        title = str(row.get("title", "")).strip()

        if not title:
            print(f"[SKIP] idx={idx}: нет названия")
            continue

        filename = f"book_{book_id}.jpg"
        filepath = os.path.join(COVERS_DIR, filename)

        print(f"[{downloaded + 1}/{MAX_TO_PROCESS}] Ищу обложку: «{title}» (id={book_id})")

        authors = str(row.get("authors", "")).strip()
        cover_url = find_cover_labirint(title, authors)

        if not cover_url:
            print(f"[SKIP] Обложка не найдена для «{title}»")
            continue

        try:
            img_data = requests.get(cover_url, timeout=10).content
            with open(filepath, "wb") as f:
                f.write(img_data)

            downloaded += 1
            print(f"[OK] Скачано: {filename}")

        except Exception as e:
            print(f"[ERROR] Ошибка скачивания: {e}")
            print("[SKIP] Пропускаю книгу")
            continue

        time.sleep(1)

    print(f"\nГотово! Скачано новых обложек: {downloaded}")


if __name__ == "__main__":
    main()
