# ViralTrac integration

## Connect from the interface or your AI app

In AURA, select the intended business and open **Settings → API connections → ViralTrac**. Continue to ViralTrac, sign in and approve the intended business in its existing **Connected AI Agents → Use with AURA** section. No new navigation page is required. The temporary pairing window closes its local listener after success or ten minutes.

Starting in ViralTrac, the same **Use with AURA** section provides the AURA settings location and CLI entry below. A website cannot silently start a local AURA installation; if it is not running, open it or use the CLI. The existing sign-in return path preserves the pairing request.

Without AURA's interface, run from the product folder (use `--workspace` when the business lives elsewhere):

```sh
python scripts/workspace_viraltrac.py --workspace /path/to/workspace --business-id my-business pair
python scripts/workspace_viraltrac.py --workspace /path/to/workspace --business-id my-business status --live
python scripts/workspace_viraltrac.py --workspace /path/to/workspace --business-id my-business discover
python scripts/workspace_viraltrac.py --workspace /path/to/workspace --business-id my-business discover --group measurement
python scripts/workspace_viraltrac.py --workspace /path/to/workspace --business-id my-business call --tool performance_summary --input arguments.json
```

`pair --no-browser` prints a short-lived local URL instead of opening it. For an existing authorized service/user-agent token, use `connect --token-stdin`: send the secret through stdin from your secret manager, never as a command argument or chat message. Saved credentials use the existing OS-protected storage mechanism; Linux needs an unlocked supported keyring. No plaintext fallback is created. The CLI needs no running AURA or ViralTrac dashboard after authorization. A truly remote/cloud host must use its own authorized ViralTrac connection; it cannot read a local computer's keyring.

`mcp-config` prints a secret-free stdio MCP configuration bound to this exact workspace and business. Add it through your host's supported MCP settings. AURA supplies the same stdio configuration to its ACP sessions; other local hosts can use the CLI directly, and native ViralTrac connections remain valid. The adapter forwards requests to ViralTrac's current tools rather than duplicating a tool registry. Use `discover --group` where a host cannot expand tool groups itself.

On a headless machine without an OS keyring, `connect --token-stdin --no-store` verifies and saves only the business association. Supply `AURA_VIRALTRAC_TOKEN` through your process's secret manager, together with `AURA_VIRALTRAC_ORG_ID` and, for non-production services, `AURA_VIRALTRAC_API_ORIGIN`. The helper checks both the association and the token's actual organization before use. A token for a different business is rejected rather than silently reused. Never put these secrets in shared workspace configuration. Local disconnect cannot remove credentials supplied by an external process environment; remove them there or revoke remotely.

The shared Business record contains only the ViralTrac service origin, organization ID and display name. Authorization is separate per computer/OS user/workspace/business. A different person opening the shared workspace must authorize their own access. Different businesses do not share an environment token. Do not treat the manifest's legacy workspace field or semantic-query `default` scope as interchangeable with organization identity; `connection.scopes` identifies these meanings.

**Disconnect on this computer** removes the local credential, preserving the shared business association and saved findings. **Unlink business** also removes that association for everyone sharing the workspace. Revoke the user-agent connection in ViralTrac to invalidate it remotely. Expired/revoked credentials require reconnection; this implementation does not silently renew a user's grant.

## Save and refresh useful evidence

Tool responses retain ViralTrac's reporting windows, coverage, source/evidence handles and limitations. CLI calls add a small `aura_source` origin/retrieval descriptor, not an assertion that every response includes platform-account lineage or user attribution. Tool errors are not observations of zero activity.

Use existing `SourceRecord`, `MetricDefinition`, `MetricObservation`, findings and decisions with `scripts/remember.py` or the existing research bundle helper. Preserve the measurement window separately from retrieval time; retain currency, attribution definition and available source-connection references when material. Distinguish provider results from model conclusions. Do not save credentials or bulk operational histories.

Before refresh, retrieve the existing result and its query/source context. Reuse comparable definitions and explicit periods. Update the same observation for a provider restatement of the same period, with a correction summary; create a new dated observation for a genuinely different period. Use existing finding supersession and maintained collections rather than a separate synchronization service. ViralTrac artifact links can expire, so retain a stable query/receipt reference and an authorized bounded excerpt when necessary. Existing transfer/data policies still apply to what may be retained.

## Verification scope

`tests/run_viraltrac_connection.py` exercises real loopback HTTP, protected local storage where available, wrong-origin rejection, business mismatch, credential exclusion from workspace records, stdio forwarding, revocation, and existing measurement update behavior in an isolated workspace. This is integration fixture evidence, not a live customer marketing-data acceptance claim. Native host discovery and service-history coverage still follow each host's supported interfaces.

ViralTrac is an optional first-party integration for ViralTrac AURA. It is **not** AURA's runtime, provider resolver, scheduler, event engine, permission system, or required execution path.

## Boundary

AURA owns durable organizational meaning: relevant facts and evidence, decisions, work/results, measurements and outcomes, and evidence-supported Learning.

The active model/harness/user owns method choice and reasoning. The active runtime owns authentication, tools, provider selection, capability discovery, retries, scheduling, webhooks/events, concurrency, and execution mechanics.

When ViralTrac is available and useful, the active intelligence may use its current interfaces for business data, attribution, tracking, measurements, experiments, artifacts, or supported actions. When another source or tool is better, use that instead. AURA must never force ViralTrac merely because it is first-party.

## Combined operating model

When AURA and ViralTrac are both available, they should compose rather than compete:

1. AURA supplies relevant organization-owned context, prior evidence, decisions, Learning, and reusable business operating knowledge.
2. The active model uses that context and its own judgment to decide what work is useful and which methods or tools fit the job.
3. ViralTrac supplies current first-party business evidence and specialist capabilities where relevant, such as attribution, tracking, measurement, experiments, funnel or content evidence, and supported growth actions.
4. AURA Playbooks and Workflows provide business operating expertise. ViralTrac agent/operator playbooks provide product-specific guidance for using ViralTrac surfaces. They may be combined when useful; neither is a routing authority or replacement for model judgment.
5. Execute through ViralTrac only when its current interface says the action is available and authorized. Otherwise use another appropriate host tool or treat ViralTrac guidance as evidence/advice rather than pretending an external action occurred.
6. After the work, preserve in AURA only the durable organizational meaning that will materially help future work, with references back to authoritative ViralTrac evidence, artifacts, measurements, experiments, or receipts when useful.

Do not create fixed one-to-one mappings between AURA Workflows and ViralTrac tools or playbooks. The active intelligence should combine them semantically according to the user's actual outcome and the capabilities currently available.

## Persist meaning, not a second data plane

Do not bulk-copy ViralTrac operational history into AURA. Preserve only the durable organizational information a capable future model would materially benefit from, with references back to authoritative ViralTrac evidence or receipts when available.

Examples include:
- evidence-backed business observations;
- metric observations and outcome evaluations;
- artifacts/results worth retaining;
- material external changes;
- durable decisions prompted by the evidence;
- unresolved attention;
- Learning supported by measured outcomes.

Absence or unavailability from ViralTrac is not evidence that a business fact is false or zero.

## Tooling

AURA does not maintain ViralTrac capability bindings. The active harness discovers and invokes whatever ViralTrac interface is actually available (for example MCP, API, connector, or future interface). Credentials remain outside AURA durable state.

When ViralTrac exposes an AI-native bootstrap, capability, tool-group, or equivalent discovery surface, prefer that current interface over hard-coding assumptions about available tools. If MCP is available and task scope is unclear, let ViralTrac's own current discovery metadata guide which product-specific surfaces to load while keeping the model responsible for the overall business method.

`semantic-mapping.json` contains optional correspondence hints between ViralTrac concepts and AURA records. Those mappings are not execution contracts or routing authority.
