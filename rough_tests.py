import json
import os

# files = os.listdir("zara/extracted_data/products_data")
# list_products = []
#
# for i in files:
#     file_path = os.path.join("zara/extracted_data/products_data", i)
#     with open(file_path, "r") as f:
#         catList = json.load(f)
#     print(len(catList), i)
#     list_products.extend(catList)
#
# # Convert the list to a set to remove duplicates and then back to a list
# unique_list_products = [json.loads(item) for item in set(json.dumps(item) for item in list_products)]
#
# print("Total unique products:", len(unique_list_products))
#
# with open("all_extracted_zara_unique.json", "w", encoding="UTF-8") as f:
#     json.dump(unique_list_products, f)


files = os.listdir("category_files")
list_products = []

for i in files:
    file_path = os.path.join("category_files", i)
    with open(file_path, "r") as f:
        catList = f.readlines()
    print(len(catList), i)
    list_products.extend(catList)

print(len(set(list_products)))

with open("all_zara_product_links.txt", "w") as f:
    f.writelines(list(set(list_products)))