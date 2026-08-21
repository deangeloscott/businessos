# Capability Preflight

Before executing an atomic job, determine whether its **required** provider-neutral capabilities can be satisfied in the active environment. Do this before expensive research/execution, not after the workflow is already underway.

Use `python scripts/preflight_capabilities.py <business-id> <contract-id>`; it defaults to the portable `local` environment unless another environment is selected.

For each required capability:
1. First ensure host capability discovery has considered the tools actually visible in the current environment. Use an enabled discovered/existing permitted binding when available. If an already-authorized connected provider exposes machine-readable capabilities, refresh its current bindings before treating the capability as missing; connection alone is not proof that every provider surface is available.
2. If no binding exists, resolve business → environment → distribution provider preference.
3. A provider recommendation is not an active capability and does not authorize signup, purchase, connection, permissions, or data sharing. Obtain the applicable authorization or choose an allowed fallback.
4. If no provider supplies the capability, preserve the required practitioner step through manual/assisted execution where possible.
5. Optional capabilities may improve the job but do not block it. Resolve them only when useful.

Preflight results are execution guidance, not business evidence. Re-run preflight when a connection changes, a tool call shows the binding is no longer usable, or the job resumes in a different environment.

A missing capability must never cause the underlying business step to disappear. If neither automation nor a safe manual path can produce the required evidence/action, preserve the Run as blocked and make the missing dependency explicit.
