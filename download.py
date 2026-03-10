import os
import tarfile
import time
import argparse
import requests
from multiprocessing import Pool

def process_shard(args):
    """Handles the robust downloading and extracting of a single shard."""
    file_name, url, raw_dir, images_dir, ann_dir, max_retries = args
    
    final_tar_path = os.path.join(raw_dir, file_name)
    part_file_path = os.path.join(raw_dir, f"{file_name}.part")
    
    # ==========================================
    # PHASE 1: ROBUST DOWNLOAD
    # ==========================================
    download_complete = False
    
    if os.path.exists(final_tar_path):
        print(f"[SKIP] {file_name} already fully downloaded.")
        download_complete = True
    else:
        # Create the .part file immediately so we can track it
        if not os.path.exists(part_file_path):
            open(part_file_path, 'wb').close()

        for attempt in range(max_retries):
            try:
                # Check current size to resume partial downloads
                downloaded_bytes = os.path.getsize(part_file_path)
                headers = {}
                
                if downloaded_bytes > 0:
                    print(f"[RESUME] {file_name} from {downloaded_bytes} bytes (Attempt {attempt+1}/{max_retries})")
                    headers['Range'] = f'bytes={downloaded_bytes}-'
                else:
                    print(f"[DOWNLOAD] {file_name} (Attempt {attempt+1}/{max_retries})")

                # 15s to connect, 30s max wait between chunks
                response = requests.get(url, headers=headers, stream=True, timeout=(15, 30))
                response.raise_for_status()

                # If server allows resume (206), append. Otherwise (200), overwrite.
                mode = 'ab' if response.status_code == 206 else 'wb'

                with open(part_file_path, mode) as f:
                    for chunk in response.iter_content(chunk_size=65536): # 64KB chunks
                        if chunk:
                            f.write(chunk)
                
                # If we made it out of the loop without timing out, the file is done.
                os.rename(part_file_path, final_tar_path)
                download_complete = True
                print(f"[SUCCESS] {file_name} downloaded completely.")
                break 

            except requests.exceptions.RequestException as e:
                print(f"[NETWORK ERROR] {file_name} on attempt {attempt+1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5) # Catch our breath before hitting the server again

    # ==========================================
    # PHASE 2: EXTRACTION
    # ==========================================
    if not download_complete:
        print(f"[FAILED] {file_name} failed to download after {max_retries} attempts. Skipping extraction.")
        return

    # Create subdirectories for this specific shard to keep things organized
    shard_name = file_name.replace('.tar', '')
    shard_img_dir = os.path.join(images_dir, shard_name)
    shard_ann_dir = os.path.join(ann_dir, shard_name)

    if os.path.exists(shard_img_dir) and os.path.exists(shard_ann_dir):
        print(f"[SKIP] {file_name} already extracted.")
        return

    print(f"[EXTRACT] Unpacking {file_name}...")
    os.makedirs(shard_img_dir, exist_ok=True)
    os.makedirs(shard_ann_dir, exist_ok=True)

    try:
        with tarfile.open(final_tar_path, 'r') as tar:
            for member in tar.getmembers():
                if member.name.endswith(".jpg"):
                    tar.extract(member, path=shard_img_dir)
                elif member.name.endswith(".json"):
                    tar.extract(member, path=shard_ann_dir)
        print(f"[DONE] {file_name} extracted successfully!")
    except tarfile.TarError as e:
        print(f"[CORRUPTION ERROR] Could not extract {file_name}. The archive might be broken: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Robust SA-1B Downloader')
    parser.add_argument('--input_file', type=str, default='sa1b_links.txt', help='Path to the links text file')
    parser.add_argument('--raw_dir', type=str, default='raw', help='Where to save the .tar files')
    parser.add_argument('--images_dir', type=str, default='images', help='Where to save the .jpg files')
    parser.add_argument('--ann_dir', type=str, default='annotations', help='Where to save the .json files')
    parser.add_argument('--processes', type=int, default=16, help='Number of parallel downloads')
    parser.add_argument('--retries', type=int, default=5, help='How many times to retry a failed download')
    args = parser.parse_args()

    # Create necessary root directories
    for directory in [args.raw_dir, args.images_dir, args.ann_dir]:
        os.makedirs(directory, exist_ok=True)

    # Read and parse the input file
    tasks = []
    with open(args.input_file, 'r') as f:
        # Skip the header row
        lines = f.readlines()[1:] 
        for line in lines:
            parts = line.strip().split()
            # Ensure the line actually has a filename and a URL
            if len(parts) >= 2: 
                file_name = parts[0]
                url = parts[1]
                tasks.append((file_name, url, args.raw_dir, args.images_dir, args.ann_dir, args.retries))

    print(f"Loaded {len(tasks)} files to process. Starting {args.processes} workers...")

    # Execute in parallel
    with Pool(processes=args.processes) as pool:
        pool.map(process_shard, tasks)

    print("\nAll tasks completed!")