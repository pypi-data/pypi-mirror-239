#!/usr/bin/env python3
import pandas as pd
import argparse
import ipaddress
import sys
from tqdm import tqdm
import requests
import os
import time
import logging
import json

logger = logging.getLogger(os.path.basename(__file__))

DIR_NAME = ".cache/as-search"
DB_NAME = "ip2asn-v4-u32.tsv.gz"

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file",
        help="Provide the db file. For debugging purposes"
    )

    commands = parser.add_subparsers(dest="command", required=True)

    ip_parser = commands.add_parser(
        "ip",
        help="Retrieve the AS that contains the ip"
    )

    ip_parser.add_argument(
        "target",
        help="string or file with lines to process. "
        "If none then stdin will be use",
        nargs="*",
    )

    ip_parser.add_argument(
        "-j", "--json",
        help="Output in json format",
        action="store_true",
        default=False
    )

    org_parser = commands.add_parser(
        "org",
        help="Search AS by organization name"
    )

    org_parser.add_argument(
        "-i", "--ignore-case",
        help="Ignore case in regex match",
        default=False,
        action="store_true",
    )

    org_parser.add_argument(
        "target",
        help="string or file with lines to process. "
        "If none then stdin will be use",
        nargs="*",
    )

    org_parser.add_argument(
        "-j", "--json",
        help="Output in json format",
        action="store_true",
        default=False
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    db_file = retrieve_db(db_file=args.file)

    df = pd.read_csv(
        db_file,
        sep="\t",
        header=None,
        names=["start_ip", "end_ip", "asn", "country", "organization"]
    )

    print_entry = print_entry_json if args.json else print_entry_line

    if args.command == "ip":
        for ip in read_text_targets(args.target):
            entry = search_ip(df, ip)
            print_entry(entry)

    elif args.command == "org":
        for name in read_text_targets(args.target):
            entries = search_by_name(df, name, case=not args.ignore_case)
            for entry in entries:
                print_entry(entry)
    else:
        logger.error("This is not the command you're looking for")
        return -1

def print_entry_line(entry):
    line = " ".join([
        entry["target"],
        entry["start_ip"],
        entry["end_ip"],
        str(entry["country"]),
        entry["organization"],
    ])
    print(line)

def print_entry_json(entry):
    print(json.dumps(entry))

def search_ip(as_df, ip):
    ip_number = int(ipaddress.ip_address(ip))
    row = as_df.query(
        "start_ip <= @ip_number and end_ip >= @ip_number"
    ).iloc[0]

    start_ip = str(ipaddress.ip_address(int(row["start_ip"])))
    end_ip = str(ipaddress.ip_address(int(row["end_ip"])))
    organization = row["organization"]
    asn = row["asn"]
    country = row["country"]

    return {
        "target": ip,
        "asn": int(asn),
        "organization": organization,
        "country": country,
        "start_ip": start_ip,
        "end_ip": end_ip,
    }

def search_by_name(as_df, name, case=True):
    rows = as_df[as_df.organization.str.contains(name, case=case)]

    entries = []
    for _, row in rows.iterrows():
        start_ip = str(ipaddress.ip_address(int(row["start_ip"])))
        end_ip = str(ipaddress.ip_address(int(row["end_ip"])))
        organization = row["organization"]
        asn = row["asn"]
        country = row["country"]

        entries.append({
            "target": name,
            "asn": int(asn),
            "organization": organization,
            "country": country,
            "start_ip": start_ip,
            "end_ip": end_ip,
        })

    return entries

def retrieve_db(db_file=None):
    if db_file:
        return db_file

    db_dir = os.path.join(os.environ["HOME"], DIR_NAME)
    db_file = os.path.join(db_dir, DB_NAME)

    download_again = False
    try:
        m_time = os.path.getmtime(db_file)
        if time.time() - m_time > 60 * 60 * 24 * 1:
            download_again = True
    except FileNotFoundError:
        download_again = True

    if download_again:
        os.makedirs(db_dir, exist_ok=True)
        eprint("Downloading ASN database...")
        download_db(db_file)

    return db_file

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def download_db(path):
    url = "https://iptoasn.com/data/ip2asn-v4-u32.tsv.gz"
    resp = requests.get(url, stream=True)
    total_size = int(resp.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(path, 'wb') as file:
        for data in resp.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
        progress_bar.close()


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
