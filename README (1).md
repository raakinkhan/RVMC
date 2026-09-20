# RVMC — RV Marks Checker 🎯

*"Am I getting the Achiever's Card or not?" — the question that started this repo.*

RVMC is a small Playwright-powered automation script that logs into RV's student portal for every classmate in a section, pulls their latest mock-exam marks, and prints them out — instantly. No more refreshing the portal fifty times or manually clicking through classmates' scores to figure out where you rank.

## Why this exists

Every time results drop, half the class scrambles to compare marks one login at a time. That's slow, tedious, and error-prone. RVMC automates the boring part: it walks through the whole class roster, logs in, navigates to the right exam, scrapes the score, and hands you a clean printout — so you can spend less time clicking and more time obsessing over whether you cleared the cutoff.

## How it works

1. **`Reader.py`** loads the class seating chart (`2E SEC SEATING.xlsx`) with `pandas` and builds a `{student_id: [name]}` lookup.
2. **`main.py`** spins up a real Chrome browser via [Playwright](https://playwright.dev/python/), and for each student ID:
   - Logs into the portal (`https://rvlh.ilearn.edusquares.com/login`), falling back to the parent account (`_p` suffix) if the student's own password has been changed.
   - Navigates into the course dashboard, hops into **Test Performance**, and picks the right exam category (KCET or JEE Main).
   - Opens the specified test and scrapes the marks off the results page.
   - Prints `name, marks` to the console.
3. Handles the portal's occasional "throws you back to the same page" bug with a friendly re-click, and gracefully skips students whose results aren't published yet or who've changed both account passwords.

## Tech stack

| Piece | Purpose |
|---|---|
| [Playwright](https://playwright.dev/python/) (sync API) | Browser automation / scraping |
| [pandas](https://pandas.pydata.org/) | Reading the seating-chart Excel sheet |
| `openpyxl` (via pandas) | `.xlsx` parsing |

## Setup

```bash
git clone https://github.com/raakinkhan/RVMC.git
cd RVMC
pip install playwright pandas openpyxl
playwright install chromium
```

Make sure `2E SEC SEATING.xlsx` (or your own seating-chart file) is in the project root — `Reader.py` expects the student name in column `Unnamed: 2` and student ID in `Unnamed: 1`, starting from row 3.

## Usage

```bash
python main.py
```

By default it runs against everyone in the roster (skipping the first 11 rows — tweak that loop in `main.py` to suit your class list), checking marks for `"II PU WEEKLY TEST 09 (KCET 03)"`. Want a different test or the JEE stream instead?

```python
get_indiviual(username="251689", exam_type="jee", exam_name="II PU WEEKLY TEST 10 (JEE MAIN)")
```

## A quick honesty note ⚠️

This script logs into other students' accounts using portal-issued default credentials (student ID as both username and password, with a parent-account fallback). It was built as a personal, small-scale convenience tool for checking a class rank — **not** as a way to snoop on people who've actually secured their accounts, which is why it politely gives up the moment someone's changed their password. If you fork this, please keep that spirit: use it only where you already have legitimate access, respect your school's IT policies, and don't turn it into anything that oversteps consent.

## Known quirks

- The portal sometimes bounces back to the same page after clicking the course card — handled with a double-click safety net.
- Headless mode is off by default (`headless=False`) since the site can be finicky; feel free to flip it once you trust the flow.
- Timeouts are tuned tight (7s) for a fast local connection — bump them up if your Wi-Fi is having a day.

## License

Apache License 2.0 — see [`LICENSE`](./LICENSE).
