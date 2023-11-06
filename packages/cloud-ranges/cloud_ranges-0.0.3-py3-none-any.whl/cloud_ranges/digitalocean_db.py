from .range_db import CloudRangeDb
from .db_common import retrieve_db
from .utils import download_file
import ipaddress
import pandas as pd
from functools import partial

CLOUD_PROVIDER = "digitalocean"

class DigitalOceanRangeDb(CloudRangeDb):

    @classmethod
    def retrieve_db(cls):
        return retrieve_digitalocean_db()

    @classmethod
    def prepare_db(cls, db_file):
        return prepare_digitalocean_db(db_file)

    @classmethod
    def name(cls):
        return CLOUD_PROVIDER


def retrieve_digitalocean_db():
    seconds = 60 * 60 * 24 * 1
    db_url = "https://digitalocean.com/geo/google.csv"
    return retrieve_db(
        CLOUD_PROVIDER,
        seconds,
        partial(download_file, db_url)
    )

def prepare_digitalocean_db(db_file):
    df = pd.read_csv(
        db_file,
        header=None,
        names=["network", "country", "region", "city", "postcode"]
    )

    df["start_ip"] = df["network"].map(
        lambda n: int(ipaddress.ip_network(n)[0])
    )
    df["end_ip"] = df["network"].map(
        lambda n: int(ipaddress.ip_network(n)[-1])
    )
    df["version"] = df["network"].map(
        lambda n: ipaddress.ip_network(n).version
    )
    df["service"] = ""

    return df
