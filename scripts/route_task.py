#!/usr/bin/env python3
"""Return bounded AURA playbook candidates without owning semantic intent.

Deterministic code is good at indexing and existence checks. The active model/user is
better suited to judge what a natural-language request actually means and whether an
AURA playbook is useful. This module therefore returns lexical candidates only; it never
claims that a candidate is the correct method for the user's request.
"""
from _common import ROOT
import argparse,json,re

# Kept out of discovery while generated artifacts still contain the legacy semantic
# resolver. It is no longer part of the active AURA method-selection path and can be
# physically removed when generated registries/docs are regenerated for the release.
INACTIVE_DISCOVERY_IDS={'core.routing.resolve-intent'}


def _index():
    return json.loads((ROOT/'generated/route-index.json').read_text())


def _words(value):
    return set(re.findall(r'[a-z0-9]{2,}',str(value or '').lower()))


def route(task,top=5):
    q=str(task or '').strip().lower()
    if not q:return []
    rows=_index();words=_words(q);scored=[]
    for row in rows:
        cid=str(row.get('contract_id') or '')
        if not cid or cid in INACTIVE_DISCOVERY_IDS:continue
        if q==cid.lower():score=10000
        else:
            tokens=set(row.get('tokens') or [])
            cid_words=_words(cid.replace('.',' ').replace('-',' '))
            overlap=len(words & tokens);id_overlap=len(words & cid_words)
            phrase_bonus=4 if any(token in q for token in cid_words if len(token)>=5) else 0
            score=(overlap*3)+(id_overlap*2)+phrase_bonus
        if score<=0:continue
        scored.append((score,cid,row))
    scored.sort(key=lambda item:(item[0],item[1]),reverse=True)
    out=[]
    for score,cid,row in scored[:max(1,int(top))]:
        out.append({
            'score':score,'contract_id':cid,'owner_system':row.get('owner_system'),'status':'available',
            'selection_authority':False,
            'reason':'lexical/index candidate only; the active model/user must judge semantic applicability',
        })
    return out


def main():
    p=argparse.ArgumentParser(description='Find bounded AURA playbook candidates. This does not semantically select a method.')
    p.add_argument('task');p.add_argument('--top',type=int,default=5);a=p.parse_args()
    print(json.dumps(route(a.task,a.top),indent=2))


if __name__=='__main__':main()
