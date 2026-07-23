# OCPF Suspected Data-Quality Issues

A running log of OCPF API responses that appear incorrect or internally
inconsistent, kept so they can be raised with OCPF. This tracks **data** problems
(wrong/inconsistent values), distinct from `ENDPOINT-STATUS.md`, which tracks
which **endpoints** work.

Each entry records what was observed, the evidence (with an independent source
where available), what we'd expect instead, and the status of reporting it.

**Base URL:** `https://api.ocpf.us/`

Status legend: `open` (found, not yet reported) · `reported` (raised with OCPF) ·
`resolved` (fixed/confirmed by OCPF) · `wontfix`.

---

## DQ-001 — `ballotYears/166` reports years the district did not exist

- **Status:** open
- **Discovered:** 2026-07-23
- **Endpoints:** `onballot/ballotYears/{districtCode}`, `districts`,
  `onballot/finsummaries/{year}/{districtCode}`
- **District:** code `166` = Senate "Suffolk and Middlesex" (per the current
  `districts` reference)

### What was observed

`onballot/ballotYears/166` returns:

```
[2002, 2004, 2006, 2008, 2010, 2012]
```

claiming Senate district code 166 ("Suffolk and Middlesex") was on the ballot in
each of those years.

### Why it looks wrong

1. **Independent election record disagrees.** In the Massachusetts general
   election record (`ma-election-db`, sourced from official results), a State
   Senate district *named* "Suffolk and Middlesex" existed only in **1990–2000**
   and again in **2022–2024**. It did **not** exist from 2002 through 2020. In
   the 2002–2012 window the area was covered by two differently named districts
   created in the 2001 redistricting:
   - *First Suffolk and Middlesex* — Anthony W. Petruccelli (2008, 2010, 2012)
   - *Second Suffolk and Middlesex* — Steven A. Tolman (2008, 2010), then
     William N. Brownsberger (2012)

   The plain "Suffolk and Middlesex" name returned only with the 2021
   redistricting (effective 2022), which is Brownsberger's current seat.

2. **OCPF is internally inconsistent.** For the very years `ballotYears/166`
   lists, OCPF's own financial-summary endpoint returns nothing:

   ```
   onballot/finsummaries/2008/166 -> [] (0 rows)
   onballot/finsummaries/2010/166 -> [] (0 rows)
   onballot/finsummaries/2012/166 -> [] (0 rows)
   ```

   If code 166 were genuinely on the ballot in 2008–2012, the summaries feed for
   those year/code pairs should not be empty.

### Likely root cause

OCPF district codes appear to reference the **current** districting map, and the
historical code↔district association is not stable across decennial
redistricting. `ballotYears/166` seems to attribute prior-cycle ballot years to
today's code 166 even though the district under that name/geography did not exist
then.

### Expected behavior

`ballotYears/{code}` should return only the years the district as identified by
that code actually appeared on the ballot — or the API should otherwise make the
redistricting discontinuity explicit, so a code is not credited with years from a
different district that happened to share (or later acquire) the name.

### Impact

Name→code district resolution against the current `districts` reference silently
returns wrong or empty historical results across redistricting boundaries. This
surfaced in `ocpf-cli` (`ocpf race --year 2010 "Suffolk and Middlesex"`), which
correctly reports "no candidates found" because `finsummaries/2010/166` is empty
— but only because the code no longer maps to a real 2010 district.

### Reproduction

```bash
curl -s "https://api.ocpf.us/onballot/ballotYears/166"
curl -s "https://api.ocpf.us/onballot/finsummaries/2010/166"   # -> []
curl -s "https://api.ocpf.us/districts" | \
  python3 -c "import sys,json;[print(r['code'],r['office'],r['description']) for r in json.load(sys.stdin) if r['code']==166]"
```
