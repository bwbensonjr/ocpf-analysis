"""Download data from a set of OCPF endpoints for use as example data."""

import json
import requests

BASE_URL = "https://api.ocpf.us/"

API_PATHS = [
    # Reference
    ["account-types", "accountTypes/full"],
    ["filer-ui-categories", "filers/uicategories"],
    ["office-types", "officeTypeList"],
    ["districts", "districts"],
    # Filers
    ["filer-example-14770", "filer/14770"],
    ["recently-organized-candidates", "filers/recentlyOrganized/C"],
    ["incumbents-house", "filers/incumbents/200/299"],
    ["incumbents-senate", "filers/incumbents/100/199"],
    ["incumbens-gov-council", "filers/incumbents/1100/1199"],
    # Elections
    ["on-ballot-summary-2010-294", "onballot/finsummaries/2010/294"],
    ["on-ballot-candidates-2010-294", "onballot/candidates/2010/294"],
    # ["special-elections-2025", "specialElections/2025"],
    # ReportData
    ["reports-log", "reports/log"],
    ["report-example-986767", "report/986767"],
    ["Reports-legislative-nd-2010", "reports/legislative/race/nd/2010"],
    ["reports-legislative-depository-2025", "reports/legislative/race/depository/2025"],
]


def main():
    print(f"Exercising {len(API_PATHS)} endpoints...")
    for description, api_path in API_PATHS:
        print(f"{api_path}: {description}...")
        data = get_data(api_path)
        file_name = f"data/{description}.json"
        with open(file_name, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Writing {file_name}...")
    print("Done.")


def get_data(api_path: str) -> dict:
    resp = requests.get(BASE_URL + api_path)
    resp.raise_for_status()
    resp_json = resp.json()
    return resp_json


if __name__ == "__main__":
    main()
