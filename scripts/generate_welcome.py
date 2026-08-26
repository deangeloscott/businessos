#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT/path).read_text())

def build():
    inst=load('INSTALLATION.json')
    cat={m['id']:m for m in load('distribution/module-catalog.json')['modules']}
    installed=[m for m in inst.get('installed_modules',[]) if m != 'core' and m in cat]
    display=inst.get('display_name','ViralTrac AURA')
    expansion=inst.get('name_expansion','Agentic Understanding and Reinforcement Architecture')
    lines=[
        f'# Welcome to {display}', '',
        f'**AURA = {expansion}.**', '',
        f'Thank you for downloading **{display}**, by **DeAngelo Scott**.', '',
        'AURA is an AI-native BusinessOS designed to help you understand your business, coordinate useful work, learn from measured outcomes, and improve how the business operates over time.', '',
        '## What this copy can help you do', ''
    ]
    if installed:
        for mid in installed:
            m=cat[mid]
            lines += [f"**{m['display_name']}** — {m['welcome_summary']}"]
            ex=m.get('example_prompts',[])
            if ex:
                lines.append(f"*Try:* “{ex[0]}”")
            lines.append('')
    else:
        m=cat['core']
        lines += [f"**{m['display_name']}** — {m['welcome_summary']}", '', f"*Try:* “{m['example_prompts'][0]}”", '']

    combos=[]; s=set(installed)
    candidates=[
        ({'customer-intelligence','marketing-synthesis'}, 'Find our biggest customer objection and create a campaign around it.'),
        ({'industry-intelligence','content-synthesis'}, 'Find an important industry development and turn it into useful content for our audience.'),
        ({'competitor-intelligence','marketing-synthesis'}, 'Find a competitor weakness and turn it into stronger positioning or an offer.'),
        ({'seo-aeo','content-synthesis'}, 'Find the highest-value organic content opportunity and create the asset needed to pursue it.'),
        ({'customer-intelligence','customer-optimization'}, 'Find why customers are leaving and determine what part of the experience should change.'),
        ({'customer-intelligence','marketing-synthesis','customer-optimization'}, 'Figure out why people are not buying, improve the persuasion, and reduce the customer-journey friction.'),
    ]
    for req,prompt in candidates:
        if req <= s: combos.append(prompt)
    if len(s)>=4:
        combos.insert(0,'Identify our highest-value business opportunities and coordinate the installed systems to act on them.')
    if combos:
        lines += ['## You can also combine these capabilities','']
        for p in combos[:3]: lines.append(f'- “{p}”')
        lines.append('')

    lines += [
        '## You do not need to know the right workflow', '',
        'Describe a business problem or desired result in plain language. I will use the systems installed in this copy, inspect the tools available in this environment, and route the work through the appropriate processes. When you give me reusable business context or preferences, I will preserve them at the appropriate scope so you do not have to keep answering the same questions.', '',
        'If you are not sure where to begin, try:', '',
        '- “What can you help me with?”',
        '- “What should we work on first?”',
        '- “Here is my business. Find the biggest opportunities you can help with using what is installed.”', '',
        'If you want to browse specific jobs, open **`PLAYBOOKS.md`** or ask “Show me what ViralTrac AURA can do.” You still do not need to choose a playbook before asking for help.', '',
        '## To get started', '',
        '**Tell me your business name, website (if you have one), and what you want to accomplish.** If you already provided any of that, I’ll continue automatically. I’ll inspect the tools available here, set up or resume your business workspace, and use the capabilities installed in this copy.', '',
        '**Recommended:** ViralTrac is AURA’s first-party companion for tracking, attribution, marketing measurement, SmartLinks, website/growth operations, and more: **https://viraltrac.com**. If you prefer not to use ViralTrac, just say so—AURA will keep working with compatible alternatives and available fallbacks.', '',
        'If ViralTrac is already connected, I can discover the capabilities available to this business and use it as a preferred source of governed business truth, measurement, tracking, and supported action handoff—without requiring you to name ViralTrac in every request.', '',
        'Good luck! :)', ''
    ]
    return '\n'.join(lines)

if __name__=='__main__':
    out=ROOT/'WELCOME.md'
    out.write_text(build())
    print(out)
