#!/usr/bin/env python3
"""Find a small set of human-meaningful AURA Playbooks.

A Playbook is an end-to-end business job, not a tool binding or execution controller.
Candidate discovery is only a navigation aid. The active model/user decides whether an
AURA Playbook is useful, combines it with other Skills/methods, or works another way.
"""
import argparse,json
from operating_knowledge import installed_playbooks
from _lexical import contains_phrase, document_frequency, tokens, weighted_overlap


def find_candidates(task,top=3):
    query=str(task or '').strip()
    if not query:return []
    playbooks=installed_playbooks()
    words=tokens(query)
    frequencies=document_frequency(playbooks,('id','title','summary','discovery_terms','example'))
    rows=[]
    for playbook in playbooks:
        title_score,title_matches=weighted_overlap(words,playbook.get('title',''),frequencies,len(playbooks))
        summary_score,summary_matches=weighted_overlap(words,playbook.get('summary',''),frequencies,len(playbooks))
        discovery_text=' '.join(str(term) for term in playbook.get('discovery_terms',[]))
        discovery_score,discovery_matches=weighted_overlap(words,discovery_text,frequencies,len(playbooks))
        example_score,example_matches=weighted_overlap(words,playbook.get('example',''),frequencies,len(playbooks))
        matched=sorted(set(title_matches+summary_matches+discovery_matches+example_matches))
        score=title_score*4+summary_score*2+discovery_score*3+example_score
        exact_id=query.casefold()==str(playbook.get('id') or '').casefold()
        exact_title=query.casefold()==str(playbook.get('title') or '').casefold()
        if exact_id or exact_title:
            score=10000
        # Discovery phrases are matched as words, never as arbitrary substrings.
        phrase_matches=[term for term in playbook.get('discovery_terms',[]) if contains_phrase(query,term)]
        if phrase_matches and score<10000:score+=3*len(phrase_matches)
        if score<=0:continue
        rows.append((score,{
            **playbook,'score':round(score,6),'matched_terms':matched,'selection_authority':False,
            'path':f"docs/playbooks/{playbook['owner_system']}.md",
            'reason':'Playbook candidate only; lexical matches are navigation help and the active model/user judges whether this end-to-end business job is the right frame.'
        }))
    rows.sort(key=lambda item:(item[0],item[1]['id']),reverse=True)
    return [row for _,row in rows[:max(1,int(top))]]


def main():
    p=argparse.ArgumentParser(description='Find bounded AURA Playbook candidates without semantically routing the request.')
    p.add_argument('task');p.add_argument('--top',type=int,default=3);a=p.parse_args()
    print(json.dumps(find_candidates(a.task,a.top),indent=2,ensure_ascii=False))

if __name__=='__main__':main()
