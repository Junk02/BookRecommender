import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse


COVERS_DIR = "booksite/public/covers"


def normalize(s: str) -> str:
    return s.lower().strip()


def init_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--remote-debugging-port=0")

    # отключаем картинки — ускоряет ×2–3
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def find_cover_litres(title: str, author: str = "") -> str | None:
    driver = init_driver()

    query = urllib.parse.quote(f"{title} {author}".strip())
    url = f"https://www.litres.ru/search/?q={query}"

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="art__wrapper"]')))

        results = driver.find_elements(By.CSS_SELECTOR, '[data-testid="art__wrapper"]')[:3]

        target_title = normalize(title)
        target_author = normalize(author)

        for block in results:
            try:
                title_el = block.find_element(By.CSS_SELECTOR, '[data-testid="art__title"]')
                found_title = normalize(title_el.text)
            except:
                continue

            try:
                author_el = block.find_element(By.CSS_SELECTOR, '[data-testid="art__authorName--link"]')
                found_author = normalize(author_el.text)
            except:
                found_author = ""

            if target_title in found_title and (target_author in found_author or not target_author):
                img = block.find_element(By.CSS_SELECTOR, 'img[data-testid="adaptiveCover__img"]')
                cover_url = img.get_attribute("src")
                driver.quit()
                return cover_url

        driver.quit()
        return None

    except Exception as e:
        print(f"[ERROR] Selenium LitRes: {e}")
        driver.quit()
        return None


def download_image(url: str, path: str):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            return True
    except:
        pass
    return False


def process_books(csv_path: str):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        book_id = row["id"]
        title = row["title"]
        author = row.get("authors", "")

        filename = f"book_{book_id}.jpg"
        filepath = os.path.join(COVERS_DIR, filename)

        if os.path.exists(filepath):
            print(f"[SKIP] {book_id}: already exists")
            continue

        print(f"[SEARCH] {book_id}: {title} — {author}")

        cover_url = find_cover_litres(title, author)

        if cover_url:
            print(f"[FOUND] {book_id}: {cover_url}")
            if download_image(cover_url, filepath):
                print(f"[SAVED] {filename}")
            else:
                print(f"[ERROR] Failed to download {cover_url}")
        else:
            print(f"[MISS] {book_id}: cover not found")

        time.sleep(0.1)


process_books("books.csv")
