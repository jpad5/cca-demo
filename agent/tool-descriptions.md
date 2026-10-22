# Tool names and descriptions

Paste these into each tool in the agent. Clear descriptions are what make the agent pick the right tool in Act 2.

## Check Claim

**Description:** Returns the valuation case for an exact claim number, for example ZAV-1042: claim details, every inventory item with its category, replacement link, unit replacement price, confidence, review reason and disposition, and the latest calculation totals. Call this first whenever a claim number is mentioned. Read-only.

| Input | Type | Description |
|---|---|---|
| `claimId` | Text | Exact claim number as the user typed it, for example ZAV-1042. Never guess or reformat it. |

## Save Replacement Selections

**Description:** Saves replacement selections the adjuster has confirmed for one claim: for each item, the product page link, unit price in CAD and confidence. Clears the item's review reason. Call only after the adjuster explicitly confirms the exact product and price you showed. Doesn't calculate values.

| Input | Type | Description |
|---|---|---|
| `selectionsJson` | Text | JSON text: `{"claimId":"ZAV-1042","selections":[{"ref":"6","productName":"...","replacementUrl":"https://...","unitPriceCAD":449.99,"confidence":"Medium"}]}`. Unit price only; never multiply by quantity. |

## Calculate Valuation

**Description:** Recalculates the contents valuation for one claim from the approved depreciation rule set and saves a new calculation run. Returns totals (RCV, depreciation, ACV) and per-item values. Call after saving replacement selections, or when the adjuster asks to recalculate. The returned values are final: present them exactly and never change them.

| Input | Type | Description |
|---|---|---|
| `claimId` | Text | Exact claim number, for example ZAV-1042. |

## Remove for the demo

- **Upload excel to Dataverse TEST**: not used.
- **Microsoft Dataverse MCP Server**: gives the agent a general write path to Dataverse, including approvals.
