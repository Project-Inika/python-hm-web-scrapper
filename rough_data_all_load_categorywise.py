import concurrent
import os
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import NoSuchWindowException
from selenium.webdriver.chrome.options import Options

window_handles = []


def scrape_product_details_new_tab(driver, url):
    # Open URL in a new tab
    driver.execute_script("window.open('{}', '_blank');".format(url))
    id = len(driver.window_handles) - 1
    window_handles.append(id)
    # driver.switch_to.window( driver.window_handles[-1])

    try:
        # Wait for page to load
        time.sleep(2)  # Adjust sleep time as needed

        # Perform scraping
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
        product_title = soup.find("h1", class_="product-detail-info__header-name").text.strip()
        image_desc_div = soup.find("div", class_="product-detail-description")
        image_desc = image_desc_div.find("p").text.strip()

        if image_url:
            image_url = image_url["src"]
        else:
            print("Image URL not found.")
            image_url = ""

        return {"image_url": image_url, "product_details": image_desc, "product_title": product_title}

    except NoSuchWindowException:
        print(f"Failed to scrap: {url}, Error: NoSuchWindowException - Window already closed")




def close_first_window(driver):
    # Get all window handles
    window_handles = driver.window_handles

    # Check if the number of tabs exceeds 10
    if len(window_handles) == 3:
        # Execute JavaScript to close the first window
        first_window_handle = window_handles[0]


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
    product_title = soup.find("h1", class_="product-detail-info__header-name").text.strip()
    image_desc_div = soup.find("div", class_="product-detail-description")
    image_desc = image_desc_div.find("p").text.strip()

    if image_url:
        image_url = image_url["src"]
    else:
        print("Image URL not found.")
        image_url = ""

    return {"image_url": image_url, "product_details": image_desc, "product_title": product_title}


def scrape_product_urls(driver, category_file):
    category_name = category_file
    print(f"Scraping product details for category: {category_name}")

    with open(category_file, 'r') as f:
        product_urls = f.readlines()

    category_product_details = []
    # Use single driver for product URLs less than or equal to 10
    for url in product_urls:
        try:
            product_data = scrape_product_details(driver, url)
            product_data["url"] = url
            category_product_details.append(product_data)
            print(f"Scraped details for product: {url}")
        except Exception as e:
            print(f"Failed to extract details for {url}: {e}")

    # Check if the directory exists, if not, create it
    directory = "category_products"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save the scraped product details to a JSON file
    with open(f"category_products/{category_name.replace("\\","_" )}_products_details.json", "w") as f:
        json.dump(category_product_details, f)


def extract_data_for_category(category_file):
    with webdriver.Chrome() as driver:
        var = os.path.splitext(os.path.basename(category_file))[0]
        scrape_product_urls(driver, category_file)


def extract_data_for_categories(category_files):
    for category_file in category_files:
        extract_data_for_category(category_file)


if __name__ == "__main__":
    category_files = [os.path.join('category_files', filename) for filename in os.listdir('category_files')]
    extract_data_for_categories(category_files)
