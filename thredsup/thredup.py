import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

all_threds_products_data = []




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
count = 0

def get_products_list(driver, url):
    driver.get(url)
    make_click_at_right_corner(driver)
    time.sleep(5)
    content = driver.page_source

    soup = BeautifulSoup(content, 'html.parser')

    product_list = soup.find_all("div", "Vb607oOokVxxYVL7SQwh")

    return product_list


def extract_product_description(driver, url):
    # driver = webdriver.Chrome(options=chrome_options)
    global count
    count += 1
    print(count)

    driver.get(url)
    time.sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Find the <ul> tag with class "list-disc black"
    ul_tag = soup.find_all('ul', class_='list-disc black')
    product_description = []

    # Extract the content within the <ul> tag
    if ul_tag:
        for tag in ul_tag:
            list_items = tag.find_all('li', class_="u-mr-1x")
            for item in list_items:
                product_description.append(item.text.strip())
    driver.close()
    # driver.quit()
    return ", ".join(product_description)


def extract_product_info(driver, product):
    img = product.find("img", class_="BQ6FcxrnnnmSna3sncgu")

    # Extracting type
    type_tag = product.find('div', class_='spot-grey-5')
    type_info = type_tag.text.strip() if type_tag else None

    # Extracting link
    link_tag = product.find('a', class_='wAhTkKjWOmWyIy2F13MZ')
    link = link_tag['href'] if link_tag else ""
    base = "https://www.thredup.com"

    description = extract_product_description(driver, base + link) if link != "" else ""

    result = {"Description:": description,
              "Type:": type_info,
              "Link:": base + link,
              "Image link": img["src"] if img else ""}
    try:
        driver.close()
    except:
        pass


    return result


def get_products_data_from_thredup(numOfPages=1):
    driver = webdriver.Chrome()
    for n in range(numOfPages):
        url = f'https://www.thredup.com/women?department_tags=women&page={2}'
        product_list_html = get_products_list(driver, url)

        for product in product_list_html:
            product_info = extract_product_info(driver, product)
            all_threds_products_data.append(product_info)
            insert_update_all_threadsup_data()

def insert_update_all_threadsup_data():
    with open("all_threds_up_data_headless.json", "w") as f:
        json.dump(all_threds_products_data, f)


get_products_data_from_thredup(1)