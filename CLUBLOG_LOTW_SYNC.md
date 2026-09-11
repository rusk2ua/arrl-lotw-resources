# Syncing Your LoTW Log with Club Log

A step-by-step workflow for new users who want their [Logbook of The World (LoTW)](https://lotw.arrl.org/) confirmations reflected in [Club Log](https://clublog.org), using the `lotw_download.py` tool from this repo.

## Two ways to do this — pick one

Club Log actually offers **two different paths** to get LoTW data into your account. They are not the same thing, and it's worth understanding the difference before you start:

| | **Option A: Manual ADIF import (this repo)** | **Option B: Club Log's native LoTW Tools** |
|---|---|---|
| What it does | Downloads your LoTW QSL report as a file, which you upload to Club Log like any other ADIF log | Two-way integration: Club Log stores your LoTW certificates and syncs directly with LoTW's servers |
| Credentials shared with Club Log | None — your LoTW login/password never touch Club Log | Your LoTW **certificate files** (via an encrypted Encryption Key) are uploaded to and stored by Club Log |
| Can upload/sign new QSOs to LoTW from Club Log? | No — download only | Yes |
| Setup complexity | Low | Higher (requires TQSL, certificate export, Encryption Key management) |
| Good for | Users who just want QSL status/DXCC credit to show up in Club Log, and who'd rather not hand their LoTW certificates to a third-party site | Users who want Club Log to actively manage signing and uploading new QSOs to LoTW on their behalf |

**This document focuses on Option A**, since that's what `lotw_download.py` is built for. Option B is covered briefly at the end for context, in case you decide you want that instead down the road.

---

## Option A: Manual ADIF import using this repo's tools

### Prerequisites

- A Club Log account for your call sign — sign up free at [clublog.org](https://clublog.org) if you don't have one yet
- Your call sign's log already uploaded to Club Log at least once (via Club Log's normal "Upload" feature, or real-time logging integration from your desktop software)
- This repo cloned and set up per the main [README.md](README.md) (Python 3, `pip install -r requirements.txt`, `LOTW_LOGIN` / `LOTW_PASSWORD` environment variables set)

### Step 1: Download your LoTW QSL report

Run the download script, specifying the earliest date you want covered. If this is your first time syncing, use your earliest LoTW QSO date (or just a date well before you started using LoTW) as the start date:

```bash
python3 lotw_download.py --start-date 2021-04-16
```

This produces a file like `adif_downloads/K2XYZ_log_2021-04-16_to_2026-09-11.adi`.

> **Note:** This script requests QSOs with `qso_qsl=no`, meaning it captures your *entire* logged history from LoTW — not just confirmed QSLs. That's intentional: it gives Club Log the full picture of your logged activity plus whatever QSL/confirmation status LoTW has on record for each QSO, rather than a QSL-only subset.

### Step 2: Log in to Club Log

Go to [clublog.org](https://clublog.org) and log in with your Club Log account.

### Step 3: Upload the ADIF file to Club Log

1. From the Club Log menu, choose **Upload**.
2. Select the `.adi` file you just downloaded (e.g., `K2XYZ_log_2021-04-16_to_2026-09-11.adi`).
3. Confirm the call sign you're uploading against matches the one you want updated — **do not** select "any" if given the option; pick your specific call sign explicitly.
4. Submit the upload.

Club Log will process the file and match records against your existing log by date, time, band, mode, and worked call sign.

### Step 4: Verify the QSL status updated

Once processing finishes (usually within a few minutes):

- Open your **DXCC** chart in Club Log.
- QSOs that have been credited via LoTW confirmations should now show a **blue "V"** marker.
- Spot-check a handful of QSOs you know were LoTW-confirmed to make sure they're reflected correctly.

### Step 5: Repeat periodically

Every time you want to refresh Club Log with your latest LoTW confirmations:

1. Re-run the script with an updated `--start-date` (or the same one — duplicates are generally handled gracefully by Club Log's matching, but using a tighter date range keeps your uploads smaller and faster):

   ```bash
   python3 lotw_download.py --start-date 2026-01-01
   ```

2. Upload the new `.adi` file to Club Log the same way (Step 3).

> **Tip:** Once the [incremental sync mode](README.md#roadmap) planned in this repo's roadmap is built, this manual "pick a start date" step will be replaced by automatic tracking of the last sync point (`APP_LoTW_LASTQSORX`), so you can just re-run the script with no date math required.

---

## Option B: Club Log's native LoTW Tools (for reference)

If later on you decide you'd rather have Club Log manage the sync directly — including *sending* signed QSOs to LoTW, not just pulling confirmations — Club Log has a built-in feature for this at **LoTW Tools** (menu: "Club Log tools" → "LoTW Tools", or directly at `https://clublog.org/lotw`). Broadly, it works in three stages:

1. **Upload your LoTW certificates.** Export a `.tbk` (Trusted QSL Backup) file from your TQSL desktop application and upload it to Club Log. Club Log encrypts your certificates using an Encryption Key that only you control — save this key somewhere safe, since it's required to unlock your certificates again.
2. **Download QSLs from LoTW into Club Log.** Enter your LoTW login credentials directly into Club Log's LoTW Tools page (Club Log states these aren't stored) and click "Sync LoTW with Club Log."
3. **Sign and send new QSOs from Club Log to LoTW.** Once you've downloaded at least once (step 2), you can use Club Log to sign and upload new QSOs straight to LoTW using your stored certificates.

This is a more involved setup and means trusting Club Log with your certificate material (encrypted, but stored on their servers). Option A avoids that entirely by keeping certificate handling and LoTW downloads local to your own machine, at the cost of not being able to push new QSOs to LoTW from Club Log.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Script exits with a credentials error | `LOTW_LOGIN` / `LOTW_PASSWORD` environment variables aren't set, or are wrong |
| Downloaded `.adi` file looks empty or tiny | Double check `--start-date` isn't set in the future, and that your LoTW account actually has QSOs logged in that range |
| Club Log upload doesn't show new QSLs | Confirm you selected the correct call sign during upload (not "any"); also allow a few minutes for Club Log's queue to process |
| QSOs appear in Club Log but no blue "V" on DXCC chart | The QSO may not yet be eligible for DXCC credit, or the matching station's LoTW record doesn't confirm the specific band/mode needed |

For anything specific to LoTW itself (certificates, TQSL, account issues), see [ARRL's LoTW help](http://www.arrl.org/lotw-help). For Club Log—specific issues, see [Club Log's support site](https://clublog.freshdesk.com/support/home).
