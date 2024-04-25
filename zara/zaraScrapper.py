import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
"""
Single product scrapper script 
"""

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
# Function to scrape Zara product URLs from a page
def scrape_product_urls(url):
    driver = webdriver.Chrome()
    driver.get(url)
    # Find all buttons
    buttons = driver.find_elements(By.CLASS_NAME, "view-option-selector-button")

    # Click the last button
    buttons[-1].click()
    time.sleep(5)

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
    print(len(product_urls))
    return list(product_urls)

# Function to scrape product details from a Zara product page
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
    # Create a WebDriver instance
    driver = webdriver.Chrome()

    # Scrape Zara product URLs
    product_urls = scrape_product_urls('https://www.zara.com/in/en/woman-dresses-l1066.html')
    if not product_urls:
        print("No product URLs found.")
        driver.quit()
        return

    # Initialize an empty list to store scraped product data
    products_data = []

    # Scrape details for each product
    for url in product_urls:
        image_url = scrape_product_details(driver, url)
        product_data = {"url": url, "image_url": image_url}
        products_data.append(product_data)

        # Save/update product data to JSON file after scraping each product
        with open("zara_products_data.json", "w") as f:
            json.dump(products_data, f)

    # Quit the WebDriver instance
    driver.quit()
    driver.close()

if __name__ == "__main__":
    main()
