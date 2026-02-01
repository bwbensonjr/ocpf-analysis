"""Fetch and compare campaign finance data for special election candidates.

This script retrieves data from the OCPF API for the February 3rd, 2025
special election candidates in the 37th Middlesex district:
- Vanna Howard (CPF ID: 17499)
- Rodney Elliott (CPF ID: 12877)
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import requests

BASE_URL = "https://api.ocpf.us/"

# Candidate CPF IDs for the special election
CANDIDATES = {
    "vanna_howard": 17499,
    "rodney_elliott": 12877,
}


def get_data(api_path: str, params: dict | None = None) -> dict | list | None:
    """Fetch data from the OCPF API."""
    url = BASE_URL + api_path
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        print(f"  HTTP error for {api_path}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  Request error for {api_path}: {e}")
        return None


def fetch_filer_info(cpf_id: int) -> dict | None:
    """Fetch basic filer information."""
    print(f"Fetching filer info for CPF ID {cpf_id}...")
    return get_data(f"filer/{cpf_id}")


def fetch_filer_payload(cpf_id: int) -> dict | None:
    """Fetch extended filer information including related data."""
    print(f"Fetching filer payload for CPF ID {cpf_id}...")
    return get_data(f"filer/payload/{cpf_id}")


def fetch_report_types(cpf_id: int) -> list | None:
    """Fetch the report types this filer has submitted."""
    print(f"Fetching report types for CPF ID {cpf_id}...")
    return get_data(f"reports/baseReportTypes/{cpf_id}")


def fetch_report_list(cpf_id: int, base_report_type_id: int) -> dict | None:
    """Fetch list of reports for a filer filtered by report type."""
    print(f"  Fetching reports of type {base_report_type_id}...")
    params = {
        "baseReportTypeId": base_report_type_id,
        "pageSize": 100,
        "startIndex": 1,
    }
    return get_data(f"reports/reportList/{cpf_id}", params=params)


def fetch_report_detail(report_id: int) -> dict | None:
    """Fetch full report details including receipts and expenditures."""
    return get_data(f"report/{report_id}")


def fetch_independent_expenditures(cpf_id: int) -> list | None:
    """Fetch independent expenditure reports related to this candidate."""
    print(f"Fetching independent expenditures for CPF ID {cpf_id}...")
    return get_data(f"miscreports/related/{cpf_id}")


def parse_currency(value: str) -> float:
    """Parse a currency string like '$1,234.56' to a float."""
    if not value:
        return 0.0
    try:
        # Remove $ and commas
        cleaned = value.replace("$", "").replace(",", "")
        return float(cleaned)
    except (ValueError, AttributeError):
        return 0.0


def fetch_candidate_data(cpf_id: int, name: str) -> dict:
    """Fetch all relevant data for a candidate."""
    print(f"\n{'='*60}")
    print(f"Fetching data for {name} (CPF ID: {cpf_id})")
    print("=" * 60)

    candidate_data = {
        "cpf_id": cpf_id,
        "name": name,
        "fetched_at": datetime.now().isoformat(),
        "filer_info": None,
        "filer_payload": None,
        "report_types": None,
        "reports": [],
        "report_details": [],
        "independent_expenditures": None,
        "summary": {
            "year_end_2025": {
                "receipts": 0.0,
                "expenditures": 0.0,
                "period": "",
            },
            "special_election_2026": {
                "receipts": 0.0,
                "expenditures": 0.0,
                "report_count": 0,
                "reports": [],
            },
            "cash_on_hand": 0.0,
            "report_count": 0,
        },
    }

    # Fetch basic filer info
    candidate_data["filer_info"] = fetch_filer_info(cpf_id)
    candidate_data["filer_payload"] = fetch_filer_payload(cpf_id)

    # Fetch report types
    report_types = fetch_report_types(cpf_id)
    candidate_data["report_types"] = report_types

    if report_types:
        print(f"Found {len(report_types)} report type(s):")
        for rt in report_types:
            print(f"  - {rt.get('baseReportTypeDescription', 'Unknown')}")

    # Get recent reports from filer_payload.logReports (most reliable source)
    recent_reports = []
    if (
        candidate_data["filer_payload"]
        and "logReports" in candidate_data["filer_payload"]
    ):
        log_reports = candidate_data["filer_payload"]["logReports"]
        print(f"\nFound {len(log_reports)} recent reports in log")
        for lr in log_reports:
            recent_reports.append(lr)
            candidate_data["reports"].append(lr)

    # Fetch full details for recent reports
    if recent_reports:
        print(f"\nFetching full details for {min(len(recent_reports), 10)} reports...")
        for report in recent_reports[:10]:  # Limit to most recent 10
            report_id = report.get("reportId")
            if report_id:
                detail = fetch_report_detail(report_id)
                if detail:
                    candidate_data["report_details"].append(detail)
                    print(
                        f"  - Report {report_id}: {report.get('reportTypeDescription', 'Unknown')}"
                    )

    # Fetch independent expenditures
    candidate_data["independent_expenditures"] = fetch_independent_expenditures(cpf_id)

    # Separate 2025 year-end from 2026 special election activity
    for report in recent_reports:
        report_type = report.get("reportTypeDescription", "")
        period = report.get("reportingPeriod", "")
        receipts = parse_currency(report.get("receiptTotal", "$0.00"))
        expenditures = parse_currency(report.get("expenditureTotal", "$0.00"))

        # Check if this is a Year-End Report for 2025
        if "Year-End" in report_type and "12/31/25" in period:
            candidate_data["summary"]["year_end_2025"]["receipts"] = receipts
            candidate_data["summary"]["year_end_2025"]["expenditures"] = expenditures
            candidate_data["summary"]["year_end_2025"]["period"] = period
        # Check if this is a 2026 report (special election activity)
        elif "/26" in period or "2026" in period:
            candidate_data["summary"]["special_election_2026"]["receipts"] += receipts
            candidate_data["summary"]["special_election_2026"][
                "expenditures"
            ] += expenditures
            candidate_data["summary"]["special_election_2026"]["report_count"] += 1
            candidate_data["summary"]["special_election_2026"]["reports"].append(
                {
                    "type": report_type,
                    "period": period,
                    "receipts": receipts,
                    "expenditures": expenditures,
                }
            )

    candidate_data["summary"]["report_count"] = len(recent_reports)

    # Get cash on hand from year-end report or most recent report
    if candidate_data["report_details"]:
        # First try to find a year-end report
        for report in candidate_data["report_details"]:
            if report.get("isYe"):
                cash_on_hand = report.get("totalCashOnHand", 0)
                if isinstance(cash_on_hand, str):
                    cash_on_hand = parse_currency(cash_on_hand)
                candidate_data["summary"]["cash_on_hand"] = cash_on_hand
                break
        else:
            # Fall back to most recent report's end balance
            latest_report = candidate_data["report_details"][0]
            cash_on_hand = latest_report.get("endBalance", 0) or latest_report.get(
                "adjustedEndBalance", 0
            )
            if isinstance(cash_on_hand, str):
                cash_on_hand = parse_currency(cash_on_hand)
            candidate_data["summary"]["cash_on_hand"] = cash_on_hand

    return candidate_data


def extract_top_donors(report_details: list, limit: int = 10) -> list:
    """Extract top donors from report details."""
    donors = {}

    for report in report_details:
        receipts = report.get("receipts", [])
        for receipt in receipts:
            # In OCPF API: "firstName" is first name, "name" is last name
            first_name = receipt.get("firstName", "")
            last_name = receipt.get("name", "")  # 'name' field holds last name

            if first_name and last_name:
                donor_name = f"{first_name} {last_name}"
            elif last_name:
                donor_name = last_name
            elif first_name:
                donor_name = first_name
            else:
                # Try fullNameReverse (format: "Last, First")
                full_name_reverse = receipt.get("fullNameReverse", "")
                if full_name_reverse:
                    parts = full_name_reverse.split(", ")
                    if len(parts) == 2:
                        donor_name = f"{parts[1]} {parts[0]}"
                    else:
                        donor_name = full_name_reverse
                else:
                    donor_name = receipt.get("contributorName", "") or "Unknown"

            # Get amount - handle both numeric and string formats
            amount = receipt.get("amountValue", 0)  # Use amountValue for numeric
            if not amount:
                amount = receipt.get("amount", 0)
                if isinstance(amount, str):
                    amount = parse_currency(amount)
                else:
                    amount = float(amount) if amount else 0.0

            # Get receipt type for context
            receipt_type = receipt.get("recordTypeDescription", "")

            if donor_name and amount > 0:
                key = donor_name.strip()
                if key in donors:
                    donors[key]["total"] += amount
                    donors[key]["count"] += 1
                else:
                    donors[key] = {
                        "name": key,
                        "total": amount,
                        "count": 1,
                        "type": receipt_type,
                    }

    # Sort by total amount and return top donors
    sorted_donors = sorted(donors.values(), key=lambda x: x["total"], reverse=True)
    return sorted_donors[:limit]


def print_comparison(candidates_data: dict):
    """Print a comparison summary of the candidates."""
    print("\n")
    print("=" * 70)
    print("CAMPAIGN FINANCE COMPARISON - 37th Middlesex Special Election")
    print("=" * 70)

    for key, data in candidates_data.items():
        print(f"\n{data['name']} (CPF ID: {data['cpf_id']})")
        print("-" * 50)

        # Filer info
        if data["filer_info"]:
            filer = data["filer_info"]
            print(f"  Committee: {filer.get('committeeName', 'N/A')}")

            # Format office sought nicely
            office_sought = filer.get("officeSought", {})
            if isinstance(office_sought, dict):
                office_str = office_sought.get("officeDistrict", "N/A")
            else:
                office_str = str(office_sought) if office_sought else "N/A"
            print(f"  Office Sought: {office_str}")

            print(f"  Party: {filer.get('partyAffiliation', 'N/A')}")
            print(f"  Organized: {filer.get('organizationDate', 'N/A')}")

        # Financial summary
        summary = data["summary"]
        ye_2025 = summary["year_end_2025"]
        se_2026 = summary["special_election_2026"]

        print(f"\n  2025 Year-End Report ({ye_2025['period']}):")
        print(f"    Receipts:     ${ye_2025['receipts']:,.2f}")
        print(f"    Expenditures: ${ye_2025['expenditures']:,.2f}")

        print(f"\n  2026 Special Election Activity ({se_2026['report_count']} reports):")
        print(f"    Receipts:     ${se_2026['receipts']:,.2f}")
        print(f"    Expenditures: ${se_2026['expenditures']:,.2f}")
        if se_2026["reports"]:
            for rpt in se_2026["reports"]:
                print(
                    f"      - {rpt['period']}: ${rpt['receipts']:,.2f} in / ${rpt['expenditures']:,.2f} out"
                )

        print(f"\n  Current Cash on Hand: ${summary['cash_on_hand']:,.2f}")

        # Top donors
        if data["report_details"]:
            top_donors = extract_top_donors(data["report_details"], limit=5)
            if top_donors:
                print(f"\n  Top Donors:")
                for i, donor in enumerate(top_donors, 1):
                    donor_type = f" ({donor['type']})" if donor.get("type") else ""
                    print(
                        f"    {i}. {donor['name']}: ${donor['total']:,.2f}{donor_type}"
                    )

        # Independent expenditures
        ie_reports = data["independent_expenditures"]
        if ie_reports:
            print(f"\n  Independent Expenditures ({len(ie_reports)} report(s)):")
            for ie in ie_reports[:5]:  # Show first 5
                committee = ie.get("filingEntity", "Unknown")
                exp_total = parse_currency(ie.get("expenditureTotal", "$0.00"))
                period = ie.get("reportingPeriod", "")
                # Extract candidate listing to show support/oppose
                candidate_listing = ie.get("candidateListing", "")
                print(f"    - {committee}")
                print(f"      Period: {period}, Expenditures: ${exp_total:,.2f}")
                if candidate_listing:
                    # Truncate if too long
                    if len(candidate_listing) > 80:
                        candidate_listing = candidate_listing[:77] + "..."
                    print(f"      Candidates: {candidate_listing}")
            if len(ie_reports) > 5:
                print(f"    ... and {len(ie_reports) - 5} more")
        else:
            print(f"\n  Independent Expenditures: None reported")


def save_data(candidates_data: dict, output_dir: Path):
    """Save candidate data to JSON files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for key, data in candidates_data.items():
        filename = output_dir / f"candidate_{key}_{data['cpf_id']}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Saved: {filename}")

    # Save combined comparison file
    combined_file = output_dir / "special_election_comparison.json"
    with open(combined_file, "w") as f:
        json.dump(candidates_data, f, indent=2, default=str)
    print(f"Saved: {combined_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and compare OCPF data for special election candidates"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent / "data",
        help="Directory to save output JSON files",
    )
    args = parser.parse_args()

    print("OCPF Special Election Candidate Comparison")
    print("Fetching data from https://api.ocpf.us/")
    print(f"Output directory: {args.output_dir}")

    candidates_data = {}

    for key, cpf_id in CANDIDATES.items():
        name = key.replace("_", " ").title()
        candidates_data[key] = fetch_candidate_data(cpf_id, name)

    # Print comparison
    print_comparison(candidates_data)

    # Save data
    print("\n" + "=" * 70)
    print("SAVING DATA")
    print("=" * 70)
    save_data(candidates_data, args.output_dir)

    print("\nDone!")


if __name__ == "__main__":
    main()
