#!/usr/bin/env python3
"""Find a small set of human-meaningful AURA Playbooks.

A Playbook is an end-to-end business job, not a tool binding or execution controller.
Candidate discovery is only a navigation aid. The active model/user decides whether an
AURA Playbook is useful, combines it with other Skills/methods, or works another way.
"""
import argparse,json,re
from operating_knowledge import installed_playbooks


def _words(value):
    return set(re.findall(r'[a-z0-9]{2,}',str(value or '').lower()))


def find_candidates(task,top=3):
    query=str(task or '').strip().lower()
    if not query:return []
    words=_words(query);rows=[]
    for playbook in installed_playbooks():
        text=' '.join([
            playbook['id'],playbook['title'],playbook['summary'],
            *playbook.get('discovery_terms',[]),playbook.get('example','')
        ]).lower()
        tokens=_words(text)
        score=len(words & tokens)*3
        if query==playbook['id'] or query==playbook['title'].lower():score+=10000
        if any(term in query for term in playbook.get('discovery_terms',[]) if len(term)>=5):score+=6
        if score<=0:continue
        rows.append((score,{
            **playbook,'score':score,'selection_authority':False,
            'path':f"docs/playbooks/{playbook['owner_system']}.md",
            'reason':'Playbook candidate only; the active model/user judges whether this end-to-end business job is the right frame.'
        }))
    rows.sort(key=lambda item:(item[0],item[1]['id']),reverse=True)
    return [row for _,row in rows[:max(1,int(top))]]


def main():
    p=argparse.ArgumentParser(description='Find bounded AURA Playbook candidates without semantically routing the request.')
    p.add_argument('task');p.add_argument('--top',type=int,default=3);a=p.parse_args()
    print(json.dumps(find_candidates(a.task,a.top),indent=2,ensure_ascii=False))

if __name__=='__main__':main()
