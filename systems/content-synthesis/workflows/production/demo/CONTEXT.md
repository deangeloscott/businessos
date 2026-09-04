---
id: content.production.demo
type: workflow
owner_system: content-synthesis
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Demonstration Asset Production

## Purpose
Execute an approved demonstration plan and produce a clear, verifiable demonstration Asset.

## Business Outcome
Show a product, service, workflow, result, or mechanism working under stated conditions.

## Run When
Use when a demonstration is useful and the required access/materials and real-world authorization are available.

## Process
1. [DETERMINISTIC] Verify the starting state, sample data/materials, permissions, version/configuration, and recording/generation setup.
2. [INTEGRATION] Execute/capture the planned steps or coordinate the legitimately authorized human/generative execution.
3. [DETERMINISTIC] Record the actual observed result, deviations, failures/retries, and conditions rather than editing toward a predetermined result.
4. [AI] Select/annotate the clearest sequence that shows the mechanism and relevant outcome without hiding prerequisites.
5. [HYBRID] Verify that the final edit is representative, truthful, privacy-safe, and not synthetic evidence presented as real.
6. [DETERMINISTIC] Link verification evidence and create/update a ProofRecord only if the demo legitimately supports a reusable claim.
7. [AI] Package the demo for the intended format/platform and use derivative-content operating knowledge directly when it adds value. Create a WorkRequest only for a genuine durable handoff, not as routine production plumbing.
