# Content Synthesis

Turn validated ideas and signals into communication that is native to the audience, platform, medium, and consumption context.

## Common jobs
- Find trending/strong content patterns → `contracts/intelligence/`
- Monitor creators / validate a trend → `content.intelligence.creator-monitoring` / `content.intelligence.trend-validation`
- Turn a comment, proof item, news Insight, search signal, or other intelligence into content → `content.opportunity.signal-to-content`
- Choose platform/format → `content.strategy.format-platform`
- Refresh current platform behavior → `content.strategy.platform-profile-refresh`
- Adapt one idea natively → `content.adaptation.platform-native`
- Produce article/video/carousel/infographic/GIF/image/podcast/avatar video/etc. → `contracts/production/`
- Create useful derivative scripts/clips/captions/thumbnails → `content.production.derivative-package`
- QA/fact/brand → `contracts/qa/`
- Publish/schedule approved Assets → `content.publishing.publish-asset`

## Boundary
Content Intelligence studies creative mechanisms and audience communication behavior. Customer, competitor, industry, SEO, offer, and journey truth remain with their canonical owners. A WorkRequest from another system is delegated execution, not a new Content Opportunity.

## AI execution
Do not load this entire system. Route to one atomic contract and use the root Context Planner.

## Complete process map
`process-map.json` lists the common important activities this system claims to perform. Use `python scripts/process_plan.py --system content-synthesis --activity <activity-id>` to expand a composite activity into its required and conditional sub-processes.
