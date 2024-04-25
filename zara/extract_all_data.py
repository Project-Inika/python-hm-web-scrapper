import concurrent
import os
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import NoSuchWindowException


"""
This script is to extract all the product information from product page it stores data in the file all_product_details.json
use download_and_save_zara_images.py to download and create the csv file 
"""


# Perform scraping
from bs4 import BeautifulSoup

category_product_details = []

chrome_options = webdriver.ChromeOptions()

# Add options
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration, can help with headless mode
chrome_options.add_argument("--window-size=1920x1080")  # Set window size
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Generate a random user agent string
chrome_options.add_argument(
    "user-agent= Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320")


def scrape_product_details(driver, url):
    driver.get(url)
    time.sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    product_container = soup.find("div", class_="product-detail-view__main-content")
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
    image_url = product.find("img", class_="media-image__image media__wrapper--media")
    product_title = soup.find("h1", class_="product-detail-info__header-name").text.strip()
    image_desc_div = soup.find("div", class_="product-detail-description")
    image_desc = image_desc_div.find("p").text.strip()
    product_color_container = soup.find("p", class_="product-detail-info__color")
    product_color = product_color_container.text.strip() if product_color_container else ""

    if image_url:
        image_url = image_url["src"]
    else:
        print("Image URL not found.")
        image_url = ""
    print(image_url)

    return {"image_url": image_url, "product_details": image_desc, "product_color": product_color,
            "product_title": product_title, "product_url": url}


def scrape_all_product_urls(filename):
    global category_product_details
    print(f"Scraping product details for all products")

    with open(filename, 'r') as f:
        product_urls = f.readlines()

    for url in product_urls:
        driver = webdriver.Chrome(options=chrome_options)
        try:
            product_data = scrape_product_details(driver, url)
            category_product_details.append(product_data)
            print(f"Scraped details for product: {url}")
            # Check if the directory exists, if not, create it
            # Create the directory if it doesn't exist

            # Write to the file
            with open("all_products_details.json",
                      "w") as f:
                json.dump(category_product_details, f)

        except Exception as e:
            print(f"Failed to scrap: {url}, Error: {e}")
        driver.quit()


if __name__ == "__main__":
    category_dir = "all_zara_product_links.txt"
    scrape_all_product_urls(category_dir)
