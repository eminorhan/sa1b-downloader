# SA-1B downloader
A simple Python script to robustly download and extract the [SA-1B](https://ai.meta.com/datasets/segment-anything-downloads/) dataset, mostly written by Gemini. It implements the following features:

* Resuming from partial downloads.
* Retries in case of connection failures.

## Requirements
The only external requirement is `requests`. Install it with:
```
pip install requests
```

## Usage
First, download the text file that contains the download links from [here](https://ai.meta.com/datasets/segment-anything-downloads/). Note that the links in this file are dynamic, so if you haven't downloaded the file recently, you may have to redownload it for fresh links. Then, simply run:

```python
python -u download.py
```

This script takes the following arguments:
* `processes`: number of parallel processes to use for downloading and extracting files (default: `16`)
* `input_file`: path to the text file containing the download links (default: `sa1b_links.txt`)
* `raw_dir`: directory to store downloaded data shard files (default: `raw`)
* `images_dir`: directory to store extracted jpg files (default: `images`)
* `ann_dir`: directory to store extracted json files (default: `annotations`)
* `retries`: maximum number of retries if the connection fails for any reason (default: `5`)

### Sorting the contents of the sharded `.tar` files and repacking them
Instead of extracting the contents of the sharded `.tar` archives into separate image and annotation directories, you might want to use them directly as a `webdataset`. However, in the original data released by Meta, the files within the sharded `.tar` archives are randomly ordered. To be able to use the `.tar` archives as a `webdataset`, you will need to reorder their contents so that the image files and their corresponding annotation files within each `.tar` file are correctly paired together. I provide a simple script here (`repack.py`) that does this. You can run this script as follows: 

```python
python -u repack.py
```

This script takes the following arguments:
* `raw_dir`: directory where the original unsorted `.tar` files are stored (default: `raw`)
* `sorted_dir`: directory where the final correctly sorted `.tar` files will be saved (default: `sorted`)
* `temp_dir`: a temporary directory to be used during sorting (default: `temp`)
* `num_workers`: number of parallel workers (default: `16`)