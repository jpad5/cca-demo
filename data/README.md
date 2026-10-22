# Data

All data is synthetic. Prices in `fixtures/` are illustrative and use the reserved `retailer.example` domain; live runs use real retailer pages found by the research agent.

| Path | What it is |
|---|---|
| `claims.csv` | Claim header values for ZAV-1042 to ZAV-1049 and the inventory template each one uses |
| `inventories/ZAV-1042.csv` | 8 items; produces 2 flags (Ref 6 unknown confidence, Ref 8 jewelry). Used for the pre-run claim |
| `inventories/ZAV-1043.csv` | 6 well-known items; expected to produce no flags. Used for the live claim |
| `build_workbooks.py` | Writes `workbooks/<claim>.xlsx` with the `ClaimHeader` and `Inventory` tables the workflow reads |
| `rules/zava-demo-depreciation-rules-v1.json` | Rule Set Version payload: category rates and caps, specialty flag, high-value threshold, retailer allowlist. Illustrative values |
| `valuation_reference.py` | Reference implementation of the validation gate and valuation loop |
| `fixtures/ZAV-1042-normalized.json` | Expected Item Normalizer output for ZAV-1042 |
| `fixtures/ZAV-1042-research.json` | Illustrative research output for ZAV-1042 |
| `fixtures/ZAV-1042-act2-fix.json` | Maya's Act 2 fix for Ref 6 |
| `fixtures/ZAV-1042-expected.md` | Expected valuation after intake and after the Act 2 fix |

Rehearsal claims: ZAV-1044, 1046 and 1048 use the ZAV-1042 template (flagged path); ZAV-1045, 1047 and 1049 use ZAV-1043 (clean path).
