"""Query for candidates registered for a specific district."""

import csv
import sys
import requests


def check_candidate_activity(cpf_id: int) -> dict:
    """
    Check if a candidate has recent filing activity via the API.

    Returns dict with:
        - has_reports: bool - whether they've ever filed reports
        - latest_year: int or None - most recent year-end report year
        - balance: str or None - most recent balance
    """
    result = {"has_reports": False, "latest_year": None, "balance": None}

    try:
        # Check if they have any report types
        resp = requests.get(
            f"https://api.ocpf.us/reports/baseReportTypes/{cpf_id}", timeout=10
        )
        if not resp.ok or not resp.json():
            return result

        result["has_reports"] = True
        types = resp.json()

        # Find Year-End type
        year_end_type = None
        for t in types:
            if "Year" in t.get("baseReportTypeDescription", ""):
                year_end_type = t.get("baseReportTypeId")
                break

        if year_end_type:
            resp2 = requests.get(
                f"https://api.ocpf.us/reports/reportList/{cpf_id}",
                params={"baseReportTypeId": year_end_type, "pageSize": 1},
                timeout=10,
            )
            if resp2.ok:
                data = resp2.json()
                items = data.get("items", [])
                if items:
                    result["latest_year"] = items[0].get("reportYear")
                    result["balance"] = items[0].get("endBalance")
    except Exception:
        pass

    return result


def get_candidates_for_district(district_code: int, include_closed: bool = False):
    """
    Get all candidates seeking a specific district from the bulk filers data.

    Args:
        district_code: The district code to search for
        include_closed: If True, include candidates with closed committees
    """
    candidates = []

    with open("data/filers/candidates.txt", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            try:
                sought_code = int(row.get("District Code Sought", 0))
            except (ValueError, TypeError):
                sought_code = 0

            if sought_code == district_code:
                closed_date = row.get("Closed Date", "").strip()
                if include_closed or not closed_date:
                    candidates.append(row)

    return candidates


def main():
    # Default to 1st Middlesex Senate (district 115)
    district_code = 115
    if len(sys.argv) > 1:
        try:
            district_code = int(sys.argv[1])
        except ValueError:
            pass

    include_closed = "--include-closed" in sys.argv
    check_activity = "--check-activity" in sys.argv or "-a" in sys.argv
    active_only = "--active-only" in sys.argv

    print(f"Querying candidates for district code {district_code}...")
    print(f"Include closed committees: {include_closed}")
    if check_activity or active_only:
        print("Checking filing activity via API...")
    print("=" * 80)

    candidates = get_candidates_for_district(district_code, include_closed)

    if not candidates:
        print("No candidates found for this district.")
        return

    print(f"\nFound {len(candidates)} registered candidate(s):\n")

    active_count = 0
    for c in candidates:
        cpf_id = c.get("CPF ID", "")
        first_name = c.get("Candidate First Name", "").strip('"')
        last_name = c.get("Candidate Last Name", "").strip('"')
        party = c.get("Party Affiliation", "").strip('"')
        org_date = c.get("Organization Date", "").strip('"')
        closed_date = c.get("Closed Date", "").strip('"')
        office_sought = c.get("Office Type Sought", "").strip('"')
        district_sought = c.get("District Name Sought", "").strip('"')
        office_held = c.get("Office Type Held", "").strip('"')
        district_held = c.get("District Name Held", "").strip('"')
        is_candidate_only = c.get("Is_Candidate_Only", "").strip('"').lower() == "true"
        committee_name = c.get("Comm_Name", "").strip('"')

        # Check activity if requested
        activity = None
        if check_activity or active_only:
            activity = check_candidate_activity(int(cpf_id))

        # Skip inactive if --active-only
        if active_only and activity:
            if not activity["has_reports"] or (
                activity["latest_year"] and activity["latest_year"] < 2023
            ):
                continue

        if activity and activity["has_reports"]:
            active_count += 1

        print(f"CPF ID: {cpf_id}")
        print(f"  Name: {first_name} {last_name}")
        print(f"  Party: {party}")
        if committee_name:
            print(f"  Committee: {committee_name}")
        print(f"  Organized: {org_date}")
        if closed_date:
            print(f"  Closed: {closed_date}")
        print(f"  Seeking: {office_sought} - {district_sought}")
        if office_held and office_held != "N/A":
            print(f"  Holds: {office_held} - {district_held}")

        # Show activity info
        if activity:
            if activity["has_reports"]:
                status = "ACTIVE"
                if activity["latest_year"]:
                    status += f" (filed {activity['latest_year']} Year-End)"
                if activity["balance"]:
                    status += f" Balance: {activity['balance']}"
                print(f"  Status: {status}")
            else:
                print(f"  Status: INACTIVE (no reports filed)")
        elif is_candidate_only:
            print(f"  Note: Candidate-only registration (no committee)")

        print()

    # Summary
    if check_activity or active_only:
        print("=" * 80)
        print(f"SUMMARY: {active_count} active committee(s) with recent filings")


if __name__ == "__main__":
    main()
