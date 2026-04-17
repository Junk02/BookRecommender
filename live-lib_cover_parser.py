import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.parse
import re


def normalize(s: str) -> str:
    if not s:
        return ""
    s = s.lower().strip()
    s = s.replace("ё", "е")
    s = re.sub(r"[^a-zа-я0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def find_cover_livelib(title: str, author: str = "") -> str | None:
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "ru-RU,ru;q=0.9"
    }

    query = urllib.parse.quote(f"{title} {author}".strip())
    search_url = f"https://www.livelib.ru/find/{query}"

    try:
        resp = requests.get(search_url, headers=headers, timeout=10)
        print(resp.text[:2000])

        if resp.status_code != 200:
            print(f"[ERROR] LiveLib status {resp.status_code}")
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # 1. Находим блок с результатами
        results_block = soup.find("div", id="objects-block")
        if not results_block:
            print("[INFO] LiveLib: нет блока результатов")
            return None

        # 2. Находим первый объект книги
        first_obj = results_block.find("div", class_=lambda c: c and "object-wrapper" in c)
        if not first_obj:
            print("[INFO] LiveLib: книга не найдена")
            return None

        # 3. Достаём ссылку на книгу из ll-redirect
        redirect = first_obj.find("div", class_="ll-redirect")
        if not redirect:
            print("[INFO] LiveLib: нет ll-redirect")
            return None

        data_link = redirect.get("data-link")
        if not data_link:
            print("[INFO] LiveLib: нет data-link")
            return None

        book_url = "https://www.livelib.ru" + data_link

        # 4. Загружаем страницу книги
        resp2 = requests.get(book_url, headers=headers, timeout=10)
        if resp2.status_code != 200:
            print(f"[ERROR] LiveLib book page status {resp2.status_code}")
            return None

        soup2 = BeautifulSoup(resp2.text, "html.parser")

        # 5. Находим большую обложку
        img = soup2.find("img", class_="book-cover__image")
        if not img:
            print("[INFO] LiveLib: обложка не найдена")
            return None

        cover_url = img.get("src")
        if not cover_url:
            return None

        if cover_url.startswith("//"):
            cover_url = "https:" + cover_url
        elif cover_url.startswith("/"):
            cover_url = "https://www.livelib.ru" + cover_url

        return cover_url

    except Exception as e:
        print(f"[ERROR] LiveLib ошибка: {e}")
        return None


if __name__ == "__main__":
    url = find_cover_livelib("Посторонний", "Альбер Камю")
    print("Результат:", url)
