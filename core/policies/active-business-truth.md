# Active-Business Truth & Artifact Policy

BusinessOS must preserve the truth boundary in **every output that describes, operates, markets, or represents the active business**, not only in canonical JSON. A non-canonical artifact is not a loophole for unsupported business claims.

## Scope
This policy applies to canonical objects, Markdown, plans, recommendations, user-facing answers, code, webpages, landing pages, ads, emails, scripts, briefs, generated assets, tool inputs, and other active-business artifacts.

## Truth classes
- **Business fact:** explicit authorized user/first-party information or verified governed business-system truth.
- **External evidence:** sourced information about markets, competitors, customers, industry conditions, benchmarks, regulations, or other external entities.
- **Inference / hypothesis:** reasoned interpretation that may guide investigation or testing but is not established active-business truth.
- **Unknown business state:** an active-business fact that has not been established.

## Required behavior
1. Do not state an inference, external pattern, or convenient placeholder as an established fact about the active business. **Necessary/strongly entailed implications may be used operationally as derived reasoning when they genuinely follow from established facts, but they remain derived rather than `explicit_user` truth and may not add unsupported specifics.** Example: if Google Ads currently generates leads, it is reasonable to infer that some Google Ads activity/spend exists; the amount, efficiency, budget, campaign structure, CAC, or profitability remain unknown.
2. **Unknown is not absent.** “Not supplied,” “not discovered,” “not connected,” or “search returned no result” does not establish that a website, profile, offer, service, team, customer base, capability, or other asset does not exist. Record it as unknown/unverified unless absence is authoritatively established.
3. Conservative semantic normalization is allowed when it preserves meaning; material expansion is not. For example, “installing, repairing, and maintaining residential heating and cooling systems” may normalize to installation/repair/maintenance services, but it does not establish boilers, duct cleaning, indoor-air-quality products, 24/7 service, financing, guarantees, or additional geography.
4. External competitor/industry patterns may be used as labeled evidence or hypotheses (for example, “competitors commonly advertise emergency service; evaluate whether Northstar should offer it”). They must not become first-person/business claims (for example, “our 24/7 emergency team”) without business-specific support.
5. Do not invent business commitments or representations such as service availability, hours, response times, prices, discounts, financing, warranties, guarantees, certifications, locations, testimonials, values, positioning, customer promises, ownership structure, or performance claims.
6. If a draft/template is useful before facts are known, use explicit placeholders such as `[confirm service hours]` or clearly labeled hypothetical alternatives. Do not create realistic-looking unsupported claims that could be mistaken for approved business truth.
7. A fictional/test business is still governed by the same rules. “Fictional” does not mean “has no assets,” nor does it authorize the agent to invent them.
8. Before writing or presenting a business-facing artifact, verify that every material business-specific assertion is either supported, explicitly labeled provisional/hypothetical, or left unknown.
9. Keep a market/customer/competitor **opportunity** separate from an active-business **promise or commitment**. External evidence may justify investigating a service level, offer, position, guarantee, or operating change; it does not establish that the business can or should promise it. Verify capability/feasibility and follow normal authorization before turning an opportunity into a public claim or operational commitment.
10. Canonical decision state has the same truth boundary. A verified Observation does not establish every economic, causal, ranking, traffic, lead, conversion, or AI-answer consequence inferred from it. Qualified/prioritized Opportunities must follow `core/policies/decision-grounding.md` and explicitly separate established basis, measured outcomes, derived inferences, and unknowns.
11. A generation constraint is not automatically a business promise. For example, “do not use pressure tactics in this asset” constrains the draft; it does not establish the public claim “we are a no-pressure company.” Likewise, “provide written estimates” does not authorize enlarging the promise to separate estimates for every possible option unless that commitment is established. Preserve reusable explicit promises/constraints as `BusinessClaim` objects and follow `core/policies/context-provenance-and-claims.md`.

12. Existing customer-facing assets are not a claim-governance loophole. Any workflow that mutates customer-facing copy must preserve the before state and validate newly introduced claim candidates under `core/policies/customer-facing-mutations.md`. A technical/CRO/SEO edit may remove an unsupported element, but it may not rewrite it into an unsupported service/capability CTA.

## Execution boundary
A request to analyze, diagnose, prioritize, or **determine what to do next** authorizes that decision work; it does not by itself authorize implementation of the recommended intervention. Creating/deploying business-facing assets, changing external systems, making commitments, or adopting new business facts requires the ordinary action/autonomy/approval path and must remain within the user's requested scope.
