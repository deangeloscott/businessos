# Example: Public Review to Reusable Proof and Content

A customer publicly writes: “Setup was hard, but once it was working it saved us 10 hours a week.”

1. **Customer Intelligence** captures the original public review as a SourceRecord and direct Observations.
2. `customer.analysis.sentiment-themes` can preserve the mixed experience: setup frustration plus positive realized outcome.
3. `customer.analysis.before-after-proof` extracts only the supported result and creates/updates a permission-aware ProofRecord. It does not invent a cleaner before/after story than the customer actually provided.
4. **Customer Optimization** may independently evaluate setup friction. That is a separate journey intervention if warranted.
5. `content.opportunity.signal-to-content` evaluates whether the comment/proof justifies content. If another system already requested production, it uses that WorkRequest instead of creating another Opportunity.
6. **Content Synthesis** can produce a response post, demonstration, carousel, infographic, video, or other native Asset. A proof-based carousel preserves the exact supported claim and screenshot/source restrictions.
7. **Marketing/SEO/AEO** may reuse the same ProofRecord when relevant; they do not create copied testimonial stores.

The result is one source of proof, multiple legitimate downstream uses, preserved lineage, and no duplicate research or Opportunities.
