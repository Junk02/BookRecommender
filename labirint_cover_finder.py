import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.parse


def find_cover_labirint(title: str) -> str | None:
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "ru-RU,ru;q=0.9"
    }

    # Лабиринт принимает кириллицу, но quote безопаснее
    query = urllib.parse.quote(title)
    url = f"https://www.labirint.ru/search/{query}/?stype=0"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] Labirint status {resp.status_code}")
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # Ищем первую карточку книги
        product = soup.find("div", class_="product-card")
        if not product:
            print("[INFO] Книга не найдена на Лабиринте")
            return None

        # Ищем тег <img> внутри карточки
        img = product.find("img", class_="book-img-cover")
        if not img:
            print("[INFO] Обложка не найдена")
            return None

        # Лабиринт использует data-src для настоящей обложки
        cover_url = img.get("data-src") or img.get("src")
        if not cover_url:
            return None

        # Приводим к абсолютному URL
        if cover_url.startswith("//"):
            cover_url = "https:" + cover_url
        elif cover_url.startswith("/"):
            cover_url = "https://www.labirint.ru" + cover_url

        return cover_url

    except Exception as e:
        print(f"[ERROR] Ошибка при запросе Лабиринта: {e}")
        return None

print(find_cover_labirint("Посторонний"))