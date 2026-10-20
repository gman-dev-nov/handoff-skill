# HANDOFF: bookshop-sync — full context for transfer

> 2026-10-20, Claude Code session, working folder `/home/dev/projects/bookshop-sync`.
> Redundancy is intentional. This is a fictional example of the skill's output.

## Contents

1. The task
2. Timeline
3. Current artifacts and files
4. Current state
5. Architecture and key decisions
6. Rules and agreements applied
7. Not done / known issues
8. Open questions for the user
9. Environment pitfalls
10. Research / background
11. Recommended next steps

## 1. The task

Original request (close to verbatim): "Every night, take the supplier's CSV
price list and update prices and stock in our online shop. Don't touch books
we marked as 'manual price'."

Inputs:
- supplier price list sample: `/home/dev/projects/bookshop-sync/samples/supplier-2026-10-19.csv` (4 812 rows);
- shop API: REST, token in env var `SHOP_API_TOKEN` (value not in this document).

Expected result: a CLI script that can run from cron and prints a summary.

## 2. Timeline

| Round | User asked | Done | Result |
|---|---|---|---|
| 1 | Initial request | `sync.py` with CSV parser and dry-run mode | 4 812 rows parsed, 37 rows rejected (empty ISBN) |
| 2 | "Prices are off by 100x for some books" | Found that the supplier uses `,` as decimal separator in 212 rows; parser now accepts both | Dry run matches 20 spot-checked books |
| 3 | "Skip manual-price books" | Fetch tag `manual-price` from the shop API before updating | 58 books skipped in dry run |

Abandoned approach: pandas for parsing — dropped because the cron host has
Python 3.9 without pip access; the script now uses only the standard library.

## 3. Current artifacts and files

| File | Purpose |
|---|---|
| `/home/dev/projects/bookshop-sync/sync.py` | The CLI script |
| `/home/dev/projects/bookshop-sync/tests/test_parse.py` | Parser tests (decimal separators, empty ISBN) |
| `/home/dev/projects/bookshop-sync/samples/` | Supplier CSV samples, not committed |

Reproduce:

```bash
cd /home/dev/projects/bookshop-sync
python3 -m unittest discover tests
SHOP_API_TOKEN=<REDACTED: shop API token, ask the user> python3 sync.py samples/supplier-2026-10-19.csv --dry-run
```

## 4. Current state

- Tests: 9 passed (last run in this session).
- Dry run on the 2026-10-19 sample: 4 517 updates, 58 skipped (manual price), 37 rejected, 200 unchanged.
- A real (non-dry) run has **not** been executed.
- Git: branch `feat/nightly-sync`, 3 commits, not pushed.

## 5. Architecture and key decisions

- `parse_rows()` normalizes decimals and ISBNs; rejected rows go to `rejected.csv`.
- `fetch_manual_price_ids()` pages through the API (100 items per page).
- Updates are sent in batches of 50 (the API rejects larger batches with HTTP 413).
- Standard library only, because of the cron host (see section 9).

## 6. Rules and agreements applied

- Manual-price books are never updated (user, round 3).
- Stock is overwritten with the supplier value; local reservations are **not** taken into account — not discussed yet (see Q2).

## 7. Not done / known issues

1. No real run yet → waiting for Q1 → open.
2. Rows with an empty ISBN are rejected; the supplier sometimes puts the ISBN in the title → cause known → open.
3. No cron entry and no alerting → not started.

## 8. Open questions for the user

- **Q1.** May I run a real update on the production shop?
  a) yes, now; b) yes, but on a staging shop first; c) no, only dry runs for now.
- **Q2.** Stock: should local reservations be subtracted from the supplier value?
  a) yes; b) no, the supplier value is the truth.
- **Q3.** Where should the nightly summary go?
  a) email; b) a chat channel; c) only the log file.

## 9. Environment pitfalls

- Cron host has Python 3.9 and no pip → symptom: `ModuleNotFoundError: pandas` → workaround: standard library only.
- Shop API returns HTTP 413 for more than 50 items per request → workaround: batches of 50.

## 10. Research / background

Not applicable: no external research in this session.

## 11. Recommended next steps

1. Get answers to Q1–Q3.
2. If Q1-b: run against the staging shop and compare 20 random books.
3. Handle the ISBN-in-title case (issue 2).
4. Add the cron entry and the summary channel from Q3.
