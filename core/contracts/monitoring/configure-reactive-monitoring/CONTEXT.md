---
id: core.monitoring.configure-reactive-monitoring
type: playbook
version: 1.8.1
owner_system: core
reads:
- Business
- SourceRecord
writes:
- SourceRecord
capabilities:
  required:
  - none
  optional:
  - business.event.catalog.read
  - business.event.coverage.read
  - business.event.readiness.read
  - business.event.subscription.manage
  - business.event.evaluate.preview
  - business.event.delivery.receive
  - business.event.subscribe
context:
- Business
---
# Configure Reactive Monitoring

## Purpose
Prepare an active business to use a governed event/reaction plane for continuous BusinessOS evaluation without making live event delivery a hidden dependency.

## Business Outcome
Use trustworthy first-party changes as timely BusinessOS triggers when the provider and host can support them, while automatically retaining polling/scheduled/manual monitoring when they cannot.

## Run When
When a connected provider exposes an event plane, when its readiness/operational mode changes, when a host gains or loses an event-delivery mechanism, or when the user asks for continuous/proactive monitoring.

## Process
1. [DETERMINISTIC] Load `instances/<business-id>/config/reactive-monitoring.json`, current capability bindings, installed modules, and the generic BusinessOS event consumer profile; reuse current valid setup rather than recreating subscriptions.
2. [INTEGRATION] Discover the provider's current event catalog, coverage, consumer capabilities/managed recipes, readiness, and operational mode. For ViralTrac, use the ViralTrac Event / Reactive Plane surfaces described in `core/providers/viraltrac/event-interoperability.json`; route presence or repository capability alone is not runtime readiness.
3. [DETERMINISTIC] Determine whether the host/harness has a compatible delivery mechanism (`business.event.delivery.receive`) and whether the provider supports an authorized subscription/handoff. Never invent a webhook URL, credential, callback, scheduler, or public endpoint merely to make reactive mode appear available.
4. [HYBRID] Select the smallest useful event families from `core/monitoring/event-consumer-profile.json` based on installed modules, active objectives/initiatives, event-catalog semantics, likely materiality, and the business's allow/block preferences. Do not subscribe BusinessOS to raw high-volume firehoses when aggregate/provider-native consumers already own routine handling.
5. [INTEGRATION] Where available, run dry-run evaluation/recipe preview to confirm expected projections, eligibility, fan-out, policy decisions, conflicts, cost, and side-effect posture. Preserve reason codes and do not treat preview as delivery, action, exposure, or outcome.
6. [HYBRID] Apply provider operational mode: `off`/`publish_shadow` => keep fallback; `evaluate_shadow` => evaluation-only reactive use when deliverable, never event-triggered external effects; `allowlisted_actions` => only separately eligible allowlisted effects; `broad` => normal governed reactive evaluation; `degraded` => preserve critical evaluation and fall back for optional work. Equivalent non-ViralTrac modes should be mapped conservatively.
7. [INTEGRATION] Only after current readiness plus delivery checks pass and authorization exists, create/reconcile the provider subscription/managed binding and mark `business.event.subscribe` active for the environment. Otherwise persist a reason-coded fallback state and use scheduled/polling/manual monitoring.
8. [DETERMINISTIC] Update the business reactive-monitoring profile with status, provider/subscription reference, selected families, and configuration time; persist a SourceRecord for authoritative readiness/coverage evidence without copying raw provider event history.
9. [DETERMINISTIC] Re-run capability preflight and a synthetic/dry-run event where supported. Confirm that an eligible event reaches `core.monitoring.react-to-business-event`, while an ineligible or duplicate event cannot create a duplicate externally visible effect.

## Verification
Reactive monitoring is either demonstrably ready with a compatible provider/host delivery path and bounded event families, or explicitly in fallback/degraded state; no route presence, shadow mode, or missing delivery mechanism is misrepresented as live continuous operation.
