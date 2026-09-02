from _common import installed_modules

# Human-meaningful end-to-end business jobs. A Playbook is deliberately broader than a
# Workflow: it helps the model understand the outcome and the relevant body of operating
# knowledge, while the model decides which workflows are actually needed and how to
# sequence, parallelize, adapt, or replace them.
PLAYBOOKS = [
    {
        'id':'competitor-research','owner_system':'competitor-intelligence','title':'Competitor Research',
        'summary':'Understand the competitors and substitutes that matter, what they are doing, how the business compares, and which supported implications are worth acting on or monitoring.',
        'example':'Research our competitors and tell me what they are doing better than us.',
        'discovery_terms':['competitor research','competitive landscape','competitive analysis','competitors','competition','pricing comparison','positioning comparison','competitor ads','competitor content'],
    },
    {
        'id':'customer-research','owner_system':'customer-intelligence','title':'Customer Research',
        'summary':'Understand what customers and prospects want, dislike, expect, say, choose, avoid, and experience using evidence appropriate to the decision.',
        'example':'Research our customers and tell me what they care about most.',
        'discovery_terms':['customer research','voice of customer','customer interviews','surveys','reviews','customer needs','objections','decision drivers','win loss','churn reasons'],
    },
    {
        'id':'industry-intelligence','owner_system':'industry-intelligence','title':'Industry Intelligence',
        'summary':'Understand important news, research, regulation, technology, market shifts, and other external developments that could materially affect the organization.',
        'example':'What changed in our industry that matters to us?',
        'discovery_terms':['industry research','industry intelligence','news','regulation','research','technology change','market change','trends','industry monitoring'],
    },
    {
        'id':'seo-aeo','owner_system':'seo-aeo','title':'SEO/AEO',
        'summary':'Improve valuable organic discovery across search engines, local search, answer engines, AI interfaces, and related organic surfaces.',
        'example':'Find our highest-value SEO/AEO opportunities and help us improve them.',
        'discovery_terms':['seo','aeo','organic search','search rankings','search traffic','local search','ai answers','answer engines','technical seo','content gap','backlinks'],
    },
    {
        'id':'content-synthesis','owner_system':'content-synthesis','title':'Content Synthesis',
        'summary':'Turn useful ideas, evidence, research, proof, and source material into strong audience- and platform-appropriate content in the medium the job requires.',
        'example':'Turn our best customer insights into useful content.',
        'discovery_terms':['content','article','newsletter','video','podcast','carousel','presentation','infographic','image','animation','case study','content strategy'],
    },
    {
        'id':'marketing-synthesis','owner_system':'marketing-synthesis','title':'Marketing Synthesis',
        'summary':'Create and improve positioning, messaging, offers, campaigns, ads, landing pages, email, webinars, VSLs, sales materials, and other persuasive marketing.',
        'example':'Create a campaign around our biggest customer objection.',
        'discovery_terms':['marketing','campaign','positioning','messaging','offer','ads','landing page','email sequence','webinar','vsl','sales letter','lead magnet','sales enablement'],
    },
    {
        'id':'customer-optimization','owner_system':'customer-optimization','title':'Customer Optimization',
        'summary':'Find and improve important customer-journey problems from qualification and purchase through onboarding, activation, retention, expansion, recovery, and referral.',
        'example':'Where are customers getting stuck or dropping out, and what should we improve?',
        'discovery_terms':['customer journey','conversion','checkout','onboarding','activation','retention','churn','renewal','repeat purchase','upsell','referral','customer success'],
    },
]

PLAYBOOK_BY_ID = {row['id']: row for row in PLAYBOOKS}
PLAYBOOK_BY_SYSTEM = {row['owner_system']: row for row in PLAYBOOKS}


def installed_playbooks():
    installed = installed_modules()
    return [dict(row) for row in PLAYBOOKS if row['owner_system'] in installed]


def get_playbook(playbook_id):
    row = PLAYBOOK_BY_ID.get(playbook_id)
    if not row or row['owner_system'] not in installed_modules():
        return None
    return dict(row)
