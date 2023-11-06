import requests
from bs4 import BeautifulSoup
import argparse
import os
import pandas as pd
import time
import sys

DB_FILEPATH = os.path.join(os.environ["HOME"],  ".cache/tldgen/domains.csv")

CATEGORIES = [
    "country-code",  "generic", "generic-restricted", "infrastructure",
    "sponsored", "test"
]

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "target",
        help="string or file with lines to process. "
        "If none then stdin will be use",
        nargs="*",
    )

    parser.add_argument(
        "-c", "--category",
        help="Just append domains from given categories. Categories: {}.".format(", ".join(CATEGORIES)),
        metavar="CATEGORY",
        choices=CATEGORIES,
        action='append',
        nargs="+"
    )

    args = parser.parse_args()
    if args.category:
        args.category = flatten(args.category)

    return args


def main():
    args = parse_args()
    db = retrieve_db()

    if args.category:
        db = db[db["category"].isin(args.category)]


    for t in read_text_targets(args.target):
        domains = t.strip(".") + "." + db["ascii_tld"]
        print("\n".join(domains.to_list()))

def flatten(l):
    return [item for sublist in l for item in sublist]

def retrieve_db():
    seconds = 60 * 60 * 24 * 2
    if is_db_outdated(DB_FILEPATH, seconds=seconds):
        os.makedirs(os.path.dirname(DB_FILEPATH), exist_ok=True)
        download_db(DB_FILEPATH)

    return pd.read_csv(DB_FILEPATH)


def is_db_outdated(path, seconds):
    try:
        return is_file_older_than(path, seconds)
    except FileNotFoundError:
        return True

def is_file_older_than(path, seconds):
    m_time = os.path.getmtime(path)
    return time.time() - m_time > seconds

def download_db(path):
    resp = requests.get("https://www.iana.org/domains/root/db")
    soup = BeautifulSoup(resp.text, "html.parser")
    table_soup = soup.find("table", {"id": "tld-table"})
    tbody_soup = table_soup.find("tbody")

    domains = []
    for tr in tbody_soup.find_all("tr"):
        tds = tr.find_all("td")

        ascii_tld = tds[0].find("a")["href"][len("/domains/root/db/"):-len(".html")]
        domains.append({
            "ascii_tld": ascii_tld,
            "tld": tds[0].text.strip(),
            "category": tds[1].text,
            "org": tds[2].text.replace("\n", " ")
        })

    df = pd.DataFrame(domains)
    df.to_csv(path, index=False)


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
