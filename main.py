import os
import csv
import requests
import json
from urllib.parse import urlparse, quote

def download_images(image_data, output_folder):
    """Download images from the provided image data and store them in the specified folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for product in image_data:
        product_url = product.get("product_url")
        product_image_url = product.get("product_image_main")
        if product_url and product_image_url:
            # Encode the image URL to make it compatible with the filesystem
            encoded_url = quote(product_image_url, safe="")
            # Generate a filename based on the product URL
            filename = os.path.basename(urlparse(product_url).path) + ".jpg"
            image_filename = os.path.join(output_folder, filename)

            try:
                response = requests.get(product_image_url)
                if response.status_code == 200:
                    with open(image_filename, 'wb') as f:
                        f.write(response.content)
                    print(f"Image downloaded: {image_filename}")
                else:
                    print(f"Failed to download image for product URL: {product_url}")
            except Exception as e:
                print(f"Error downloading image for product URL {product_url}: {e}")

def convert_to_csv(image_data, output_csv):
    """Convert image data to CSV format and modify links to be clickable."""
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = image_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for product in image_data:
            # Modify product URL to make it clickable
            product['product_url'] = f"https://{product['product_url'].strip('/')}"
            writer.writerow(product)

if __name__ == "__main__":
    with open("new_data.json" , "r", encoding="UTF-8") as f:
        image_data = json.load(f)

    # Convert image data to CSV format and modify links
    csv_filename = "image_data.csv"
    convert_to_csv(image_data, csv_filename)
    print(f"Image data converted to CSV: {csv_filename}")

    # Download images
    output_folder = "images"
    download_images(image_data, output_folder)
