#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]


def load(path):return json.loads((ROOT/path).read_text())


def build():
    inst=load('INSTALLATION.json')
    cat={m['id']:m for m in load('distribution/module-catalog.json')['modules']}
    installed=[m for m in inst.get('installed_modules',[]) if m!='core' and m in cat]
    display=inst.get('display_name','ViralTrac AURA')
    expansion=inst.get('name_expansion','Agentic Understanding and Reinforcement Architecture')
    version=inst.get('source_version') or (ROOT/'VERSION').read_text().strip()
    maturity=str(inst.get('maturity','alpha')).capitalize()

    lines=[
        f'# Welcome to {display}','',
        f'**{maturity} · v{version}**  ',
        f'**AURA = {expansion}.**','',
        'AURA gives capable AI durable organizational memory, reusable operating knowledge, and lightweight continuity. It is not the AI model, agent harness, tool runtime, scheduler, provider router, or permission system.','',
        '> Alpha means the architecture is usable and integrity-tested, while real-work quality, playbooks, retrieval, Learning, and usability are still being actively improved before 1.0.','',
        '## Start','',
        '1. Give this AURA folder to a capable AI/agent harness.',
        '2. Tell it about the business and what you want.',
        '3. Talk normally; you do not need to choose a playbook first.','',
        'For example:','',
        '> Use ViralTrac AURA for my business. My company is Acme, our website is acme.com, and I want to grow qualified leads. Use what we already know and help me get the highest-value work done.','',
        '## What this copy can help with',''
    ]
    for mid in installed:
        m=cat[mid]
        lines.append(f"- **{m['display_name']}** — {m['welcome_summary']}")
    if not installed:
        m=cat['core'];lines.append(f"- **{m['display_name']}** — {m['welcome_summary']}")

    lines += [
        '',
        'A capable AI should retrieve the smallest useful AURA context, use an AURA playbook when it helps, use its actual tools/capabilities normally, do the substantive work, and preserve only material organizational meaning worth carrying forward.','',
        'If you want to browse specific jobs, open **`PLAYBOOKS.md`**. For the shortest setup guide, open **`START-HERE.md`**.','',
        'ViralTrac is an optional first-party companion for tracking, attribution, measurement, experiments, and supported growth-operation surfaces. AURA also works without it.','',
        '**Core invariant:** AURA provides organizational memory and operating knowledge; capable intelligence determines how best to work.',''
    ]
    return '\n'.join(lines)


if __name__=='__main__':
    out=ROOT/'WELCOME.md';out.write_text(build());print(out)
