# AURA Attachment Contract

AURA can be useful even when the active AI starts outside the AURA product or organization workspace.

The goal is **once-only awareness, then relevance-based retrieval**. AURA should not require a daemon, scheduler, background watcher, proprietary plugin, or mandatory MCP server.

## Harness contract

A harness may attach AURA through any native persistent mechanism it already supports: global instructions, a Skill, an MCP/tool description, an agent profile, workspace configuration, or another equivalent mechanism.

The attachment should communicate only this durable contract:

> ViralTrac AURA is available at `<AURA_ROOT>`. For substantive work on behalf of an organization managed by AURA, identify the relevant organization, retrieve only the organizational memory and operating knowledge that can materially improve the current work, use the active model/harness capabilities normally, and preserve durable organizational meaning afterward when useful. Ignore AURA for unrelated work. AURA does not own semantic intent, tool/provider selection, permissions, orchestration, scheduling, or execution.

That contract is intentionally small. The harness remains responsible for how it exposes files/tools and how the active model reasons and executes.

## Normal flow

```text
user request anywhere
        ↓
model recognizes organization-relevant work
        ↓
AURA organization directory
        ↓
resolve exactly one organization
        ↓
retrieve bounded relevant memory / optional SOP knowledge
        ↓
model works with normal harness capabilities
        ↓
persist only durable organizational meaning
```

If several organizations are plausible, the model should use the organization directory and current conversation context to resolve the intended one. If ambiguity would materially change the work, ask the user. AURA must not guess across organizations.

## What attachment must not become

Attachment is not:

- an AURA orchestration runtime;
- a semantic intent router;
- a permission or approval layer;
- a provider/tool registry;
- a scheduler or background monitoring daemon;
- a requirement to load AURA context for unrelated work;
- a requirement to start a Run before reasoning or persistence.

MCP can be a useful adapter when a harness already uses MCP, but MCP is not part of AURA's core architecture. The same AURA-owned primitives should remain usable through ordinary files and command-line helpers.

## Portable examples

### Global instruction / agent profile

Store the harness contract above in the harness's persistent instruction mechanism and replace `<AURA_ROOT>` with the local AURA product path.

### Skill or tool adapter

Expose only thin operations such as:

- list managed organizations;
- retrieve bounded organizational context;
- discover relevant AURA operating knowledge;
- persist/update/retire durable organization-owned meaning;
- validate organization state.

The adapter should call AURA-owned filesystem/helpers rather than reimplement AURA semantics.

### Working directly inside AURA

Harnesses that automatically read `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` already receive the local adapter when they enter the AURA folder. The attachment contract matters most when the active work starts elsewhere.

## Invariant

**Attach once → retrieve only when relevant → let the capable model work → remember what matters.**
