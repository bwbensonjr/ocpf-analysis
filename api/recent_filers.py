"""Query recent filers and update CSV."""

import pandas as pd
import requests
from pathlib import Path

BASE_URL = "https://api.ocpf.us/"
CSV_PATH = Path(__file__).parent.parent / "data" / "recent-filers.csv"


def fetch_recent_filers() -> list[dict]:
    """Fetch recently organized candidate committees."""
    resp = requests.get(BASE_URL + "filers/recentlyOrganized/C?officeFilter=")
    resp.raise_for_status()
    return resp.json()


def fetch_filer_details(cpf_id: int) -> dict:
    """Fetch detailed info for a single filer."""
    resp = requests.get(BASE_URL + f"filer/{cpf_id}")
    resp.raise_for_status()
    return resp.json()


def fetch_incumbents(district_code: int) -> list[dict]:
    """Fetch incumbents for an exact district."""
    resp = requests.get(
        BASE_URL + f"filers/incumbents/{district_code}/{district_code}"
    )
    resp.raise_for_status()
    return resp.json()


def party_abbreviation(party: str) -> str:
    """Map full party name to abbreviation."""
    mapping = {"Democratic": "D", "Republican": "R"}
    return mapping.get(party, "U")


def format_display_name(full_name: str, party: str, city: str) -> str:
    """Format as 'Name (P-City)'."""
    abbrev = party_abbreviation(party)
    return f"{full_name} ({abbrev}-{city})"


def build_full_name(first: str, middle: str, last: str) -> str:
    """Build full name from parts, including middle if present."""
    parts = [first]
    if middle:
        parts.append(middle if len(middle) == 1 else middle)
    parts.append(last)
    return " ".join(parts)


def lookup_incumbent(district_code: int) -> str:
    """Look up the incumbent display name for a district code."""
    try:
        incumbents = fetch_incumbents(district_code)
        for inc in incumbents:
            if inc.get("districtCodeHeld") == district_code:
                inc_name = inc.get("candidateFullName", "")
                inc_party = inc.get("partyAffiliation", "")
                inc_city = inc.get("candidateCity", "")
                return format_display_name(inc_name, inc_party, inc_city)
    except requests.RequestException:
        pass
    return ""


def backfill_incumbents(df: pd.DataFrame) -> int:
    """Re-check incumbent for rows with empty incumbent_display."""
    count = 0
    for idx, row in df.iterrows():
        val = row["incumbent_display"]
        if pd.notna(val) and val != "":
            continue
        cpf_id = int(row["cpf_id"])
        details = fetch_filer_details(cpf_id)
        office_sought = details.get("officeSought") or {}
        district_code = office_sought.get("districtCode")
        if not district_code:
            continue
        incumbent = lookup_incumbent(district_code)
        if incumbent:
            print(f"  Backfill {cpf_id}: {incumbent}")
            df.at[idx, "incumbent_display"] = incumbent
            count += 1
    return count


def main():
    # Step 1: Fetch recent filers
    print("Fetching recently organized filers...")
    recent = fetch_recent_filers()
    print(f"  Found {len(recent)} recent filers")

    # Step 2: Load existing CSV and filter
    df_existing = pd.read_csv(CSV_PATH)
    known_ids = set(df_existing["cpf_id"].dropna().astype(int))
    new_filers = [f for f in recent if f["cpfId"] not in known_ids]
    print(f"  {len(new_filers)} new filers to add")

    # Step 3-6: Process each new filer
    new_rows = []
    for filer in new_filers:
        cpf_id = filer["cpfId"]
        print(f"  Processing {cpf_id}: {filer['fullNameReverse']}...")

        # Fetch details
        details = fetch_filer_details(cpf_id)

        # Extract candidate info
        candidate = details.get("candidate", {})
        first = candidate.get("firstName", "")
        middle = candidate.get("middleName", "")
        last = candidate.get("lastName", "")
        city = candidate.get("city", "")
        party_full = details.get("partyAffiliation", "")
        full_name = build_full_name(first, middle, last)
        candidate_display = format_display_name(full_name, party_full, city)

        # Office and district from detail endpoint
        office_sought = details.get("officeSought") or {}
        office = office_sought.get("officeDescription", "")
        district = office_sought.get("districtDescription", "")
        district_code = office_sought.get("districtCode")

        # Fallback to list data if no officeSought
        if not office:
            office = filer.get("officeSoughtDescription", "")

        # Incumbent lookup
        incumbent_display = ""
        if district_code:
            incumbent_display = lookup_incumbent(district_code)

        # Format organization date as M/D/YY
        org_date_raw = filer.get("organizationDate", "")
        try:
            org_date = pd.to_datetime(org_date_raw).strftime("%-m/%-d/%y")
        except (ValueError, TypeError):
            org_date = org_date_raw

        new_rows.append(
            {
                "cpf_id": cpf_id,
                "organization_date": org_date,
                "candidate_display": candidate_display,
                "address": filer.get("fullAddress", ""),
                "office": office,
                "district": district,
                "incumbent_display": incumbent_display,
                "reason": "",
                "link": "",
            }
        )

    # Combine new rows with existing data
    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df_combined = pd.concat([df_new, df_existing], ignore_index=True)
    else:
        df_combined = df_existing

    # Backfill missing incumbents
    print("Backfilling missing incumbents...")
    backfilled = backfill_incumbents(df_combined)
    print(f"  Backfilled {backfilled} rows")

    # Write back
    df_combined.to_csv(CSV_PATH, index=False)
    print(f"Wrote {len(df_combined)} rows to {CSV_PATH}")


if __name__ == "__main__":
    main()
