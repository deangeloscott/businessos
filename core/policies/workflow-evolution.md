# AURA Workflow Evolution

AURA may improve reusable operating knowledge from real organizational Learning without turning internal product maintenance into customer bureaucracy.

## Canonical rule

A `Learning` is durable business memory. A `ProcessExtension` is durable business-scoped reusable operating knowledge.

Neither requires an internal proposal, review, adoption, or product-version compatibility lifecycle.

A ProcessExtension has one Workflow relationship:

- an installed AURA `workflow_id` means the ProcessExtension augments that Workflow; or
- an organization-local `custom.*` `workflow_id` defines a local Workflow.

The Workflow relationship is for retrieval and composition of knowledge. It is not an execution contract, and no separate `mode` field is needed to restate what the identifier already tells us.

## What a ProcessExtension should contain

Preserve only the reusable meaning that helps future work:

- what the procedure is for;
- when it applies and does not apply;
- the few instructions that materially improve the work;
- optional verification guidance when it is genuinely useful;
- discoverability terms;
- scope when narrower than the whole business;
- provenance to organization Learning, sources, or evidence when those exist.

Do not copy AURA Workflow metadata such as `reads` / `writes`, product-system ownership, host capabilities, provider bindings, schedules, permissions, or AURA version gates into ProcessExtension state. Those do not become organization-owned operating knowledge merely because a procedure mentions them.

## Organization-authored procedures

A user/model may intentionally persist a local Workflow or Workflow augmentation directly from explicit organizational instruction. Do not fabricate Learning, a proposal, an approval record, a source classification label, or a fake source reference first.

## Learning-derived improvements

When existing canonical Learning supports a reusable procedural improvement, the active model/user may create or update a ProcessExtension directly. Preserve the relevant Learning/evidence references so the improvement remains traceable. The presence of `source_learning_refs` already records that provenance; no separate source-kind classification is required.

## Canonical AURA source changes

Editing packaged AURA Playbooks, Workflows, schemas, policies, or scripts is product maintenance outside the active business knowledge lifecycle. Business Learning may inform that work, but a ProcessExtension never mutates product source.

## Sharing

Innovation Exchange packages may carry ProcessExtension operating knowledge and bounded supporting evidence. Importing a package records contributed material as support evidence; it does not make the method true, compatible, adopted, or authoritative for the recipient organization.

Package `format_version` exists only so the portable file can be parsed correctly. AURA product versions are not compatibility gates for reusable operating knowledge.
