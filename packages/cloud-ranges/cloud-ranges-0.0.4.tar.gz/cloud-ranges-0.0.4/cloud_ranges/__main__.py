#!/usr/bin/env python3
import argparse
import json
import sys
from .aws_db import AwsRangeDb
from .gcp_db import GcpRangeDb
from .azure_db import AzureRangeDb
from .digitalocean_db import DigitalOceanRangeDb
from .oracle_db import OracleRangeDb
from .ibm_db import IbmRangeDb

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "ip",
        help="IP or file with IPs (per line). "
        "If none then stdin will be use",
        nargs="*",
    )

    parser.add_argument(
        "-j", "--json",
        help="Output in json format",
        action="store_true",
        default=False
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    dbs = [
        AwsRangeDb(),
        AzureRangeDb(),
        GcpRangeDb(),
        DigitalOceanRangeDb(),
        OracleRangeDb(),
        IbmRangeDb(),
    ]

    if args.json:
        print_entry = print_entry_json
    else:
        print_entry = print_entry_line

    for ip in read_text_targets(args.ip):
        for db in dbs:
            try:
                entry = db.search_ip(ip)
                entry["target"] = ip
            except KeyError:
                continue

            print_entry(entry)
            break


def print_entry_line(entry):
    services = ",".join(entry["services"])
    line = " ".join([
        entry["target"],
        entry["cloud"],
        entry["region"],
        entry["network"],
        services,
    ])
    print(line)

def print_entry_json(entry):
    print(json.dumps(entry))

def read_text_targets(targets):
    yield from read_text_lines(read_targets(targets))

def read_targets(targets):
    """Function to process the program ouput that allows to read an array
    of strings or lines of a file in a standard way. In case nothing is
    provided, input will be taken from stdin.
    """
    if not targets:
        yield from sys.stdin

    for target in targets:
        try:
            with open(target) as fi:
                yield from fi
        except FileNotFoundError:
            yield target


def read_text_lines(fd):
    """To read lines from a file and skip empty lines or those commented
    (starting by #)
    """
    for line in fd:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            continue

        yield line


if __name__ == '__main__':
    exit(main())
