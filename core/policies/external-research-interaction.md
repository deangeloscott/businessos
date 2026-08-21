# External Research Interaction

Use public and legitimately accessible third-party experiences as a truthful researcher/prospect. Do not fabricate identity, company facts, purchase intent, authority, or eligibility to unlock information.

Follow `core/policies/context-reuse-and-question-minimization.md`: check durable context before asking and persist reusable answers at the narrowest correct scope so the user is not repeatedly asked for the same information.

## Identity and form fields
1. When interaction requires only navigation, no identity data is needed.
2. Before asking for or submitting identity/contact/business facts, resolve the effective research profile. Business-specific values in `instances/<business-id>/config/external-research-profile.json` win. When `inherit_operator_profile=true`, reusable fields from `deployment/operator-profile.json` may fill otherwise-missing operator identity fields. Current Business Context may supply truthful business facts.
3. If a required field is still unknown, do not invent a plausible value. Ask the user only when the downstream evidence is valuable enough to justify interruption; otherwise record the blocked/unknown branch.
4. When the user supplies a durable missing value, persist it using `scripts/update_research_profile.py` unless they say it is one-time only. Default ambiguous contact/business details to the active business. Use operator scope only when the value clearly belongs to the recurring human/operator and may be reused across brands.
5. Never use another person's identity, fake company/employment facts, fake purchasing authority, or deceptive buying intent.

## Interaction thresholds
- Actions listed as allowed in the active business research profile may proceed within the active autonomy/risk policy.
- Actions listed as requiring approval must pause for authorization before submission.
- Prohibited actions remain prohibited even if technically possible.
- A public/free trial may still require approval when it creates an account, accepts material terms, triggers sales contact, or creates external obligations.

## Funnel boundaries
Stop at private/authenticated/restricted boundaries that are not legitimately available to the research identity. Never bypass access controls. Preserve the last observed state, mark downstream steps unknown, and continue with other evidence.

## Email/follow-up
Read only follow-up that was legitimately received in an authorized mailbox/research inbox. Preserve source/time/sequence and do not infer messages that were not received.

## Recordkeeping
Preserve what was submitted, why it was allowed, the observed response/redirect, and any approval or blocker needed to reproduce the research without misrepresenting the interaction.
