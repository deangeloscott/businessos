# Deployment

Business logic names capabilities, not vendors. Capability bindings and environment policy compile an effective capability profile. Missing automation creates manual work.


## Session/operator labels
A host may set `BUSINESSOS_OPERATOR_REF`, `BUSINESSOS_TEAM_REF`, and `BUSINESSOS_ROLE_REF` per shell/session. `scripts/create_run.py` records them and resolves a run-local preference snapshot. These labels are context/attribution only and do not grant permission. Different harness windows can use different labels against the same business instance; coordinate simultaneous writes according to `core/policies/shared-workspace-coordination.md`.
