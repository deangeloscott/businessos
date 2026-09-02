#!/usr/bin/env python3
"""Generate natural-language Playbook and Workflow navigation from canonical AURA source.

Playbooks are meaningful end-to-end business jobs. Workflows are reusable procedures that
help accomplish those jobs and can also be used independently. Generated pages are browse
views only; authored Workflow files remain the detailed source of operating knowledge.
"""
from pathlib import Path
import json,os

from operating_knowledge import OPERATING_AREAS,installed_playbooks,playbooks_for_system

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'/'playbooks'

GROUP_NAMES={
    'adaptation':'Adaptation','ads':'Advertising','aeo':'AI / answer-engine visibility','analysis':'Analysis',
    'assets':'Assets','bootstrap':'Setup and starting state','campaigns':'Campaigns','context':'Business context',
    'diagnosis':'Diagnosis','discovery':'Discovery','email':'Email','event':'Events and changes',
    'evidence-collection':'Evidence collection','execution':'Execution','experimentation':'Experiments',
    'instrumentation':'Tracking and instrumentation','intake':'Intake and briefs','intelligence':'Intelligence and research',
    'intervention':'Customer journey improvements','journey':'Customer journey','landing-page':'Landing pages',
    'learning':'Learning and improvement','measurement':'Measurement','monitoring':'Monitoring','offer':'Offers',
    'opportunity':'Opportunities','planning':'Planning','production':'Production','publishing':'Publishing',
    'qa':'Quality checks','research':'Research','social':'Social','strategy':'Strategy','vsl':'Video sales letters','webinar':'Webinars',
}


def load_json(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def rel_link(from_file,target):return Path(os.path.relpath(ROOT/target,from_file.parent)).as_posix()
def contract_map(registry):return {row['id']:row for row in registry}
def workflows_for(registry,system):return [row for row in registry if row.get('owner_system')==system and row.get('type')=='workflow']
def process_map(system):
    path=ROOT/'core/process-map.json' if system=='core' else ROOT/'systems'/system/'process-map.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'activities':[]}


def write_root(registry,installed):
    playbooks=installed_playbooks(registry);workflow_total=sum(1 for row in registry if row.get('type')=='workflow')
    lines=[
        '# What AURA Can Do','',
        'AURA gives capable AI reusable **Playbooks** and **Workflows** while leaving reasoning, tool choice, orchestration, and execution to the active model/harness. Tell the AI what outcome you want in normal language; you do not need to choose a Playbook or Workflow manually.','',
        f'This edition currently exposes **{len(playbooks)} Playbooks** backed by **{workflow_total} detailed Workflows**. Playbook count is intentionally much smaller than Workflow count because a Playbook is an end-to-end business job, not every reusable procedure.','',
        '## The hierarchy','',
        '**Playbook → Workflow → Step**','',
        '- **Playbook** — a meaningful end-to-end business job that bundles relevant operating knowledge.','- **Workflow** — a reusable procedure that helps accomplish part of a Playbook and may also be useful independently.','- **Step** — the minimum guidance needed inside a Workflow to make the intended result reliably achievable.','',
        'A Playbook is not an execution graph. The model chooses which Workflows matter, how to sequence or parallelize them, which host tools or external Skills to use, and whether another sound method is better.','',
        '## Business areas',''
    ]
    for system,area in OPERATING_AREAS.items():
        if system not in installed:continue
        rows=playbooks_for_system(system,registry);page=f'docs/playbooks/{system}.md'
        lines += [f"### [{area['title']}]({page})",'',area['summary'],'',f"**{len(rows)} Playbooks** in this area.",'']
        for row in rows:lines.append(f"- **{row['title']}** — {row['summary']}")
        lines.append('')
    lines += [
        '## AURA Core','',
        'AURA Core supplies shared organizational memory, truth/evidence handling, decisions, continuity, measurement, Learning, and workspace integrity. It is support for the business work rather than another business Playbook. See [AURA Core Workflows](docs/playbooks/core.md).','',
        '## For advanced users','',
        '- `TASK-NAVIGATOR.md` shows the installed Playbooks and common Workflow entry points.','- `WORKFLOW-INDEX.md` lists all detailed Workflow IDs.','- Each Workflow `CONTEXT.md` contains its outcome, when-to-use guidance, steps, evidence needs, and quality requirements.','- `docs/operating-knowledge.md` explains the minimum-sufficient-guidance philosophy.',''
    ]
    (ROOT/'PLAYBOOKS.md').write_text('\n'.join(lines),encoding='utf-8')


def write_domain(registry,system):
    area=OPERATING_AREAS[system];outfile=DOCS/f'{system}.md';cmap=contract_map(registry);pmap=process_map(system);workflows=workflows_for(registry,system);playbooks=playbooks_for_system(system,registry)
    lines=[f"# {area['title']}",'',area['summary'],'',
           '**Ask for the outcome in normal language.** Playbooks below are useful end-to-end frames, not commands the user must select. The model may use their entry Workflows, other AURA Workflows, external Skills, or another sound method.','',
           '## Playbooks','']
    for row in playbooks:
        lines += [f"### {row['title']}",'',row['summary'],'',f'*Try:* “{row["example"]}”','']
        entry=row.get('entry_workflow');workflow=cmap.get(entry) if entry else None
        if workflow:
            link=rel_link(outfile,workflow['path']);lines += [f"**Common entry Workflow:** [{workflow.get('title',entry)}]({link})",'']
        elif entry:
            lines += [f"**Common entry Workflow:** `{entry}`",'']
        else:
            lines += ['**Composition:** Choose the smallest useful set of Workflows below from the actual request and evidence.','']
    lines += ['## Common Workflows','',
              'These reusable procedures may support one or more Playbooks or be used independently. They are not a mandatory sequence.','']
    seen=set()
    for activity in pmap.get('activities',[]):
        wid=activity.get('entry_contract');workflow=cmap.get(wid,{})
        title=workflow.get('title') or activity.get('id','').replace('-',' ').title();result=' '.join(str(activity.get('result') or '').split())
        link=rel_link(outfile,workflow.get('path')) if workflow.get('path') else None;label=f'[{title}]({link})' if link else title
        lines.append(f'- **{label}** — {result}');seen.add(wid)
    remaining=[workflow for workflow in workflows if workflow.get('id') not in seen]
    if remaining:
        lines += ['','## Additional Workflows','',
                  'Use these when the specific need arises. A Workflow can be useful even when no broader Playbook is needed.','']
        groups={}
        for workflow in remaining:
            parts=workflow['id'].split('.');group=parts[1] if len(parts)>2 else 'other';groups.setdefault(group,[]).append(workflow)
        for group in sorted(groups,key=lambda value:GROUP_NAMES.get(value,value).lower()):
            lines += [f"### {GROUP_NAMES.get(group,group.replace('-',' ').title())}",'']
            for workflow in sorted(groups[group],key=lambda item:item.get('title','')):
                lines.append(f"- [{workflow.get('title',workflow['id'])}]({rel_link(outfile,workflow['path'])})")
            lines.append('')
    lines += ['## Working principle','',
              'Use the fewest instructions and Workflows necessary to repeatedly achieve the desired outcome at the required truth and quality standard. Preserve non-obvious expertise, evidence requirements, and real constraints; let the capable model/harness choose implementation details, tools, providers, external Skills, and orchestration unless the implementation itself matters.','']
    outfile.parent.mkdir(parents=True,exist_ok=True);outfile.write_text('\n'.join(lines),encoding='utf-8')


def write_core(registry):
    outfile=DOCS/'core.md';cmap=contract_map(registry);pmap=process_map('core');workflows=workflows_for(registry,'core');seen=set()
    lines=['# AURA Core Workflows','',
           'AURA Core supplies organization-owned memory, truth/evidence handling, decisions, continuity, measurement, Learning, and workspace integrity used across business Playbooks. It is support infrastructure and reusable operating knowledge, not another business Playbook.','',
           '## Common Workflows','']
    for activity in pmap.get('activities',[]):
        wid=activity.get('entry_contract');workflow=cmap.get(wid,{});title=workflow.get('title') or activity.get('id','').replace('-',' ').title();link=rel_link(outfile,workflow.get('path')) if workflow.get('path') else None;label=f'[{title}]({link})' if link else title
        lines.append(f"- **{label}** — {' '.join(str(activity.get('result') or '').split())}");seen.add(wid)
    remaining=[workflow for workflow in workflows if workflow.get('id') not in seen]
    if remaining:
        lines += ['','## Additional Core Workflows','']
        for workflow in sorted(remaining,key=lambda item:item.get('title','')):lines.append(f"- [{workflow.get('title',workflow['id'])}]({rel_link(outfile,workflow['path'])})")
    lines.append('');outfile.parent.mkdir(parents=True,exist_ok=True);outfile.write_text('\n'.join(lines),encoding='utf-8')


def main():
    registry=load_json('generated/contract-registry.json').get('contracts',[]);installed=set(load_json('INSTALLATION.json').get('installed_modules',[]));DOCS.mkdir(parents=True,exist_ok=True)
    write_root(registry,installed);write_core(registry)
    for system in OPERATING_AREAS:
        if system in installed:write_domain(registry,system)
    print(f'Generated Playbook/Workflow navigation for {len(installed_playbooks(registry))} installed Playbooks.')

if __name__=='__main__':main()
