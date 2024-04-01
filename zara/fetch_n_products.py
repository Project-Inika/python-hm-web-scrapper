import os
import json
import urllib.request
import uuid
import csv
from urllib.parse import urlparse, urlunparse, parse_qs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}


def download_image(image_url, output_dir):
    image_name = str(uuid.uuid4()) + '.jpg'  # Generate a UUID for the image filename
    output_path = os.path.join(output_dir, image_name)

    # Create a request object with a custom User-Agent header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    req = urllib.request.Request(image_url, headers=headers)

    # Open the URL and retrieve the data
    with urllib.request.urlopen(req) as response:
        with open(output_path, 'wb') as out_file:
            out_file.write(response.read())

    print(f"Downloaded {image_name}")
    return image_name


def clean_image_url(image_url):
    parsed_url = urlparse(image_url)
    query_params = parse_qs(parsed_url.query)
    if 'w' in query_params:
        del query_params['w']
    cleaned_url = parsed_url._replace(query='')
    return urlunparse(cleaned_url)

def main():
    # Path to the JSON file
    json_file = 'all_products_zara_metadata_2.json'

    # Directory to store the images
    output_dir = 'zara_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open CSV file for writing
    csv_file = 'zara_product_data_2.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product_title', 'product_details', 'product_color', 'product_url', 'image_url', 'image_path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                try:
                    image_url = item.get('image_url')
                    if image_url:
                        cleaned_url = clean_image_url(image_url)
                        try:
                            image_name = download_image(cleaned_url, output_dir)
                            item['image_path'] = os.path.join(output_dir, image_name)
                            item['image_url'] = cleaned_url
                        except:
                            item['image_path'] = "Not downloaded"
                            item['image_url'] = cleaned_url
                    writer.writerow(item)
                except:
                    print(item)

    print(f"CSV file '{csv_file}' created successfully.")

if __name__ == "__main__":
    main()
