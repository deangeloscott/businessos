#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from route_task import route

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
 ('Create a carousel','content.production.carousel'),
 ('Improve customer onboarding','customer-optimization.intervention.onboarding'),
 ('Find trending creator content','content.intelligence.trending-content-discovery'),
 ('Research industry news and turn it into LinkedIn posts','core.coordination.multi-domain-request'),
 ('Build an infographic','content.production.infographic'),
 ('Analyze lost deals','customer.analysis.win-loss'),
 ('Help me figure out what to improve','core.routing.resolve-intent'),
]

def main():
    failures=[]
    for text,expected in CASES:
        rows=route(text)
        got=rows[0].get('contract_id') if rows else None
        if got!=expected: failures.append((text,expected,got))
    if failures:
        for text,expected,got in failures:
            print(f'FAIL: {text!r}: expected {expected}, got {got}')
        raise SystemExit(1)
    print(f'routing acceptance passed: {len(CASES)}/{len(CASES)}')

if __name__=='__main__': main()
