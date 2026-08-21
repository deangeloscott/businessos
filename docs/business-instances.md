# Business Instances

Each business is isolated under `instances/<business-id>/`. Canonical business state, intelligence, decisions, operations, Assets, measurement, and Learning remain inside that instance. Cross-business references fail by default.

`intelligence/proof/` stores canonical ProofRecords for reusable, source-linked, permission-aware evidence such as testimonials, reviews, case results, demonstrations, metrics, and certifications. The customer/CRM system remains the identity system of record; the Business OS stores only necessary subject references and evidence relationships.

## Shared operator identity vs business state
`deployment/operator-profile.json` is workspace/operator-scoped convenience state, not canonical business truth. It may supply only operator identity fields explicitly marked `reuse_across_businesses`. Brand/company facts remain isolated under their `business_id`, and a business research-profile value overrides an inherited operator value. This avoids repeat questions without allowing one brand's facts to leak into another.
