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


def extract_category_links(html):
    """Extracts category links from the given HTML and returns them as a list of dictionaries.

    Args:
        html: The HTML string to parse.

    Returns:
        A list of dictionaries, where each dictionary has the format:
        {"category_name": "link"}
    """

    soup = bs4.BeautifulSoup(html, "html.parser")

    category_links = []
    for category_li in soup.find_all("li", class_="layout-categories-category--level-2"):
        category_a = category_li.find("a", class_="layout-categories-category__link")
        if category_a and category_a.has_attr("href"):  # Check if href attribute exists
            category_name_span = category_a.find("span", class_="layout-categories-category__name")
            if category_name_span:
                category_name = category_name_span.text.strip()
            else:
                category_name = category_a.text.strip()
            link = category_a["href"]
            category_links.append({category_name: link})

    return category_links


def scroll_to_bottom(driver):
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the page to load


def check_for_new_content(driver, last_height):
    # Get the current scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != last_height


def scroll_until_no_more_content(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to the bottom
        scroll_to_bottom(driver)

        # Check for new content
        if not check_for_new_content(driver, last_height):
            break

        last_height = driver.execute_script("return document.body.scrollHeight")


def scrape_product_urls(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # Find all buttons
    buttons = driver.find_elements(By.CLASS_NAME, "view-option-selector-button")
    try:

        # Click the last button
        buttons[-1].click()
        time.sleep(5)
    except:
        pass

    scroll_until_no_more_content(driver)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    products_list_container = soup.find("ul", class_="product-grid__product-list")
    if not products_list_container:
        print("No products found on this page.")
        return []

    products = products_list_container.find_all("li", class_="product-grid-product")
    product_urls = set()  # Using set to store unique URLs
    for product in products:
        product_url_tag = product.find("a", class_="product-link")
        if product_url_tag:
            url = product_url_tag["href"]
            product_urls.add(url)

    driver.quit()
    return list(product_urls)


def scrape_product_details(driver, url):
    driver.get(url)
    time.sleep(0.5)
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
    if image_url:
        image_url = image_url["src"]
    else:
        print("Image URL not found.")
        image_url = ""

    return image_url


def main():
    driver = webdriver.Chrome()
    url = 'https://www.zara.com/in/'
    driver.get(url)
    time.sleep(2)
    content = driver.page_source

    # Find all buttons
    buttons = driver.find_elements(By.CLASS_NAME, "slider-spot-universes-bar__item")

    # Click the last button
    buttons[0].click()
    time.sleep(5)

    category_links = extract_category_links(driver.page_source)

    # Create a directory to store category files
    category_dir = 'category_files'
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

    for category in category_links:
        category_name, category_link = list(category.items())[0]

        # Concatenate category name and parsed link to create a unique file name
        parsed_link = urlparse(category_link)
        category_file_name = f"{category_name}_{parsed_link.path.strip('/').replace('/', '_')}"

        # Replace special characters with underscores
        category_file_name = re.sub(r'[^\w\s]', '_', category_file_name)

        print(f"Extracting products for category: {category_file_name}")

        category_product_urls = scrape_product_urls(category_link)

        if category_product_urls:
            with open(f'{category_dir}/{category_file_name}_products.txt', 'w') as f:
                for product_url in category_product_urls:
                    f.write(product_url + '\n')
            print(f"Products for category '{category_file_name}' extracted successfully.")
        else:
            print(f"No products found for category '{category_file_name}'.")

    all_product_details = []

    for category_file in os.listdir(category_dir):
        category_name = category_file.split('_')[0]
        print(f"Scraping product details for category: {category_name}")

        with open(os.path.join(category_dir, category_file), 'r') as f:
            product_urls = f.readlines()

        category_product_details = []

        for product_url in product_urls:
            product_url = product_url.strip()
            if product_url:
                product_details = scrape_product_details(driver, product_url)
                category_product_details.append({"url": product_url, "image_url": product_details})
                print(f"Scraped details for product: {product_url}")

        all_product_details.extend(category_product_details)

    driver.quit()

    with open("all_products_details.json", "w") as f:
        json.dump(all_product_details, f)


if __name__ == "__main__":
    main()
