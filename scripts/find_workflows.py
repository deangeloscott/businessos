#!/usr/bin/env python3
"""Return bounded AURA Workflow candidates without owning semantic intent.

Workflows are reusable procedures inside or alongside Playbooks. The generated index is a
retrieval optimization, not semantic authority. The active model/user decides which
workflows are useful and may sequence, parallelize, adapt, combine, or replace them.
"""
from _common import ROOT,contract_files,read_frontmatter
from functools import lru_cache
import argparse,json,re

PRODUCTION_ACTION_WORDS={'build','create','design','draft','generate','make','produce','write'}


def _index():
    current=ROOT/'generated/workflow-candidate-index.json'
    legacy=ROOT/'generated/playbook-candidate-index.json'
    path=current if current.exists() else legacy
    return json.loads(path.read_text())

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


def _score(words,q,cid,row):
    if q==cid.lower():return 10000
    cid_words=_words(cid.replace('.',' ').replace('-',' '))
    title_tokens=set(row.get('title_tokens') or [])
    purpose_tokens=set(row.get('purpose_tokens') or [])
    run_when_tokens=set(row.get('run_when_tokens') or [])
    if title_tokens or purpose_tokens or run_when_tokens:
        score=(len(words & title_tokens)*5)+(len(words & purpose_tokens)*3)+(len(words & run_when_tokens)*5)
    else:score=len(words & set(row.get('tokens') or []))*3
    score+=len(words & cid_words)*2
    if any(token in q for token in cid_words if len(token)>=5):score+=4
    if 'production_root' in str(row.get('artifact_role') or '') and words & PRODUCTION_ACTION_WORDS:score+=10
    return score


def find_candidates(task,top=6,owner_system=None):
    q=str(task or '').strip().lower()
    if not q:return []
    installed=_installed_ids();words=_words(q);scored=[]
    for row in _index():
        cid=str(row.get('contract_id') or row.get('workflow_id') or '')
        if not cid or cid not in installed:continue
        if owner_system and row.get('owner_system')!=owner_system:continue
        score=_score(words,q,cid,row)
        if score<=0:continue
        scored.append((score,cid,row))
    scored.sort(key=lambda item:(item[0],item[1]),reverse=True)
    out=[]
    for score,cid,row in scored[:max(1,int(top))]:
        out.append({
            'score':score,'workflow_id':cid,'owner_system':row.get('owner_system'),'status':'available',
            'selection_authority':False,
            'reason':'Workflow candidate only; authored title/purpose/When-to-use cues help discovery while the active model/user judges applicability and execution approach.'
        })
    return out


def main():
    p=argparse.ArgumentParser(description='Find bounded existing AURA Workflow candidates. This does not semantically select a method.')
    p.add_argument('task');p.add_argument('--top',type=int,default=6);p.add_argument('--owner-system');a=p.parse_args()
    print(json.dumps(find_candidates(a.task,a.top,a.owner_system),indent=2,ensure_ascii=False))

if __name__=='__main__':main()
