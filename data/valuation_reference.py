"""Reference implementation of the demo valuation rules.

Mirrors the validation gate (step 6) and valuation loop (step 7) in
docs/03-intake-workflow.md and the formulas in workflow/expressions.md, so you
can check the numbers the workflow and the Calculate Valuation tool produce.

Usage:
  python data/valuation_reference.py \
      --inventory data/inventories/ZAV-1042.csv \
      --normalized data/fixtures/ZAV-1042-normalized.json \
      --research data/fixtures/ZAV-1042-research.json \
      --allow-host retailer.example

  Add --override data/fixtures/ZAV-1042-act2-fix.json to apply the Act 2 fix.
"""
import argparse
import csv
import json
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
CENT = Decimal("0.01")


def r2(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def number(text, default):
    text = (text or "").strip()
    return Decimal(text) if text else Decimal(default)


def host_of(url):
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def money(value):
    return "" if value is None else f"{value:,.2f}"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--normalized", required=True)
    parser.add_argument("--research", required=True)
    parser.add_argument("--override", help="Research entries applied on top of --research, for example the Act 2 fix")
    parser.add_argument("--rules", default=str(HERE / "rules" / "zava-demo-depreciation-rules-v1.json"))
    parser.add_argument("--allow-host", action="append", default=[], help="Extra allowed host for test fixtures")
    args = parser.parse_args()

    rules = json.loads(Path(args.rules).read_text(encoding="utf-8"))
    categories = {c["category"]: c for c in rules["categories"]}
    allowed = set(rules["allowedRetailerHosts"]) | set(args.allow_host)
    threshold = Decimal(str(rules["highValueThresholdCAD"]))

    with open(args.inventory, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    normalized = {str(i["ref"]): i for i in json.loads(Path(args.normalized).read_text(encoding="utf-8"))["items"]}
    research_items = json.loads(Path(args.research).read_text(encoding="utf-8"))["items"]
    if args.override:
        for fix in json.loads(Path(args.override).read_text(encoding="utf-8"))["items"]:
            research_items = [fix if str(x["ref"]) == str(fix["ref"]) else x for x in research_items]

    # Step 6: validation gate
    refs = [str(r["Ref"]) for r in rows]
    if len(research_items) != len(rows):
        sys.exit(f"GATE FAILED: {len(research_items)} research items for {len(rows)} inventory rows")
    for ref in refs:
        matches = [x for x in research_items if str(x["ref"]) == ref]
        if len(matches) != 1:
            sys.exit(f"GATE FAILED: Ref {ref} appears {len(matches)} times in research output")
    research = {str(x["ref"]): dict(x) for x in research_items}

    # Step 7: valuation loop
    lines, flags = [], []
    total_rcv = total_dep = total_acv = Decimal("0")
    valued = specialist = 0
    for row in rows:
        ref = str(row["Ref"])
        item = normalized[ref]
        found = research[ref]
        url, price = str(found.get("replacementUrl", "Unknown")), found.get("unitPriceCAD", "Unknown")
        verified = (url != "Unknown" and host_of(url) in allowed
                    and isinstance(price, (int, float)) and not isinstance(price, bool) and price > 0)
        if not verified:
            found.update(replacementUrl="Unknown", unitPriceCAD="Unknown", confidence="Unknown")

        rule = categories.get(item["category"])
        qty = number(row["Qty"], "1")
        age = number(row["Years"], "0") + number(row["Months"], "0") / Decimal(12)
        reasons = []
        rcv = dep = acv = dep_pct = None
        if rule and rule["specialty"]:
            reasons.append("Specialty category: specialist appraisal")
            specialist += 1
        elif rule is None:
            reasons.append("No depreciation rule for category")
        elif found["unitPriceCAD"] == "Unknown":
            reasons.append("Replacement not verified")
        else:
            unit = Decimal(str(found["unitPriceCAD"]))
            rcv = r2(unit * qty)
            dep_pct = min(Decimal(str(rule["annualRate"])) * age, Decimal(str(rule["maxRate"])))
            dep = r2(rcv * dep_pct)
            acv = rcv - dep
            total_rcv += rcv
            total_dep += dep
            total_acv += acv
            valued += 1
            if found["confidence"] == "Low":
                reasons.append("Low replacement confidence")
            if rcv >= threshold:
                reasons.append("High value: CAD 2,500 or more")
        if reasons:
            flags.append((ref, item["displayName"], "; ".join(reasons)))
        lines.append((ref, item["displayName"], item["category"], qty, age, found["unitPriceCAD"],
                      rcv, dep_pct, dep, acv, found["confidence"], "; ".join(reasons)))

    print("| Ref | Item | Category | Qty | Age (yrs) | Unit price | RCV | Dep. % | Depreciation | ACV | Confidence | Review reason |")
    print("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for (ref, name, cat, qty, age, unit, rcv, pct, dep, acv, conf, reason) in lines:
        unit_text = money(Decimal(str(unit))) if unit != "Unknown" else "Unknown"
        pct_text = "" if pct is None else f"{(pct * 100).normalize():f}%"
        age_text = f"{age.normalize():f}"
        print(f"| {ref} | {name} | {cat} | {qty} | {age_text} | {unit_text} | {money(rcv)} | {pct_text} | "
              f"{money(dep)} | {money(acv)} | {conf} | {reason} |")
    print(f"| **Total** | {valued} valued, {specialist} specialist | | | | | **{money(total_rcv)}** | | "
          f"**{money(total_dep)}** | **{money(total_acv)}** | | |")
    print()
    print(f"Reconciliation (RCV - depreciation = ACV): {'pass' if total_rcv - total_dep == total_acv else 'FAIL'}")
    print(f"Flags: {len(flags)}")
    for ref, name, reason in flags:
        print(f"- Ref {ref} · {name}: {reason}")


if __name__ == "__main__":
    main()
