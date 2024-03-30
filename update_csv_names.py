import csv

def update_image_paths(input_csv, output_csv):
    """Read the existing CSV file, update image paths, and write back to a new CSV file."""
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Remove unwanted part from image path
            row['image_path'] = row['image_path'].replace('images/', 'hm_images/')
            # Remove unwanted part from image path
            row['image_path'] = row['image_path'].replace('/content/images_woman/', 'hm_images/')

            writer.writerow(row)

if __name__ == "__main__":
    input_csv = "hm_images_metadata.csv"  # Replace with your existing CSV file
    output_csv = "hm_all_data.csv"  # Replace with the desired output CSV file
    update_image_paths(input_csv, output_csv)
    print(f"Image paths updated and written to: {output_csv}")
