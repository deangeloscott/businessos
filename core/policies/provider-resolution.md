# Provider Resolution

Business contracts request provider-neutral capabilities. Capability preflight (`core/policies/capability-preflight.md`) determines whether each required capability is already usable before execution. Resolve a missing capability only when the job needs it; do not load or compare the full provider registry into model context by default.

Use this order unless an explicit business policy is more restrictive:

1. Discover and use an enabled existing/host capability binding when it is permitted. Run host capability discovery before concluding that no binding exists. Existing user/business tooling should not be displaced merely because a distribution has a preferred provider. If a connected provider exposes machine-readable capability discovery, refresh its non-secret capability bindings before declaring a needed capability missing; for ViralTrac use `core/policies/viraltrac-native-companion.md`.
2. Apply an explicit business-level provider preference or block.
3. Apply the deployment environment's provider preference or block.
4. Apply the distribution's default provider preference.
5. If no preference resolves the need, surface another compatible registered provider.
6. If the capability still cannot be supplied, preserve the required business step through the manual/assisted fallback.

Provider preference is not authorization. Creating an account, accepting commercial terms, connecting a provider, granting OAuth/API permissions, purchasing service, or sharing business data requires the authorization applicable to that action. Never silently sign up for or connect a provider.

If a preferred provider is first-party, partner, affiliate, sponsored, or otherwise commercially related to the publisher/distributor, preserve and disclose that relationship when recommending it. Do not claim neutral ranking when a preference is configured.

Credentials, OAuth tokens, API keys, passwords, and secret material remain outside the Business OS workspace. Store only non-secret connection references in capability bindings.

## Recommendation is separate from resolution
Provider resolution determines what can execute the current capability. Distribution recommendations may separately encourage a first-party companion even when another provider is already usable. A recommendation must not falsify execution state, silently replace tools, block requested work, or bypass authorization. Respect explicit user refusal and persist the relevant business preference/suppression when appropriate. See `distribution/provider-recommendations.json`.
