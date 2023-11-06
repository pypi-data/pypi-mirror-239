from .range_db import CloudRangeDb
from .db_common import retrieve_db
from .utils import download_file
import json
import ipaddress
import pandas as pd
from functools import partial

CLOUD_PROVIDER = "oracle"

class OracleRangeDb(CloudRangeDb):

    @classmethod
    def retrieve_db(cls):
        return retrieve_oracle_db()

    @classmethod
    def prepare_db(cls, db_file):
        return prepare_oracle_db(db_file)

    @classmethod
    def name(cls):
        return CLOUD_PROVIDER

def retrieve_oracle_db():
    seconds = 60 * 60 * 24 * 1
    db_url = "https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json"
    return retrieve_db(
        CLOUD_PROVIDER,
        seconds,
        partial(download_file, db_url)
    )

def prepare_oracle_db(db_file):
    with open(db_file) as fi:
        content = json.load(fi)

    ranges = []
    for r in content["regions"]:
        region = r["region"]
        for c in r["cidrs"]:
            network_str = c["cidr"]
            network = ipaddress.ip_network(network_str)
            for tag in c["tags"]:
                ranges.append({
                    "start_ip": int(network[0]),
                    "end_ip": int(network[-1]),
                    "network": network_str,
                    "version": network.version,
                    "region": region,
                    "service": tag
                })

    return pd.DataFrame(ranges)
