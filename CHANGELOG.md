# Changelog

## 0.1.3 — Alpha

This release moves AURA from architecture closure into evidence-backed Alpha use. The product architecture remains centered on organization-owned memory and reusable operating knowledge for capable AI; the work since v0.1.2 focused on proving that architecture with real business work, fixing defects exposed by that proof, and removing qualification machinery that no longer served the product.

### What changed

- Established a maintainer-only library of **57 realistic business-use cases** across **5 industries** and all **8 operating areas**. The library uses ordinary requests plus separate hidden judge guidance and is intentionally excluded from user distributions.
- Completed a representative **10-case real-work campaign**, with all **10 selected cases ultimately qualifying** after product, harness, and evaluator defects were diagnosed and corrected. This is representative evidence; it does **not** mean all 57 library cases were executed.
- Proved longitudinal continuity across fresh model contexts and later contradictory/new evidence: useful organization state carried forward and prior understanding was revised when better evidence arrived.
- Fixed a real AURA external-workspace/local-evidence defect exposed by qualification, preserving the boundary between mutable organization state and immutable product source.
- Hardened qualification observation and isolation by pinning the intended workspace, capturing the candidate-visible result as legitimate review evidence, isolating judging to the exact run, correcting duplicate detection for evolving shared artifacts, and strengthening claim-grounding review.
- Simplified qualification from first principles: removed the generated all-Workflow suite, synthetic missions/cases, semantic rubric profiles, exhaustive Playbook-coverage obligation, duplicate candidate launcher, and duplicate recovery program.
- Reduced qualification to two task modes: **real-world use cases** for primary product proof and **focused Workflow diagnostics** only when evidence points to one specific body of operating knowledge.
- Kept provider/model/harness process failures classified as execution interruptions rather than automatically turning them into AURA semantic blockers.
- Corrected the release entry point so public releases are built from the curated **full AURA edition** rather than archiving the maintainer checkout. The release builder now strips qualification/developer state, reruns source gates, validates the fresh ZIP, and smoke-tests a separate organization workspace.

### Validation

The current v0.1.3 release baseline has demonstrated:

- **466 authored Workflows** and **42 Playbooks** generated and validated with **0 errors and 0 warnings**;
- **34/34 AURA product-integrity suites**;
- **4/4 qualification-harness self-test suites**;
- a **57-case** realistic qualification library spanning 5 industries and 8 operating areas;
- a representative **10/10 qualified** real-work campaign, including longitudinal memory/evidence evolution.

The release packaging command reruns both source gates and then validates the freshly unpacked curated distribution before publication.

### Current status

AURA's first-principles architecture, source coherence, deterministic integrity, representative real-work proof, longitudinal continuity proof, and qualification simplification are now closed to a strong Alpha standard. The next phase is normal Alpha use: put AURA in real hands, observe what happens over time, and change the product only when real evidence exposes a reusable weakness that matters to users.

Alpha still means interfaces and Playbooks/Workflows may change before 1.0 when real usage earns those changes.

## 0.1.2 — Alpha

This release is the validated architecture-closure baseline for the first-principles AURA refactor. It makes the simplified AURA model the canonical product on `main`: organization-owned memory and reusable operating knowledge for capable AI, without recreating a hidden execution control plane around the model.

### What changed

- Standardized operating knowledge around the simple **Playbook → Workflow → Step** hierarchy and retired Contract-era execution semantics.
- Removed the remaining capability-ontology, routing, provider-resolution, approval, mandatory lifecycle, composition-graph, and internal handoff residue that did not belong in AURA.
- Kept reasoning, planning, tool choice, providers, orchestration, scheduling, retries, concurrency, and execution mechanics with the active model/harness.
- Tightened the canonical organization-memory boundary to **39 organization-owned object types**, with support/interface records kept outside canonical memory and reference traversal.
- Simplified durable memory semantics around facts, evidence, observations, Insights, decisions, Opportunities, Assets, measurements, outcomes, Learning, preferences, and genuine continuity.
- Removed generic semantic confidence/priority scoring where it invented precision instead of preserving evidence and uncertainty honestly.
- Simplified organization-local operating knowledge and Innovation Exchange around direct Workflow identity and Learning provenance without proposal/runtime bureaucracy.
- Cleaned component packaging so each edition ships only the operating knowledge, schemas, navigation, and user-facing documentation it actually contains.
- Regenerated the human-facing Playbook and Workflow navigation from the final authored source.
- Preserved the detailed refactor history with the `aura-architecture-closure-c233a55` tag while squashing the completed architecture update into one coherent `main` commit.

### Validation

The v0.1.2 architecture-closure baseline passed from a clean committed checkout:

- **466 authored Workflows** and **42 Playbooks** generated and validated with **0 errors and 0 warnings**;
- **34/34 AURA product-integrity suites**;
- **4/4 qualification-harness self-test suites**;
- full-distribution validation plus all **9 named component editions**;
- deterministic regeneration with a clean working tree afterward.

### Current status

AURA is ready for real users and capable AI systems to use and test as an **Alpha** product. The architecture and deterministic integrity layer are validated. The next phase is real-work product proof: whether AURA consistently improves useful business work, memory, retrieval, continuity, Learning, and later work because the organization remembers what matters.

Alpha still means interfaces and Playbooks/Workflows may change before 1.0 when real usage exposes genuine weaknesses.

## 0.1.1 — Alpha

This release closes the first-principles AURA architecture refactor and establishes the new validated Alpha baseline for real-world use and qualification.

### What changed

- Completed the first-principles simplification around **organization-owned memory + reusable operating knowledge + lightweight continuity**.
- Removed remaining legacy BusinessOS control-plane residue from authored playbooks, including runtime-event emission, internal routing/delegation, fake handoff state, and mandatory execution-lifecycle assumptions.
- Kept useful business methods while moving semantic judgment back to the capable model and execution mechanics back to the active harness/runtime.
- Simplified durable memory around direct create/update/correct/forget behavior and preserved optional one-way Run receipts only when continuity is useful.
- Strengthened organization truth, evidence provenance, unknown-vs-absent handling, customer-facing claim manifests, and organization isolation.
- Improved playbook discovery without making AURA a semantic router; candidate discovery remains bounded and model selection remains authoritative.
- Restored useful domain expertise that had been over-pruned, including contextual organic competition guidance.
- Aligned Innovation Exchange version metadata with AURA terminology and removed remaining legacy package-field mismatch.
- Removed stale qualification/test assumptions that would have recreated retired architecture, while keeping tests strict about real product invariants.
- Validated all named component distributions against the same current AURA Core and provider-neutral capability model.

### Validation

The v0.1.1 release candidate passed:

- workspace validation for **496 contracts** with **0 errors and 0 warnings**;
- **37/37 AURA product-integrity suites**;
- **4/4 qualification-harness self-test suites**;
- full/component distribution validation across current named editions.

### Current status

AURA is ready for real users and capable AI systems to use and test as an **Alpha** product. The architecture and deterministic integrity layer are validated. The next qualification phase focuses on real-work quality: whether AURA consistently improves useful business work, retrieval, continuity, Learning, and later work because the organization remembers what matters.

Alpha still means interfaces and playbooks may change before 1.0 as real usage exposes genuine weaknesses.

## 0.1.0 — Alpha

This release resets ViralTrac AURA to an honest pre-1.0 version after the first-principles architecture audit.

### What changed

- Reframed AURA around **organizational memory + operational knowledge + lightweight continuity**.
- Removed generic approval, ActionPacket, autonomy/risk-tier, provider-resolution, capability-binding, scheduler/event-runtime, and universal execution-control machinery.
- Kept AURA strict about organizational truth, evidence, provenance, business isolation, useful continuity, measurement, and Learning.
- Made Runs optional work receipts rather than a universal execution requirement.
- Kept model/harness reasoning, tools, browsing, APIs, subagents, scheduling, retries, credentials, rendering, and provider choice outside AURA.
- Simplified the front door so ordinary requests retrieve relevant organizational context and may surface a useful AURA playbook without forcing execution through it.
- Preserved component editions as the same current AURA Core plus selected domain operating knowledge.
- Separated AURA product-integrity tests from maintainer-only qualification-harness self-tests.
- Realigned qualification around one question: does AURA help capable intelligence produce truthful, professionally useful real business work?
- Removed obsolete release/test artifacts that no longer protected a real AURA invariant.

### Current status

AURA is **alpha software**. The product-integrity architecture is validated, but real-work quality, playbook/SOP excellence, retrieval, Learning, and usability are still being actively qualified and may change before 1.0.

### Version history note

Earlier `1.x` tags were pre-alpha development snapshots created before the product maturity model was corrected. They should not be interpreted as stable predecessors to a future `1.0` release. Git history remains the source of truth for those development changes.
