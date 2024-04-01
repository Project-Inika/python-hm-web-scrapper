import concurrent
import os
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import NoSuchWindowException

window_handles = []
category_product_details = []

def scrape_product_details_new_tab(driver, url):
    # Open URL in a new tab
    driver.execute_script("window.open('{}', '_blank');".format(url))
    driver.switch_to.window( driver.window_handles[-1])

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


def scrape_product_urls(category_file):
    global category_product_details
    category_name = category_file
    print(f"Scraping product details for category: {category_name}")

    with open(category_file, 'r') as f:
        product_urls = f.readlines()

    num_of_drivers = 25
    # Split the list of URLs into chunks of 10
    url_chunks = [product_urls[i:i + num_of_drivers] for i in range(0, len(product_urls), num_of_drivers)]

    # Run extraction for each chunk asynchronously
    for chunk in url_chunks:
        driver = webdriver.Chrome()

        with ThreadPoolExecutor(max_workers=num_of_drivers) as executor:
            future_to_url = {executor.submit(scrape_product_details_new_tab, driver, url.strip()): url.strip() for url
                             in
                            chunk}
            for n, future in enumerate(concurrent.futures.as_completed(future_to_url)):
                url = future_to_url[future]
                try:
                    product_data = future.result()
                    category_product_details.append(product_data)
                    print(f"Scraped details for product: {url}")

                except Exception as e:
                    print(f"Failed to scrap: {url}, Error: {e}")
        driver.quit()

    # Check if the directory exists, if not, create it
    # Create the directory if it doesn't exist
    os.makedirs(f"category_products", exist_ok=True)

    # Write to the file
    with open(f"category_products/{category_name.replace('/', '_').replace('\\', '_').replace(" ", "_")}_products_details.json",
              "w") as f:
        json.dump(category_product_details, f)


def extract_data_for_category(category_file):
    # with webdriver.Chrome() as driver:
    #     var = os.path.splitext(os.path.basename(category_file))[0]
    scrape_product_urls(category_file)


def extract_data_for_categories(category_files):
    for category_file in category_files:
        extract_data_for_category(category_file)
    # extract_data_for_category("category_files/hoodies _ sweatshirts_in_en_man_sweatshirts_l821_html_products.txt")


if __name__ == "__main__":
    category_files = [os.path.join('category_files', filename) for filename in os.listdir('category_files')]
    extract_data_for_categories(category_files)
