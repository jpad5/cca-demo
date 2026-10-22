# Research request: message from the workflow to the published agent

Send this as the Agent node's message. Replace `{ClaimId}` and `{NormalizedItemsJson}` with dynamic content.

```text
[WORKFLOW REQUEST] replacement-research
Claim: {ClaimId}

Return only JSON in this shape, with no prose and no code fences:
{"items":[{"ref":"<ref>","productName":"<name or Unknown>","retailer":"<host or Unknown>","replacementUrl":"<url or Unknown>","unitPriceCAD":<number or "Unknown">,"confidence":"High|Medium|Low|Unknown","note":"<short note>"}]}

Rules:
- One entry per item, in the same order, with the same ref values.
- Allowlisted retailers only, as listed in the replacement-research skill.
- Unit price only. Don't multiply by quantity or add tax.
- Never invent a product, link or price. Use "Unknown" when you can't verify.
- Jewelry and other specialty items: "Unknown" with the note "Specialty item".

Items:
{NormalizedItemsJson}
```

**Parse with:** [research-results.schema.json](../../contracts/research-results.schema.json).
