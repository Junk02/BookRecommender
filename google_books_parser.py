import requests
import urllib.parse

def find_cover_google(title: str, author: str = "") -> str | None:
    query = urllib.parse.quote(f"{title} {author}".strip())
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"[ERROR] Google Books status {resp.status_code}")
            return None

        data = resp.json()

        if "items" not in data or len(data["items"]) == 0:
            print("[INFO] Google Books: книга не найдена")
            return None

        volume = data["items"][0]
        info = volume.get("volumeInfo", {})
        images = info.get("imageLinks", {})

        # Берём лучшую доступную обложку
        cover_url = images.get("thumbnail") or images.get("smallThumbnail")
        if not cover_url:
            print("[INFO] Google Books: нет обложки")
            return None

        # Google иногда отдаёт http — заменим на https
        cover_url = cover_url.replace("http://", "https://")

        return cover_url

    except Exception as e:
        print(f"[ERROR] Google Books ошибка: {e}")
        return None

if __name__ == "__main__":
    print(find_cover_google("Посторонний", "Альбер Камю"))




