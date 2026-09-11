#!/usr/bin/env python3
"""
Download a LoTW log history in ADIF format.

Credentials are pulled from environment variables so this script is safe
to commit to a public GitHub repo:

    export LOTW_LOGIN="K2XYZ"
    export LOTW_PASSWORD="your-lotw-password"

Or use a .env file (see python-dotenv usage in the README) — just make
sure .env is listed in your .gitignore.

Usage:
    python3 lotw_download.py --start-date 2021-04-16
    python3 lotw_download.py --start-date 2021-04-16 --end-date 2024-12-31
    python3 lotw_download.py --start-date 2021-04-16 --output-dir logs
"""

import argparse
import os
import sys
from datetime import date
from pathlib import Path

import requests

LOTW_BASE_URL = "https://lotw.arrl.org/lotwuser/lotwreport.adi"
DEFAULT_OUTPUT_DIR = "adif_downloads"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download a LoTW log history in ADIF format."
    )
    parser.add_argument(
        "--start-date",
        required=True,
        metavar="YYYY-MM-DD",
        help="Earliest QSO date to include (required).",
    )
    parser.add_argument(
        "--end-date",
        default=None,
        metavar="YYYY-MM-DD",
        help="Latest QSO date to include (default: no upper bound, i.e. through today).",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save the .adi file into (default: {DEFAULT_OUTPUT_DIR}).",
    )
    return parser.parse_args()


def build_query_params(login: str, password: str, start_date: str, end_date: str | None) -> dict:
    params = {
        "login": login,
        "password": password,
        "qso_query": "1",
        "qso_qsl": "no",           # entire log, not just QSL-confirmed records
        "qso_startdate": start_date,
        "qso_mydetail": "yes",
        "qso_qsldetail": "yes",
    }
    if end_date:
        params["qso_enddate"] = end_date
    return params


def download_log(login: str, password: str, start_date: str, end_date: str | None, output_dir: Path) -> Path:
    params = build_query_params(login, password, start_date, end_date)

    range_desc = f"{start_date} to {end_date}" if end_date else f"{start_date} through today"
    print(f"Requesting LoTW log for {login}, {range_desc}...")
    resp = requests.get(LOTW_BASE_URL, params=params, timeout=60)
    resp.raise_for_status()

    text = resp.text
    if "<eoh>" not in text.lower():
        # LoTW returns plain ADIF; if the header terminator is missing,
        # something went wrong (bad login/password, etc.)
        print("Warning: response doesn't look like a valid ADIF file.")
        print("First 500 chars of response:")
        print(text[:500])
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    end_str = end_date if end_date else date.today().isoformat()
    out_path = output_dir / f"{login}_log_{start_date}_to_{end_str}.adi"
    out_path.write_text(text, encoding="utf-8")

    # Quick record count for a sanity check
    record_count = text.lower().count("<eor>")
    print(f"Saved {record_count} QSO records to {out_path}")

    return out_path


def main():
    args = parse_args()

    login = os.environ.get("LOTW_LOGIN")
    password = os.environ.get("LOTW_PASSWORD")

    if not login or not password:
        print(
            "Missing credentials. Set LOTW_LOGIN and LOTW_PASSWORD "
            "environment variables (or use a .env file) before running."
        )
        sys.exit(1)

    download_log(login, password, args.start_date, args.end_date, Path(args.output_dir))


if __name__ == "__main__":
    main()
