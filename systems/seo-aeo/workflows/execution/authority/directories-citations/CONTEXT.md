---
id: seo.execution.authority.directories-citations
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- location/profile data, local-result observations, and local competitors
- backlink/referring-domain/mention evidence and prospect records
---
# Directories & Citations

## Purpose
Create, correct, or retire legitimate business listings and citations where accurate presence materially helps users, entity verification, local discovery, or industry discovery.

## Business Outcome
Strengthen discoverability and trust through useful third-party business references rather than maximizing citation counts or domain metrics.

## Run When
Use when the organization needs relevant directory/citation coverage, conflicting business identity data needs correction, or local/industry evidence suggests an important legitimate source is missing or wrong.

## Process
1. [AI] Identify sources that matter to the actual business and market: major data/listing ecosystems, industry directories, local chambers or associations, government/community resources, neighborhood resources, and other legitimate directories used by the target audience. Context determines relevance; do not pursue every available listing.
2. [HYBRID] Prioritize by legitimacy, audience utility, geographic/industry relevance, data-ecosystem importance, business fit, and expected value—not raw domain metrics or citation count. A local source may be highly valuable even when it is not globally prominent.
3. [AI] Distinguish a true listing/citation task from another authority mechanism. A supplier/partner relationship, sponsorship, expert contribution, news opportunity, resource-page inclusion, or earned editorial mention may call for the relevant Authority Workflow rather than being forced into directory submission.
4. [HYBRID] Establish the canonical business identity and intended destination URL from organization truth before changing third-party data. Resolve material NAP/entity/category/service inconsistencies without inventing unsupported fields.
5. [HYBRID] Claim, submit, correct, or remove listings through the real channels available under the user's request and provider rules. Keep credentials/ownership secrets outside public AURA artifacts.
6. [HYBRID] Verify the published state and important identity/destination fields. Preserve material ownership/source context when it will help future correction or relocation work.
7. [AI] Evaluate value through useful evidence such as referral traffic/leads, local visibility, entity consistency, customer utility, or relevant authority effects rather than citation volume alone. If future drift matters, preserve monitoring intent; the harness owns recurrence.

## Verification
- Every material listing field is grounded in current business truth.
- Sources are selected for real audience/ecosystem relevance rather than availability alone.
- Different authority mechanisms are not collapsed into directory submissions.
- Publication or correction is verified from the external source where practical.
