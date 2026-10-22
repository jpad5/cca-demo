# Demo runbook

## The day before (Tue Oct 27)

- [ ] Build frozen since Monday night; no changes today except fixes for failed tests.
- [ ] Two timed dry runs, both 12 minutes or less.
- [ ] Backup clips A1-A4 recorded, saved locally on both presenter laptops and in OneDrive.
- [ ] Laptops, phone and a hotspot charged; adapters packed.

## Show day (Wed Oct 28)

### By 11:00 AM

1. Reset the demo claims:

   ```powershell
   ./scripts/Reset-DemoClaim.ps1 -OrgUrl https://<org>.crm.dynamics.com -ClaimId ZAV-1042,ZAV-1043
   ```

2. Email `ZAV-1042.xlsx` to the intake mailbox with the subject `Contents inventory - ZAV-1042`.
3. Confirm the ZAV-1042 run reached Human Review with exactly 2 flags (Ref 6, Ref 8) and that Maya's review card arrived. **Don't complete it.**
4. On the phone, prepare a draft email with `ZAV-1043.xlsx` attached and the subject `Contents inventory - ZAV-1043`. Don't send it.
5. Warm up the agent in Teams with a rehearsal claim: `Show the flagged items on claim ZAV-1044.`

### At 2:30 PM

- [ ] Copilot Studio: all connections show Connected; the agent is published.
- [ ] Tabs open on the driver laptop: workflow run history (ZAV-1042 run), Dataverse Approvals view, CAT Desk channel, the ZAV-1043 workbook.
- [ ] Maya's laptop: Teams open on the review card and the agent chat; notifications on.
- [ ] Screens zoomed to 125-150%; other notifications off; hotspot ready.
- [ ] Backup clips open in a video player, paused at 0:00.

### During the demo

- The timekeeper calls time at 5:00, 8:00 and 9:30.
- **Rule:** if any step stalls for more than 20 seconds, cut to that act's clip and keep talking.

## Failure modes

| Symptom | Likely cause | On stage | Afterwards |
|---|---|---|---|
| ZAV-1043 run hasn't finished by 9:30 | Trigger latency or slow research | Play clip A4: "Here's the same claim from rehearsal." | Check trigger latency and research batch size |
| Agent replies with prose instead of JSON | Instructions drift | The validation gate holds the case. Show it: "That's the gate doing its job." | Tighten the workflow-mode instructions |
| Agent is slow or a tool fails in Act 2 | Research latency, connection consent | Play clip A2 | Re-consent connections; shorten the prompt |
| Approval card doesn't appear in Teams | Notification delay | Open the Approvals app or the Outlook actionable message; else clip A3 | Check the Approvals connection |
| Agent appears to approve in chat | Dataverse MCP tool still attached | Show that no Approval row exists | Remove the tool (agent changes, section 2) |
| Teams post fails | Connection or channel ID | Show the Approval row in Dataverse | Fix the channel environment variables |

## Q&A prep

| Question | Answer |
|---|---|
| Why not let the agent do the math? | Money must be reproducible and auditable. The same inputs and rule set always produce the same numbers; a model can't guarantee that. |
| What stops the agent from approving? | It has no tool that can write a decision, and only the approval step records one, bound to a specific calculation run. |
| Can this run without the agent? | Yes. Every deterministic step works without AI; the agents handle the steps that need judgment. |
| What do the AI steps cost? | Only the AI and agent steps use generative AI. Check the current Copilot Studio licensing guide for how workflow runs and AI steps are metered. |
| Where do Document Extract and Computer-Using Agents fit? | Both are planned building blocks (slide 5): receipts and photos (Document Extract); entering results into a legacy claims system (Computer-Using Agents). |
| Is this production-ready? | No. It's a demo built on a production design, which adds a full state machine, idempotency and challenge-bound approvals. |
