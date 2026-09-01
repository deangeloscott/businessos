#!/usr/bin/env python3
"""Generate plain-language human playbook navigation from canonical AURA metadata.

The contracts/process maps remain authoritative. These pages are views for people, not a
second workflow definition.
"""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs' / 'playbooks'

PLAIN = {
    'core': {
        'name': 'AURA Core',
        'summary': 'Keep organizational context, evidence, decisions, continuity, and reusable operating knowledge organized so capable AI can work from what the organization already knows.',
        'ask': 'What should we work on first?'
    },
    'competitor-intelligence': {
        'name': 'Competitor Intelligence',
        'summary': 'Find the competitors that matter, study what they do, compare them with the business, and watch for important changes.',
        'ask': 'What are our competitors doing better than us?'
    },
    'customer-intelligence': {
        'name': 'Customer Intelligence',
        'summary': 'Learn what customers want, dislike, expect, say, buy, avoid, and experience using real customer evidence.',
        'ask': 'What do customers care about most when choosing us?'
    },
    'industry-intelligence': {
        'name': 'Industry Intelligence',
        'summary': 'Track news, research, regulation, technology, market changes, and other outside developments that could matter to the business.',
        'ask': 'What changed in our industry that matters to us?'
    },
    'seo-aeo': {
        'name': 'SEO/AEO',
        'summary': 'Improve how the business is found in search engines, local search, AI answers, and other organic discovery surfaces.',
        'ask': 'What are our biggest SEO/AEO opportunities?'
    },
    'content-synthesis': {
        'name': 'Content Synthesis',
        'summary': 'Turn useful ideas, research, proof, and source material into content made for the right audience, format, and platform.',
        'ask': 'Turn our best customer insights into useful content.'
    },
    'marketing-synthesis': {
        'name': 'Marketing Synthesis',
        'summary': 'Create and improve positioning, messaging, offers, ads, landing pages, email, webinars, VSLs, and other persuasive marketing.',
        'ask': 'Create a campaign around our biggest customer objection.'
    },
    'customer-optimization': {
        'name': 'Customer Optimization',
        'summary': 'Find and improve problems in the customer journey, from conversion and purchase through onboarding, retention, repeat purchase, expansion, and referral.',
        'ask': 'Where are customers getting stuck or dropping out?'
    },
}


RESULT_OVERRIDES = {
    'core.diagnosis.business-problem': 'Find the most likely causes of a broad business problem and decide what should be investigated or done next before jumping to a fix.',
    'competitor.discovery.entity-resolution': 'Make sure websites, social profiles, review pages, ad profiles, and other sources belong to the correct competitor before combining the evidence.',
    'competitor.analysis.strength-weakness': 'Identify specific competitor strengths and weaknesses that matter to customers and the business.',
    'content.intelligence.creative-pattern-extraction': 'Find the reusable idea or structure behind strong content without copying the original creator.',
    'content.intelligence.cross-niche-pattern-transfer': 'Adapt a useful content pattern from another niche or category without copying the original content.',
    'customer.evidence-collection.surveys': 'Design, run, and interpret a survey with enough reliable responses for the question being asked.',
    'customer.analysis.objections': 'Identify the objections that stop or delay customers and understand where each objection matters.',
    'customer.analysis.decision-drivers': 'Identify what makes customers choose, delay, switch, or decide not to buy.',
    'customer.analysis.insight-refresh': 'Keep customer insights current and update them when new evidence conflicts with what was previously believed.',
    'customer-optimization.journey.instrumentation': 'Determine whether customer-journey transitions can be measured reliably and improve the real source instrumentation when that work is requested.',
    'customer-optimization.instrumentation.data-quality': 'Check that customer-journey tracking and measurements are reliable enough to use for decisions.',
    'industry.monitoring.news': 'Find important news developments that could affect the business.',
    'industry.monitoring.regulation': 'Find and explain important regulation or standards changes that could affect the business.',
    'industry.event.detect': 'Preserve an important industry event with enough evidence and context for later verification, analysis, and reuse.',
    'industry.analysis.event-verification': 'Check the important facts about an industry event before using it for business decisions.',
    'industry.analysis.materiality': 'Decide whether an industry event is important enough to change a business decision or action.',
    'industry.analysis.business-impact': 'Explain the specific ways an industry event could affect this business.',
    'industry.analysis.rapid-response': 'Quickly verify a time-sensitive industry event and turn it into useful business guidance.',
    'marketing.strategy.mechanism': 'Explain in a credible, easy-to-understand way why or how the product, service, or offer works.',
    'marketing.strategy.objection-handling': 'Address the important concerns that may stop a customer from buying.',
}

GROUP_NAMES = {
    'adaptation': 'Adaptation',
    'adoption': 'Adoption',
    'ads': 'Advertising',
    'aeo': 'AI / answer-engine visibility',
    'analysis': 'Analysis',
    'assets': 'Marketing assets',
    'bootstrap': 'Setup and starting state',
    'campaigns': 'Campaigns',
    'checkout': 'Checkout',
    'context': 'Business context',
    'conversion': 'Conversion',
    'coordination': 'Coordination',
    'data': 'Business data',
    'diagnosis': 'Diagnosis',
    'discovery': 'Discovery',
    'email': 'Email',
    'event': 'Events and changes',
    'evidence-collection': 'Evidence collection',
    'execution': 'Execution',
    'expansion': 'Expansion',
    'experimentation': 'Experiments',
    'handoff': 'Handoffs',
    'incident': 'Incidents and recovery',
    'instrumentation': 'Tracking and instrumentation',
    'intake': 'Intake and briefs',
    'intelligence': 'Intelligence and research',
    'intervention': 'Customer journey improvements',
    'journey': 'Customer journey',
    'landing-page': 'Landing pages',
    'learning': 'Learning and improvement',
    'measurement': 'Measurement',
    'monitoring': 'Monitoring',
    'offer': 'Offers',
    'onboarding': 'Onboarding',
    'opportunity': 'Opportunities',
    'planning': 'Planning',
    'production': 'Content production',
    'publishing': 'Publishing',
    'qa': 'Quality checks',
    'referral': 'Referrals',
    'rendering': 'Rendering',
    'renewal': 'Renewals',
    'repeat-purchase': 'Repeat purchase',
    'research': 'Research planning',
    'retention': 'Retention',
    'scheduling': 'Scheduling',
    'service-recovery': 'Service recovery',
    'social': 'Social marketing',
    'source-mapping': 'Source mapping',
    'strategy': 'Strategy',
    'vsl': 'Video sales letters',
    'webinar': 'Webinars',
}

ORDER = [
    'core','competitor-intelligence','customer-intelligence','industry-intelligence',
    'seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'
]


def load_json(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


def rel_link(from_file: Path, target: str) -> str:
    import os
    return Path(os.path.relpath(ROOT/target, from_file.parent)).as_posix()


def clean_result(text: str) -> str:
    """Small presentation-only substitutions; canonical contract text is untouched."""
    s = ' '.join((text or '').split())
    swaps = [
        ('evidence-backed', 'evidence-based'),
        ('decision-relevant', 'relevant'),
        ('material changes', 'important changes'),
        ('material change', 'important change'),
        ('observable', 'visible'),
        ('acquisition funnels', 'customer acquisition funnels'),
    ]
    for a,b in swaps: s=s.replace(a,b)
    return s


def system_contracts(registry, system):
    return [c for c in registry if c.get('owner_system') == system]


def playbooks_for(registry, system):
    return [c for c in system_contracts(registry,system) if c.get('type') == 'playbook']


def process_map(system):
    p = ROOT/'core/process-map.json' if system == 'core' else ROOT/'systems'/system/'process-map.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'activities':[]}


def contract_map(registry): return {c['id']:c for c in registry}


def write_root(registry, installed):
    total = sum(len(playbooks_for(registry,s)) for s in installed)
    lines = [
        '# What AURA Can Do', '',
        'This is the plain-language guide to the work AURA can help with.', '',
        '**You do not need to choose a playbook before asking for help.** Tell the AI what you want to accomplish in normal language. AURA can supply relevant organizational memory and reusable operating knowledge; the active model/user chooses the method. Use this guide when you want to browse what is possible or understand how a job works.', '',
        f'This copy currently includes **{total} detailed playbooks** across the installed AURA areas. The contracts and process maps remain the source of truth; this guide is only a simpler view of them.', '',
        '## How to use this guide', '',
        '- **Just ask:** “Research our competitors and tell me what matters.”',
        '- **Browse an area:** open one of the sections below.',
        '- **Ask about a playbook:** “Show me how Review Intelligence works.”',
        '- **Ask for the detailed method:** “Show me the steps, inputs, outputs, and evidence rules for that playbook.”', '',
        '## AURA areas', ''
    ]
    for s in ORDER:
        if s not in installed: continue
        info=PLAIN[s]; count=len(playbooks_for(registry,s))
        page='docs/playbooks/core.md' if s=='core' else f'docs/playbooks/{s}.md'
        lines += [f"### [{info['name']}]({page})", '', info['summary'], '', f'**{count} detailed playbooks.**', '', f'*Try:* “{info["ask"]}”', '']
    lines += [
        '## What a playbook means', '',
        'A playbook is reusable operating knowledge for a specific kind of job. It can tell the AI:', '',
        '1. **When the method is useful.**',
        '2. **What information or evidence it needs.**',
        '3. **Which capabilities may help.**',
        '4. **What substantive work the method includes.**',
        '5. **What durable results or evidence may be worth remembering.**',
        '6. **What quality or verification checks materially define good work.**', '',
        'The active model/user may combine relevant playbook knowledge when one business request spans several kinds of work. The playbooks do not form an internal service or routing graph.', '',
    ]
    if 'customer-intelligence' in installed:
        lines += [
            '## Worked example', '',
            '### [Research public reviews and conversations](docs/playbooks/examples/research-public-reviews.md)', '',
            'See a plain-language example of how a capable AI can use AURA context and operating knowledge to find reviews, preserve useful source text and screenshots when allowed, remove duplicates, analyze themes and customer language, save reusable evidence, and reuse relevant findings directly in later work.', '',
        ]
    lines += [
        '## For advanced users', '',
        '- `TASK-NAVIGATOR.md` shows the main activities and their entry contracts.',
        '- `PLAYBOOK-INDEX.md` lists the contract-level playbooks directly from contract metadata.',
        '- `generated/contract-registry.json` and `generated/process-map-registry.json` are machine-readable indexes.',
        '- Each contract `CONTEXT.md` contains the authoritative detailed operating instructions.', '',
    ]
    (ROOT/'PLAYBOOKS.md').write_text('\n'.join(lines),encoding='utf-8')


def write_domain(registry, system):
    info=PLAIN[system]; cmap=contract_map(registry); pmap=process_map(system)
    outfile=DOCS/('core.md' if system=='core' else f'{system}.md')
    plays=playbooks_for(registry,system)
    lines=[f"# {info['name']} Playbooks",'',info['summary'],'',
           '**You can ask for the outcome in normal language.** You do not need to know the names below. This page is here so you can see what is possible.','',
           f"*Example:* “{info['ask']}”",'', '## Common jobs','']
    seen=set()
    for a in pmap.get('activities',[]):
        cid=a.get('entry_contract'); c=cmap.get(cid,{})
        title=c.get('title') or a.get('id','').replace('-',' ').title()
        result=RESULT_OVERRIDES.get(cid, clean_result(a.get('result','')))
        link=rel_link(outfile,c.get('path')) if c.get('path') else None
        title_md=f'[{title}]({link})' if link else title
        lines.append(f'- **{title_md}** — {result}')
        if cid: seen.add(cid)
    lines += ['', '## More detailed playbooks','',
              'These are smaller, specific playbooks whose knowledge may help inside the larger jobs above. The names are kept simple here; open the linked contract or ask the AI to explain one if you want the exact method.','']
    groups={}
    for c in plays:
        parts=c['id'].split('.')
        group=parts[1] if len(parts)>2 else 'other'
        groups.setdefault(group,[]).append(c)
    for group in sorted(groups,key=lambda x: GROUP_NAMES.get(x,x).lower()):
        lines += [f"### {GROUP_NAMES.get(group,group.replace('-',' ').title())}",'']
        for c in sorted(groups[group],key=lambda x:x.get('title','')):
            link=rel_link(outfile,c['path'])
            marker=' *(main entry playbook)*' if c['id'] in seen else ''
            lines.append(f"- [{c.get('title',c['id'])}]({link}){marker}")
        lines.append('')
    lines += ['## Want to see exactly how one works?','',
              'Ask the AI something like:', '',
              f'> “Show me the exact method for {plays[0].get("title") if plays else "this playbook"}, including what it reads, what it may save, and the important quality checks.”','',
              'The linked contract is the authoritative version. This page is only a simpler map for people.','']
    outfile.write_text('\n'.join(lines),encoding='utf-8')


def write_review_example(registry, installed):
    exdir=DOCS/'examples'; exdir.mkdir(parents=True,exist_ok=True)
    out=exdir/'research-public-reviews.md'
    if 'customer-intelligence' not in installed:
        if out.exists(): out.unlink()
        return
    cmap=contract_map(registry)
    ids=[
      'customer.evidence-collection.reviews',
      'customer.evidence-collection.public-conversation',
      'customer.analysis.before-after-proof',
      'core.intelligence.register-proof',
    ]
    links=[]
    for cid in ids:
        c=cmap.get(cid)
        if c: links.append((c['title'],rel_link(out,c['path']),cid))
    lines=['# Example Playbook Flow: Research Public Reviews and Conversations','',
           'This example shows how a capable AI can use AURA memory and operating knowledge for one user-level request. It is **not a second set of rules**. The linked contracts remain authoritative.','',
           '## What the user can say','',
           '> “Research what customers are saying about us and our competitors. Find the biggest complaints, praise, objections, and useful customer language.”','',
           'The user does not need to name websites, tools, folders, contracts, or AURA systems unless they want to.','',
           '## How the work can proceed','',
           '### 1. Define what the research needs to answer','',
           'The AI uses relevant organizational context, the market, product/service, competitors, time window, and current decision to judge what evidence is worth collecting. It should not search every possible source just because a source exists.','',
           '### 2. Find the right review and conversation sources','',
           'Depending on the business, useful sources might include Google Business Profile, Trustpilot, Yelp, Reddit, industry review sites, social platforms, marketplaces, app stores, owned reviews, support data, or other relevant public/first-party sources. These are examples, not a fixed checklist.','',
           '### 3. Collect allowed source evidence','',
           'For each useful review or public conversation, the active model/harness first opens or retrieves the underlying item. A search result or URL can help find evidence, but it is not enough by itself for an important supported conclusion. Preserve the information that is actually available and allowed, such as:', '',
           '- review/comment text', '- rating', '- date or timestamp', '- source/platform', '- page or permalink', '- product, service, location, or thread context', '- public author label only when it is needed', '- useful public context such as thread or engagement information', '',
           '### 4. Preserve a screenshot or snapshot when it adds value','',
           'Useful source text and metadata should normally remain searchable and checkable later. A screenshot is extra preservation, not a requirement for every review. When the source permits it and visual context, proof value, or page-change risk matters, the active model/harness can capture the original page/review and link it to the same source evidence.','',
           '### 5. Remove duplicates','',
           'Remove exact duplicates, syndicated copies, reposts, and repeated captures while keeping genuinely different people or meaningful follow-up comments separate.','',
           '### 6. Analyze each piece of evidence','',
           'The AI can extract:', '',
           '- praise', '- complaints', '- pain points', '- desired outcomes', '- expectations', '- objections', '- comparisons', '- buying or switching signals', '- use cases', '- before/after statements', '- feature or service requests', '- exact customer wording', '- sentiment about specific parts of the experience', '',
           'Direct customer statements stay separate from interpretation. If the original evidence was not preserved or cannot be reliably revisited, the interpretation stays provisional instead of being marked as fully supported.','',
           '### 7. Look for patterns across the evidence','',
           'Compare reviews and conversations to find recurring themes, emerging issues, differences between products/locations/segments, and contradictions with other evidence such as interviews, support conversations, or sales calls.','',
           '### 8. Save reusable business knowledge','',
           'Useful evidence can become linked AURA objects instead of disappearing inside one chat:', '',
           '- **SourceRecord** — where the evidence came from', '- **Asset** — a screenshot or snapshot when one was captured', '- **Observation** — what was directly observed', '- **Insight** — a supported pattern or conclusion', '- **ProofRecord** — reusable proof/testimonial evidence when the claim and permission rules support it', '',
           '### 9. Reuse useful findings directly','',
           'One finding can matter to several kinds of work without being copied into separate truth stores or routed through internal AURA services. The active model can apply the same supported evidence wherever it is relevant:', '',
           '- a repeated complaint can inform customer understanding',
    ]
    if 'competitor-intelligence' in installed:
        lines.append('- a competitor complaint can inform competitor analysis')
    if 'customer-optimization' in installed:
        lines.append('- checkout or service friction can inform customer-journey improvement')
    if 'marketing-synthesis' in installed:
        lines.append('- strong customer language can inform marketing')
    if 'content-synthesis' in installed:
        lines.append('- supported proof can be reused in content when relevant')
    if 'seo-aeo' in installed:
        lines.append('- supported proof can be reused in SEO/AEO when relevant')
    lines += ['',
           '### 10. Stop when more collection is unlikely to change the decision','',
           'Collect enough evidence to answer the current question responsibly. Do not keep researching simply because more data is available. If the organization wants ongoing monitoring, AURA may preserve the monitoring intent and prior evidence; the active host/runtime owns any actual recurring schedule or future check.','',
           '## What the user should get back','',
           'The final result should be useful to a business person, not just a pile of saved reviews. A good result could include:', '',
           '- the most important themes', '- what customers repeatedly praise or dislike', '- useful exact customer language', '- differences between the business and competitors', '- important uncertainties or evidence gaps', '- links/citations back to the source evidence', '- saved screenshots where useful and allowed', '- the best next action supported by the evidence', '',
           '## Authoritative AURA playbooks','']
    for title,link,cid in links:
        lines.append(f'- [{title}]({link}) — `{cid}`')
    lines += ['', 'These contracts define the actual operating knowledge. This page only explains the flow in simpler language.','']
    out.write_text('\n'.join(lines),encoding='utf-8')


def main():
    DOCS.mkdir(parents=True,exist_ok=True)
    reg=load_json('generated/contract-registry.json')['contracts']
    inst=load_json('INSTALLATION.json')
    installed=[s for s in ORDER if s in inst.get('installed_modules',[])]
    # Remove generated domain pages that do not belong to this edition.
    valid={'core.md'} | {f'{s}.md' for s in installed if s!='core'}
    generated_names={'core.md'} | {f'{s}.md' for s in PLAIN if s != 'core'}
    for p in DOCS.glob('*.md'):
        if p.name in generated_names and p.name not in valid:
            p.unlink()
    write_root(reg,installed)
    for s in installed: write_domain(reg,s)
    write_review_example(reg,set(installed))
    print(f'Generated human playbook catalog for {len(installed)} installed areas.')

if __name__=='__main__': main()