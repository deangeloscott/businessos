# Host Capability Discovery

ViralTrac's BusinessOS is designed to be dropped into different AI/agent environments. A fresh agent should inspect its own visible tools before treating the built-in empty `local` environment as the final capability state.

Typical startup:

```text
open workspace
→ show WELCOME.md once
→ inspect host tools/connectors/MCP/filesystem/code/browser
→ conservatively map clear abilities to BusinessOS capabilities
→ persist non-secret inventory/bindings
→ initialize/resume business
→ route goal
→ capability preflight
→ execute
```

The helper `scripts/bootstrap_environment.py` compiles an agent-prepared host manifest. It does not introspect a proprietary runtime by itself; the agent/harness supplies the visible tool descriptions it already has.

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

Then run:

```bash
python scripts/bootstrap_environment.py local --manifest host-tools.json --mark-welcome-shown
```

Only map a capability when the tool clearly satisfies it. Unknown or risky mappings remain unbound until needed/confirmed.
