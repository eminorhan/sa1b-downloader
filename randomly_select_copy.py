import os
import random
import shutil

# Source directory containing the JPG files
source_directory = '/vast/eo41/sa-1b/images'

# Destination directory where the selected images will be copied
destination_directory = '/vast/eo41/sa-1b/images_1000'

n_imgs = 1000

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# List all JPG files in the source directory
jpg_files = [f for f in os.listdir(source_directory) if f.endswith('.jpg')]

# Check if there are at least 100 JPG files
if len(jpg_files) < n_imgs:
    print("There are not enough JPG files in the source directory.")
else:
    # Randomly select 100 unique JPG files
    selected_files = random.sample(jpg_files, n_imgs)

    # Copy the selected files to the destination directory
    for file_name in selected_files:
        source_path = os.path.join(source_directory, file_name)
        destination_path = os.path.join(destination_directory, file_name)
        shutil.copy2(source_path, destination_path)
        print(f"Copied: {file_name}")

print("Done")
