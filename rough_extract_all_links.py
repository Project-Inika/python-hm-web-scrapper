import bs4
import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def extract_category_links(html):
    """Extracts category links from the given HTML and returns them as a list of dictionaries.

    Args:
        html: The HTML string to parse.

    Returns:
        A list of dictionaries, where each dictionary has the format:
        {"category_name": "link"}
    """

    soup = bs4.BeautifulSoup(html, "html.parser")

    category_links = []
    for category_li in soup.find_all("li", class_="layout-categories-category--level-2"):
        category_a = category_li.find("a", class_="layout-categories-category__link")
        if category_a and category_a.has_attr("href"):  # Check if href attribute exists
            category_name_span = category_a.find("span", class_="layout-categories-category__name")
            if category_name_span:
                category_name = category_name_span.text.strip()
            else:
                category_name = category_a.text.strip()
            link = category_a["href"]
            category_links.append({category_name: link})

    return category_links



driver = webdriver.Chrome()
url = 'https://www.zara.com/in/'
driver.get(url)
time.sleep(2)
content = driver.page_source

# Find all buttons
buttons = driver.find_elements(By.CLASS_NAME, "slider-spot-universes-bar__item")

# Click the last button
buttons[0].click()
time.sleep(5)




category_links = extract_category_links(content)
print(category_links)