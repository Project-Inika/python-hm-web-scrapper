import concurrent.futures
import os
import re
from urllib.parse import urlparse

import bs4
import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By



def scrape_product_details(driver, url):
    driver.get(url)
    time.sleep(0.05)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    product_container = soup.find("div", class_="product-detail-view__content")
    if not product_container:
        print("Product container not found.")
        return ""

    product_container_images = product_container.find("ul", class_="product-detail-images-thumbnails")
    if not product_container_images:
        print("Product images container not found.")
        return ""

    products_image_list = product_container_images.find_all("li", class_="product-detail-images-thumbnails__item")
    if not products_image_list:
        print("No product images found.")
        return ""

    # Assuming you want the third last image
    product = products_image_list[-3]
    image_url = product.find("img", class_="media-image__image")
    product_title = soup.find("h1", class_="product-detail-info__header-name")
    image_desc_div = soup.find("div", class_="product-detail-description")
    image_desc = image_desc_div.find("p").text.strip()

    if image_url:
        image_url = image_url["src"]
    else:
        print("Image URL not found.")
        image_url = ""

    return image_url, image_desc, product_title


# def extract_data_for_categories():
#     # Create a directory to store category files
#     driver = webdriver.Chrome()
#     category_dir = 'category_files'
#     all_product_details = []
#
#     for category_file in os.listdir(category_dir):
#         category_product_details = []
#         try:
#             category_name = category_file.split('_')[0]
#             print(f"Scraping product details for category: {category_name}")
#
#             with open(os.path.join(category_dir, category_file), 'r') as f:
#                 product_urls = f.readlines()
#
#
#
#             for product_url in product_urls:
#                 product_url = product_url.strip()
#                 if product_url:
#                     product_img_url, product_details, product_title = scrape_product_details(driver, product_url)
#                     category_product_details.append({"url": product_url, "image_url": product_img_url, "product_details": product_details, "product_title":product_title})
#                     print(f"Scraped details for product: {product_url}")
#         except:
#             pass
#
#         all_product_details.extend(category_product_details)
#
#
#     driver.quit()
#
#     with open("all_products_details.json", "w") as f:
#         json.dump(all_product_details, f)

def scrape_category(category_file, category_dir):
    driver = webdriver.Chrome()
    category_product_details = []
    category_name = category_file.split('_')[0]
    print(f"Scraping product details for category: {category_name}")

    with open(os.path.join(category_dir, category_file), 'r') as f:
        product_urls = f.readlines()

    for product_url in product_urls:
        product_url = product_url.strip()
        if product_url:
            product_img_url, product_details, product_title = scrape_product_details(driver, product_url)
            category_product_details.append({"url": product_url, "image_url": product_img_url, "product_details": product_details, "product_title":product_title})
            print(f"Scraped details for product: {product_url}")
    driver.quit()
    return category_product_details

def extract_data_for_categories():

    category_dir = 'category_files'
    all_product_details = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_category = {executor.submit(scrape_category, category_file, category_dir): category_file for category_file in os.listdir(category_dir)}
        for future in concurrent.futures.as_completed(future_to_category):
            category_file = future_to_category[future]
            try:
                category_product_details = future.result()
                all_product_details.extend(category_product_details)
            except Exception as exc:
                print(f"Scraping failed for category {category_file}: {exc}")



    with open("all_products_details.json", "w") as f:
        json.dump(all_product_details, f)

extract_data_for_categories()