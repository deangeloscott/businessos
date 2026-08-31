# Autonomy Policy

Autonomy describes the level of action authority that the user, organization, account/platform, law, or another real governing source has actually granted for the work. AURA records and applies that authority; it does not invent a separate permission regime merely because a task appears risky or consequential.

The existing tiers remain useful descriptive labels: 0 Observe, 1 Recommend, 2 Prepare, 3 Execute with bounded write authority, 4 Autonomous within explicit policy. Use them to represent known authority and execution scope when that representation helps continuity or enforcement.

For a proposed Action:

- preserve explicit user/organization permissions, prohibitions, approval requirements, spending limits, account/platform restrictions, legal/compliance constraints, and the original requested scope;
- distinguish a preference or risk tolerance from actual authorization;
- do not raise authority because a tool is capable of acting;
- do not lower authority solely because AURA independently prefers a more conservative business choice;
- when several real authority sources apply, respect the most restrictive applicable boundary;
- if authorization is genuinely unknown and an external/business-facing mutation would exceed the already granted scope, preserve the uncertainty and obtain the smallest necessary approval rather than treating silence as permission.

AURA may help the model/human reason about risk and reversibility, but semantic business risk judgment is not itself a substitute for an organization-defined authorization rule.
