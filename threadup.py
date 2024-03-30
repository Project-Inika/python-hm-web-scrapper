import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
url = 'https://www.thredup.com/product/women-rayon-mi-ami-navy-casual-dress/161271659?query_id=887067618984140800&result_id=887067621056126976'
driver.get(url)
time.sleep(2)
content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

# Find the <ul> tag with class "list-disc black"
ul_tag = soup.find_all('ul', class_='list-disc black')

# Extract the content within the <ul> tag
if ul_tag:
    for tag in ul_tag:
        list_items = tag.find_all('li')
        for item in list_items:
            print(item.text.strip())

driver.close()