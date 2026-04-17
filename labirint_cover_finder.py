import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.parse
import re


def normalize(s: str) -> str:
    """Нормализация строки: нижний регистр, ё→е, убираем пунктуацию."""
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

            # --- проверка названия ---
            if title_norm not in found_name:
                continue

            # --- проверка автора (если указан) ---
            if author_norm:
                author_block = product.find("div", class_="product-card__author")
                found_author = ""

                if author_block:
                    found_author = normalize(author_block.get_text(" ", strip=True))

                # Проверяем мягко: фамилия или имя должны быть в строке
                author_parts = author_norm.split()

                if not any(part in found_author for part in author_parts):
                    print(f"[SKIP] Автор не совпал: '{found_author}' != '{author_norm}'")
                    continue

            # --- достаём обложку ---
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
