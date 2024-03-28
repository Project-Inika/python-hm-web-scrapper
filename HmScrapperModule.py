import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver


class HMScrapperModule:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def fetch_content(self, url,numOfImages, delay=2):
        """
        Fetch the HTML content of a given URL.

        Args:
            url (str): The URL to fetch.
            numOfImages (Int): Number of products to fetch.
            delay (int, optional): The delay in seconds before fetching the content. Defaults to 2.

        Returns:
            str: The HTML content of the page.
        """
        url = f"{url}?page-size={numOfImages}"
        self.driver.get(url)
        time.sleep(delay)
        return self.driver.page_source

    def get_extracted_data(self, url, numOfImages):
        """
        Extract product information from the given URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            list: A list of dictionaries containing the extracted product information.
        """
        content = self.fetch_content(url, numOfImages)
        product_list = self.extract_product_list_html(content)

        result_list = []
        for product in product_list:
            result_json = self.extract_product_info(product)
            result_list.append(result_json)

        return result_list

    @staticmethod
    def extract_product_list_html(content):
        """
        Extract the product list HTML from the given content.

        Args:
            content (str): The HTML content to extract the product list from.

        Returns:
            list: A list of BeautifulSoup objects representing the product items.
        """
        soup = BeautifulSoup(content, 'html.parser')
        products_container = soup.find("ul", class_="products-listing")
        if products_container:
            return products_container.find_all("li", class_="product-item")
        return []

    def extract_product_info(self, product):
        """
        Extract product information from a single product item.

        Args:
            product (BeautifulSoup): The BeautifulSoup object representing the product item.

        Returns:
            dict: A dictionary containing the extracted product information.
        """
        product_link = product.find("a")["href"] if product.find("a") else None
        product_image = product.find("img")["src"] if product.find("img") else None
        product_image_main = product.find("img").get("data-altimage") if product.find("img") else None
        product_title = product.find("h3").text.strip() if product.find("h3") else None
        product_description = product.find("p").text.strip() if product.find("p") else None
        product_price = product.find("span", class_="price").text.strip() if product.find("span",
                                                                                          class_="price") else None
        first_item = product.find("li", class_="item")
        color_title = first_item.find("a")["title"] if first_item else ""

        return {
            "product_url": product_link,
            "product_color": color_title,
            "product_image": product_image,
            "product_image_main": self.process_image_link(product_image_main),
            "product_title": product_title,
            "product_description": product_description,
            "product_price": product_price
        }

    @staticmethod
    def process_image_link(link):
        """
        Process the image link to get the fullscreen image URL.

        Args:
            link (str): The original image link.

        Returns:
            str: The fullscreen image URL.
        """
        if link:
            new_link = link.replace("/product/main", "/product/fullscreen")
            new_link = new_link.replace("/product/style", "/product/fullscreen")
            return "https:" + new_link
        return None

    @staticmethod
    def save_to_json(data, filename):
        """
        Save the data to a JSON file.

        Args:
            data (list): The data to be saved as JSON.
            filename (str): The name of the JSON file.
        """
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)


if __name__ == "__main__":
    # pass

    # Usage
    url = ('https://www2.hm.com/en_in/men/shop-by-product/tshirts-tank-tops.html')
    scrapper = HMScrapperModule()
    result_list = scrapper.get_extracted_data(url, 400)
    scrapper.save_to_json(result_list, "hm_data_tshirts-tank-tops.json")


