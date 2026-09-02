#!/usr/bin/env python3
"""Generate natural-language Playbook and Workflow navigation from canonical AURA source.

Playbooks are high-level end-to-end business jobs. Contract files marked `workflow` are
reusable procedures inside or alongside those Playbooks. Generated pages are views only;
the authored workflow files and process maps remain the detailed source of operating
knowledge.
"""
from pathlib import Path
import json,os

from operating_knowledge import PLAYBOOKS,PLAYBOOK_BY_SYSTEM

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'/'playbooks'
ORDER=[row['owner_system'] for row in PLAYBOOKS]

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
    playbooks=[row for row in PLAYBOOKS if row['owner_system'] in installed]
    workflow_total=sum(len(workflows_for(registry,row['owner_system'])) for row in playbooks)
    lines=[
        '# What AURA Can Do','',
        'AURA gives capable AI a small set of end-to-end **Playbooks** backed by reusable **Workflows**. You do not need to choose either one manually: tell the AI what outcome you want in normal language.','',
        f'This edition includes **{len(playbooks)} business Playbooks** and **{workflow_total} detailed Workflows** across the installed business areas. AURA Core supplies shared memory, truth, evidence, continuity, measurement, and Learning support.','',
        '## The hierarchy','',
        '**Playbook → Workflow → Step**','',
        '- **Playbook** — a meaningful end-to-end business job.','- **Workflow** — a reusable procedure that helps accomplish part of a Playbook and may also be useful independently.','- **Step** — the minimum guidance needed for a Workflow to reliably achieve its intended result.','',
        'The model chooses which workflows matter, how to sequence or parallelize them, which host tools or external Skills to use, and whether another sound method is better. AURA does not prescribe a provider/tool allowlist.','',
        '## Playbooks',''
    ]
    for row in playbooks:
        page=f"docs/playbooks/{row['owner_system']}.md";count=len(workflows_for(registry,row['owner_system']))
        lines += [f"### [{row['title']}]({page})",'',row['summary'],'',f'**{count} reusable Workflows.**','',f'*Try:* “{row["example"]}”','']
    lines += [
        '## AURA Core','',
        'AURA Core is shared organizational memory and operating support rather than another business Playbook. See [AURA Core Workflows](docs/playbooks/core.md) for the reusable context, evidence, decision, continuity, measurement, and Learning procedures.','',
        '## For advanced users','',
        '- `TASK-NAVIGATOR.md` shows common workflows by Playbook.','- `WORKFLOW-INDEX.md` lists detailed workflow IDs.','- Each workflow `CONTEXT.md` contains its detailed outcome, when-to-use guidance, process steps, evidence needs, and quality requirements.','- `docs/operating-knowledge.md` explains the minimum-sufficient-guidance philosophy.',''
    ]
    (ROOT/'PLAYBOOKS.md').write_text('\n'.join(lines),encoding='utf-8')


def write_domain(registry,system):
    row=PLAYBOOK_BY_SYSTEM[system];outfile=DOCS/f'{system}.md';cmap=contract_map(registry);pmap=process_map(system);workflows=workflows_for(registry,system)
    lines=[
        f"# {row['title']} Playbook",'',row['summary'],'',
        '**Ask for the outcome in normal language.** The model may use the workflows below, combine them with other AURA knowledge or external Skills, run independent work in parallel, adapt the approach, or use another sound method when it better serves the outcome.','',
        f'*Example:* “{row["example"]}”','',
        '## Common workflows','',
        'These are common reusable procedures for this Playbook. They are not a mandatory sequence. Use only what materially helps the request.',''
    ]
    seen=set()
    for activity in pmap.get('activities',[]):
        wid=activity.get('entry_contract');workflow=cmap.get(wid,{})
        title=workflow.get('title') or activity.get('id','').replace('-',' ').title();result=' '.join(str(activity.get('result') or '').split())
        link=rel_link(outfile,workflow.get('path')) if workflow.get('path') else None;label=f'[{title}]({link})' if link else title
        lines.append(f'- **{label}** — {result}');seen.add(wid)
    remaining=[workflow for workflow in workflows if workflow.get('id') not in seen]
    if remaining:
        lines += ['','## Additional workflows','',
                  'Use these when the specific need arises. A workflow can be used on its own even when the broader Playbook is unnecessary.','']
        groups={}
        for workflow in remaining:
            parts=workflow['id'].split('.');group=parts[1] if len(parts)>2 else 'other';groups.setdefault(group,[]).append(workflow)
        for group in sorted(groups,key=lambda value:GROUP_NAMES.get(value,value).lower()):
            lines += [f"### {GROUP_NAMES.get(group,group.replace('-',' ').title())}",'']
            for workflow in sorted(groups[group],key=lambda item:item.get('title','')):
                link=rel_link(outfile,workflow['path']);lines.append(f"- [{workflow.get('title',workflow['id'])}]({link})")
            lines.append('')
    lines += ['## Working principle','',
              'Use the fewest instructions and workflows necessary to repeatedly achieve the desired outcome at the required truth and quality standard. Preserve non-obvious expertise, evidence requirements, and real constraints; let the capable model/harness choose implementation details, tools, providers, external Skills, and orchestration unless the implementation itself matters.','']
    outfile.parent.mkdir(parents=True,exist_ok=True);outfile.write_text('\n'.join(lines),encoding='utf-8')


def write_core(registry):
    outfile=DOCS/'core.md';cmap=contract_map(registry);pmap=process_map('core');workflows=workflows_for(registry,'core');seen=set()
    lines=['# AURA Core Workflows','',
           'AURA Core supplies organization-owned memory, truth/evidence handling, decisions, continuity, measurement, Learning, and workspace integrity used across the business Playbooks. It is support infrastructure and operating knowledge, not another business Playbook.','',
           '## Common workflows','']
    for activity in pmap.get('activities',[]):
        wid=activity.get('entry_contract');workflow=cmap.get(wid,{});title=workflow.get('title') or activity.get('id','').replace('-',' ').title();link=rel_link(outfile,workflow.get('path')) if workflow.get('path') else None;label=f'[{title}]({link})' if link else title
        lines.append(f"- **{label}** — {' '.join(str(activity.get('result') or '').split())}");seen.add(wid)
    remaining=[workflow for workflow in workflows if workflow.get('id') not in seen]
    if remaining:
        lines += ['','## Additional Core workflows','']
        for workflow in sorted(remaining,key=lambda item:item.get('title','')):
            lines.append(f"- [{workflow.get('title',workflow['id'])}]({rel_link(outfile,workflow['path'])})")
    lines.append('');outfile.parent.mkdir(parents=True,exist_ok=True);outfile.write_text('\n'.join(lines),encoding='utf-8')


def main():
    registry=load_json('generated/contract-registry.json').get('contracts',[]);installed=set(load_json('INSTALLATION.json').get('installed_modules',[]));DOCS.mkdir(parents=True,exist_ok=True)
    write_root(registry,installed);write_core(registry)
    for system in ORDER:
        if system in installed:write_domain(registry,system)
    print(f'Generated Playbook/Workflow navigation for {len([x for x in PLAYBOOKS if x["owner_system"] in installed])} installed business Playbooks.')

if __name__=='__main__':main()
