#!/usr/bin/env python3
"""Return bounded AURA Workflow candidates without owning semantic intent.

Workflows are reusable procedures inside or alongside Playbooks. The generated index is a
retrieval optimization, not semantic authority. The active model/user decides which
Workflows are useful and may sequence, parallelize, adapt, combine, or replace them.
"""
from _common import ROOT,workflow_files,read_frontmatter
from functools import lru_cache
import argparse,json
from _lexical import contains_phrase, document_frequency, tokens, weighted_overlap


def _index():
    path=ROOT/'generated/workflow-candidate-index.json'
    if not path.exists():raise ValueError('Workflow candidate index is missing; run scripts/generate_registry.py')
    return json.loads(path.read_text())

@lru_cache(maxsize=1)
def _installed_ids():
    ids=set()
    for path in workflow_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        wid=meta.get('id')
        if isinstance(wid,str) and wid and meta.get('type')=='workflow':ids.add(wid)
    return ids


def _score(words,q,wid,row,frequencies,document_count):
    title_score,title_matches=weighted_overlap(words,row.get('title',''),frequencies,document_count)
    purpose_score,purpose_matches=weighted_overlap(words,row.get('purpose_tokens') or [],frequencies,document_count)
    run_when_score,run_when_matches=weighted_overlap(words,row.get('run_when_tokens') or [],frequencies,document_count)
    id_score,id_matches=weighted_overlap(words,wid.replace('.',' ').replace('-',' '),frequencies,document_count)
    matched=sorted(set(title_matches+purpose_matches+run_when_matches+id_matches))
    score=title_score*5+purpose_score*3+run_when_score*5+id_score*2
    # ID cues are useful only when they occur as complete words, not substrings.
    score+=4*sum(1 for token in set(id_matches) if contains_phrase(q,token))
    if q.casefold()==wid.casefold():score=10000
    return round(score,6),matched


def find_candidates(task,top=6,owner_system=None):
    q=str(task or '').strip()
    if not q:return []
    index=_index();installed=_installed_ids();words=tokens(q);scored=[]
    frequencies=document_frequency(index,('workflow_id','title','purpose_tokens','run_when_tokens','tokens'))
    for row in index:
        wid=str(row.get('workflow_id') or '')
        if not wid or wid not in installed:continue
        if owner_system and row.get('owner_system')!=owner_system:continue
        score,matched_terms=_score(words,q,wid,row,frequencies,len(index))
        if score<=0:continue
        scored.append((score,wid,row,matched_terms))
    scored.sort(key=lambda item:(item[0],item[1]),reverse=True)
    return [
        {'score':score,'workflow_id':wid,'title':row.get('title') or wid,'path':row.get('path'),'matched_terms':matched_terms,'owner_system':row.get('owner_system'),'status':'available','selection_authority':False,'reason':'Workflow candidate only; lexical title/purpose/When-to-use matches help discovery while the active model/user judges applicability and execution approach.'}
        for score,wid,row,matched_terms in scored[:max(1,int(top))]
    ]


def main():
    p=argparse.ArgumentParser(description='Find bounded existing AURA Workflow candidates. This does not semantically select a method.');p.add_argument('task');p.add_argument('--top',type=int,default=6);p.add_argument('--owner-system');a=p.parse_args()
    try:rows=find_candidates(a.task,a.top,a.owner_system)
    except ValueError as exc:raise SystemExit(str(exc))
    print(json.dumps(rows,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
