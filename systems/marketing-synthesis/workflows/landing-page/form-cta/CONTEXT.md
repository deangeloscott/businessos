---
id: marketing.landing-page.form-cta
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Landing Page Form and CTA Persuasion Requirements

## Purpose
Define what information and expectation-setting should surround the conversion action while distinguishing persuasion from real journey mechanics.

## Business Outcome
Improve qualified completion without collecting unnecessary information or hiding next-step consequences.

## Run When
Use when a landing page includes a form, booking, checkout handoff, trial, application, or other conversion action.

## Process
1. [AI] Define the purpose of the action, minimum qualification needed before action, and what the visitor must know first.
2. [AI] Specify CTA wording, expectation/next-step copy, trust/privacy reassurance, required qualification questions, and optional fields from a persuasion perspective.
3. [HYBRID] Challenge every requested field: keep only what is operationally/qualification-required before conversion.
4. [HYBRID] Identify friction or technical issues that cannot be fixed with copy and use relevant Customer Optimization/technical operating knowledge directly to solve or specify the real change. Persist a WorkRequest only when a separate executor needs a durable handoff.
5. [HYBRID] Define useful tracking events, success/failure states, consent requirements, and error/confirmation content needs based on the real conversion flow.
6. [AI] Ensure form/CTA message matches the actual downstream process and Offer.
7. [HYBRID] Preserve the useful form/CTA requirements as an Asset and verify implemented fields/copy against them when the implemented surface is available.
