from _common import ROOT, installed_modules
import json,re

# AURA business areas organize operating knowledge. They are not themselves execution
# services and do not imply that every request needs a Playbook.
OPERATING_AREAS = {
    'competitor-intelligence': {'title':'Competitive Intelligence','summary':'Understand competitors, substitutes, competitive movement, and supported implications.'},
    'customer-intelligence': {'title':'Customer Intelligence','summary':'Understand customers, prospects, needs, language, decisions, and experiences from appropriate evidence.'},
    'industry-intelligence': {'title':'Industry Intelligence','summary':'Understand material external developments in the market, regulation, research, technology, and industry.'},
    'seo-aeo': {'title':'SEO/AEO','summary':'Improve valuable organic discovery across search, answer engines, AI interfaces, local discovery, and related surfaces.'},
    'content-synthesis': {'title':'Content Synthesis','summary':'Turn useful ideas, evidence, and source material into strong audience-appropriate content.'},
    'marketing-synthesis': {'title':'Marketing Synthesis','summary':'Create and improve persuasive strategy, campaigns, offers, and customer-facing marketing assets.'},
    'customer-optimization': {'title':'Customer Optimization','summary':'Improve the customer journey from qualification and purchase through value, retention, expansion, recovery, and referral.'},
}

# Curated end-to-end jobs that are broader than one narrow procedure. A Playbook may name
# an entry Workflow when one authored Workflow already composes the core method. The active
# model remains free to use additional/alternate Workflows and external Skills when useful.
BASE_PLAYBOOKS = [
    {
        'id':'competitor-research','owner_system':'competitor-intelligence','title':'Competitor Research',
        'summary':'Identify the competitors and substitutes that matter, understand what they are doing, compare the business against them, and derive supported implications.',
        'example':'Research our competitors and tell me what they are doing better than us.',
        'entry_workflow':'competitor.analysis.competitive-position',
        'discovery_terms':['competitor research','competitive analysis','competitive landscape','competitors','competition','pricing comparison','positioning comparison','competitor ads','competitor content'],
    },
    {
        'id':'competitor-monitoring','owner_system':'competitor-intelligence','title':'Competitor Monitoring',
        'summary':'Keep important competitive movement current and distinguish observed changes from unsupported assumptions about effectiveness or intent.',
        'example':'Tell me what materially changed with our competitors since we last looked.',
        'entry_workflow':'competitor.intelligence.ecosystem-radar',
        'discovery_terms':['competitor monitoring','competitive monitoring','competitor changes','emerging competitors','competitive movement'],
    },
    {
        'id':'customer-research','owner_system':'customer-intelligence','title':'Customer Research',
        'summary':'Resolve an important customer knowledge need with evidence appropriate to the decision, using the relevant research and analysis workflows.',
        'example':'Research our customers and tell me what they care about most.',
        'entry_workflow':'customer.research.plan',
        'discovery_terms':['customer research','customer needs','customer interviews','surveys','reviews','decision drivers','customer problems','customer expectations'],
    },
    {
        'id':'voice-of-customer','owner_system':'customer-intelligence','title':'Voice of Customer',
        'summary':'Build reusable evidence-backed understanding of the language, pains, desires, objections, outcomes, and decision criteria customers actually express.',
        'example':'Build a voice-of-customer view we can use in our product and marketing work.',
        'entry_workflow':'customer.analysis.voice-of-customer',
        'discovery_terms':['voice of customer','voc','customer language','pains','desires','objections','jobs to be done','customer quotes'],
    },
    {
        'id':'industry-intelligence','owner_system':'industry-intelligence','title':'Industry Intelligence',
        'summary':'Discover and evaluate material news, research, regulation, technology, market shifts, and other external changes that could affect the organization.',
        'example':'What changed in our industry that actually matters to us?',
        'entry_workflow':'industry.intelligence.ecosystem-radar',
        'discovery_terms':['industry research','industry intelligence','market research','news','regulation','research','technology change','market change','trends'],
    },
    {
        'id':'industry-rapid-response','owner_system':'industry-intelligence','title':'Industry Rapid Response',
        'summary':'Build a fast, evidence-backed understanding of a time-sensitive external development and its plausible business implications.',
        'example':'This just happened in our industry. Figure out what it means for us.',
        'entry_workflow':'industry.analysis.rapid-response',
        'discovery_terms':['breaking industry news','rapid response','industry event','urgent industry change','regulatory change'],
    },
    {
        'id':'seo-aeo-growth','owner_system':'seo-aeo','title':'SEO/AEO Growth',
        'summary':'Find and improve the highest-value realistic opportunities for organic discovery across search engines, answer engines, AI interfaces, and local discovery.',
        'example':'Find our highest-value SEO/AEO opportunities and do the useful work to improve them.',
        'entry_workflow':None,
        'discovery_terms':['seo','aeo','organic search','search rankings','organic traffic','local search','ai answers','answer engines','technical seo','content gap','search opportunity'],
    },
    {
        'id':'seo-aeo-experimentation','owner_system':'seo-aeo','title':'SEO/AEO Experimentation and Learning',
        'summary':'Test uncertain SEO/AEO tactics when testing is worthwhile, evaluate the results without overstating causality, and preserve reusable Learning when supported.',
        'example':'Test whether this SEO/AEO tactic actually helps us and learn from the result.',
        'entry_workflow':'seo.learning.strategy-experiment-design',
        'discovery_terms':['seo experiment','aeo experiment','organic experiment','seo test','seo learning','measure seo change'],
    },
    {
        'id':'content-strategy','owner_system':'content-synthesis','title':'Content Strategy and Synthesis',
        'summary':'Turn audience context, evidence, ideas, performance signals, and communication goals into a strong content approach before or across specific formats.',
        'example':'Figure out what content we should create and why, then turn the best ideas into useful work.',
        'entry_workflow':'content.intake.content-brief',
        'discovery_terms':['content strategy','content plan','content ideas','content research','content performance','trending content','creator research'],
    },
    {
        'id':'marketing-strategy','owner_system':'marketing-synthesis','title':'Marketing Strategy and Messaging',
        'summary':'Develop or improve positioning, messaging, value proposition, mechanism, proof, objection handling, and offer presentation around current customer and business truth.',
        'example':'Improve how we position and explain this offer so qualified buyers understand why it matters.',
        'entry_workflow':'marketing.strategy.messaging',
        'discovery_terms':['marketing strategy','positioning','messaging','value proposition','mechanism','proof','objections','offer presentation'],
    },
    {
        'id':'campaign-development','owner_system':'marketing-synthesis','title':'Campaign Development',
        'summary':'Build a coherent campaign concept and the useful persuasive work needed to carry it across the relevant customer-facing surfaces.',
        'example':'Build a campaign around our strongest customer insight and offer.',
        'entry_workflow':'marketing.campaigns.campaign-concept',
        'discovery_terms':['campaign','campaign strategy','campaign concept','marketing campaign','launch campaign'],
    },
    {
        'id':'customer-journey-optimization','owner_system':'customer-optimization','title':'Customer Journey Optimization',
        'summary':'Understand the journey, identify the most important progression problem, diagnose the likely cause, improve it, and evaluate what changed.',
        'example':'Figure out where customers are getting stuck and improve the most important part of the journey.',
        'entry_workflow':'customer-optimization.diagnosis.bottleneck-prioritization',
        'discovery_terms':['customer journey','journey optimization','funnel optimization','bottleneck','drop off','conversion','customer experience'],
    },
    {
        'id':'retention-and-churn','owner_system':'customer-optimization','title':'Retention and Churn',
        'summary':'Understand why customers leave or fail to realize value, improve the relevant experience, and evaluate durable retention rather than manipulating short-term staying behavior.',
        'example':'Figure out why customers are churning and what we should improve.',
        'entry_workflow':'customer-optimization.intervention.retention',
        'discovery_terms':['retention','churn','renewal','customer success','activation','adoption','time to value'],
    },
]


def _registry_rows():
    path=ROOT/'generated/contract-registry.json'
    if not path.exists():return []
    try:return json.loads(path.read_text(encoding='utf-8')).get('contracts',[])
    except Exception:return []


def _slug(value):
    return re.sub(r'[^a-z0-9]+','-',str(value or '').lower()).strip('-')


def _production_playbooks(registry=None):
    rows=registry if registry is not None else _registry_rows();out=[]
    for row in rows:
        if row.get('artifact_role')!='customer_facing_production_root':continue
        owner=row.get('owner_system');workflow_id=row.get('id')
        if owner not in OPERATING_AREAS or not workflow_id:continue
        title=str(row.get('title') or workflow_id).strip();purpose=' '.join(str(row.get('purpose') or '').split())
        suffix=workflow_id.split('.')[-1].replace('-',' ')
        out.append({
            'id':f"{_slug(owner)}-{_slug(suffix)}",'owner_system':owner,'title':title,
            'summary':purpose or f'Produce a complete, usable {suffix} at the quality and truth standard required by the request.',
            'example':f'Create the {suffix} we need for this job.',
            'entry_workflow':workflow_id,
            'discovery_terms':sorted(set([suffix,title.lower(),workflow_id.replace('.',' ').replace('-',' ')])),
            'generated_from_workflow':True,
        })
    return sorted(out,key=lambda row:(row['owner_system'],row['title'].lower(),row['id']))


def all_playbooks(registry=None):
    rows=[dict(row) for row in BASE_PLAYBOOKS]
    seen={row['id'] for row in rows}
    for row in _production_playbooks(registry):
        if row['id'] not in seen:rows.append(row);seen.add(row['id'])
    return rows


def installed_playbooks(registry=None):
    installed=installed_modules()
    return [row for row in all_playbooks(registry) if row['owner_system'] in installed]


def playbooks_for_system(owner_system,registry=None):
    return [row for row in installed_playbooks(registry) if row['owner_system']==owner_system]


def get_playbook(playbook_id,registry=None):
    return next((row for row in installed_playbooks(registry) if row['id']==playbook_id),None)
