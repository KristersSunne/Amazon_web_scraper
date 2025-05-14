from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import re
from datetime import datetime

# Functions
def find_price(pr):
    price_whole = pr.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
    price_fraction = pr.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
    price = f"{price_whole},{price_fraction} €"
    price_numeric = float(price_whole.replace(',', '.') + '.' + price_fraction)
    return price, price_numeric

def clean_title(raw_title):
    title = re.sub(r":.*", "", raw_title)
    title = re.sub(r"\(.*?\)", "", title)
    title = re.sub(r"\s{2,}", " ", title)
    return title.strip()

def save_to_json(file_path, new_entry):
    data = []

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in data:
        if item["title"] == new_entry["title"]:
            if item["price"] != new_entry["price"]:
                item["price"] = new_entry["price"]
                item.setdefault("price_history", []).append({
                    "price": new_entry["price"],
                    "timestamp": timestamp
                })
            return

    new_entry["price_history"] = [{
        "price": new_entry["price"],
        "timestamp": timestamp
    }]
    data.append(new_entry)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


while True:
    search_term = input("Input item name (or 'q' to quit): ").lower().strip()
    if search_term == "q":
        break
    min_price = int(input("Input minimum price: "))

    chrome_driver_path = "chromedriver-win64/chromedriver.exe"
    service = Service(chrome_driver_path)

    options = Options()
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-data-dir=C:/Temp/SeleniumProfile")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.amazon.de")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']"))
        )

        products = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")

        for product in products[:20]:
            try:
                try:
                    title = product.find_element(By.CSS_SELECTOR, "h2 span").text
                    if search_term in title.lower():
                        price_text, price_value = find_price(product)
                        if price_value > min_price:
                            cleaned_title = clean_title(title)
                            print(f"{cleaned_title} - {price_text}")
                            save_to_json("filtered_results.json", {
                                "title": cleaned_title,
                                "price": price_text
                            })
                except Exception:
                    continue
            except Exception:
                continue
        driver.quit()
    except Exception:
        continue

