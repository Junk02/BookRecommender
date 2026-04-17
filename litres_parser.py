from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time

def normalize(s: str) -> str:
    return s.lower().strip()

def find_cover_litres_selenium(title: str, author: str = "") -> str | None:
    query = urllib.parse.quote(f"{title} {author}".strip())
    url = f"https://www.litres.ru/search/?q={query}"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 3)

        # Ждём появления хотя бы одного результата
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="art__wrapper"]')))

        # Берём все результаты
        results = driver.find_elements(By.CSS_SELECTOR, '[data-testid="art__wrapper"]')

        target_title = normalize(title)
        target_author = normalize(author)

        for block in results:
            # Название
            try:
                title_el = block.find_element(By.CSS_SELECTOR, '[data-testid="art__title"]')
                found_title = normalize(title_el.text)
            except:
                continue

            # Автор
            try:
                author_el = block.find_element(By.CSS_SELECTOR, '[data-testid="art__authorName--link"]')
                found_author = normalize(author_el.text)
            except:
                found_author = ""

            # Проверка совпадения
            if target_title in found_title and (target_author in found_author or not target_author):
                # Берём обложку
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

print(find_cover_litres_selenium("Святая ложь", "Александр Куприн"))
