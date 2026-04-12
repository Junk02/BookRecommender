import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def find_book_on_labirint(title, author=None):
    query = title
    if author:
        query += " " + author

    url = f"https://www.labirint.ru/search/{quote(query)}/?stype=0"

    html = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")

    # Новый селектор
    book_link = soup.select_one("a.product-card__name")
    if not book_link:
        return None

    book_url = "https://www.labirint.ru" + book_link["href"]
    return book_url


def get_description_from_labirint(book_url):
    html = requests.get(book_url, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")

    desc_block = soup.select_one(".card-description")
    if not desc_block:
        desc_block = soup.select_one(".text")

    if not desc_block:
        return None

    description = desc_block.get_text(strip=True)
    return description


def get_book_description(title, author=None):
    url = find_book_on_labirint(title, author)
    # print(url)
    if not url:
        return None

    return get_description_from_labirint(url)
