import requests
import urllib.parse

def find_cover_openlibrary(title: str, author: str = "") -> str | None:
    # Формируем поисковый запрос
    query = urllib.parse.quote(f"{title} {author}".strip())
    url = f"https://openlibrary.org/search.json?title={query}"
    print(url)

    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] OpenLibrary status {resp.status_code}")
            return None

        data = resp.json()

        # Нет результатов
        if "docs" not in data or len(data["docs"]) == 0:
            print("[INFO] OpenLibrary: книга не найдена")
            return None

        # Берём первую книгу
        book = data["docs"][0]

        # Проверяем наличие cover_i
        cover_id = book.get("cover_i")
        if not cover_id:
            print("[INFO] OpenLibrary: нет обложки")
            return None

        # Формируем URL обложки
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        return cover_url

    except Exception as e:
        print(f"[ERROR] OpenLibrary ошибка: {e}")
        return None

if __name__ == "__main__":
    print(find_cover_openlibrary("Stranger", "Alber Camus"))
