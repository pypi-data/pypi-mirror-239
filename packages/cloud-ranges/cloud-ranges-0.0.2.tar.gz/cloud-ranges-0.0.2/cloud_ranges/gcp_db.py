
from .range_db import CloudRangeDb
from .db_common import retrieve_db
from .utils import download_file
import json
import pandas as pd
import ipaddress
from functools import partial

# GCP ranges
# https://www.gstatic.com/ipranges/cloud.json

CLOUD_PROVIDER = "gcp"

class GcpRangeDb(CloudRangeDb):

    @classmethod
    def retrieve_db(cls):
        return retrieve_gcp_db()

    @classmethod
    def prepare_db(cls, db_file):
        return prepare_gcp_db(db_file)

    @classmethod
    def name(cls):
        return CLOUD_PROVIDER



def prepare_gcp_db(db_file):
    with open(db_file) as fi:
        content = json.load(fi)

    ranges = []
    for p in content["prefixes"]:
        try:
            network_str = p["ipv4Prefix"]
        except KeyError:
            network_str = p["ipv6Prefix"]
            continue

        network = ipaddress.ip_network(network_str)
        service = p["service"] if p["service"] != "Google Cloud" else ""

        ranges.append({
            "start_ip": int(network[0]),
            "end_ip": int(network[-1]),
            "network": network_str,
            "version": network.version,
            "region": p["scope"],
            "service": service
        })

    return pd.DataFrame(ranges)



def retrieve_gcp_db():
    seconds = 60 * 60 * 24 * 1
    db_url = "https://www.gstatic.com/ipranges/cloud.json"
    return retrieve_db(
        CLOUD_PROVIDER,
        seconds,
        partial(download_file, db_url)
    )
