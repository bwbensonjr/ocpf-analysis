# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains tools for downloading, analyzing, and understanding campaign finance data from the Massachusetts Office of Campaign and Political Finance (OCPF). It includes:

- Python scripts for fetching data from the OCPF REST API (`https://api.ocpf.us/`)
- R scripts for data analysis and manipulation
- Downloaded data in both JSON (from API) and TSV (from bulk downloads) formats

## Development Commands

### Python

```bash
# Install dependencies (using uv)
uv sync

# Run the API inspection script to download example data
uv run python api/api_inspection.py

# Format Python code
uv run black .
```

### R

The R analysis script (`ocpf-data.R`) uses tidyverse and janitor packages. Run interactively in RStudio or:

```bash
Rscript ocpf-data.R
```

## Architecture

### Data Sources

1. **OCPF REST API** (`https://api.ocpf.us/`) - JSON responses stored in `api/data/`
2. **OCPF Bulk Downloads** - TSV files stored in `data/` subdirectories

### Key Files

- `api/api_inspection.py` - Fetches sample data from various OCPF API endpoints
- `api/ocpf-endpoints.json` - Comprehensive catalog of available OCPF API endpoints organized by controller (Reference, Filers, Elections, ReportData, etc.)
- `ocpf-data.R` - R script for loading and analyzing bulk download data
- `data/reports/*/readme.txt` - Documentation of report types and record type IDs

### Data Model

Key entities in the OCPF data model:

- **Filers** - Campaign committees identified by `cpf_id`
- **Reports** - Financial filings with `report_id`, linked to filers
- **Report Items** - Individual transactions (contributions, expenditures) within reports, identified by `record_type_id`
- **Districts** - Electoral districts with `district_code`

Report types are categorized as: Depository, Non-Depository, Political Action Committee, IEPAC, Ballot Question Committee, Local Party Committee, Municipal, and Non-Registered.

## Code Style

- Python: Use double quotes for strings (e.g., `"foo"` not `'foo'`)
