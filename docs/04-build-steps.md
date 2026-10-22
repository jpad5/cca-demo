# Build steps

Target: demo-ready by 3:00 PM PT on Wednesday, October 28, 2026. About 18.5 hours of build and rehearsal.

## Schedule (Pacific time)

| When | Work | Done when |
|---|---|---|
| Thu Oct 22, 4-5 PM and evening | Phase 0 spikes; Phase 1 environment and import; start the rebrand | The agent returns valid JSON 3 times out of 3 |
| Fri Oct 23, 10 AM | Team review: lock the story and roles | Run of show agreed |
| Fri Oct 23, 11 AM | Confirm what can be shown publicly about the solution this demo builds on | A clear yes or no |
| Fri Oct 23, 1-3 PM and evening | Phase 3 data, rules and bulletin; Calculate Valuation fix; workflow steps 1-7 | ZAV-1042 reaches the valuation step |
| Sat Oct 24, morning | Workflow steps 8-12; first full run | One clean end-to-end run |
| Sun Oct 25 and Mon Oct 26 evenings | Phase 5 tests; five back-to-back runs; tuning. **Freeze Monday night.** | At least 4 of 5 clean |
| Tue Oct 27 | Two timed dry runs; record backup clips A1-A4 before 6 PM | Both runs 12 minutes or less |
| Wed Oct 28 morning | Show-day steps in the [runbook](06-demo-runbook.md) | Ready by 3:00 PM |

**Cut order if behind:** 1) M365 Copilot step, 2) the live ZAV-1043 run (show its recording), 3) the Item Normalizer (pass rows straight to research).
**Never cut:** the trigger, the research agent, the rules valuation, human review and approval, the agent calling workflows.

## Phase 0: spikes (about 2 hours)

| Spike | How | Exit criteria |
|---|---|---|
| S1 Agent node round trip | Test workflow: Agent node calls the published agent with 2 items using [research-request.md](../workflow/prompts/research-request.md) | Valid JSON 3 of 3; latency noted |
| S2 Review and approval surfaces | Send a Human Review Request and a custom-response approval to Maya | Both appear in Teams within 30 seconds; note where |
| S3 Trigger latency | Send 3 emails to the intake mailbox | Runs start in under 60 seconds |
| S4 M365 Copilot node | Ask about the bulletin page | Grounded answer in under 30 seconds, or cut the step |

## Phase 1: environment and solution

1. Use a dedicated environment with Dataverse, for example **Zava CAT Demo**. Apply the DLP grouping in [architecture](02-architecture.md#connections).
2. Import `CATContentsAssistant_1_0_0_1.zip` from [jpad5/cca](https://github.com/jpad5/cca) as an unmanaged solution. Map the connection references during import.
3. Add to **Inventory Item**:
   - **Replacement Confidence**, Choice: High, Medium, Low, Unknown (`cca_replacementconfidence`).
   - **Review Reason**, Text, 500 characters (`cca_reviewreason`).
4. Add these labels to the **Case State** choice on Valuation Case (it has Open, Closed, Pending): **Needs Review**, **Pending Approval**, **Approved**, **Held**.
5. Optional: turn on Dataverse auditing for Valuation Case, Inventory Item, Item Valuation and Approval, so "who changed what" is visible.
6. Create environment variables listed in [architecture](02-architecture.md#environment-variables).

## Phase 2: agent

Follow [agent changes](05-agent-changes.md): rebrand, tool fixes, research contract, approval boundary, publish.

## Phase 3: content and data

1. **SharePoint:** a site such as *Zava CAT* with a document library folder **CAT Intake**, and a page **CAT Event Bulletin - CAT-26-07** with the text in [content/cat-event-bulletin.md](../content/cat-event-bulletin.md).
2. **Teams:** a team *Zava CAT* with a channel **CAT Desk**. Add Maya's account.
3. **Workbooks:**

   ```bash
   pip install openpyxl
   python data/build_workbooks.py
   ```

   This writes `data/workbooks/ZAV-1042.xlsx` to `ZAV-1049.xlsx`. For an extra rehearsal claim: `python data/build_workbooks.py --claim ZAV-1050 --template ZAV-1043`.
4. **Rule set:** add a Rule Set Version row:

   | Column | Value |
   |---|---|
   | Rule Set Name | Zava Demo Depreciation Rules v1.0 |
   | Approval Status | Approved |
   | Effective Start | 2026-01-01 |
   | Rule Payload JSON | The contents of [data/rules/zava-demo-depreciation-rules-v1.json](../data/rules/zava-demo-depreciation-rules-v1.json) |

5. **Check the math:** `python data/valuation_reference.py --inventory data/inventories/ZAV-1042.csv --normalized data/fixtures/ZAV-1042-normalized.json --research data/fixtures/ZAV-1042-research.json --allow-host retailer.example` must match [ZAV-1042-expected.md](../data/fixtures/ZAV-1042-expected.md).

## Phase 4: workflow

Build [CAT Contents Intake](03-intake-workflow.md) in this order, testing with a rehearsal claim after each group:

| Group | Steps | Test with |
|---|---|---|
| A | 1-3 | ZAV-1044: case and 8 items created |
| B | 4-6 | ZAV-1045: categories set; research passes the gate |
| C | 7 | ZAV-1046: totals reconcile; compare with the reference script |
| D | 8-12 | ZAV-1047 and ZAV-1048: full run, review, approval, Teams post |

## Phase 5: tests

Run acceptance tests T1-T9 from the [workflow spec](03-intake-workflow.md#acceptance-tests) and test 6 of the [agent changes](05-agent-changes.md#6-test-the-agent-on-its-own).

## Phase 6: rehearse and record

Two timed dry runs against the [presenter script](01-storyboard.md). Record clips A1-A4 at 1920x1080 with the screen zoomed to 125-150%.
