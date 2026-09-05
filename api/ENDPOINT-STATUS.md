# OCPF API Endpoint Status

**Test Date:** 2024-12-20
**Base URL:** `https://api.ocpf.us/`
**Summary:** 94 working, 24 not working (79.7% success rate)

> **OCPF publishes a full OpenAPI spec at
> <https://api.ocpf.us/swagger/v1/swagger.json>** (browsable at
> `https://api.ocpf.us/swagger/index.html`). It lists every route's query
> parameters, which this document does not. Read it before probing an endpoint
> by hand — several routes below take parameters that are the difference between
> "working" and "useful".

## Results by Controller

| Controller | Working | Total | Success Rate |
|------------|---------|-------|--------------|
| BallotQuestion | 5 | 5 | 100% |
| MunicipalData | 4 | 4 | 100% |
| MiscReportData | 18 | 19 | 95% |
| ReportPageData | 16 | 17 | 94% |
| OcpfUsData | 14 | 16 | 88% |
| Reference | 8 | 10 | 80% |
| Filers | 10 | 13 | 77% |
| ReportData | 11 | 16 | 69% |
| Legal | 3 | 6 | 50% |
| Elections | 5 | 11 | 45% |
| Search | 0 | 1 | 0% |

## Working Endpoints

### Reference (8/10)
| Route | Description |
|-------|-------------|
| `accountTypes` | Returns a list of account types |
| `accountTypes/full` | Returns a list of account types and additional information |
| `filers/uicategories` | Returns UI categories of filers such as Democratic LPCs |
| `officeTypeList` | Returns a list of office types, used to group districts |
| `districts` | Returns all district codes or by office type |
| `districts/{officeType}` | Returns all district codes or by office type |
| `municipalityList/options` | Dropdown list of all cities |
| `weeks/{year}` | Returns a list of weeks in the provided year |

### Filers (10/13)
| Route | Description |
|-------|-------------|
| `filer/{cpfId}` | Returns a single filer from a specified CPF ID |
| `filer/payload/{cpfId}` | Returns a single filer from a specified CPF ID and related information |
| `filer/issues/{cpfId}` | Returns all audit correspondence |
| `filer/correspondence/nonaudit/{cpfId}` | Returns all filer documents besides audit issues, letters |
| `filer/correspondence/all/{cpfId}` | Returns all filer documents |
| `filers/recentlyOrganized/{category}` | Returns recently organized filers by category |
| `filers/mayoral/{year}` | For mayoral report table/page |
| `filers/incumbents/{startDistrictCodeRange}/{endDistrictCodeRange}` | Returns incumbents in district range |
| `filers/changesOfPurpose` | Returns last 100 changes of purpose |
| `filers/barred` | Returns filers barred from running from office |

### MunicipalData (4/4)
| Route | Description |
|-------|-------------|
| `municipalities` | Returns all municipalities with elected officials |
| `municipality/byCode/{code}/{year}` | Returns a single municipality with elected officials |
| `municipality/byName/{name}/{year}` | Returns a single municipality with elected officials |
| `municipality/calculator` | Returns a calculated filing schedule |

### BallotQuestion (5/5)
| Route | Description |
|-------|-------------|
| `ballotQuestions/{year}` | Returns a list of ballot questions w/o linked committees |
| `ballotQuestions/committees/{year}/{ballotQuestionId}` | Returns a list of ballot question committees |
| `ballotQuestions/chartData/{year}/{questionId}/{chartType}` | Returns chart data for BQs |
| `reports/ballotQuestions/{year}` | Returns a list of ballot question reports by year |
| `reports/ballotQuestions/byQuestion/{year}` | Returns a list of ballot question reports by question/year |

### Elections (5/11)
| Route | Description |
|-------|-------------|
| `onballot/ballotYears/{districtCode}` | Returns all years a specified district code appeared on the ballot |
| `onballot/finsummaries/{year}/{districtCode}` | Returns financial summaries for a specified district |
| `onballot/candidates/{year}/{districtCode}` | Returns all on-ballot candidates for a specified district/year |
| `chartData/electionChart` | Returns election chart data |
| `chartData/monthly` | Returns monthly chart data |

### Legal (3/6)
| Route | Description |
|-------|-------------|
| `legal/aos` | Returns all advisory opinions or a specified one |
| `legal/gls` | Returns all guidance letters or a specified one |
| `legal/actions` | Returns all agency actions or a specified one |

### ReportData (11/16)
| Route | Description |
|-------|-------------|
| `reports/log` | Returns a list of recently filed reports |
| `report/{reportId}` | For main display, returns a specific report |
| `report/generic/{reportId}` | Returns a generic report |
| `report/pdf/{reportId}` | Creates a PDF for the specified report |
| `reports/baseReportTypes/{cpfId}` | Returns all base report types the filer has filed |
| `search/items` | Returns search contributions, expenditures, donations or subvendor payments — **see [search/items](#searchitems--report-line-items) below; it fails open in three ways** |
| `search/recordTypes/{searchTypeCategory}` | Record type filter for searches. `{searchTypeCategory}` is the **same single-letter code** as `search/items` (`B`/`R`/`S`/`D`), not a word — see below |
| `search/textOutput` | Returns search results as text |
| `search/excelOutput` | Returns search results as Excel |
| `search/pdfOutput` | Returns search results as PDF |
| `reports/{year}/{reportTypeId}` | API only, RE-IMPLEMENT |

### ReportPageData (16/17)
| Route | Description |
|-------|-------------|
| `reports/legislative/race/nd/{year}` | Legislative non-depository reports |
| `reports/legislative/race/depository/{year}` | Legislative depository reports |
| `reports/legislative/fullYear/{year}` | Legislative full year reports |
| `reports/legislative/depository/ytd/{year}` | Legislative depository YTD reports |
| `reports/county/ytd/{year}` | County YTD reports |
| `reports/statewide/ytd/{year}` | Statewide YTD reports |
| `reports/mayoral/depository/{year}` | Mayoral depository reports |
| `reports/mayoral/nd/{year}` | Mayoral non-depository reports |
| `reports/cc/ytd/{year}` | Constitutional committee YTD reports |
| `reports/pacs/{year}` | Returns PAC reports by year |
| `reports/stateparties/{year}` | Returns State Party reports by year |
| `reports/lpc/{year}` | Local party committee reports |
| `reports/lpc/textOutput/{year}` | LPC reports as text |
| `reports/lpc/excelOutput/{year}` | LPC reports as Excel |
| `reports/ballotQuestions/{year}` | Returns all active BQ committee reports |
| `reports/ballotQuestions/byQuestion/{year}` | Returns BQ reports related to ballot questions |

### MiscReportData (18/19)
| Route | Description |
|-------|-------------|
| `miscreports/log` | Returns log of misc reports |
| `miscreports/expenditures/{year}` | Returns misc expenditures by year |
| `miscreports/expenditures/summary/{year}` | Returns misc expenditures summary |
| `miscreports/reports/{year}` | Returns misc reports by year |
| `miscreports/reports/summary/{year}` | Returns misc reports summary |
| `miscreports/textOutput/{year}` | Returns misc reports as text |
| `miscreports/entities/{year}` | Returns entities by year |
| `miscreports/vendors/{year}` | Returns vendors by year |
| `miscreports/candidates/{year}` | Returns candidates by year |
| `miscreports/iepacs/reports/{year}` | Returns multiple IEPAC reports |
| `miscreports/iepacs/reports/summary/{year}` | Returns IEPAC reports summary |
| `miscreports/iepacs/committeeNames/{year}` | Returns IEPAC committee names |
| `miscreports/iepacs/candidates/{year}` | Returns IEPAC candidates |
| `miscreport/receipts/{reportId}` | Returns a single misc report's receipts |
| `miscreport/expenditures/{reportId}` | Returns a single misc report's expenditures |
| `miscreport/liabilities/{reportId}` | Returns a single misc report's liabilities |
| `miscreports/related/{cpfId}` | Returns all reports that support or oppose a specified candidate |

### OcpfUsData (14/16)
| Route | Description |
|-------|-------------|
| `photos` | Returns the homepage pictures URLs |
| `news/{id}` | Returns all news posts or a specified one |
| `news/recent` | Returns last 4 news posts |
| `videos/{id}` | Returns all help videos or a specified one |
| `events/{year}/{month}` | Returns calendar events by year/month |
| `events/upcoming` | Returns all public calendar events in the next 6 mos |
| `events/upcoming/next4` | Returns next 4 public calendar events |
| `releases/{id}` | Returns all press releases or a specific press release |
| `filingDeadlines` | From filing notices |
| `newsletters` | Returns all newsletters |
| `checkingin` | Returns all checking-in emails |
| `forms/all` | Returns all forms |
| `publications/studies` | Returns all OCPF studies |
| `filingSchedules/{year}` | Returns filing schedules |

---

## `search/items` — report line items

Verified against the live API on 2026-09-04 (filer cpfId 17436, 1,019
expenditure records). This endpoint returns the individual records inside filed
reports — contributions received, expenditures made, subvendor payments. It is
the only working route for "who did this committee pay?", and it **fails open in
three ways that produce plausible-looking wrong answers rather than errors.**

### 1. `SearchTypeCategory` — an unrecognized value silently returns receipts

| Code | Records | Global count | Global total |
|------|---------|-------------:|-------------:|
| `B` | Expenditures | 1,824,032 | $1,553,093,477.87 |
| `R` | Receipts / contributions (**the fallback**) | 6,134,871 | $1,664,541,084.54 |
| `S` | Subvendor payments | 14,207 | $305,298,610.22 |
| `D` | Donations | 10,565 | $15,781,689.95 |

Any *unrecognized* value falls back to **receipts** with no error and no
warning. `E`, `expenditures`, `EXP`, `exp` and `""` all return the receipt set,
which reads as a perfectly plausible table of money flowing the opposite
direction. Never build this parameter from user input, and validate the shape of
what comes back (expenditure items carry `vendor`; receipt items carry
`contributorCpfId`/`fullNameReverse` instead).

### 2. `StartIndex` is 1-based, not 0-based

`StartIndex=0` and `StartIndex=1` both return the first record; `StartIndex=2`
returns the second. Paging from a 0-based offset re-fetches the boundary record
on every page and **inflates any total computed from the result**. Check the
accumulated count against `summary.count` in both directions — a short read
understates a total and an overlap overstates it, both silently.

### 3. A misnamed filter is ignored, not rejected

`Name` filters the counterparty and works. **`VendorName` is inert** despite
appearing in the swagger spec: passing it returns the entire unfiltered database
(1,823,947 records, $1.55B). An ignored filter is indistinguishable from one
that matched everything, so verify a filter narrows the result before trusting
it.

### Response shape

```json
{"summary": {"count": 0, "total": 0, "totalDisplay": "$0.00", "description": ""},
 "items": [...]}
```

`summary` is **null unless `withSummary=true`** is passed.

Useful parameters (full list in the swagger spec): `CpfId`, `Name`, `StartDate`,
`EndDate`, `MinAmount`, `MaxAmount`, `PageSize`, `StartIndex`, `withSummary`,
`SortField`, `SortDirection`.

### Item fields

Expenditure items carry `vendor`, `purpose`, `clarifiedName`,
`clarifiedPurpose`, `date` (`M/D/YYYY`), `amount` (a **display string** like
`"$1,234.56"`, not a number), `recordTypeId`/`recordTypeDescription`,
`reportId`, and `sourceLink`/`sourceDescription`.

- `recordTypeDescription` of `Bank Reported Expenditure` means the payee came
  off a bank statement and may be an opaque description (`OUTGOING WIRE
  TRANSFER`) rather than the true recipient.
- **`clarifiedName` is OCPF's own resolution of such a payee** and should be
  preferred when present. It resolves bank-OCR spelling variants of one
  recipient, and sometimes names the payee behind an opaque wire. It is
  authoritative, unlike any inference drawn from the raw string. It is sparse:
  6 of 181 records for one filer's 2026 activity.

### `search/recordTypes/{searchTypeCategory}`

Takes the **same single-letter code**, not a word. `search/recordTypes/B`
returns the 14 expenditure record types below; `R`, `S` and `D` currently return
`[]`. (An earlier note that this route was useless came from passing words like
`expenditures` and getting an empty list.)

| Id | Description |
|-----|-------------|
| 301 | General Expenditure |
| 302 | Bank Fee |
| 303 | Contribution to a registered committee |
| 304 | Liability Repayment |
| 305 | Refund of Credit Card Contribution |
| 315 | Independent Expenditure |
| 316 | Adminstrative Expense |
| 318 | Payroll Item |
| 319 | Merchant Provider Fee |
| 320 | Aggregated Un-itemized Expenditure Total |
| 331 | Out-of-pocket candidate expense (as loan) |
| 332 | Out-of-pocket candidate expense |
| 351 | Reimbursement Item |
| 354 | Credit Card Charge |

Note that out-of-pocket candidate expenses (331/332) are included here, which is
why an item-search expenditure total legitimately exceeds the depository YTD
`expendituresYtd` figure for the same filer and period.

### Reference implementation

`ocpf-cli` wraps all of the above in `src/ocpf_cli/search.py`, with the paging,
completeness checks and shape guards already written; `ocpf expenditures` is the
command built on it.

---

## Non-Working Endpoints

### 404 Not Found (15 endpoints)
These endpoints return 404, suggesting the routes may have changed or been removed.

| Route | Controller | Notes |
|-------|------------|-------|
| `municipalityList/{phrase}` | Reference | May need different parameter format |
| `states/{phrase}` | Reference | May need different parameter format |
| `filers/listings/{category}/{searchPhrase}` | Filers | Route may have changed |
| `filers/options/{category}/{searchPhrase}` | Filers | Route may have changed |
| `filers/pacs/{searchPhrase}` | Filers | Route may have changed |
| `onballot/candidates/byDistrictPhrase/{year}/{districtSearchPhrase}` | Elections | Route may have changed |
| `specialElection/{id}` | Elections | May require valid special election ID |
| `specialElections/{year}` | Elections | May require year with special elections |
| `chart/detail` | Elections | Route may have changed or requires POST |
| `chart/detail/summary` | Elections | Route may have changed or requires POST |
| `legal/search/{searchPhrase1}/{searchPhrase2}` | Legal | Route may have changed |
| `report/items/{reportId}/{scheduleCode}` | ReportData | Route may have changed |
| `news/byPhrase/{phrase}` | OcpfUsData | Route may have changed |
| `videos/byPhrase/{phrase}` | OcpfUsData | Route may have changed |
| `public/search/{term}` | Search | Route may have changed |

### 400 Bad Request (1 endpoint)
These endpoints require additional query parameters.

| Route | Controller | Notes |
|-------|------------|-------|
| `reports/reportList/{cpfId}` | ReportData | Requires `baseReportTypeId` query parameter |

### 500 Server Error (8 endpoints)
These endpoints exist but have server-side issues.

| Route | Controller | Notes |
|-------|------------|-------|
| `chartData/onBallot/{year}/{districtCode}` | Elections | Server error - may be data-dependent |
| `legal/regulations` | Legal | Server error |
| `legal/document/{docId}` | Legal | Server error - may need valid docId |
| `reports/reportList/excelOutput` | ReportData | Server error - likely needs POST with body |
| `search/itemGroupings` | ReportData | Server error |
| `search/partial` | ReportData | Server error |
| `reports/lpc/summary/{year}` | ReportPageData | Server error |
| `miscreport/{reportId}` | MiscReportData | Server error - needs valid misc report ID |

---

## Test Configuration

Test values used for path parameters:
- `cpfId`: 14770 (example filer)
- `year`: 2024
- `reportId`: 986767 (example report)
- `districtCode`: 294
- `category`: C (Candidates)
- `officeType`: House

See `api/test_endpoints.py` for the full test script and `api/endpoint-test-results.json` for detailed results.
