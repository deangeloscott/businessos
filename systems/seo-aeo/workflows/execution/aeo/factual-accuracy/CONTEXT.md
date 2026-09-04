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
Detect important incorrect, outdated, unsupported, or ambiguous claims about the organization in answer systems and identify the authoritative information that may need correction.

## Business Outcome
Reduce materially harmful answer-system misinformation while preserving uncertainty about why a model produced a claim and whether source changes will alter future answers.

## Run When
Use when current Answer Observations contain claims about the organization that may conflict with canonical business truth or materially affect customer decisions.

## Process
1. Extract the factual claims about the owned brand, products, services, locations, terms, or other business facts that materially matter to the question.
2. Compare each claim with canonical organizational context and the strongest relevant owned or authoritative third-party evidence.
3. Classify the claim as correct, partially correct, outdated, unsupported, ambiguous, materially false, or unresolved; assess customer/business impact separately from factual status.
4. Trace cited or plausible source pathways only where observable and useful, and identify conflicting owned information that may contribute without pretending to know the model’s hidden causal path.
5. Correct established owned facts, profiles, structured information, documentation, or legitimate third-party records when the current task and real permissions allow it. Use the appropriate host tools/operating knowledge directly; do not create an internal correction-routing object by default.
6. Re-observe when doing so can materially verify the result, while preserving the fact that generated answers may remain non-deterministic and source changes do not guarantee correction.

## Proportionate Scope
Prioritize errors that are consequential, repeated, high-confidence, or visible in important customer decisions. Do not launch broad reputation/source remediation for trivial wording differences or one unstable answer sample.

## Verification
- Canonical business truth and external answer claims remain separately represented.
- Corrections do not invent or broaden organizational facts merely to influence answer systems.
- Source changes and later answer changes are recorded as separate evidence; causality is not assumed.
