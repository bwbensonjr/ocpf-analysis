"""Test all OCPF API endpoints and report their status."""

import json
import requests
import re
from datetime import datetime

BASE_URL = "https://api.ocpf.us/"

# Test values to substitute for path parameters
TEST_VALUES = {
    "cpfId": "14770",
    "year": "2024",
    "officeType": "House",
    "phrase": "Boston",
    "searchPhrase": "Smith",
    "searchPhrase1": "campaign",
    "searchPhrase2": "finance",
    "category": "C",  # C = Candidates
    "districtCode": "294",
    "startDistrictCodeRange": "200",
    "endDistrictCodeRange": "299",
    "reportId": "986767",
    "id": "1",
    "code": "1",  # Municipality code
    "name": "Boston",
    "docId": "1",
    "ballotQuestionId": "1",
    "questionId": "1",
    "chartType": "receipts",
    "scheduleCode": "A",
    "searchTypeCategory": "receipts",
    "reportTypeId": "24",
    "month": "1",
    "term": "Smith",
}


def substitute_params(route: str) -> str:
    """Replace {param} placeholders with test values."""
    pattern = r"\{(\w+)\}"

    def replace(match):
        param = match.group(1)
        return TEST_VALUES.get(param, "1")

    return re.sub(pattern, replace, route)


def test_endpoint(route: str, timeout: int = 10) -> dict:
    """Test a single endpoint and return result."""
    test_url = BASE_URL + substitute_params(route)

    try:
        resp = requests.get(test_url, timeout=timeout)

        # Check response content type
        content_type = resp.headers.get("Content-Type", "")
        is_json = "application/json" in content_type

        # Try to get response size
        try:
            if is_json:
                data = resp.json()
                if isinstance(data, list):
                    item_count = len(data)
                elif isinstance(data, dict):
                    item_count = len(data.keys())
                else:
                    item_count = None
            else:
                item_count = None
        except:
            item_count = None

        return {
            "status_code": resp.status_code,
            "ok": resp.ok,
            "content_type": content_type,
            "is_json": is_json,
            "item_count": item_count,
            "test_url": test_url,
            "error": None,
        }
    except requests.exceptions.Timeout:
        return {
            "status_code": None,
            "ok": False,
            "content_type": None,
            "is_json": False,
            "item_count": None,
            "test_url": test_url,
            "error": "Timeout",
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": None,
            "ok": False,
            "content_type": None,
            "is_json": False,
            "item_count": None,
            "test_url": test_url,
            "error": str(e),
        }


def main():
    # Load endpoints
    with open("api/ocpf-endpoints.json", "r") as f:
        endpoints = json.load(f)

    print(f"Testing {len(endpoints)} endpoints...")
    print("=" * 80)

    results = []
    working = []
    not_working = []

    for i, endpoint in enumerate(endpoints, 1):
        route = endpoint["route"]
        controller = endpoint["controller"]
        description = endpoint.get("description", "")

        print(f"[{i}/{len(endpoints)}] Testing {route}...", end=" ", flush=True)

        result = test_endpoint(route)
        result["route"] = route
        result["controller"] = controller
        result["description"] = description
        results.append(result)

        if result["ok"]:
            working.append(result)
            status = f"✓ {result['status_code']}"
            if result["item_count"] is not None:
                status += f" ({result['item_count']} items)"
            print(status)
        else:
            not_working.append(result)
            if result["error"]:
                print(f"✗ {result['error']}")
            else:
                print(f"✗ {result['status_code']}")

    print("\n" + "=" * 80)
    print(f"\nSUMMARY: {len(working)} working, {len(not_working)} not working")
    print(f"Success rate: {len(working)/len(endpoints)*100:.1f}%")

    # Save detailed results
    output = {
        "test_date": datetime.now().isoformat(),
        "total_endpoints": len(endpoints),
        "working_count": len(working),
        "not_working_count": len(not_working),
        "success_rate": len(working) / len(endpoints) * 100,
        "results": results,
    }

    with open("api/endpoint-test-results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\nDetailed results saved to api/endpoint-test-results.json")

    # Print summary by controller
    print("\n" + "=" * 80)
    print("RESULTS BY CONTROLLER:")
    print("-" * 80)

    controllers = {}
    for r in results:
        ctrl = r["controller"]
        if ctrl not in controllers:
            controllers[ctrl] = {"working": 0, "not_working": 0}
        if r["ok"]:
            controllers[ctrl]["working"] += 1
        else:
            controllers[ctrl]["not_working"] += 1

    for ctrl, counts in sorted(controllers.items()):
        total = counts["working"] + counts["not_working"]
        pct = counts["working"] / total * 100
        print(f"  {ctrl}: {counts['working']}/{total} ({pct:.0f}%)")

    # Print non-working endpoints
    if not_working:
        print("\n" + "=" * 80)
        print("NON-WORKING ENDPOINTS:")
        print("-" * 80)
        for r in not_working:
            error_info = r["error"] if r["error"] else f"HTTP {r['status_code']}"
            print(f"  [{r['controller']}] {r['route']}")
            print(f"    Tested: {r['test_url']}")
            print(f"    Error: {error_info}")
            print()


if __name__ == "__main__":
    main()
