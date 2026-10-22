---
name: replacement-research
description: Research one current Canadian replacement product per inventory item at allowlisted retailers and return the product page, unit price in CAD and a confidence level. Use for [WORKFLOW REQUEST] replacement-research messages and when an adjuster asks to find a replacement for an item.
---

# Replacement research

## Allowlisted retailers

bestbuy.ca, canadiantire.ca, homedepot.ca, walmart.ca, costco.ca, staples.ca, thebrick.com, leons.ca, structube.com, sleepcountry.ca, marks.com, sportchek.ca, linenchest.com, visions.ca

Use no other site. Third-party marketplace listings aren't allowed. This list is illustrative for the demo.

## For each item

1. Search using the brand, model, description and any size or capacity in the item. Ignore damage words such as smoke-damaged, burnt, wet or old.
2. Prefer, in order: the exact brand and model; a current model from the same brand with matching size or capacity; a like-kind-and-quality equivalent.
3. Choose one specific product with a direct product-page link and a visible current price in CAD.
4. Never invent a product, link or price. If you can't verify all three, use "Unknown".
5. Return the **unit** price. Don't multiply by quantity and don't add tax. The workflow does all math.

## Confidence

- **High:** exact brand and model; direct product page; CAD price verified.
- **Medium:** closest like-kind-and-quality replacement; direct product page; CAD price verified.
- **Low:** limited similarity, or key details such as size, capacity or model are missing; product page and CAD price verified.
- **Unknown:** the product, page or CAD price can't be verified. `replacementUrl` and `unitPriceCAD` must then be "Unknown".

Specialty categories (Jewelry, Art, Collectibles, Antiques): return "Unknown" with the note "Specialty item".

## Output for workflow requests

Return only this JSON, with no prose and no code fences. One entry per input item, in the same order, with the same `ref` values.

{"items":[{"ref":"6","productName":"LG 43-inch 4K UHD smart TV","retailer":"bestbuy.ca","replacementUrl":"https://www.bestbuy.ca/en-ca/product/...","unitPriceCAD":449.99,"confidence":"Medium","note":"Closest current LG size"}]}

## Output in conversations

Show a short table: Ref, product, retailer, unit price (CAD), confidence and link. Ask the adjuster to confirm before anything is saved.
