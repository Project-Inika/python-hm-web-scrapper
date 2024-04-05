import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

all_threds_products_data = []
chrome_options = webdriver.ChromeOptions()

# Add options
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration, can help with headless mode
chrome_options.add_argument("--window-size=1920x1080")  # Set window size
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("user-agent= Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320")

def make_click_at_right_corner(driver):
    # Calculate the coordinates of the bottom-right corner
    bottom_right_x = 0  # 10 pixels from the right edge
    bottom_right_y = 0  # 10 pixels from the bottom edge

    # Create an ActionChains object
    actions = ActionChains(driver)

    # Move to the calculated coordinates and perform a click
    actions.move_by_offset(bottom_right_x, bottom_right_y)
    actions.click()
    actions.perform()

def get_products_list(driver, url):
    driver.get(url)
    make_click_at_right_corner(driver)
    time.sleep(5)
    content = driver.page_source

    soup = BeautifulSoup(content, 'html.parser')

    product_list = soup.find_all("div", "Vb607oOokVxxYVL7SQwh")

    return product_list

def extract_product_description( url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    ul_tag = soup.find_all('ul', class_='list-disc black')
    product_description = []

    if ul_tag:
        for tag in ul_tag:
            list_items = tag.find_all('li', class_="u-mr-1x")
            for item in list_items:
                product_description.append(item.text.strip())
    driver.close()
    return ", ".join(product_description)

count=0
def extract_product_info(product):
    global count
    img = product.find("img", class_="BQ6FcxrnnnmSna3sncgu")
    type_tag = product.find('div', class_='spot-grey-5')
    type_info = type_tag.text.strip() if type_tag else None

    link_tag = product.find('a', class_='wAhTkKjWOmWyIy2F13MZ')
    link = link_tag['href'] if link_tag else ""
    base = "https://www.thredup.com"

    description = extract_product_description( base + link) if link != "" else ""
    count += 1
    print(count)
    result = {"product_details": description,
              "product_title": type_info,
              "product_url": base + link,
              "image_url": img["src"] if img else "",
              "product_color":""
              }
    all_threds_products_data.append(result)
    insert_update_all_threadsup_data()
    return result

def get_products_data_from_thredup(numOfPages=1, fromPage=1):

    for n in range(fromPage, numOfPages):
        with ThreadPoolExecutor(max_workers=5) as executor:
            driver = webdriver.Chrome()
            url = f'https://www.thredup.com/women?department_tags=women&page={n}'
            product_list_html = get_products_list(driver, url)
            print("current page ", n)
            for product in product_list_html:
                executor.submit(extract_product_info, product)

def insert_update_all_threadsup_data():
    with open("all_threds_up_data_headless_1.json", "w") as f:
        json.dump(all_threds_products_data, f)

get_products_data_from_thredup(2, 1)