# AURA Innovation Exchange

The Innovation Exchange is an optional portability layer for sharing organization-owned AURA process improvements. It is not required for AURA to operate and it does not create a central authority over local copies.

## No automatic sharing

AURA does not decide on its own that a process should be shared, prepare contributions in the background, or disclose organization knowledge automatically. A contribution is prepared only as part of explicit current work chosen by the user/model.

Creating a local draft is not permission to disclose it. Export, upload, publication, or other external disclosure requires explicit current-task user authorization.

A saved sharing preference is never standing permission to disclose business data.

## Detail and identity are independent

Contribution detail:
- `workflow_only` — portable process, capabilities, applicability, instructions, and verification only.
- `anonymized_evidence` — workflow plus bounded non-identifying evidence summary.
- `full_case_study` — workflow plus a user-approved bounded case-study summary.

Identity:
- `anonymous`
- `pseudonymous`
- `named`

A user may therefore share, for example, a full case study anonymously or a workflow-only contribution with named attribution.

## Privacy boundary

Export helpers never copy canonical organization state wholesale. Evidence/case-study material must be provided as a bounded contribution summary. Known secret/credential fields are rejected. Raw private customer/business state is not included by default.

Named contributions truthfully record that source-organization identity is included. Anonymous and pseudonymous contributions reject direct identifying fields from bounded evidence/case-study summaries.

## Evidence boundary

An `InnovationPackage` is evidence that someone contributed a process and, when supplied, reported outcomes. It is not proof the process works or applies to the current organization.

Import preserves the exact package as organization-local support data and creates a canonical `SourceRecord` pointing to that stored evidence. Import does **not** manufacture an `Insight`, `Learning`, confidence score, recommendation, or adoption decision.

The active model/user interprets the contribution with the rest of the organization's evidence. If that interpretation yields a durable Insight or Learning worth remembering, preserve it through the normal canonical memory primitives with appropriate evidence/provenance.

Popularity, download count, likes, contributor prestige, repeated reposts, and raw contribution counts are discovery/attention signals only. They do not establish effectiveness or semantic applicability.

## Independence and replication

Keep contributed/reported evidence, locally measured `OutcomeEvaluation`s, independent replications when actually established, contradictions, and neutral results separate. Do not convert reported aggregate counts into independent local corroboration.

`scripts/record_innovation_outcome.py` may attach an existing local `OutcomeEvaluation` to imported support state mechanically. It does not interpret that evidence into an Insight, Learning, or adoption decision.

## Optional exchange transports

The portable package format works through files alone. A user may exchange packages by local file, repository, email/file transfer, or an optional future registry/API. A hosted exchange is an optional discovery surface, never a required AURA runtime.

## Process evolution

Evidence from community contributions may inform organization-local process evolution when a capable model/user judges the evidence sufficiently strong and applicable. AURA never edits its canonical product source automatically.

Changes to the canonical AURA product remain explicit product-development work and should be supported by evidence, repository integrity/quality checks, and release validation. This is product stewardship, not an AURA execution-approval lifecycle.

## Portable exchange indexes

An `InnovationExchangeIndex` is a discovery manifest, not an authority. Any folder, Git repository, organization, or optional service can publish one. AURA may remember exchange source references, but retrieving remote material remains a host capability and importing/adopting remain explicit local actions. Index ranking/download counts never establish effectiveness.
