# SA-1B downloader
A simple Python utility to robustly download and extract the [SA-1B](https://ai.meta.com/datasets/segment-anything-downloads/) dataset, mostly written by Gemini. It implements the following features:

* Resuming from partial downloads.
* Retries in case of connection failures.
* (Optional) extracting the downloaded `.tar` files.
* (Optional) reordering the contents of the downloaded `.tar` files to make them compatible with `webdataset`.

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
* `--processes`: number of parallel processes to use for downloading and extracting files (default: `16`)
* `--input_file`: path to the text file containing the download links (default: `sa1b_links.txt`)
* `--raw_dir`: directory to store downloaded `.tar` files (default: `raw`)
* `--retries`: maximum number of retries if the connection fails for any reason (default: `5`)
* `--extract`: if set, extracts the downloaded `.tar` files (default: unset)
* `--images_dir`: directory to store extracted jpg files (default: `images`; effective only if `--extract` is set)
* `--ann_dir`: directory to store extracted json files (default: `annotations`; effective only if `--extract` is set)

### Sorting the contents of the sharded `.tar` files
If the `--extract` flag is set in the download script above, the contents of the downloaded `.tar` files will be extracted into the `images_dir` and `ann_dir` directories (images and annotations, respectively).

Instead of extracting the contents of the sharded `.tar` files into separate image and annotation directories, you might want to use the downloaded `.tar` files directly as a `webdataset`. However, in the original data released by Meta, the files within each `.tar` file are randomly ordered. To be able to use the downloaded `.tar` files as a `webdataset`, you will need to reorder their contents so that the image files and their corresponding annotation files within each `.tar` file are correctly paired together. I provide a simple script here (`repack.py`) that does this. You can run this script as follows: 

```python
python -u repack.py
```

This script takes the following arguments:
* `--raw_dir`: directory where the original unsorted `.tar` files are stored (default: `raw`)
* `--sorted_dir`: directory where the final correctly sorted `.tar` files will be saved (default: `sorted`)
* `--temp_dir`: a temporary directory to be used during sorting (default: `temp`)
* `--num_workers`: number of parallel workers (default: `16`)

**Note:** If you choose to use this option, make sure to only download the `.tar` files without extracting them in the first step, which is the default behavior of the `download.py` script, unless the `--extract` flag is explicitly set.