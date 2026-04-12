from time import sleep

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def find_oz_book_url(title: str):
    query = quote_plus(title)
    url = f"https://oz.by/?digiSearch=true&term={title}&params=%7Csort%3DDEFAULT"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Ошибка поиска:", response.status_code)
        return None

    print(url)
    sleep(3)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)

    # Ищем первый digi-product
    product = soup.select_one(".digi-product[data-href]")
    if not product:
        print("Книга не найдена")
        return None

    href = product.get("data-href")
    return "https://oz.by" + href

def get_oz_annotation(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Ошибка запроса:", response.status_code)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Возможные блоки с аннотацией
    selectors = [
        ".b-description__text",
        ".b-description__sub",          # ← ТВОЙ БЛОК
        "#truncatedBlock",              # ← ТВОЙ БЛОК
        ".b-product-description",
        ".b-product-info__text",
        ".b-product__description",
        '[itemprop="description"]',
        ".b-product-about__text",
    ]

    for sel in selectors:
        block = soup.select_one(sel)
        if block:
            text = block.get_text(" ", strip=True)
            if text:
                return text

    print("Аннотация не найдена")
    return None


# Пример использования
title = 'Посторонний'
url = find_oz_book_url(title)
annotation = get_oz_annotation(url)

print('URL:')
print(url)

print("Аннотация:")
print(annotation)
