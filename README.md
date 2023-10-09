# SA-1B downloader
This repo is based on the [SA-1B downloader repo by Konstantinos Kallidromitis](https://github.com/KKallidromitis/SA-1B-Downloader). It provides two additional functionalities over the original repo: 
* deleting the raw data shard files once they are extracted.
* allowing for a subset of the data to be downloaded only if disk space is limited.

## Requirements
* Python >= 3.6
* requests >= 2.0

Install with:
```
pip install requests
```

## Usage

The [download.py]() script uses the provided [sa1b_links.txt]() file by default as the input file for downloading and extracting images:

```python
python -u download.py \
    --processes 8 \
    --input_file 'sa1b_links.txt' \
    --raw_dir raw \
    --images_dir images \
    --masks_dir masks \
    --num_files 48 \
    --skip_existing
```

This script takes the following arguments:
* `processes`: number of processes to use for downloading and extracting files (default: `4`)
* `input_file`: path to the input file containing file names and URLs (default: `sa1b_links.txt`)
* `raw_dir`: directory to store downloaded data shard files (default: `raw`)
* `images_dir`: directory to store extracted jpg files (default: `images`)
* `masks_dir`: directory to store extracted json files (default: `masks`)
* `num_files`: number of data shard files to download and extract (default: `1000`, *i.e.* the full dataset)
* `skip_existing`: skip extraction if the file has already been extracted (default: `False`)