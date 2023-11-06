from .range_db import CloudRangeDb
from .db_common import retrieve_db
from .utils import download_file
import json
import ipaddress
import pandas as pd
from functools import partial

CLOUD_PROVIDER = "aws"

class AwsRangeDb(CloudRangeDb):

    @classmethod
    def retrieve_db(cls):
        return retrieve_aws_db()

    @classmethod
    def prepare_db(cls, db_file):
        return prepare_aws_db(db_file)

    @classmethod
    def name(cls):
        return CLOUD_PROVIDER


def retrieve_aws_db():
    seconds = 60 * 60 * 24 * 1
    db_url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    return retrieve_db(
        CLOUD_PROVIDER,
        seconds,
        partial(download_file, db_url)
    )

def prepare_aws_db(db_file):
    with open(db_file) as fi:
        content = json.load(fi)

    ranges = []
    for p in content["prefixes"]:
        network = ipaddress.ip_network(p["ip_prefix"])
        start_ip = int(network[0])
        end_ip = int(network[-1])
        service = p["service"] if p["service"] != "AMAZON" else ""

        ranges.append({
            "start_ip": start_ip,
            "end_ip": end_ip,
            "network": p["ip_prefix"],
            "version": 4,
            "region": p["region"],
            "service": service,
        })

    for p in content["ipv6_prefixes"]:
        network = ipaddress.ip_network(p["ipv6_prefix"])
        start_ip = int(network[0])
        end_ip = int(network[-1])
        service = p["service"] if p["service"] != "AMAZON" else ""

        ranges.append({
            "start_ip": start_ip,
            "end_ip": end_ip,
            "network": p["ipv6_prefix"],
            "version": 6,
            "region": p["region"],
            "service": service,
        })

    df = pd.DataFrame(ranges)
    return df
