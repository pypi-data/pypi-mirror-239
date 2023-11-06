
from .range_db import CloudRangeDb
from .db_common import retrieve_db
from .utils import download_file
import json
import pandas as pd
import ipaddress
import requests
import bs4

# Azure
# https://www.microsoft.com/en-us/download/details.aspx?id=56519

CLOUD_PROVIDER = "azure"

class AzureRangeDb(CloudRangeDb):

    @classmethod
    def retrieve_db(cls):
        return retrieve_azure_db()

    @classmethod
    def prepare_db(cls, db_file):
        return prepare_azure_db(db_file)

    @classmethod
    def name(cls):
        return CLOUD_PROVIDER

def prepare_azure_db(db_file):
    with open(db_file) as fi:
        content = json.load(fi)

    ranges = []
    for s in content["values"]:
        region = s["properties"]["region"]
        service = s["properties"]["systemService"]
        if not region:
            continue
        for p in s["properties"]["addressPrefixes"]:
            network = ipaddress.ip_network(p)
            ranges.append({
                "start_ip": int(network[0]),
                "end_ip": int(network[-1]),
                "network": p,
                "version": network.version,
                "region": region,
                "service": service,
            })

    return pd.DataFrame(ranges)


def retrieve_azure_db():
    seconds = 60 * 60 * 24 * 1
    return retrieve_db(
        CLOUD_PROVIDER,
        seconds,
        download_azure_db_file
    )

def download_azure_db_file(db_file):
    resp = requests.get(
        "https://www.microsoft.com/en-us/download/details.aspx?id=56519",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
        }
    )

    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    db_url = soup.find_all("a", class_="dlcdetail__download-btn")[0]["href"]

    download_file(db_url, db_file)
