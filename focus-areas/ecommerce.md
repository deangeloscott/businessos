---
name: E-commerce
summary: You sell products online.
keywords: [ecommerce, e-commerce, online store, shopify, woocommerce, amazon, etsy, marketplace, products, sku, catalog, dtc, direct to consumer, dropshipping, subscription box]
views: [chart, board]
knowledge:
  - docs/playbooks/customer-optimization.md
  - docs/playbooks/marketing-synthesis.md
  - docs/playbooks/competitor-intelligence.md
  - recipes/web-design/INDEX.md
  - recipes/creative/ecommerce-image-lookbooks/INDEX.md
quick_starts:
  - title: Compare your prices with competitors
    kind: once
    prompt: Compare our main products' prices, shipping and offers with our closest online competitors. Save the comparison to a collection called "Competitor prices" with price as a number so I can chart it.
  - title: Watch competitor prices and offers
    kind: watch
    cadence: weekly
    prompt: Set up a weekly scheduled task that checks our closest competitors' prices, offers and new products and keeps the "Competitor prices" collection current, noting the pattern behind meaningful changes. Keep what we know current by folding new results into our findings instead of piling them up, and tell me only about real changes.
  - title: Find your biggest conversion leaks
    kind: once
    prompt: Review our store's product pages and checkout as a first-time buyer would. List the most likely reasons people leave without buying, in order of likely impact, with specific fixes.
goals:
  - name: Raise the store conversion rate to 3%
    measure: Store conversion rate
    unit: percent
    direction: higher_better
    target: 3
---
This organization sells products online, directly or through marketplaces. Find out where it sells, its main products and margins, and how customers find it (search, ads, social, marketplaces, email), and remember them.

Useful attention usually goes to product pages, pricing and offers, checkout friction, repeat purchase, and the channels that actually bring buyers. Treat each platform's own analytics as the source of truth for performance numbers.
