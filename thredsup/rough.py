import json

"""
Use it to rename file or var 
"""
def rename_json_fields(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    renamed_data = []

    for item in data:
        renamed_item = {
            "image_url": item.get("Image link", ""),
            "product_details": item.get("Description:", ""),
            "product_color": "",  # You need to specify the color extraction logic here
            "product_title": item.get("Type:", ""),
            "product_url": item.get("Link:", "")
        }
        renamed_data.append(renamed_item)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(renamed_data, f, indent=2)


if __name__ == "__main__":
    input_json_file = 'all_threds_up_data.json'  # Specify your input JSON file name
    output_json_file = 'all_threds_up_data_renamed.json'  # Specify your output JSON file name
    rename_json_fields(input_json_file, output_json_file)
