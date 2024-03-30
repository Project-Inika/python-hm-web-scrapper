import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# Function to load existing JSON data from file if it exists
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return []

# Function to save data to JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def process_image(link):
    new_link = link.replace("/product/main","/product/fullscreen" )
    new_link = new_link.replace("/product/style","/product/fullscreen" )
    return "https:" + new_link

driver = webdriver.Chrome()
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
url = 'https://www2.hm.com/en_in/men/shop-by-product/tshirts-tank-tops.html?sort=stock&image-size=small&image=model&offset=0&page-size=108'
driver.get(url)
time.sleep(2)
content = driver.page_source

# with open("content.txt", "r", encoding="UTF-8") as f:
#     content = f.read()


soup = BeautifulSoup(content, 'html.parser')
products_container = soup.find("ul", class_="products-listing")


if products_container:
    products = products_container.find_all("li", class_="product-item")
else:
    print("Products container not found!")
    exit()

# Load existing data or create an empty list
existing_data = load_json('products.json')

# Iterate through the products and extract information
new_data = []
for product in products:
    product_link = product.find("a")["href"] if product.find("a") else None
    product_image = product.find("img")["src"] if product.find("img") else None
    # Extracting data-altimage attribute
    product_image_main = product.find("img").get("data-altimage") if product.find("img") else None
    product_title = product.find("h3").text.strip() if product.find("h3") else None
    product_description = product.find("p").text.strip() if product.find("p") else None
    product_price = product.find("span", class_="price").text.strip() if product.find("span", class_="price") else None

    # Find the first li item
    first_item = product.find("li", class_="item")

    # Extract the title attribute
    if first_item:
        title = first_item.find("a")["title"]

    else:
        title = ""
    # Append extracted information to new_data list
    new_data.append({
        "Product URL": product_link,
        "Product Color": title,
        "Product Image": product_image,
        "Product Image Main": process_image(product_image_main),
        "Product Title": product_title,
        "Product Description": product_description,
        "Product Price": product_price
    })

# Combine existing data with new data
all_data = new_data

# Save all data to JSON file
save_to_json(all_data, 'products.json')

# Process and store extracted information (print, database, etc.)
for item in new_data:
    print(json.dumps(item, indent=4))
    print("-" * 50)  # Separator

driver.quit()






