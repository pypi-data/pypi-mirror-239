
import os
import time
import requests
from tqdm import tqdm
from .utils import is_db_outdated, eprint

DB_DIR = os.path.join(os.environ["HOME"],  ".cache/cloud-ranges")

def db_dir():
    return DB_DIR

def retrieve_db(
        cloud_provider,
        seconds,
        download_db
):

    db_file = os.path.join(db_dir(), "{}-ip-ranges.json".format(cloud_provider))

    if is_db_outdated(db_file, seconds=seconds):
        os.makedirs(db_dir(), exist_ok=True)
        eprint("Downloading {} database...".format(cloud_provider))
        download_db(db_file)

    return db_file

