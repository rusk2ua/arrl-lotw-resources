# lotw-tools

Python utilities for pulling data from ARRL's [Logbook of The World (LoTW)](https://lotw.arrl.org/) for call sign **K2UA**.

This started as a simple ADIF log downloader and is expected to grow into a small toolkit for other LoTW-related tasks (see [Roadmap](#roadmap)).

## What's here

| Script | Description |
|---|---|
| `lotw_download.py` | Downloads the full QSO log history (as ADIF) via LoTW's `lotwreport.adi` query interface |

## Background: how LoTW queries work

LoTW returns log data over HTTPS `GET` requests to:

```
https://lotw.arrl.org/lotwuser/lotwreport.adi
```

with query parameters selecting which records and fields come back. Full parameter reference: [ARRL ADIF / LoTW Output docs](http://www.arrl.org/adif).

Key parameters used by this project:

| Parameter | Value used | Why |
|---|---|---|
| `login` | your LoTW username | required |
| `password` | your LoTW password | required |
| `qso_query` | `1` | required, or no records are returned |
| `qso_qsl` | `no` | returns **all** QSOs, not just QSL-confirmed ones (default is `yes`, which silently filters to confirmed-only) |
| `qso_startdate` | `2021-04-16` | earliest QSO date to include (filters on QSO date, not upload date) |
| `qso_mydetail` | `yes` | includes your own station's location fields (MY_DXCC, MY_GRIDSQUARE, MY_STATE, etc.) |
| `qso_qsldetail` | `yes` | includes the confirming station's location fields, where available |

**Note:** `qso_qslsince` only applies when `qso_qsl=yes`; `qso_qsorxsince` only applies when `qso_qsl=no`. Don't mix them up when adjusting filters.

## Setup

```bash
git clone <this-repo-url>
cd lotw-tools
pip install -r requirements.txt
```

### Credentials

Credentials are **never** hardcoded or committed. Set them as environment variables:

```bash
export LOTW_LOGIN="K2UA"
export LOTW_PASSWORD="your-lotw-password"
```

Or use a `.env` file (already covered by `.gitignore` in this repo — see [Security](#security) below):

```
LOTW_LOGIN=K2UA
LOTW_PASSWORD=your-lotw-password
```

## Usage

### Download full log history

```bash
python3 lotw_download.py
```

Saves to `adif_downloads/K2UA_log_<start-date>_to_<today>.adi` and prints the number of QSO records retrieved.

To change the start date, edit `START_DATE` near the top of `lotw_download.py`.

## Security

- Credentials load from environment variables / `.env` only — never from source.
- `.env` is included in `.gitignore`. **Double-check `git status` before committing** if you ever create one.
- Downloaded `.adi` files under `adif_downloads/` are also gitignored by default, since they contain your full QSO history (worked stations, timestamps, grid squares, etc.).

## Roadmap

Planned additions as this grows beyond a single download script:

- [ ] Incremental sync mode (track `APP_LoTW_LASTQSORX` between runs instead of re-pulling full history)
- [ ] QSL-confirmed-only report (`qso_qsl=yes` path) for award-tracking use cases
- [ ] Filtering helpers (by band, mode, DXCC entity, date range) as CLI flags
- [ ] Parsing/analysis layer to turn ADIF output into a DataFrame for stats (worked DXCC count, band/mode breakdowns, etc.)
- [ ] Possibly: LoTW certificate/upload-side functions, if useful

## License

TBD
