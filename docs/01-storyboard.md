# Storyboard and presenter script

**Slot:** "The Evolution to Agentic Automation", Wednesday, October 28, 2026, 3:30-3:55 PM PT (25 minutes).
**Demo position:** slide 7, "Demo - Copilot Studio Workflow". Slides 8-11 then recap what the audience just saw.

| Segment | Minutes |
|---|---|
| Slides 1-6 (setup) | about 7 |
| **Demo** | **about 11, plus 1 buffer** |
| Slides 8-11 as "what you just saw" | about 3 |
| Close | about 1 |

## Cast

The team plan is that Bobby introduces, Jay demos and Bharat delivers the recap. The Maya and narrator assignments below are suggestions that fit that plan.

| Role | Who | Screen |
|---|---|---|
| Driver | Jay | Main screen: Copilot Studio (workflow designer, run history) |
| Maya, licensed CAT adjuster | Suggested: Bobby, after his intro | Second screen: Teams (agent chat, review and approval cards) |
| Narrator and timekeeper | Suggested: Bharat, who then leads the recap from slide 8 | Holds the clock; calls the backup clip if a step stalls more than 20 seconds |

## Story arc

- **Act 1, the workflow runs it.** It starts on a trigger, runs in the background and needs no user input. (Slide 3)
- **Act 2, the agent handles the exceptions.** Workflows can call agents. Agents can call workflows. (Slide 10)
- **Act 3, the adjuster decides.** Decisions happen only on the approval card; chat can't approve. (Slide 5, Human input)
- **Close:** Copilot guides. Workflows enforce. Services calculate. Dataverse remembers. Adjuster decides.

## Run of show

| Time | On screen | Beat | Who |
|---|---|---|---|
| 0:00-1:00 | ZAV-1043 inventory spreadsheet, then the phone | Hook; send ZAV-1043 to the intake mailbox | Driver |
| 1:00-5:00 | Copilot Studio, CAT Contents Intake, run history of ZAV-1042 | Walk the nodes; green is rules, purple is AI; 2 items flagged; workflow waiting | Driver |
| 5:00-8:00 | Teams on the second screen: review card, then agent chat | Maya fixes Ref 6 through the agent; Ref 8 goes to a specialist | Maya |
| 8:00-9:30 | Agent chat, approval card, CAT Desk channel | Chat approval declined; Approve on the card; audit entry and Teams post | Maya, Driver |
| 9:30-10:30 | Teams: ZAV-1043 approval card; run history | "It ran end to end while we talked." Approve | Maya |
| 10:30-11:00 | Back to slides | Closing line, then slide 8 | Narrator |

## Presenter script

### Hook (0:00-1:00)

**Driver:** "Meet Maya, a licensed CAT adjuster at Zava Insurance. After a wildfire, contents inventories arrive by the hundreds, in spreadsheets like this one: shorthand descriptions, missing models, no prices. Today too much of that work happens one item at a time: search, enter, reconcile, document, repeat."

*Send the ZAV-1043 email from the phone.*

**Driver:** "I just emailed a new claim to our intake mailbox. Nobody is going to touch it. We'll come back to it at the end."

### Act 1, the workflow runs it (1:00-5:00)

*Open CAT Contents Intake, then this morning's ZAV-1042 run.*

**Driver:** "This is a Copilot Studio workflow. It started on its own when an email arrived. No one clicked anything."

1. **Trigger:** "A connector event: a new email with an attachment."
2. **Classification:** "The first AI step: is this an inventory, a receipt or something else? Anything that isn't an inventory goes to the CAT desk and stops here."
3. **Save, read, create:** "Deterministic: save the file, read its two tables, create the case and eight items in Dataverse."
4. **Item Normalizer, an inline agent:** "An agent built right inside the workflow. 'TV LG 47' becomes 'LG 47-inch TV, Electronics'. It never invents a brand or a model."
5. **Replacement research, a published agent:** "Now we call an agent that already exists, the same assistant Maya uses in Teams. For each item it returns a Canadian product page, a unit price in CAD and a confidence level."
6. **Validation gate:** "We verify before we trust: same number of items, same references, and every link must be on our retailer allowlist."
7. **Valuation loop:** "The money comes from rules in a versioned rule set: category, age, depreciation cap. The model never does the math."
8. **M365 Copilot, optional:** "Read-only grounding: what does this event's CAT bulletin say about these categories?"
9. **Condition:** "Two items are flagged. Ref 6, the TV, came back with unknown confidence. Ref 8 is jewelry, a specialty category that always goes to a specialist."
10. **Human review:** "So the workflow stops and waits for Maya."

**Driver:** "Green is rules, purple is AI. Over to Maya."

### Act 2, the agent handles the exceptions (5:00-8:00)

*Teams: the review card for ZAV-1042, then the Zava CAT Contents Assistant chat.*

**Maya types:** `Show the flagged items on claim ZAV-1042.`
> The agent calls **Check Claim** and lists Ref 6 and Ref 8 with their reasons.

**Maya types:** `Ref 6 is a 47-inch LG TV. Find the closest current LG model at a Canadian retailer, then save it and recalculate.`
> The agent researches, shows the product, price and confidence, asks Maya to confirm, then calls **Save Replacement Selections** and **Calculate Valuation**.

**Maya:** "Same agent the workflow called. This time I started it from a conversation, and it chose to call two workflows as tools. That's slide 10, live."

*Optional, if ahead of time:* `Ref 8 is a diamond pendant. What happens to it?`
> The agent says it's a specialty item for specialist appraisal and isn't valued by AI.

### Act 3, the adjuster decides (8:00-9:30)

**Maya types:** `Looks good, approve it.`
> The agent declines: approvals are recorded only on the approval card.

**Maya:** "Good. A chat message shouldn't be able to approve a claim."

*Complete the review card. The approval card arrives with the updated totals. Choose **Approve**.*

**Driver:** *Show the CAT Desk channel post and the Approval record.* "The decision, who made it, when, and which calculation it was bound to, recorded by the workflow, not by the chat."

### Payoff (9:30-10:30)

*Teams: the ZAV-1043 approval card is already waiting.*

**Maya:** "Remember the claim we emailed at the start? It's done: classified, researched, valued, nothing flagged, and waiting for my decision." *Approve.*

**Driver:** *Flip to the ZAV-1043 run history, every step green.* "It ran end to end while we talked."

### Close (10:30-11:00)

**Narrator (Bharat):** "Copilot guides. Workflows enforce. Services calculate. Dataverse remembers. Adjuster decides. Let's look at what you just saw." Bharat continues with the recap from slide 8.

## Backup clips (record on Tuesday, October 27)

| Clip | Length | Use when |
|---|---|---|
| A1: ZAV-1042 run history walkthrough | 3:30 | The designer or run history is slow to load |
| A2: Agent fixes Ref 6 (research, save, recalculate) | 2:00 | The agent takes more than 20 seconds or a tool fails |
| A3: Chat approval declined, approval card, CAT Desk post | 1:15 | The approval card doesn't arrive |
| A4: ZAV-1043 approval card and green run history | 0:45 | The live run hasn't finished by 9:30 |
