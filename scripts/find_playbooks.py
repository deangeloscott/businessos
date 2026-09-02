#!/usr/bin/env python3
"""Return bounded AURA playbook candidates without owning semantic intent.

The generated candidate index is a retrieval optimization, not semantic or existence
authority. Every candidate is mechanically checked against current AURA product source so
a stale index cannot advertise a deleted playbook. The active model/user decides whether
any candidate is actually useful for the natural-language request.
"""
from _common import ROOT,contract_files,read_frontmatter
from functools import lru_cache
import argparse,json,re


PRODUCTION_ACTION_WORDS={'build','create','design','draft','generate','make','produce','write'}


def _index():
    return json.loads((ROOT/'generated/playbook-candidate-index.json').read_text())

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


def _candidate_score(words,q,cid,row):
    if q==cid.lower():return 10000
    cid_words=_words(cid.replace('.',' ').replace('-',' '))
    title_tokens=set(row.get('title_tokens') or [])
    purpose_tokens=set(row.get('purpose_tokens') or [])
    run_when_tokens=set(row.get('run_when_tokens') or [])
    if title_tokens or purpose_tokens or run_when_tokens:
        # Authored retrieval cues help cheaply narrow the library; they are not semantic
        # rules. The active model/user still judges whether the method actually applies.
        score=(len(words & title_tokens)*5)+(len(words & purpose_tokens)*3)+(len(words & run_when_tokens)*5)
    else:
        score=len(words & set(row.get('tokens') or []))*3
    score+=len(words & cid_words)*2
    if any(token in q for token in cid_words if len(token)>=5):score+=4
    # A generic create/build request should surface an authored production root ahead of
    # its narrower QA/strategy leaves when both share the same literal subject tokens.
    # This is still a lexical/metadata hint, never semantic selection authority.
    if 'production_root' in str(row.get('artifact_role') or '') and words & PRODUCTION_ACTION_WORDS:
        score+=10
    return score


def find_candidates(task,top=5):
    q=str(task or '').strip().lower()
    if not q:return []
    rows=_index();installed=_installed_ids();words=_words(q);scored=[]
    for row in rows:
        cid=str(row.get('contract_id') or '')
        if not cid or cid not in installed:continue
        score=_candidate_score(words,q,cid,row)
        if score<=0:continue
        scored.append((score,cid,row))
    scored.sort(key=lambda item:(item[0],item[1]),reverse=True)
    out=[]
    for score,cid,row in scored[:max(1,int(top))]:
        out.append({
            'score':score,'contract_id':cid,'owner_system':row.get('owner_system'),'status':'available',
            'selection_authority':False,
            'reason':'lexical candidate only; authored title/purpose/Run When and structural production cues help discovery while the active model/user judges semantic applicability',
        })
    return out


def main():
    p=argparse.ArgumentParser(description='Find bounded existing AURA playbook candidates. This does not semantically select a method.')
    p.add_argument('task');p.add_argument('--top',type=int,default=5);a=p.parse_args()
    print(json.dumps(find_candidates(a.task,a.top),indent=2))


if __name__=='__main__':main()
