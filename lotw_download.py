#!/usr/bin/env python3
"""
Download K2UA's LoTW log history in ADIF format.

Credentials are pulled from environment variables so this script is safe
to commit to a public GitHub repo:

    export LOTW_LOGIN="K2UA"
    export LOTW_PASSWORD="your-lotw-password"

Or use a .env file (see python-dotenv usage below) — just make sure
.env is listed in your .gitignore.
"""

import os
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlencode

import requests

LOTW_BASE_URL = "https://lotw.arrl.org/lotwuser/lotwreport.adi"

# --- Config -----------------------------------------------------------
START_DATE = "2021-04-16"   # earliest QSO date to include
OUTPUT_DIR = Path("adif_downloads")
# ------------------------------------------------------------------------


def build_query_params(login: str, password: str) -> dict:
    return {
        "login": login,
        "password": password,
        "qso_query": "1",
        "qso_qsl": "no",           # entire log, not just QSL-confirmed records
        "qso_startdate": START_DATE,
        "qso_mydetail": "yes",
        "qso_qsldetail": "yes",
    }


def download_log(login: str, password: str) -> Path:
    params = build_query_params(login, password)

    print(f"Requesting LoTW log for {login} since {START_DATE}...")
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

    OUTPUT_DIR.mkdir(exist_ok=True)
    today_str = date.today().isoformat()
    out_path = OUTPUT_DIR / f"{login}_log_{START_DATE}_to_{today_str}.adi"
    out_path.write_text(text, encoding="utf-8")

    # Quick record count for a sanity check
    record_count = text.lower().count("<eor>")
    print(f"Saved {record_count} QSO records to {out_path}")

    return out_path


def main():
    login = os.environ.get("LOTW_LOGIN")
    password = os.environ.get("LOTW_PASSWORD")

    if not login or not password:
        print(
            "Missing credentials. Set LOTW_LOGIN and LOTW_PASSWORD "
            "environment variables (or use a .env file) before running."
        )
        sys.exit(1)

    download_log(login, password)


if __name__ == "__main__":
    main()
