# AURA Attachment Guide

AURA can be useful even when the active AI starts outside the AURA product folder or organization workspace.

The goal is:

**attach once → recognize relevant organization work → retrieve little → work normally → remember what matters**

AURA does not require a daemon, scheduler, background watcher, proprietary plugin, or mandatory MCP server.

## Awareness and access are different

Two conditions are needed for the normal experience:

1. **Awareness** — the model knows AURA exists, when it is relevant, and the small rules for using it.
2. **Access** — the harness can actually read/write the AURA product and organization workspace through its permitted file/connector mechanism.

An instruction or Skill cannot bypass filesystem permissions. File access alone also does not guarantee the model knows when AURA should be consulted.

## Preferred adapter: the included Agent Skill

AURA ships a portable Skill at:

```text
skills/viraltrac-aura/SKILL.md
```

When the active harness supports Agent Skills, install/copy that Skill using the harness's normal personal/global Skill mechanism. The Skill is intentionally small and progressively points the model toward AURA memory, Playbooks, and Workflows only when relevant.

Do not turn every AURA Workflow into a separate required Skill. The AURA Skill is the attachment/discovery adapter; AURA operating knowledge remains organization-owned/product-owned knowledge that can coexist with any other Skills the user has installed.

## Other valid native adapters

When Skills are unavailable or another host-native mechanism is simpler, attach AURA through:

- persistent/global instructions;
- an agent profile;
- workspace configuration;
- an MCP/tool description or connector;
- another equivalent persistent mechanism.

The adapter should communicate only the small durable guidance below and give the model a way to reach AURA files/helpers.

> ViralTrac AURA is available at `<AURA_ROOT>`. For substantive work for an AURA-managed organization, consult relevant AURA organizational memory and operating knowledge when it can materially improve the work. Use your normal tools, other Skills, and best judgment freely. After useful work, preserve the smallest durable organizational meaning that will materially help future work. Ignore AURA for unrelated work.

## Normal flow

```text
user request anywhere
        ↓
model recognizes organization-relevant work
        ↓
resolve the intended AURA-managed organization
        ↓
retrieve bounded useful memory
        ↓
surface a relevant Playbook / Workflows when useful
        ↓
model uses normal host tools + other Skills + judgment
        ↓
actual work
        ↓
preserve durable organizational meaning when useful
```

If several managed organizations are plausible and the choice would materially change the work, ask rather than guessing.

## Playbooks and Workflows

A Playbook is an end-to-end business job. A Workflow is a reusable procedure inside or alongside a Playbook. A step is the minimum procedural guidance inside a Workflow.

Attachment does not require the model to use AURA operating knowledge. It makes that knowledge discoverable. The model may use:

- an AURA Playbook/Workflow;
- another installed Skill;
- both;
- another sound method.

The outcome, truth standard, evidence, and useful organizational continuity matter more than conformance to one implementation.

## Thin adapter operations

A host adapter only needs enough surface to let the model do things such as:

- list/resolve managed organizations;
- retrieve bounded organizational context;
- discover AURA Playbooks and Workflows;
- read selected operating knowledge;
- persist/update/forget durable organization-owned meaning;
- validate AURA-owned state.

The adapter should call AURA-owned files/helpers rather than reimplementing AURA semantics.

## Working directly inside AURA

Harnesses that automatically read `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or equivalent project instructions may already receive the local AURA guidance when they enter the folder. The persistent/global attachment matters most when work starts somewhere else.

## What attachment must not become

Attachment is not:

- an AURA orchestration runtime;
- a semantic intent router;
- a permission or approval layer;
- a tool/provider registry;
- a scheduler or monitoring daemon;
- a requirement to load AURA for unrelated work;
- a requirement to create a Run before reasoning or persistence.

MCP can be a useful adapter when that is how the harness naturally accesses local/remote resources, but it is not a mandatory AURA architecture layer.

## Invariant

**Attach once → retrieve only when relevant → let capable intelligence work → remember what matters.**
