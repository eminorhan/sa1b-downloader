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
First, download the text file that contains the download links from [here](https://ai.meta.com/datasets/segment-anything-downloads/). Note that the links in this file are dynamic, so if you haven't downloaded the file recently, you will have to redownload it for fresh links. Then, simply run:

```python
python -u download.py
```

This script takes the following arguments:
* `processes`: number of parallel processes to use for downloading and extracting files (default: `16`)
* `input_file`: path to the text file containing the download links (default: `sa1b_links.txt`)
* `raw_dir`: directory to store downloaded data shard files (default: `raw`)
* `images_dir`: directory to store extracted jpg files (default: `images`)
* `ann_dir`: directory to store extracted json files (default: `annotations`)
* `retries`: maximum number of retries if the download fails for any reason (default: `5`)