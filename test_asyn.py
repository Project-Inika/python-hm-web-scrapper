import asyncio
import concurrent.futures
import concurrent
import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import NoSuchWindowException


all_data = []


def scrape_product_details_new_tab(url):
    driver = webdriver.Chrome()
    driver.get(url)

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

        data =  {"image_url": image_url, "product_details": image_desc, "product_title": product_title}
        all_data.append(data)

    except NoSuchWindowException:
        print(f"Failed to scrap: {url}, Error: NoSuchWindowException - Window already closed")

    finally:
        # Switch back to the main window/tab
        driver.quit()

        # # Close the tab
        # driver.close()
        #
        # # Remove the closed window's ID from the dictionary
        # for key, value in window_ids.items():
        #     if value == driver.current_window_handle:
        #         del window_ids[key]
        #         break
def scrape_product_details(driver, url):
    # Open URL in a new tab
    driver.execute_script("window.open('{}', '_blank');".format(url))

    # Switch to the newly opened tab
    driver.switch_to.window(driver.window_handles[-1])


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

    data = {"image_url": image_url, "product_details": image_desc, "product_title": product_title}
    all_data.append(data)



async def async_extract_data(urls):

    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        # Schedule extraction tasks concurrently, limiting to 10 at a time
        extraction_tasks = [loop.run_in_executor(executor, scrape_product_details_new_tab ,url) for url in urls]
        # Wait for all tasks to complete
        await asyncio.gather(*extraction_tasks)


if __name__ == "__main__":
    # Example list of URLs
    product_urls = []
    with open("category_files/shorts_in_en_man_bermudas_l592_html_products.txt", "r") as f:
        product_urls = f.readlines()



    num_of_drivers = 5
    # Split the list of URLs into chunks of 10
    url_chunks = [product_urls[i:i+num_of_drivers] for i in range(0, len(product_urls), num_of_drivers)]

    # Run extraction for each chunk asynchronously
    for chunk in url_chunks:
        asyncio.run(async_extract_data(chunk))

    with open("temp_sso.json", "w") as f:
        json.dump(all_data,f )

