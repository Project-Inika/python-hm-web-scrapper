import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url = 'https://www.thredup.com/women?department_tags=women&page=2'
driver.get(url)


# Calculate the coordinates of the bottom-right corner
bottom_right_x = 0  # 10 pixels from the right edge
bottom_right_y = 0  # 10 pixels from the bottom edge

# Create an ActionChains object
actions = ActionChains(driver)

# Move to the calculated coordinates and perform a click
actions.move_by_offset(bottom_right_x, bottom_right_y)
actions.click()
actions.perform()

time.sleep(5)
content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

product_list = soup.find_all("div", "Vb607oOokVxxYVL7SQwh")


for product in product_list:
    img = product.find("img", class_="BQ6FcxrnnnmSna3sncgu")


    # Extracting description
    description_tag = product.find('h3', class_='u-font-bold')
    description = description_tag.text.strip() if description_tag else None

    # Extracting type
    type_tag = product.find('div', class_='spot-grey-5')
    type_info = type_tag.text.strip() if type_tag else None

    # Extracting link
    link_tag = product.find('a', class_='u-block')
    link = link_tag['href'] if link_tag else None

    print("Description:", description)
    print("Type:", type_info)
    print("Link:", link)
    print("Image link", img["src"] if img else "")

driver.close()