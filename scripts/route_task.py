#!/usr/bin/env python3
"""Return bounded AURA playbook candidates without owning semantic intent.

The generated route index is an optimization/view, not semantic or existence authority.
Every candidate is mechanically checked against current AURA product source so a stale
index cannot advertise a deleted playbook. The active model/user decides whether any
remaining candidate is actually useful for the natural-language request.
"""
from _common import ROOT,contract_files,read_frontmatter
from functools import lru_cache
import argparse,json,re


def _index():
    return json.loads((ROOT/'generated/route-index.json').read_text())

@lru_cache(maxsize=1)
def _installed_ids():
    ids=set()
    for path in contract_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        cid=meta.get('id')
        if isinstance(cid,str) and cid:ids.add(cid)
    return ids


def _words(value):
    return set(re.findall(r'[a-z0-9]{2,}',str(value or '').lower()))


def route(task,top=5):
    q=str(task or '').strip().lower()
    if not q:return []
    rows=_index();installed=_installed_ids();words=_words(q);scored=[]
    for row in rows:
        cid=str(row.get('contract_id') or '')
        if not cid or cid not in installed:continue
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
            'reason':'lexical/index candidate only; current product source confirms the playbook exists, and the active model/user must judge semantic applicability',
        })
    return out


def main():
    p=argparse.ArgumentParser(description='Find bounded existing AURA playbook candidates. This does not semantically select a method.')
    p.add_argument('task');p.add_argument('--top',type=int,default=5);a=p.parse_args()
    print(json.dumps(route(a.task,a.top),indent=2))


if __name__=='__main__':main()
