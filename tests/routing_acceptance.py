#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from route_task import route

CASES=[
    ('Create a webinar.', 'marketing.assets.webinar', 'marketing-synthesis'),
    ('Why are customers leaving?', 'customer.analysis.churn', 'customer-intelligence'),
    ('Reduce customer churn.', 'customer-optimization.intervention.churn', 'customer-optimization'),
    ('What should we work on first?', 'core.opportunity.discover-next-best-work', 'core'),
    ('I want to grow revenue profitably.', 'core.opportunity.discover-next-best-work', 'core'),
    ('We are getting traffic and leads but revenue is not growing. Figure out what is wrong.', 'core.diagnosis.business-problem', 'core'),
    ('Find what our market cares about and turn the best opportunities into content and campaigns.', 'core.coordination.multi-domain-request', 'core'),
    ('Help me improve the business.', 'core.opportunity.discover-next-best-work', 'core'),
    ('Can you help me figure this out?', 'core.routing.resolve-intent', 'core'),
    ('Find important news and turn it into LinkedIn posts.', 'core.coordination.multi-domain-request', 'core'),
    ('Research competitors and create a campaign from what you find.', 'core.coordination.multi-domain-request', 'core'),
    ('What are our competitors charging?', 'competitor.analysis.pricing', 'competitor-intelligence'),
    ('Find out what competitors are doing better.', 'competitor.analysis.tactic-validation', 'competitor-intelligence'),
    ('Our sales are down and I do not know why.', 'core.diagnosis.business-problem', 'core'),
    ('Our marketing is not working.', 'core.diagnosis.business-problem', 'core'),
    ('We have lots of traffic but few customers.', 'core.diagnosis.business-problem', 'core'),
    ('What is the highest value thing we can do next?', 'core.opportunity.discover-next-best-work', 'core'),
    ('How can we make more money?', 'core.opportunity.discover-next-best-work', 'core'),
]

def run():
    errors=[]
    for task,expected_contract,expected_owner in CASES:
        rows=route(task,5)
        first=rows[0] if rows else {}
        if first.get('status')!='available' or first.get('contract_id')!=expected_contract or first.get('owner_system')!=expected_owner:
            errors.append(f'{task!r}: expected {expected_contract}/{expected_owner}, got {rows}')
    if errors:
        print(f'Routing acceptance errors: {len(errors)}')
        for e in errors: print('ERROR',e)
        raise SystemExit(1)
    print(f'routing acceptance passed: {len(CASES)} natural-language cases')

if __name__=='__main__': run()
