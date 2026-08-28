# Host Capability Discovery

**ViralTrac AURA** is designed to be dropped into different AI/agent environments. A fresh agent should inspect its own visible tools before treating the built-in empty `local` environment as the final capability state.

Typical startup:

```text
open AURA workspace
→ show WELCOME.md once
→ inspect host tools/connectors/MCP/filesystem/code/browser
→ conservatively map clear abilities to BusinessOS capabilities
→ persist non-secret inventory/bindings in workspace host state
→ initialize/resume business
→ route goal
→ capability preflight
→ execute
```

The helper `scripts/bootstrap_environment.py` compiles an agent-prepared host manifest. It does not introspect a proprietary runtime by itself; the agent/harness supplies the visible tool descriptions it already has. Live discovered environment state is stored under the active workspace at `.businessos/environments/<environment>/`; shipped `deployment/environments/<environment>/` files remain immutable defaults.

Example manifest:

```json
{
  "format_version": "1.0",
  "host_id": "example-agent",
  "host_name": "Example Agent",
  "tools": [
    {
      "id": "web.search",
      "description": "Search and retrieve public web sources",
      "capabilities": ["research.web.read"],
      "permissions": ["read"],
      "enabled": true
    }
  ]
}
```

Save temporary discovery input under the active workspace (for example `runtime/host-tools.json`) or provide it over stdin, then run:

```bash
python scripts/bootstrap_environment.py local --manifest runtime/host-tools.json --mark-welcome-shown
```

A `runtime/...` manifest ref resolves through the active workspace rather than the AURA product folder. `--manifest -` may be used for stdin. Only map a capability when the tool clearly satisfies it. Unknown or risky mappings remain unbound until needed/confirmed.
