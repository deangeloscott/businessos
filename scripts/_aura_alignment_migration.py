#!/usr/bin/env python3
"""One-time AURA alignment migration.

Mechanically removes retired control-plane metadata/type declarations from contract
frontmatter and updates regression assertions whose wording encoded the retired model.
Delete this helper after the migration commit is validated.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RETIRED_SCALARS = ("risk:", "autonomy_ceiling:")
RETIRED_TYPES = {"- ActionPacket", "- Approval"}
LIST_KEYS = {"reads:", "writes:"}


def contract_files():
    paths = list((ROOT / "core" / "contracts").rglob("CONTEXT.md"))
    for system in (ROOT / "systems").iterdir():
        contracts = system / "contracts"
        if contracts.exists():
            paths.extend(contracts.rglob("CONTEXT.md"))
    return sorted(set(paths))


def migrate_frontmatter(text: str):
    if not text.startswith("---\n"):
        return text, False
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    front = text[4:end].splitlines()
    body = text[end + 5 :]

    filtered = []
    for line in front:
        stripped = line.strip()
        if any(line.startswith(key) for key in RETIRED_SCALARS):
            continue
        if stripped in RETIRED_TYPES:
            continue
        filtered.append(line)

    normalized = []
    i = 0
    while i < len(filtered):
        line = filtered[i]
        if line in LIST_KEYS:
            j = i + 1
            has_item = False
            while j < len(filtered):
                nxt = filtered[j]
                if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", nxt):
                    break
                if nxt.startswith("-") or nxt.startswith("  -"):
                    has_item = True
                    break
                j += 1
            if not has_item:
                normalized.append(line[:-1] + ": []")
                i += 1
                continue
        normalized.append(line)
        i += 1

    new = "---\n" + "\n".join(normalized) + "\n---\n" + body
    return new, new != text


def replace_exact(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")
        return True
    return False


def main():
    changed = []
    for path in contract_files():
        text = path.read_text(encoding="utf-8")
        new, did_change = migrate_frontmatter(text)
        if did_change:
            path.write_text(new, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())

    knowledge = ROOT / "scripts" / "generate_knowledge_layer.py"
    if knowledge.exists():
        text = knowledge.read_text(encoding="utf-8")
        text = text.replace(
            "('Operations','Actions, approvals, incidents, change/verification and operational attention.'),",
            "('Operations','Decisions, incidents, material changes/verification, work requests and operational attention.'),",
        )
        text = text.replace(
            "OPERATIONS_TYPES={'ActionPacket','Approval','Incident','ChangeEvent','VerificationRecord','WorkRequest','AttentionItem','EventReactionDecision','PlatformChange'}",
            "OPERATIONS_TYPES={'DecisionRecord','Incident','ChangeEvent','VerificationRecord','WorkRequest','AttentionItem','EventReactionDecision','PlatformChange'}",
        )
        knowledge.write_text(text, encoding="utf-8")

    hardening = ROOT / "tests" / "run_agent_hardening.py"
    replace_exact(
        hardening,
        "'customer-facing Asset must reference a Run whose root contract is marked'",
        "'customer-facing Asset using an AURA playbook must reference a root marked'",
    )
    replace_exact(
        hardening,
        "        approval=(ROOT/'core/policies/approval.md').read_text(encoding='utf-8')\n        require('Silence is not approval' in approval,'silence-not-approval rule missing')",
        "        for retired in ['core/policies/approval.md','core/policies/risk.md','core/policies/autonomy.md','core/schemas/action/action-packet.schema.json','core/schemas/action/approval.schema.json']:\n            require(not (ROOT/retired).exists(),f'retired control-plane component must be deleted: {retired}')\n        agent_interface=(ROOT/'CONTEXT.md').read_text(encoding='utf-8')\n        require('does not silently become a request to publish or mutate external state' in agent_interface,'real request-scope boundary missing from AURA agent interface')",
    )

    errors = []
    for path in contract_files():
        text = path.read_text(encoding="utf-8")
        end = text.find("\n---\n", 4)
        front = text[4:end] if text.startswith("---\n") and end >= 0 else ""
        for token in ("risk:", "autonomy_ceiling:", "- ActionPacket", "- Approval"):
            if token in front:
                errors.append(f"{path.relative_to(ROOT)} still contains retired frontmatter token {token!r}")
    if errors:
        raise SystemExit("\n".join(errors))

    print(f"AURA alignment migration updated {len(changed)} contract file(s).")


if __name__ == "__main__":
    main()
