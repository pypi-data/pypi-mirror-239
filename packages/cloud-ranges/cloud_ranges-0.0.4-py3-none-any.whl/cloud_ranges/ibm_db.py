from .range_db import CloudRangeDb
from .db_common import retrieve_db
import json
import pandas as pd
import ipaddress
import requests
import bs4

CLOUD_PROVIDER = "ibm"

class IbmRangeDb(CloudRangeDb):

    @classmethod
    def retrieve_db(cls):
        return retrieve_ibm_db()

    @classmethod
    def prepare_db(cls, db_file):
        return prepare_ibm_db(db_file)

    @classmethod
    def name(cls):
        return CLOUD_PROVIDER

def prepare_ibm_db(db_file):
    with open(db_file) as fi:
        content = json.load(fi)

    ranges = []
    for n in content:
        network_str = n["network"]
        network = ipaddress.ip_network(network_str)
        ranges.append({
            "start_ip": int(network[0]),
            "end_ip": int(network[-1]),
            "network": network_str,
            "version": network.version,
            "region": n["city"],
            "service": n["service"],

        })

    return pd.DataFrame(ranges)

def retrieve_ibm_db():
    seconds = 60 * 60 * 24 * 1
    return retrieve_db(
        CLOUD_PROVIDER,
        seconds,
        download_ibm_db_file
    )

def download_ibm_db_file(db_file):
    base_url = "https://cloud.ibm.com"
    resp = requests.get(base_url + "/docs-content/v4/toc/cloud-infrastructure")

    ips_path = resp.json()\
        ["topics"]\
        ["cloud-infrastructure-ibm-cloud-ip-ranges"]\
        ["content"]

    resp = requests.get(base_url + ips_path)
    ranges = extract_public_ips(resp)

    with open(db_file, "w") as fo:
        json.dump(ranges, fo, indent=2)

def extract_public_ips(resp):
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    public_rows = soup.select("#section-front-end-network tbody tr")

    ranges = []
    for row in public_rows:
        fields = row.find_all("td")
        ranges.append({
            "datacenter": fields[0].text,
            "city": fields[1].text,
            "network": fields[2].text,
            "service": "front-end",
        })

    load_balancer_rows = soup.select("#section-load-balancer-ips tbody tr")
    for row in load_balancer_rows:
        fields = row.find_all("td")
        for network in fields[2].text.split():
            ranges.append({
                "service": "load-balancer",
                "network": network,
                "datacenter": fields[0].text,
                "city": fields[1].text,
            })

    legacy_rows = soup.select("#section-legacy-networks tbody tr td")
    for row in legacy_rows:
        ranges.append({
            "service": "legacy",
            "datacenter": "",
            "city": "",
            "network": row.text
        })

    return ranges

