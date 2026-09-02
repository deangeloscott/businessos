---
id: seo.execution.aeo.factual-accuracy
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
- prompt/question observations, answer text, citations, mentions, and competing sources
---
# AI Factual Accuracy

## Purpose
Detect high-value incorrect, outdated, or ambiguous claims about the brand and route corrections to authoritative information sources.

## Business Outcome
Improve valuable organic discovery through ai factual accuracy, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **AI Factual Accuracy**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Extract factual claims about the owned brand/products/services/locations from Answer Observations.
2. [HYBRID] Compare each claim with canonical Brand Context and authoritative owned/third-party evidence.
3. [AI] Classify correct, partially correct, outdated, unsupported, ambiguous, or materially false; assess customer/business impact.
4. [AI] Trace cited/likely source pathways where observable and identify conflicting owned information that may contribute.
5. [HYBRID] Create corrective actions: update canonical site facts, profiles, structured information, documentation, third-party profiles, or outreach where legitimate.
6. [HYBRID] Re-observe after source changes; preserve uncertainty because answer generation may remain nondeterministic.


