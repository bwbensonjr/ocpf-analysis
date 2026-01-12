# OCPF API Endpoint Status

**Test Date:** 2024-12-20
**Base URL:** `https://api.ocpf.us/`
**Summary:** 94 working, 24 not working (79.7% success rate)

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
| `search/items` | Returns search contributions, expenditures, donations or subvendor payments |
| `search/recordTypes/{searchTypeCategory}` | Returns record type filter for searches |
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
