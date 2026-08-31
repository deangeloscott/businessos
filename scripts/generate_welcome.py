#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def load(path):return json.loads((ROOT/path).read_text())

def build():
    inst=load('INSTALLATION.json');cat={m['id']:m for m in load('distribution/module-catalog.json')['modules']};installed=[m for m in inst.get('installed_modules',[]) if m!='core' and m in cat];display=inst.get('display_name','ViralTrac AURA');expansion=inst.get('name_expansion','Agentic Understanding and Reinforcement Architecture')
    lines=[f'# Welcome to {display}','',f'**AURA = {expansion}.**','',f'Thank you for downloading **{display}**, by **DeAngelo Scott**.','', 'AURA gives a capable AI durable organization-owned context, evidence, reusable operating processes, work continuity, outcomes, and Learning. It is not the AI model, agent harness, tool runtime, scheduler, or permission system.','', '## What this copy can help you do','']
    if installed:
        for mid in installed:
            m=cat[mid];lines.append(f"**{m['display_name']}** — {m['welcome_summary']}");ex=m.get('example_prompts',[])
            if ex:lines.append(f"*Try:* “{ex[0]}”")
            lines.append('')
    else:
        m=cat['core'];lines += [f"**{m['display_name']}** — {m['welcome_summary']}",'',f"*Try:* “{m['example_prompts'][0]}”",'']
    combos=[];s=set(installed);candidates=[
        ({'customer-intelligence','marketing-synthesis'},'Find our biggest customer objection and create a campaign around it.'),
        ({'industry-intelligence','content-synthesis'},'Find an important industry development and turn it into useful content for our audience.'),
        ({'competitor-intelligence','marketing-synthesis'},'Find a competitor weakness and turn it into stronger positioning or an offer.'),
        ({'seo-aeo','content-synthesis'},'Find the highest-value organic content opportunity and create the asset needed to pursue it.'),
        ({'customer-intelligence','customer-optimization'},'Find why customers are leaving and determine what part of the experience should change.'),
    ]
    for req,prompt in candidates:
        if req<=s:combos.append(prompt)
    if len(s)>=4:combos.insert(0,'Identify our highest-value business opportunities and coordinate the useful work needed to pursue them.')
    if combos:
        lines += ['## You can also combine these capabilities','']+[f'- “{p}”' for p in combos[:3]]+['']
    lines += [
        '## You do not need to know the right workflow','',
        'Describe a business problem or desired result in plain language. The active AI should retrieve relevant AURA memory, surface a useful AURA playbook when one fits, use its actual harness/tools normally, do the real work, and preserve only the material organizational meaning worth carrying forward.','',
        'If you are not sure where to begin, try:','',
        '- “What can you help me with?”','- “What should we work on first?”','- “Here is my business. Find the biggest opportunities you can help with using what is installed.”','',
        'If you want to browse specific jobs, open **`PLAYBOOKS.md`** or ask “Show me what ViralTrac AURA can do.” You still do not need to choose a playbook before asking for help.','',
        '## To get started','',
        '**Tell the agent your business name, website if you have one, and what you want to accomplish.** If that context already exists in AURA, it should reuse it instead of asking again.','',
        'ViralTrac is AURA’s optional first-party companion for tracking, attribution, measurement, SmartLinks, and supported growth-operation surfaces. AURA should also work before ViralTrac, alongside it, or without it.','',
        'The invariant is simple: **AURA provides organizational memory and operational knowledge; the active intelligence/runtime determines how best to work.**',''
    ]
    return '\n'.join(lines)

if __name__=='__main__':
    out=ROOT/'WELCOME.md';out.write_text(build());print(out)
