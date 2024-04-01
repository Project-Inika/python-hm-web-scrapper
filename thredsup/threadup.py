import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def extract_product_description(driver, url):
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
            list_items = tag.find_all('li', class_= "u-mr-1x")
            for item in list_items:
                product_description.append(item.text.strip())

    print(product_description)

    driver.close()


driver =webdriver.Chrome()
url = "https://www.thredup.com/product/women-cotton-easel-white-short-sleeve-blouse/163456190?query_id=887768206550073344&result_id=887768209096015872"
extract_product_description(driver, url)