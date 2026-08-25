#!/usr/bin/env python3
from _common import *
import argparse, json
from route_task import route
from resolve_contract import resolve_contract
from growth_baseline_gate import assess as assess_growth_baseline


def route_and_resolve(task,business_id=None):
    rows = route(task, 5)
    if not rows:
        raise ValueError('No route returned')
    first = rows[0]
    if first.get('status') != 'available' or not first.get('contract_id'):
        result={**first, 'task': task, 'path': None, 'executable': False}
    else:
        path, meta = resolve_contract(first['contract_id'])
        result={
            'task': task,
            'contract_id': first['contract_id'],
            'owner_system': first.get('owner_system') or meta.get('owner_system'),
            'status': first.get('status'),
            'reason': first.get('reason'),
            'path': str(path.relative_to(ROOT)),
            'executable': False,
        }
    if business_id:
        result['business_id']=business_id
        if result.get('contract_id')=='core.opportunity.discover-next-best-work':
            result['broad_growth_precheck']=assess_growth_baseline(business_id)
    return result


def main():
    ap = argparse.ArgumentParser(
        description='Route ONE natural-language business request and resolve the selected BusinessOS contract to its CONTEXT.md. The task argument is natural language, never a contract ID. Optional --business-id adds business-aware prechecks without changing routing semantics.'
    )
    ap.add_argument('task', help='The user/residual request in natural language, e.g. "What should we work on first to grow profitably?"')
    ap.add_argument('--business-id',help='Optional active business ID. For broad next-best-work routes this emits the deterministic first-party growth-baseline precheck.')
    ap.add_argument('--show', action='store_true', help='Print the resolved contract instructions after routing metadata.')
    a = ap.parse_args()
    try:
        result = route_and_resolve(a.task,a.business_id)
    except ValueError as e:
        raise SystemExit(str(e))
    print(json.dumps(result, indent=2))
    if a.show and result.get('path'):
        print('\n--- RESOLVED CONTRACT ---\n')
        print((ROOT / result['path']).read_text(), end='')


if __name__ == '__main__':
    main()
