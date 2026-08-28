#!/usr/bin/env python3
import argparse,json,re
from _common import ROOT, installed_modules

# Compound outcome patterns must be checked before direct artifact keywords so a request
# such as research news -> LinkedIn is not collapsed into only the LinkedIn production step.
COMPOUND_HINTS=[
 (r'\b(find|research|learn|understand|analy[sz]e).*(market|customers?|competitors?|industry|news|trends?).*(turn|create|make|use|into).*(content|campaign|marketing|posts?|linkedin|video|assets?)|\bturn.*(research|insights?|intelligence|news|findings?).*(content|campaign|marketing|posts?|linkedin|video)', 'core.coordination.multi-domain-request'),
 # Search-led production is inherently a composition: SEO/AEO owns discovery requirements
 # and delegates the customer-facing artifact instead of letting an artifact noun such as
 # "landing page" silently transfer the whole job to Marketing.
 (r'\b(create|write|produce|build|make|publish(?:-ready)?).*(organic|seo|serp|ai[- ]?answer|ai citation|google search).*(page|landing page|article|content|asset)|\b(organic|seo|serp|ai[- ]?answer|ai citation|google search).*(page|landing page|article|content|asset).*(create|write|produce|build|make|publish)', 'core.coordination.multi-domain-request'),
]

# High-confidence direct job patterns. These bypass semantic resolution only when the
# user has named a sufficiently clear business job/outcome.
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
 (r'^(?!.*\b(reduce|prevent|lower|improve)\b.*\bchurn\b).*?(?:\bcustomers?\b.*\b(?:keep |are |were )?(?:leav|leaving|left|cancel|cancelling|canceling|churn|churning)\b|\bwhy\b.*\b(?:customers?|people|users?)\b.*\b(?:leav|leaving|left|cancel|cancelling|canceling|churn|churning)\b)', 'customer.analysis.churn'),
 (r'\b(objection|sales objection)s?\b','customer.analysis.objections'),
 (r'\b(churn reason|why .* (churn|cancel)|reason.*cancel)', 'customer.analysis.churn'),
 (r'\bcompetitor.*(pric|charg|cost)|pricing.*competitor','competitor.analysis.pricing'),
 (r'\bcompetitor.*position|positioning.*competitor','competitor.analysis.positioning'),
 (r'\bcompetitor.*(tactic|working|doing better)|what .*competitor.*work|find out.*competitor.*better','competitor.analysis.tactic-validation'),
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
 (r'^(?!.*\boffer presentation\b).*\b(slide deck|pitch deck|executive briefing|presentation)\b','content.production.presentation'),
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

# Broad request patterns belong to Core orchestration rather than whichever atomic
# contract happens to share the most words.
CORE_HINTS=[
 (r'\b(traffic|leads?).*(increas|grow|grew|growing|up).*(but|while|yet).*(revenue|sales|customers?).*(didn.t|did not|isn.t|is not|aren.t|are not|flat|stagn|declin|down|not growing)|\b(revenue|sales|profit|growth|conversion|marketing).*(not growing|isn.t growing|is not growing|not working|flat|stagn|declin|down|dropped|drop).*(why|wrong|figure|diagnos|stuck)?|\b(why|figure out|diagnos|what.*holding back|where.*stuck).*(revenue|sales|profit|growth|business|marketing)|\bfigure out what( is|.s) wrong\b|\b(lots|plenty|more).*(traffic|leads).*(few|no|less).*(customers?|sales|revenue)', 'core.diagnosis.business-problem'),
 (r'\b(what should (we|i) (work on|do|focus on)|what (we|i) should do next|what (should|do) (we|i) do next|where should (we|i) start|what.*work on first|next best (work|thing)|highest[- ]value (opportunit|thing)|biggest (growth )?opportunit|best opportunit|what.*focus on.*(quarter|month|year)).*', 'core.opportunity.discover-next-best-work'),
 (r'\b(i|we) want to (grow|increase|improve|scale).*(business|revenue|profit|sales|profitable)|\b(grow|increase|improve|scale).*(business|revenue|profit|sales).*(profitably|overall|best|next)?|\b(help|help me|help us).*(improve|grow).*(business|revenue|profit|sales)|\bhow can (we|i).*(make more money|grow|increase revenue|increase profit)', 'core.opportunity.discover-next-best-work'),
]

SYSTEM_RULES={
 'customer-intelligence':[(5,r'\b(customer|buyer|prospect)s?\b.*\b(want|need|believe|fear|complain|language|question|reason|choose|reject|leave|leaving|cancel|churn)'),(6,r'\b(objection|win.?loss|lost deal|interview|voice of customer|feature request|testimonial|review|churn reason)')],
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

def _resolved_row(contracts,cid,reason,score=100,system_score=100,**extra):
    if cid in contracts:
        r=contracts[cid]
        return {'score':score,'system_score':system_score,'contract_id':cid,'owner_system':r['owner_system'],'status':'available','reason':reason,**extra}
    owner=_owner_for_contract_id(cid)
    return {'score':score,'system_score':system_score,'contract_id':None,'owner_system':owner,'status':'module-not-installed','reason':f'{owner} owns this task but is not installed in this distribution',**extra}

def _semantic_fallback(contracts,reason,candidate_owner=None,candidates=None):
    cid='core.routing.resolve-intent'
    extra={}
    if candidate_owner: extra['candidate_owner']=candidate_owner
    if candidates: extra['candidate_contracts']=candidates
    return [_resolved_row(contracts,cid,reason,score=50,system_score=0,**extra)]

def route(task, top=5):
    idx,contracts=_index();q=task.lower();words=set(re.findall(r'[a-z0-9]{2,}',q))
    available_owners={r['owner_system'] for r in idx}

    # Explicit multi-domain chains win before direct artifact keywords.
    for pat,cid in COMPOUND_HINTS:
        if re.search(pat,q,re.I):
            return [_resolved_row(contracts,cid,'matched explicit multi-domain outcome pattern')]

    # Explicit/specific jobs win before broad Core patterns.
    for pat,cid in HINTS:
        if re.search(pat,q,re.I):
            return [_resolved_row(contracts,cid,'matched high-confidence direct task pattern')]

    # Broad business goals/problems/compound outcomes route to Core coordination.
    for pat,cid in CORE_HINTS:
        if re.search(pat,q,re.I):
            return [_resolved_row(contracts,cid,'matched broad business intent pattern')]

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

    # Lexical matching is used only as evidence for a direct route, never as a forced fallback.
    candidate=idx if scores[owner]==0 else [r for r in idx if r['owner_system']==owner]
    scored=[]
    for r in candidate:
        overlap=len(words & set(r['tokens']));score=overlap*2
        for token in re.findall(r'[a-z0-9]{3,}',r['contract_id'].lower().replace('-',' ')):
            if token in words:score+=1
        if score:scored.append((score,r))
    scored=sorted(scored,key=lambda x:(x[0],x[1]['contract_id']),reverse=True)

    if not scored:
        return _semantic_fallback(contracts,'no sufficiently confident deterministic route; use workspace-native semantic intent resolution',candidate_owner=owner if scores[owner] else None)

    top_score=scored[0][0]
    second_score=scored[1][0] if len(scored)>1 else 0
    # Require both a strong domain signal and a reasonably distinctive contract match.
    confident = scores[owner] >= 7 and top_score >= 6 and (top_score-second_score >= 2 or top_score >= 10)
    if not confident:
        candidates=[x[1]['contract_id'] for x in scored[:min(top,5)]]
        return _semantic_fallback(
            contracts,
            'deterministic candidates were not distinctive enough for a safe direct route; use workspace-native semantic intent resolution',
            candidate_owner=owner if scores[owner] else None,
            candidates=candidates,
        )

    out=[]
    for score,r in scored[:top]:
        out.append({'score':score,'system_score':scores.get(r['owner_system'],0),'contract_id':r['contract_id'],'owner_system':r['owner_system'],'status':'available','reason':'strong semantic-owner signal plus distinctive contract lexical match'})
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('task');p.add_argument('--top',type=int,default=5);a=p.parse_args()
    for row in route(a.task,a.top):print(json.dumps(row))
if __name__=='__main__':main()
