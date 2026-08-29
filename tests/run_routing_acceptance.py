#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from route_task import route
from route_and_resolve import route_and_resolve

CASES=[
 ('Create a webinar.','marketing.assets.webinar'),
 ('Why are customers leaving?','customer.analysis.churn'),
 ('Reduce customer churn.','customer-optimization.intervention.churn'),
 ('What should we work on first?','core.opportunity.discover-next-best-work'),
 ('I want to grow revenue profitably.','core.opportunity.discover-next-best-work'),
 ("Traffic and leads increased but revenue didn't.",'core.diagnosis.business-problem'),
 ("Traffic and leads are growing but revenue isn't. What's wrong?",'core.diagnosis.business-problem'),
 ('determine what we should do next','core.opportunity.discover-next-best-work'),
 ('Compare competitor pricing','competitor.analysis.pricing'),
 ('Analyze sales objections','customer.analysis.objections'),
 ('Find regulatory changes in our industry','industry.monitoring.regulation'),
 ('Why did our organic rankings drop?','seo.diagnosis.detectors.ranking-decay'),
 ('Create a landing page','marketing.assets.landing-page'),
 ('Create a landing page for paid search traffic','marketing.assets.landing-page'),
 ('Create a publish-ready organic page for our target query','core.coordination.multi-domain-request'),
 ('Create an SEO landing page for this keyword','core.coordination.multi-domain-request'),
 ('Create a carousel','content.production.carousel'),
 ('Improve customer onboarding','customer-optimization.intervention.onboarding'),
 ('Find trending creator content','content.intelligence.trending-content-discovery'),
 ('Research industry news and turn it into LinkedIn posts','core.coordination.multi-domain-request'),
 ('Build an infographic','content.production.infographic'),
 ('Analyze lost deals','customer.analysis.win-loss'),
 ('Help me figure out what to improve','core.routing.resolve-intent'),
]
FEATURE_CASES=[
 ('Establish the real competitive set and produce a decision-grade competitive position.','competitor.analysis.competitive-position'),
 ('Research our competitors and tell us where we can win.','competitor.analysis.competitive-position'),
 ('Give me a current competitive landscape with strengths, weaknesses, and whitespace.','competitor.analysis.competitive-position'),
 ('What are you monitoring for us?','core.monitoring.status'),
 ('Show me our recurring checks and what is due.','core.monitoring.status'),
 ('Review our monitoring schedule.','core.monitoring.status'),
 ('Pause the Hormozi watch.','core.intelligence.subject-monitoring'),
 ('Only notify me when something materially changes.','core.intelligence.subject-monitoring'),
 ("Don't alert me unless something materially changes.",'core.intelligence.subject-monitoring'),
 ('Tell me after every check.','core.intelligence.subject-monitoring'),
 ('Keep this monitoring silent.','core.intelligence.subject-monitoring'),
 ('Make this watch quiet.','core.intelligence.subject-monitoring'),
 ('Monitoring for this subject should stay silent.','core.intelligence.subject-monitoring'),
 ('Make pricing monthly but hiring weekly.','core.intelligence.subject-monitoring'),
]

def main():
    failures=[]
    for text,expected in CASES:
        rows=route(text)
        got=rows[0].get('contract_id') if rows else None
        if got!=expected: failures.append((text,expected,got))
    for text,expected in FEATURE_CASES:
        try:got=route_and_resolve(text).get('contract_id')
        except Exception as e:got=f'ERROR:{e}'
        if got!=expected:failures.append((text,expected,got))
    if failures:
        for text,expected,got in failures:
            print(f'FAIL: {text!r}: expected {expected}, got {got}')
        raise SystemExit(1)
    total=len(CASES)+len(FEATURE_CASES)
    print(f'routing acceptance passed: {total}/{total}')

if __name__=='__main__': main()
