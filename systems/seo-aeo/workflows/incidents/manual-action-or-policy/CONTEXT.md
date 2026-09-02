---
id: seo.incidents.manual-action-or-policy
type: incident
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- Incident
---
# Manual Action / Policy Incident

## Purpose
Handle search/platform policy notices or credible evidence of a policy-related visibility problem with evidence-backed remediation, without making AURA the authority that pauses or resumes runtime behavior.

## Business Outcome
Resolve legitimate policy-related visibility problems quickly and completely while preserving the evidence, organizational decisions, remediation history, and reusable learning future work needs.

## Run When
Use when a platform notice or credible evidence indicates a material policy/manual-action problem that could affect search visibility or eligibility.

## Process
1. [HYBRID] Capture the exact notice/source, affected property/scope, cited behavior, dates, and current tactics/implementations that may relate.
2. [AI] Identify potentially implicated tactics or implementations and recommend pausing/removing them when the evidence and real policy risk justify it. AURA records the rationale/context; the active user/harness owns any actual operational change.
3. [AI] Audit affected patterns against current official policy and classify confirmed violation, possible issue, unrelated issue, or unknown at the confidence the evidence supports.
4. [HYBRID] Remediate confirmed/problematic implementation comprehensively rather than hiding it, creating circumvention, or changing unrelated work.
5. [HYBRID] Verify remediation across the affected templates/content/links/data and prepare any required reconsideration/appeal information through the platform's actual process.
6. [AI] Preserve the Incident result and update reusable tactic/Learning guidance only when evidence supports a broader lesson. Use qualified legal/compliance or organizational review when the real situation requires it; AURA does not impose a generic approval gate or background recovery monitor.

## Verification
- Material policy claims are grounded in current authoritative platform evidence.
- Recommended containment and actions actually executed remain distinct.
- Remediation does not depend on evasion/circumvention.
- Incident state preserves organizational continuity without controlling the active runtime.

## Completion Criteria
- The organization understands the policy issue, affected scope, remediation status, evidence, and remaining uncertainty, and any real platform process has been handled by the appropriate actor/tool without an AURA-owned autonomy or approval lifecycle.
