import os
import json
import urllib.request
import subprocess


"""
!!! Discontinued 
"""
def download_image(url, output_path):
    urllib.request.urlretrieve(url, output_path)

def upload_to_gcs(local_file, gcs_bucket):
    subprocess.run(['D:\\Local-D\\PycharmProjects\\hmScrapper\\zara\\gsutil', 'cp', local_file, gcs_bucket])

def process_json_file(json_file, gcs_bucket):
    with open(json_file, 'r') as f:
        data = json.load(f)
        for obj in data:
            image_url = obj.get('image_url')
            if image_url:
                image_name = os.path.basename(image_url)
                local_image_path = f'/tmp/{image_name}'
                download_image(image_url, local_image_path)
                upload_to_gcs(local_image_path, gcs_bucket)
                os.remove(local_image_path)

def main():
    gcs_bucket = 'gs://tidpaaws5d7ty9qo.inika.app'
    # json_files = ['file1.json', 'file2.json', 'file3.json']  # Add your JSON files here
    #
    # for json_file in json_files:
    #     process_json_file(json_file, gcs_bucket)

    upload_to_gcs("all_products_zara_metadata.json", gcs_bucket)

if __name__ == '__main__':
    main()
