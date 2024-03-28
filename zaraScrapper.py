import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
url = 'https://www.zara.com/in/en/abstract-print-satin-shirt-p04092358.html'
driver.get(url)
time.sleep(2)
content = driver.page_source


soup = BeautifulSoup(content, 'html.parser')
product_container = soup.find("div", class_="product-detail-view__content")


product_container_images  = product_container.find("ul", class_= "product-detail-images-thumbnails")

products_image_list = product_container_images.find_all("li", class_="product-detail-images-thumbnails__item")

product = products_image_list[-3]
image_url = product.find("img", class_= "media-image__image")
print(image_url)