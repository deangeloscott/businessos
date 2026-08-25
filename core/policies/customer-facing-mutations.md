# Customer-Facing Mutation Claim Safety

BusinessOS claim governance applies when an existing customer-facing surface is **modified**, not only when Content or Marketing creates a new Asset. SEO, Customer Optimization, Core, or any other workflow must not introduce a new active-business claim merely because the primary task is technical, structural, CRO, or operational.

## Invariant
A mutation of an existing customer-facing file may preserve existing text, remove unsupported material, or add text that is already authorized by canonical business truth. It may not introduce a new advertised service, capability, promise, guarantee, credential, price, offer, availability statement, or other business-specific predicate without substantive support.

A broken/unsupported service link is not permission to rewrite it into a new public capability. For example, if `maintenance` is not an established ProductService/approved BusinessClaim, fixing `/services/maintenance.html` by writing `Contact us about maintenance` is still an unsupported business representation. Remove/narrow the unsupported element instead, or obtain authorization.

## Required local-file path
For governed mutations of customer-facing `.html`, `.htm`, `.md`, or `.txt` surfaces:

1. **Before the edit**, capture the target surface with:
   `python scripts/capture_customer_facing_state.py <business-id> <surface-root-or-file> --output <before.json>`
2. Perform only the authorized mutation.
3. **After the edit**, build the deterministic claim delta with:
   `python scripts/build_mutation_claim_manifest.py <business-id> <before.json> <surface-root-or-file> --output <claim-delta.json>`
4. The delta contains only **newly introduced customer-facing claim candidates**. Classify each introduced candidate using the same classes/support rules as `core/policies/context-provenance-and-claims.md`:
   - `approved_business_claim` + substantively supporting trusted canonical refs,
   - `general_guidance`, only when it is genuinely not a business-specific/promise-like statement,
   - `placeholder`, visibly marked as a placeholder.
5. Reference the before capture and claim delta from the resulting `ChangeEvent`:

```json
{
  "extensions": {
    "businessos": {
      "customer_facing_mutations": [
        {
          "surface_root": "path/to/customer-facing-surface",
          "before_capture": "runtime/.../before-customer-facing.json",
          "claim_delta": "runtime/.../customer-facing-claim-delta.json"
        }
      ]
    }
  }
}
```

6. `validate_business.py` reproduces the before/after delta, verifies that all changed customer-facing files are represented in `ChangeEvent.target_refs`, and rejects missing/unclassified/unsupported introduced claims.

## Scope behavior
- Unchanged pre-existing customer-facing claims are not re-authorized by this control; the validator focuses on claims introduced by the current mutation.
- Removing an unsupported claim/link is allowed and creates no new claim obligation.
- Adding a new customer-facing file is a mutation. Its business-specific candidates are all treated as newly introduced claims.
- A customer-facing `ChangeEvent` may not opt out with `customer_facing: false`.
- For external CMS/platform mutations where the final surface is not locally readable, preserve an equivalent before-state capture and a post-change readable/exported artifact before claiming verification/completion. Do not use inability to inspect the final surface as permission to skip claim governance.

## Relationship to other controls
- `context-provenance-and-claims.md` governs what customer-facing predicates are authorized.
- This policy governs the **before → after mutation boundary** and reuses the same substantive support checks.
- `active-business-truth.md` remains the general truth invariant.
- `change-control.md` and `verification.md` still govern authorization, rollback, and post-change verification.
