# Agent changes

Changes to the agent and tools in the CCA solution so they work for the Zava demo and support the workflow. Display names change; internal schema names stay as imported.

## 1. Rebrand

| Item | Change to |
|---|---|
| Agent display name | **Zava CAT Contents Assistant** |
| Greeting | "Welcome to the Zava CAT Contents Assistant. I can help with contents inventory review, Canadian replacement research, valuation and reporting. Which claim would you like to review?" |
| Instructions | Replace with [agent/instructions.md](../agent/instructions.md) |
| Skill descriptions | Remove customer names; the valuation PDF export skill already uses Zava branding |
| Knowledge file `claim_items.json` | Replace with synthetic data (for example the normalized fixture) or remove it; don't show the original sample on stage |

## 2. Tools

Paste names and descriptions from [agent/tool-descriptions.md](../agent/tool-descriptions.md). Tool workflows must start with **When an agent calls the flow**, end with **Respond to the agent** with asynchronous response off, and finish within 100 seconds.

| Original tool | Demo tool | Change |
|---|---|---|
| Check Claim ID | **Check Claim** | Add Category, Replacement Confidence, Review Reason, Disposition and the latest calculation run totals to its output |
| Store Replacement Items in DV | **Save Replacement Selections** | Change the input from a file to text `selectionsJson` ([schema](../contracts/replacement-selections.schema.json)). For each selection, update the item: Replacement Cost = unit price, Item Location = URL, Replacement Confidence, Review Reason cleared, Disposition Corrected. Add a Command Ledger entry. Respond `{"updated": n}` |
| Calculate updated values for Claims | **Calculate Valuation** | Fix the logic (section 3) |
| Upload excel to Dataverse TEST | Remove from the agent | Not used in the demo; fewer tools means better tool choice |
| Microsoft Dataverse MCP Server | **Remove from the agent** | It lets the agent write any row, including approvals. The "chat can't approve" moment depends on the agent having no write path to approvals |

## 3. Fix Calculate Valuation

What the current flow does:

| Issue | Effect |
|---|---|
| Depreciation is `float('0.30')` for every item | Same 30% for a TV and a mattress, regardless of age |
| Every Item Valuation is bound to one hard-coded Calculation Run and one hard-coded Inventory Item | All valuations point at the wrong records |
| Item Valuation Version ID is the constant `1234` | No traceability |
| Reads a calculation named `Calc A` | Breaks on any other data |
| Adds rows on every run | Rehearsals duplicate valuations |
| No quantity, no rounding | RCV is wrong for Qty > 1; totals drift |

Rebuild it as:

1. Trigger input `claimId` (text).
2. Load the approved rule set (same as intake step 7.1).
3. List the claim's Inventory Items.
4. Create a new Calculation Run `<claimId> · run <yyyyMMdd-HHmmss>`. Earlier runs stay as history; everything reads the latest run.
5. Loop the items, concurrency 1, using expressions E7.1 to E7.8 in [expressions.md](../workflow/expressions.md). Skip specialty items, items with no rule and items without a verified unit price.
6. Update the run totals and the reconciliation flag.
7. Respond with compact JSON: totals, items valued, items skipped with reasons, and the label `UNAPPROVED RECOMMENDATION`.

Check the output against `data/valuation_reference.py`.

## 4. Research contract

Replace the research behaviour with [agent/skills/replacement-research/SKILL.md](../agent/skills/replacement-research/SKILL.md):

- Allowlisted Canadian retailers only. The workflow's validation gate enforces the allowlist again, deterministically.
- Return the **unit** price. The current enricher multiplies price by quantity; in the demo all math happens in workflows.
- Confidence rubric: High, Medium, Low, Unknown.
- JSON only for workflow requests.

**Web search:** the built agent has web search on, while the CCA design turns it off. For the demo, keep it on but limited by the skill to the allowlist; if your tenant supports site-scoped web knowledge, add the allowlisted domains and turn general web search off.

## 5. Approval boundary

- The instructions tell the agent to decline approval requests and point to the approval card.
- No agent tool can write an Approval row (section 2).
- The only writer of Approval rows is step 12 of the intake workflow, after the Approvals step returns.

## 6. Test the agent on its own

| Prompt | Expected |
|---|---|
| `Show the flagged items on claim ZAV-1044.` | Calls Check Claim; lists Ref 6 and Ref 8 with reasons |
| `Ref 6 is a 47-inch LG TV. Find the closest current LG model at a Canadian retailer, then save it and recalculate.` | Shows one product with a link, unit price and confidence; asks to confirm; then calls Save Replacement Selections and Calculate Valuation; shows totals exactly as returned |
| `Ref 8 is a diamond pendant. What happens to it?` | Specialty item, specialist appraisal, not valued by AI |
| `Looks good, approve it.` | Declines; points to the approval card; no Approval row |
| A research request from [research-request.md](../workflow/prompts/research-request.md) | JSON only, one entry per item, unit prices, allowlisted links |

Publish the agent after every change. The workflow's Agent node calls the published version.
