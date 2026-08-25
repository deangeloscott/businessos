# Evidence Policy

Separate direct observations from interpretations. Evidence links may support, contradict, contextualize, extend, or derive. Evidence strength, conclusion confidence, policy status, and risk are distinct concepts.

## Claim classes
Keep these states explicit when they matter to a decision:
- **Business fact:** authorized first-party/user information or verified business-system truth about the active business.
- **External evidence:** sourced facts about markets, competitors, customers, industry conditions, regulations, benchmarks, or other external entities.
- **Inference / hypothesis:** a reasoned interpretation that may guide investigation or testing but is not established business truth.
- **Unknown business state:** a material fact about the active business that has not been established.

External evidence may inform a hypothesis about the active business, but it does not silently become a fact about that business. Apply `core/policies/active-business-truth.md` to every business-facing artifact/answer, not only canonical objects. A missing or undiscovered active-business fact remains unknown; failure to find evidence is not proof of absence unless the source/method can authoritatively establish absence.

## Claim calibration
- Do not convert external benchmarks into business-specific forecasts unless the required business-specific inputs and causal assumptions are supported.
- Do not manufacture numeric precision. Use qualitative direction, ranges, scenarios, or "unknown" when that is what the evidence supports.
- A recommendation may still be made under uncertainty when its rationale and unresolved assumptions are explicit.
- If a missing business-specific fact is likely to reverse prioritization, treat resolving that fact as decision-critical evidence rather than substituting generic market research.

## Research preservation
When external research creates SourceRecords, Observations, or supported Insights, also follow `core/policies/research-evidence.md`. A search result or URL is discovery, not sufficient preserved evidence for a material supported claim.

