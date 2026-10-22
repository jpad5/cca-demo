# Zava CAT Contents: inbox to approved valuation

Demo kit for **"The Evolution to Agentic Automation"** (Power Platform Community Conference 2026, Wednesday, October 28, 2026, 3:30 PM) by Bharat Rathod, Bobby Chang and Jay Padimiti, Copilot Acceleration Team.

The demo shows both directions of agentic automation in Copilot Studio:

- **A workflow that calls agents.** The *CAT Contents Intake* workflow starts when an inventory email arrives, runs the claim end to end, and calls AI only where judgment is needed.
- **An agent that calls workflows.** The adjuster asks the *Zava CAT Contents Assistant* to fix an exception, and the agent calls deterministic workflows to save and recalculate.

> **Fictional and illustrative.** Zava Insurance and all people, claims and inventories are fictional. Depreciation rates, thresholds and the retailer list are demo values, not claims, actuarial or underwriting guidance.

## The story (about 11 minutes)

| Act | Time | What happens | Talk tie-in |
|---|---|---|---|
| Hook | 0:00-1:00 | A messy inventory spreadsheet; claim **ZAV-1043** is emailed live from a phone. | Slide 3, What is automation? |
| 1. The workflow runs it | 1:00-5:00 | Run history of **ZAV-1042**: trigger, classify, normalize, research, rules valuation, 2 items flagged, waiting for Maya. | Slides 5, 6, 9 |
| 2. The agent handles the exceptions | 5:00-8:00 | Maya asks the agent in Teams; it researches Ref 6, then saves and recalculates by calling workflows. Jewelry goes to a specialist. | Slide 10 |
| 3. The adjuster decides | 8:00-9:30 | "Looks good, approve it" in chat is declined; the approval card records Approve, Reject or Hold with an audit entry. | Slide 5, Human input |
| Payoff | 9:30-10:30 | ZAV-1043's approval card is already waiting: it ran end to end while we talked. | Slide 3 |

**Closing line:** *Copilot guides. Workflows enforce. Services calculate. Dataverse remembers. Adjuster decides.*

## Reused and new

| Piece | Source |
|---|---|
| Dataverse model: Valuation Case, Inventory Item, Item Valuation, Calculation Run, Rule Set Version, Approval, Case Issue, Command Ledger | Reused from `CATContentsAssistant_1_0_0_1.zip` in [jpad5/cca](https://github.com/jpad5/cca) |
| Agent and skills: replacement research, Excel-to-JSON, valuation PDF export | Reused, rebranded to Zava, research contract tightened |
| Agent tools: Check Claim, Save Replacement Selections, Calculate Valuation | Reused; the calculation is fixed to use the rule set |
| **CAT Contents Intake** workflow | **New**, the centrepiece |
| Depreciation rule set, synthetic inventories, CAT Event Bulletin | **New** |

## Repo map

```text
docs/        storyboard and presenter script, architecture, workflow spec, build steps, agent changes, runbook
agent/       agent instructions, tool descriptions, research skill
workflow/    prompts for the AI nodes, review and approval card text, Teams card, expressions
contracts/   JSON schemas for Parse JSON steps and the validation gate
data/        synthetic inventories, workbook generator, rule set, valuation reference, test fixtures
content/     CAT Event Bulletin page text for SharePoint
scripts/     Dataverse reset for rehearsals
slides/      the storyboard deck
```

## Build order

1. [Build steps](docs/04-build-steps.md): environment, solution import, schema additions, data, schedule.
2. [Agent changes](docs/05-agent-changes.md): rebrand, tool fixes, research contract, approval boundary.
3. [CAT Contents Intake workflow](docs/03-intake-workflow.md): node-by-node build spec.
4. [Storyboard and presenter script](docs/01-storyboard.md): rehearse against it.
5. [Demo runbook](docs/06-demo-runbook.md): show-day checklist, reset, fallbacks, Q&A.

[Architecture](docs/02-architecture.md) shows how the pieces fit.

## Prerequisites

- A Power Platform environment with Dataverse and Copilot Studio Workflows.
- Microsoft 365: a demo mailbox for intake, a SharePoint site (document library and a page), a Teams team with a **CAT Desk** channel, and a Microsoft 365 Copilot license for the optional M365 Copilot step.
- Python 3.10 or later with `openpyxl` to generate the inventory workbooks.
- Azure CLI (optional) for `scripts/Reset-DemoClaim.ps1`.

## Status

Build kit, not yet built or rehearsed. Target: ready by 3:00 PM PT on October 28, 2026.
