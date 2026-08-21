#!/usr/bin/env python3
import argparse,json,re
from _common import ROOT, installed_modules

HINTS=[
 (r'\b(set ?up|initialize|initialise|bootstrap|onboard).*(business|brand)|\b(business|brand).*(website|url).*(set ?up|initialize|bootstrap)', 'core.context.bootstrap-business'),
 (r'\b(brand voice|brand style|visual identity|brand guidelines|brand preferences|how .*brand.*look|how .*brand.*sound)', 'core.context.brand-profile'),
 (r'\bpublic (comments?|conversation|discussion)|forum discussions?.*(product|brand)|comments?.*(about|mention).*(product|brand)','customer.evidence-collection.public-conversation'),
 (r'\b(testimonial|before.?and.?after|before.?after).*(proof|review)|extract.*proof.*review','customer.analysis.before-after-proof'),
 (r'\btrending.*(creator|content)|creator.*content.*(trend|ideas?)','content.intelligence.trending-content-discovery'),
 (r'\b(why|learn why).*(viral|creator).*(post|content).*(work)|creative pattern','content.intelligence.creative-pattern-extraction'),
 (r'\bturn.*(comment|review|proof|news|signal).*(content|post|video|idea)','content.opportunity.signal-to-content'),
 (r'\binfographic\b','content.production.infographic'),
 (r'\bgif\b','content.production.gif'),
 (r'\b(ai )?avatar video\b','content.production.avatar-video'),
 (r'\b(monitor|track).*(social discussion|rss).*(industry|market|category)|industry.*social discussion','industry.monitoring.social-discussion'),
 (r'\b(what .*news.*means?|news.*for our audience|industry.*means.*audience)','industry.analysis.audience-implication'),
 (r'\b(win.?loss|lost deals?|losing deals?|why .* (won|lost) .*deal)', 'customer.analysis.win-loss'),
 (r'\b(objection|sales objection)s?\b','customer.analysis.objections'),
 (r'\b(churn reason|why .* (churn|cancel)|reason.*cancel)', 'customer.analysis.churn'),
 (r'\bcompetitor.*pric|pricing.*competitor','competitor.analysis.pricing'),
 (r'\bcompetitor.*position|positioning.*competitor','competitor.analysis.positioning'),
 (r'\bcompetitor.*(tactic|working)|what .*competitor.*work','competitor.analysis.tactic-validation'),
 (r'\b(regulation|regulatory|law|legislation)\b','industry.monitoring.regulation'),
 (r'\b(technology|platform|ai).*(trend|shift|change|development)','industry.monitoring.technology'),
 (r'\b(industry|market|category).*(trend|news|change)|\btrend.*industry\b','industry.monitoring.market'),
 (r'\b(rank|ranking|visibility).*(drop|fall|declin|lost)|organic.*(drop|declin)','seo.diagnosis.detectors.ranking-decay'),
 (r'\b(ai answer|ai citation|cited|citation).*(missing|not|gap|visibility)|not .*cited','seo.diagnosis.detectors.ai-citation-gap'),
 (r'\bindex(ed|ing)?\b.*(problem|issue|not|missing)','seo.diagnosis.detectors.indexing'),
 (r'\blanding page\b','marketing.assets.landing-page'),
 (r'\b(vsl|video sales letter)\b','marketing.assets.vsl'),
 (r'\bwebinar\b','marketing.assets.webinar'),
 (r'\b(advertorial)\b','marketing.assets.advertorial'),
 (r'\b(sales letter)\b','marketing.assets.sales-letter'),
 (r'\bcheckout\b','customer-optimization.intervention.checkout'),
 (r'\bonboarding\b','customer-optimization.intervention.onboarding'),
 (r'\bactivation\b','customer-optimization.intervention.activation'),
 (r'\b(reduce|prevent|lower).*(churn)|churn.*(reduce|prevent)','customer-optimization.intervention.churn'),
 (r'\brenewal(s)?\b','customer-optimization.intervention.renewal'),
 (r'\breferral(s)?\b','customer-optimization.intervention.referral'),
 (r'\bcarousel|slideshow\b','content.production.carousel'),
 (r'\bshort[- ]?form video|reel|tiktok|youtube short','content.production.short-video'),
 (r'\blong[- ]?form video|youtube video\b','content.production.long-video'),
 (r'\blinkedin\b','content.production.linkedin'),
 (r'\bnewsletter\b','content.production.newsletter'),
 (r'\bpodcast\b','content.production.podcast'),
]
SYSTEM_RULES={
 'customer-intelligence':[(5,r'\b(customer|buyer|prospect)s?\b.*\b(want|need|believe|fear|complain|language|question|reason|choose|reject)'),(6,r'\b(objection|win.?loss|lost deal|interview|voice of customer|feature request|testimonial|review)')],
 'competitor-intelligence':[(7,r'\b(competitor|competitive|rival)s?\b'),(4,r'\b(pricing|packaging|positioning|offer|funnel|messaging|tactic|whitespace)\b')],
 'industry-intelligence':[(7,r'\b(industry|regulation|regulatory|legislation|news|trend|research|technology shift|market change|category change)\b')],
 'seo-aeo':[(7,r'\b(seo|search|organic|ranking|serp|indexing|backlink|google search|ai citation|ai answer)\b')],
 'content-synthesis':[(5,r'\b(content|article|video|carousel|slideshow|linkedin|newsletter|podcast|presentation|image|graphic|animation|infographic|gif|creator)\b'),(3,r'\b(create|make|turn|adapt|repurpose|produce|write|trending)\b')],
 'marketing-synthesis':[(7,r'\b(marketing|landing page|vsl|webinar|advertorial|sales letter|campaign|ad copy|lead magnet|persuasion|value proposition|offer presentation)\b'),(3,r'\b(convert|sell|commercial|lead|demo|purchase)\b')],
 'customer-optimization':[(7,r'\b(checkout|onboarding|activation|retention|renewal|repeat purchase|upsell|cross.?sell|expansion|referral|no.?show|time.?to.?value|adoption|customer journey)\b'),(5,r'\b(reduce|prevent|improve).*(churn|abandon|drop.?off)')]
}

def _owner_for_contract_id(cid):
    if cid.startswith('customer-optimization.'): return 'customer-optimization'
    if cid.startswith('customer.'): return 'customer-intelligence'
    if cid.startswith('competitor.'): return 'competitor-intelligence'
    if cid.startswith('industry.'): return 'industry-intelligence'
    if cid.startswith('seo.'): return 'seo-aeo'
    if cid.startswith('content.'): return 'content-synthesis'
    if cid.startswith('marketing.'): return 'marketing-synthesis'
    if cid.startswith('core.'): return 'core'
    return None

def _index():
    idx=json.loads((ROOT/'generated/route-index.json').read_text())
    return idx,{r['contract_id']:r for r in idx}

def route(task, top=5):
    idx,contracts=_index();q=task.lower();words=set(re.findall(r'[a-z0-9]{2,}',q))
    available_owners={r['owner_system'] for r in idx}
    for pat,cid in HINTS:
        if re.search(pat,q,re.I):
            if cid in contracts:
                r=contracts[cid]
                return [{'score':100,'system_score':100,'contract_id':cid,'owner_system':r['owner_system'],'status':'available','reason':'matched high-confidence task pattern'}]
            owner=_owner_for_contract_id(cid)
            if owner and owner not in available_owners:
                return [{'score':100,'system_score':100,'contract_id':None,'owner_system':owner,'status':'module-not-installed','reason':f'{owner} owns this task but is not installed in this distribution'}]
    scores={k:0 for k in SYSTEM_RULES}
    for owner,rules in SYSTEM_RULES.items():
        for w,pat in rules:
            if re.search(pat,q,re.I):scores[owner]+=w
    if re.search(r'\b(lost deal|losing deal|why .*lost|win.?loss)',q):scores['customer-intelligence']+=10
    if re.search(r'why .*customer.*(cancel|churn)|reason.*(cancel|churn)',q):scores['customer-intelligence']+=8
    if re.search(r'(reduce|prevent|lower|improve).*(churn|retention|renewal)',q):scores['customer-optimization']+=8
    owner=max(scores,key=scores.get)
    if scores[owner]>0 and owner not in available_owners:
        return [{'score':scores[owner],'system_score':scores[owner],'contract_id':None,'owner_system':owner,'status':'module-not-installed','reason':f'{owner} is the semantic owner but is not installed in this distribution'}]
    candidate=idx if scores[owner]==0 else [r for r in idx if r['owner_system']==owner]
    scored=[]
    for r in candidate:
        overlap=len(words & set(r['tokens']));score=overlap*2
        for token in re.findall(r'[a-z0-9]{3,}',r['contract_id'].lower().replace('-',' ')):
            if token in words:score+=1
        if score:scored.append((score,r))
    if not scored and candidate:
        fallback=next((r for r in candidate if 'relevance-evaluation' in r['contract_id']),candidate[0]);scored=[(1,fallback)]
    out=[]
    for score,r in sorted(scored,key=lambda x:(x[0],x[1]['contract_id']),reverse=True)[:top]:
        out.append({'score':score,'system_score':scores.get(r['owner_system'],0),'contract_id':r['contract_id'],'owner_system':r['owner_system'],'status':'available','reason':'semantic owner selected, then contract lexical match'})
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('task');p.add_argument('--top',type=int,default=5);a=p.parse_args()
    for row in route(a.task,a.top):print(json.dumps(row))
if __name__=='__main__':main()
