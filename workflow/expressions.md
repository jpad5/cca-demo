# Expressions

Reference expressions for the CAT Contents Intake workflow and the tool workflows. Each is given in **Workflow Definition Language** (the `@{...}` expressions used by agent flows and Power Automate) and, where useful, **Power Fx**. Action names in the WDL examples assume you rename actions as shown; adjust if yours differ. Verify syntax in your designer during the Thursday spikes.

The Excel connector returns every cell as text and blanks as empty strings, so numeric reads are wrapped in `if(empty(...), default, float(...))`.

## Step 2: classification

**E2.1, classification input**

```text
concat(
  triggerOutputs()?['body/subject'], ' | ',
  triggerOutputs()?['body/bodyPreview'], ' | Attachments: ',
  join(body('Select_attachment_names'), ', ')
)
```

`Select_attachment_names` is a Select over `triggerOutputs()?['body/attachments']` that maps `item()?['name']`.

**E2.2, has a workbook**: Filter array `Filter_xlsx` over the attachments with `endsWith(toLower(item()?['name']), '.xlsx')`, then:

```text
greater(length(body('Filter_xlsx')), 0)
```

## Step 3: save, read, create

**E3.1, file name**

```text
concat(formatDateTime(utcNow(), 'yyyyMMdd-HHmmss'), '-', first(body('Filter_xlsx'))?['name'])
```

**E3.2, file content**

```text
base64ToBinary(first(body('Filter_xlsx'))?['contentBytes'])
```

**E3.3, claim header**

```text
first(outputs('List_ClaimHeader')?['body/value'])?['Claim Number']
```

Same pattern for `Insured Name`, `Policy Number`, `Date of Loss`, `Province` and `CAT Code`.

**E3.4, quantity with default 1**

```text
if(empty(items('For_each_row')?['Qty']), 1, float(items('For_each_row')?['Qty']))
```

**E3.5, append to ItemIndex**

```text
{
  "ref": "@{items('For_each_row')?['Ref']}",
  "itemId": "@{outputs('Add_inventory_item')?['body/cca_inventoryitemid']}"
}
```

## Step 4: normalizer input

**E4.1**: a Select `Select_rows_for_normalizer` over `outputs('List_Inventory')?['body/value']` mapping `ref`, `room`, `description`, `brand`, `model`, `qty`, `years`, `months`, `notes` from the same-named workbook columns, then:

```text
string(body('Select_rows_for_normalizer'))
```

## Step 6: validation gate

**E6.1, counts match**

```text
equals(length(body('Parse_research')?['items']), length(outputs('List_Inventory')?['body/value']))
```

**E6.2, each Ref exactly once**: inside a loop over the inventory rows, a Filter array `Filter_research_for_ref` over `body('Parse_research')?['items']` with

```text
equals(string(item()?['ref']), string(items('For_each_check')?['Ref']))
```

then set `GateFailed` to `true` when

```text
not(equals(length(body('Filter_research_for_ref')), 1))
```

**E6.3, retailer allowlist** (`r` is the research item)

```text
if(
  equals(string(r?['replacementUrl']), 'Unknown'),
  false,
  contains(
    variables('Rules')?['allowedRetailerHosts'],
    replace(toLower(uriHost(r?['replacementUrl'])), 'www.', '')
  )
)
```

Power Fx equivalent of the host check:

```text
With({host: Lower(First(Split(Last(Split(r.replacementUrl, "://")).Value, "/")).Value)},
  Substitute(host, "www.", "") in Rules.allowedRetailerHosts)
```

## Step 7: valuation

The worked example in [data/fixtures/ZAV-1042-expected.md](../data/fixtures/ZAV-1042-expected.md) was produced by [data/valuation_reference.py](../data/valuation_reference.py), which implements exactly these formulas. Use it to check the workflow's numbers.

Formulas:

| Value | Formula |
|---|---|
| Age (years) | `Years + Months / 12` |
| Depreciation % | `min(annualRate × age, maxRate)` |
| RCV total | `round(unitPrice × quantity, 2)` |
| Depreciation amount | `round(RCV total × depreciation %, 2)` |
| ACV total | `RCV total − depreciation amount` |
| ACV each | `round(ACV total / quantity, 2)` |

**E7.1, rule for the item's category**: Filter array `Filter_rule` over `variables('Rules')?['categories']` with `equals(item()?['category'], <item category>)`, then `first(body('Filter_rule'))`.

**E7.2, age in years**

```text
add(
  if(empty(string(item()?['Years'])), 0, float(item()?['Years'])),
  div(if(empty(string(item()?['Months'])), 0, float(item()?['Months'])), 12)
)
```

**E7.3, depreciation %**

```text
min(mul(float(first(body('Filter_rule'))?['annualRate']), variables('AgeYears')), float(first(body('Filter_rule'))?['maxRate']))
```

**E7.4, RCV total** (rounded to 2 decimals)

```text
float(formatNumber(mul(variables('UnitPrice'), variables('Qty')), '0.00', 'en-US'))
```

**E7.5, depreciation amount**

```text
float(formatNumber(mul(variables('RcvTotal'), variables('DepPct')), '0.00', 'en-US'))
```

**E7.6, ACV total**

```text
float(formatNumber(sub(variables('RcvTotal'), variables('DepAmt')), '0.00', 'en-US'))
```

**E7.7, ACV each**

```text
float(formatNumber(div(variables('AcvTotal'), variables('Qty')), '0.00', 'en-US'))
```

Power Fx equivalents:

```text
AgeYears = Coalesce(Value(ThisItem.Years), 0) + Coalesce(Value(ThisItem.Months), 0) / 12
Rule     = LookUp(Rules.categories, category = ThisItem.category)
DepPct   = Min(Rule.annualRate * AgeYears, Rule.maxRate)
RcvTotal = Round(UnitPrice * Qty, 2)
DepAmt   = Round(RcvTotal * DepPct, 2)
AcvTotal = RcvTotal - DepAmt
AcvEach  = Round(AcvTotal / Qty, 2)
```

**E7.8, lookup bindings on Add a new row (Item Valuation)**

```text
Inventory Item:   cca_inventoryitems(@{<itemId from ItemIndex>})
Calculation Run:  cca_calculationruns(@{variables('CalcRunId')})
```

Never hard-code a row ID here. The original *Calculate updated values for Claims* flow bound every valuation to one fixed item and one fixed run.

**E7.9, reconciliation**

```text
equals(
  formatNumber(sub(variables('TotalRCV'), variables('TotalDep')), '0.00', 'en-US'),
  formatNumber(variables('TotalACV'), '0.00', 'en-US')
)
```

**Item flags**

```text
or(
  contains(createArray('Low', 'Unknown'), r?['confidence']),
  equals(first(body('Filter_rule'))?['specialty'], true),
  empty(body('Filter_rule')),
  greaterOrEquals(variables('RcvTotal'), float(variables('Rules')?['highValueThresholdCAD']))
)
```

## Step 9: condition

**E9.1**

```text
greater(length(variables('Flags')), 0)
```
