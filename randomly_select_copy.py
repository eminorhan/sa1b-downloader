import os
import random
import shutil
import argparse

parser = argparse.ArgumentParser(description='Randomly select a given number of images.')
parser.add_argument('--index', type=int, default=4, help='Number of processes to use for downloading and extracting files.')
parser.add_argument('--n_imgs', type=int, default=1, help='Number of images to sample.')
parser.add_argument('--source_dir', type=str, default='/vast/eo41/sa-1b/images', help='Directory where images are stored.')
parser.add_argument('--destination_root_dir', type=str, default='/vast/eo41/sa-1b', help='Directory where randomly sampled images will be saved.')

args = parser.parse_args()
print(args)

# Destination directory where the selected images will be copied
destination_directory = f'{args.destination_root_dir}/images_{args.n_imgs}/{args.index}/{args.index}'

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# List all JPG files in the source directory
jpg_files = [f for f in os.listdir(args.source_dir) if f.endswith('.jpg')]

# Check if there are at least n_imgs JPG files
if len(jpg_files) < args.n_imgs:
    print("There are not enough JPG files in the source directory.")
else:
    # Randomly select n_imgs unique JPG files
    selected_files = random.sample(jpg_files, args.n_imgs)

    # Copy the selected files to the destination directory
    for file_name in selected_files:
        source_path = os.path.join(args.source_dir, file_name)
        destination_path = os.path.join(destination_directory, file_name)
        shutil.copy2(source_path, destination_path)
        print(f"Copied: {file_name}")

print("Done")
