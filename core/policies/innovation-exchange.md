# BusinessOS Innovation Exchange

The Innovation Exchange is an optional portability layer for sharing BusinessOS process improvements. It is not required for BusinessOS to operate and it does not create a central authority over local copies.

## No automatic sharing

BusinessOS may notice that a process appears noteworthy and may prepare a draft contribution when configured to do so. It must never submit, upload, publish, or otherwise disclose a contribution without explicit current-task user authorization.

A saved sharing preference is not standing permission to disclose business data.

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

Export helpers never copy canonical business state wholesale. Evidence/case-study material must be provided as a bounded contribution summary. Known secret/credential fields are rejected. Raw private customer/business state is not included by default.

## Evidence boundary

An InnovationPackage is evidence that someone contributed a process and, when supplied, reported outcomes. It is not proof the process works.

Popularity, download count, likes, contributor prestige, and repeated reposts are attention signals only. Imported contributions enter the normal Ecosystem Intelligence path:
`InnovationPackage -> SourceRecord -> candidate Insight -> triangulation -> ignore/watch/investigate/test/adopt`.

## Independence and replication

Community evidence must keep contributed/reported evidence, locally measured OutcomeEvaluations, independent replications when actually established, contradictions, and neutral results separate. Do not convert reported aggregate counts into independent local corroboration.

## Optional exchange transports

The portable package format works through files alone. A user may exchange packages by local file, repository, email/file transfer, or an optional future registry/API. A hosted exchange is an optional provider/discovery surface, never a required BusinessOS runtime.

## Canonical promotion

Strong community evidence may create a PlaybookEvolutionProposal. It never edits canonical BusinessOS automatically. Canonical promotion remains explicit system-development work with evidence review, approval, regression tests, and release validation.

## Portable exchange indexes

An `InnovationExchangeIndex` is a discovery manifest, not an authority. Any folder, Git repository, organization, or optional service can publish one. BusinessOS may configure exchange source references, but retrieving remote material remains a host capability and importing/adopting remain explicit local actions. Index ranking/download counts never establish effectiveness.
