import os
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path
from multiprocessing import Pool
from functools import partial

def repack_tar(tar_path, sorted_dir, temp_dir):
    tar_path = Path(tar_path)
    out_tar_path = Path(sorted_dir) / tar_path.name
    
    # Skip if already processed (great for resuming if the script gets interrupted)
    if out_tar_path.exists():
        return f"Skipped {tar_path.name} (already exists)"

    # Extract to the temp directory
    with tempfile.TemporaryDirectory(dir=temp_dir) as tmpdir:
        try:
            # 1. Extract the scrambled tar to temp dir
            subprocess.run(["tar", "-xf", str(tar_path), "-C", tmpdir], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            
            # 2. Re-pack it directly back to sorted using the --sort=name flag
            subprocess.run(["tar", "--sort=name", "-cf", str(out_tar_path), "-C", tmpdir, "."], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            
            return f"Success: Repacked {tar_path.name}"
            
        except subprocess.CalledProcessError as e:
            # Capture and return the ACTUAL error message from tar
            return f"❌ Error processing {tar_path.name}:\n{e.stderr}"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Sort and repack the SA-1B .tar files to make them compatible with webdataset')
    parser.add_argument('--raw_dir', type=str, default='raw', help='Where the original unsorted .tar files are stored')
    parser.add_argument('--sorted_dir', type=str, default='sorted', help='Where to save the sorted .tar files')
    parser.add_argument('--temp_dir', type=str, default='temp', help='Where to save temporary files to be used during sorting')
    parser.add_argument('--num_workers', type=int, default=16, help='Number of parallel workers')
    args = parser.parse_args()

    os.makedirs(args.sorted_dir, exist_ok=True)
    os.makedirs(args.temp_dir, exist_ok=True)  # ensure temp dir exists
    
    tar_files = list(Path(args.raw_dir).glob("*.tar"))
    print(f"Found {len(tar_files)} raw (unsorted) .tar files. Starting highly-parallel repacking...")
    
    # Use functools.partial to pass the directory arguments to our worker function
    repack_worker = partial(repack_tar, sorted_dir=args.sorted_dir, temp_dir=args.temp_dir)
    
    # Fire up the worker pool
    with Pool(args.num_workers) as p:
        for result in p.imap_unordered(repack_worker, tar_files):
            print(result)

    # Clean up the temp directory after all workers are done
    print(f"\nCleaning up base temporary directory: {args.temp_dir}...")
    try:
        shutil.rmtree(args.temp_dir)
        print("Cleanup complete.")
    except Exception as e:
        print(f"Warning: Could not remove temp directory {args.temp_dir}: {e}")
        
    print(f"\nAll done! Update your training script to point to the {args.sorted_dir}/ directory.")