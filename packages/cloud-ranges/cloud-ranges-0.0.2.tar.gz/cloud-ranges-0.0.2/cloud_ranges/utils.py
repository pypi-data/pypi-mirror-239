
import requests
import sys
import os
import time
from tqdm import tqdm

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def is_db_outdated(path, seconds):
    try:
        return is_file_older_than(path, seconds)
    except FileNotFoundError:
        return True

def is_file_older_than(path, seconds):
    m_time = os.path.getmtime(path)
    return time.time() - m_time > seconds

def download_file(url, path):
    resp = requests.get(url, stream=True)
    total_size = int(resp.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(path, 'wb') as file:
        for data in resp.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
        progress_bar.close()

