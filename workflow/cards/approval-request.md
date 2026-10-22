# Approval request: title and details

**Type:** Custom responses, wait for one response. **Responses:** `Approve`, `Reject`, `Hold`.

**Title**

```text
Approve contents valuation: {ClaimId}
```

**Details** (Markdown)

```markdown
**{InsuredName}** · Policy {PolicyId} · CAT event {CatCode}

- Replacement cost (RCV): **CAD {TotalRCV}**
- Depreciation: **CAD {TotalDep}**
- Actual cash value (ACV): **CAD {TotalACV}**
- Items valued: {ItemsValued} · Specialist appraisal: {SpecialistItems}
- Rule set: {RuleSetName} · Calculation run: {CalcRunName}

**Bulletin guidance:** {BulletinNotes}

UNAPPROVED RECOMMENDATION. Choose Approve, Reject or Hold. Your decision and comments are recorded with your name and the time.
```
