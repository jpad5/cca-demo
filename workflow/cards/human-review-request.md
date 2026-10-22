# Human Review Request: title and details

**Title**

```text
{ClaimId}: {FlagCount} item(s) need review
```

**Details** (Markdown)

```markdown
**{InsuredName}** · Policy {PolicyId} · CAT event {CatCode}

Items needing your review:
{FlagLines}

You can fix items with the Zava CAT Contents Assistant in Teams, for example:
"Ref 6 is a 47-inch LG TV. Find the closest current LG model at a Canadian retailer, then save it and recalculate."

Complete this review when you're done. The approval request will follow with the latest totals.
```

`{FlagLines}` is one line per flag, built with a Select and `join(..., '\n')`:

```text
- Ref {ref} · {item}: {reason}
```
