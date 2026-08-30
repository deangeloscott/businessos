#!/usr/bin/env python3
from _common import *
import argparse,json,re
from route_task import route
from resolve_contract import resolve_contract
from process_extensions import route_local_playbook,resolve_effective
from growth_baseline_gate import assess as assess_growth_baseline

# Broad domain-level business outcomes that should compose several atomic jobs rather
# than collapsing into whichever narrow contract happens to share the most words.
DOMAIN_HINTS=[
 (r'\b(?:competitive set|competitive landscape|competitive position|competitor landscape|competitor research|competitive intelligence)\b|\b(?:full|complete|comprehensive) competitor (?:analysis|research)\b|\b(?:research|analy[sz]e|understand|map|assess|establish).*(?:competitors?|competition).*(?:strengths? and weaknesses?|weaknesses? and strengths?|whitespace|where (?:we|i) can win|competitive advantage|landscape|position)', 'competitor.analysis.competitive-position','competitor-intelligence'),
]

FEATURE_HINTS=[
 (r'\b(?:build|create|develop|maintain|refresh|update)\b.*\b(?:durable|cumulative|reusable|ongoing)\b.*\b(?:understanding|knowledge|intelligence|watch)\b|\b(?:durable|cumulative|reusable)\b.*\b(?:understanding|knowledge|intelligence)\b.*\b(?:future updates?|refresh|keep current|ongoing)\b', 'core.intelligence.subject-monitoring'),
 (r'\b(make|turn|promote|formalize|formalise).*(playbook|process|workflow|standard operating|part of businessos)|\b(playbook|process).*(evolve|evolution|improve businessos)', 'core.learning.playbook-evolution'),
 (r'\binnovation exchange\b|\bshare.*(playbook|workflow|process)\b|\b(import|browse|community).*(playbook|workflow|businessos innovation)', 'core.intelligence.innovation-exchange'),
 (r'\b(?:what|which|show|list|review).*(?:monitoring|monitors|recurring checks|scheduled checks|scheduled monitoring|tracking status)|\bwhat.*(?:watching|tracking).*(?:for us|for me)|\b(?:monitoring|recurring checks).*(?:status|active|due|schedule)', 'core.monitoring.status'),
 (r'\b(?:pause|resume|stop|disable|enable|change|update|adjust|make|set|keep|mute|silence).*(?:watch|monitoring|monitor|tracked subject|recurring check|cadence|notification)|\b(?:watch|monitoring|monitor|tracked subject|recurring check|cadence|notification).*(?:pause|resume|stop|disable|enable|change|update|adjust|silent|quiet|mute|material(?:ly)?\s+chang\w*|every\s+check|all\s+checks|daily|weekly|monthly|quarterly)|\b(?:notify|notification|alert|tell me).*(?:material(?:ly)?\s+chang\w*|every\s+check|all\s+checks|silent|quiet|only)|\b(?:only|don\x27t|do not|never).*(?:notify|alert|tell me).*(?:material(?:ly)?\s+chang\w*|unless|every\s+check|all\s+checks|silent|quiet)|\b(?:daily|weekly|monthly|quarterly|every\s+\d+\s+(?:day|days|week|weeks|month|months)).*(?:watch|monitor|check|pricing|hiring|news|content)', 'core.intelligence.subject-monitoring'),
 (r'\b(?:configure|set ?up|deploy|host|store|version|move|migrate).*(?:viraltrac aura|aura|businessos).*(?:workspace|state root|external state|deployment profile|private git|github organization|gitlab|forgejo)|\b(?:viraltrac aura|aura|businessos).*(?:workspace|state root|external state|deployment profile|private git|github organization|gitlab|forgejo)|\b(?:workspace|state root|external state|deployment profile|private git|github organization|gitlab|forgejo).*(?:viraltrac aura|aura|businessos|set ?up|configure|host|store|deploy|version)', 'core.workspace.configure'),
 (r'\b(use|review|incorporate|ingest|learn from|import).*(human note|knowledge note|obsidian note|note in obsidian|workspace note)|\b(human note|knowledge note|obsidian note).*(use|review|incorporate|ingest|businessos|aura)', 'core.knowledge.ingest-human-note'),
 (r'\b(obsidian|second brain|human knowledge|knowledge layer|human-readable knowledge|human view).*(businessos|aura|workspace|refresh|generate|open)|\b(refresh|generate|update).*(knowledge layer|obsidian|second brain)', 'core.knowledge.refresh-human-layer')
]

def route_and_resolve(task,business_id=None,team_ref=None,role_ref=None,operator_ref=None):
    feature_hint=None
    for pat,cid in FEATURE_HINTS:
        if re.search(pat,task,re.I):feature_hint={'score':100,'system_score':100,'contract_id':cid,'owner_system':'core','status':'available','reason':'matched explicit AURA/BusinessOS product, monitoring, or workspace feature request'};break
    local=route_local_playbook(task,business_id,team_ref,role_ref,operator_ref) if business_id and not feature_hint else None
    domain_hint=None
    if not feature_hint and not local:
        for pat,cid,owner in DOMAIN_HINTS:
            if re.search(pat,task,re.I):domain_hint={'score':100,'system_score':100,'contract_id':cid,'owner_system':owner,'status':'available','reason':'matched broad domain-level business outcome that requires composed execution'};break
    rows=[feature_hint] if feature_hint else ([local] if local else ([domain_hint] if domain_hint else route(task,5)))
    if not rows:raise ValueError('No route returned')
    first=rows[0]
    if first.get('status')!='available' or not first.get('contract_id'):result={**first,'task':task,'path':None,'executable':False}
    elif business_id:
        path,meta,_,exts=resolve_effective(first['contract_id'],business_id,team_ref,role_ref,operator_ref);result={'task':task,'contract_id':first['contract_id'],'owner_system':first.get('owner_system') or meta.get('owner_system'),'status':first.get('status'),'reason':first.get('reason'),'path':str(path.relative_to(ROOT)) if path else None,'process_extension_ids':[x['id'] for x in exts],'local_playbook':bool(meta.get('local_playbook')),'executable':False}
    else:
        path,meta=resolve_contract(first['contract_id']);result={'task':task,'contract_id':first['contract_id'],'owner_system':first.get('owner_system') or meta.get('owner_system'),'status':first.get('status'),'reason':first.get('reason'),'path':str(path.relative_to(ROOT)),'executable':False}
    if business_id:
        result['business_id']=business_id
        if result.get('contract_id')=='core.opportunity.discover-next-best-work':result['broad_growth_precheck']=assess_growth_baseline(business_id)
    return result

def main():
    ap=argparse.ArgumentParser(description='Route one natural-language request and resolve the selected canonical/business-local AURA/BusinessOS playbook.');ap.add_argument('task');ap.add_argument('--business-id');ap.add_argument('--team-ref');ap.add_argument('--role-ref');ap.add_argument('--operator-ref');ap.add_argument('--show',action='store_true');a=ap.parse_args()
    try:result=route_and_resolve(a.task,a.business_id,a.team_ref,a.role_ref,a.operator_ref)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps(result,indent=2))
    if a.show and result.get('contract_id'):
        print('\n--- RESOLVED CONTRACT ---\n')
        if a.business_id:
            _,_,content,_=resolve_effective(result['contract_id'],a.business_id,a.team_ref,a.role_ref,a.operator_ref);print(content,end='' if content.endswith('\n') else '\n')
        elif result.get('path'):print((ROOT/result['path']).read_text(),end='')
if __name__=='__main__':main()
