import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By




driver = webdriver.Chrome()
url = 'https://www.zara.com/in/en/man-shirts-l737.html?v1=2351464&regionGroupId=80&page=8'
driver.get(url)
time.sleep(2)
content = driver.page_source




soup = BeautifulSoup(content, 'html.parser')
products_list_container = soup.find("ul", class_="product-grid__product-list")
with open("temp.txt", "w", encoding="UTF-8")as f:
    f.write(content)



if products_list_container:
    products = products_list_container.find_all("li", class_="product-grid-product")
else:
    print("no products ")
    exit()

product_urls = []
for product in products:
    product_url_tag = product.find("a", class_= "product-link")
    print(product_url_tag)
    url = product_url_tag["href"] if product_url_tag else ""
    output = {
        "url": url
    }
    product_urls.append(output)


with open("zara_products_url_list.json", "w") as f:
    json.dump(product_urls, f)