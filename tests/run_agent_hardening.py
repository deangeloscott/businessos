#!/usr/bin/env python3
"""Protect AURA's small agent-facing boundary.

This regression intentionally avoids re-testing domain methodology, claim QA, Run internals,
or artifact production. Those truths have dedicated regressions. Here we protect only the
boundary that keeps AURA useful without becoming a control plane.
"""
from pathlib import Path
import json,os,shutil,sys,tempfile

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from init_business import init_business
from enter import prepare_work
from _common import contract_files,read_frontmatter


def req(condition,message):
    if not condition:raise AssertionError(message)


def main():
    for rel in ('CONTEXT.md','AURA-ATTACHMENT.md','AGENTS.md','skills/viraltrac-aura/SKILL.md','docs/operating-knowledge.md'):
        req((ROOT/rel).exists(),f'agent-facing AURA entry artifact missing: {rel}')
    skill=(ROOT/'skills/viraltrac-aura/SKILL.md').read_text(encoding='utf-8');attachment=(ROOT/'AURA-ATTACHMENT.md').read_text(encoding='utf-8');contract=(ROOT/'CONTEXT.md').read_text(encoding='utf-8')
    for phrase in ('retrieve little','other Skills','remember','unrelated'):
        req(phrase.lower() in skill.lower(),f'AURA Skill lost small awareness behavior: {phrase}')
    req('awareness' in attachment.lower() and 'access' in attachment.lower(),'attachment contract must distinguish awareness from actual file access')
    req('Playbook → Workflow → Step' in contract,'root agent contract lost operating-knowledge hierarchy')
    req('fewest inputs necessary' in contract,'root agent contract lost minimum-sufficient-guidance principle')
    req('AURA does not define a tool allowlist or universal capability vocabulary.' in contract,'root agent contract lost tool/model freedom')

    retired=[
        'core/capabilities/catalog.json','docs/adding-a-capability.md','generated/capability-usage-index.json',
        'scripts/preflight_capabilities.py','scripts/resolve_capability.py','scripts/bootstrap_environment.py',
        'core/providers/registry.json','core/contracts/routing/resolve-intent','core/contracts/coordination/multi-domain-request',
        'core/contracts/intelligence/ecosystem/route-learning','core/contracts/learning/promote-learning',
        'core/schemas/action/action-packet.schema.json','core/schemas/action/approval.schema.json','templates/manual-action.md',
        'scripts/run_lifecycle.py','scripts/reconcile_runs.py','scripts/run_provenance.py','scripts/persist_run_results.py',
        'PLAYBOOK-INDEX.md','generated/playbook-candidate-index.json',
    ]
    for rel in retired:req(not (ROOT/rel).exists(),f'retired control/capability/routing artifact reappeared: {rel}')

    count=0
    for path in contract_files():
        meta,_=read_frontmatter(path);count+=1
        req(meta.get('type')=='workflow',f'{path.relative_to(ROOT)} is not typed as Workflow')
        req('capabilities' not in meta,f'{path.relative_to(ROOT)} retained capability ontology')
        req('subcontracts' not in meta,f'{path.relative_to(ROOT)} retained subcontract vocabulary')
    req(count>0,'no authored Workflows found')

    old=os.environ.get('BUSINESSOS_WORKSPACE');tmp=Path(tempfile.mkdtemp(prefix='aura-agent-boundary-'));os.environ['BUSINESSOS_WORKSPACE']=str(tmp)
    try:
        bid='agent-boundary';init_business(bid,'Agent Boundary Co')
        prepared=prepare_work('Research our competitors and create a useful presentation.',business_id=bid)
        req(prepared.get('status')=='ready',f'AURA entry failed: {prepared}')
        req(prepared.get('run',{}).get('created') is False,'AURA entry created a Run merely to begin work')
        req({'aura_playbook','aura_workflow','external_skill','model_created','ad_hoc'}<=set(prepared.get('method_options') or []),'AURA entry lost method freedom')
        knowledge=prepared.get('operating_knowledge') or {}
        req(knowledge.get('selected_playbook') is None and knowledge.get('selected_workflow') is None,'candidate discovery silently selected a method')
        req(all(row.get('selection_authority') is False for row in knowledge.get('playbook_candidates',[])),'Playbook candidate claimed semantic authority')
        req(all(row.get('selection_authority') is False for row in knowledge.get('workflow_candidates',[])),'Workflow candidate claimed semantic authority')
        req('best available tools' in prepared.get('execution_rule',''),'entry lost host-tool freedom')
        req(not (tmp/'runtime/runs'/bid).exists(),'entry manufactured runtime receipt state')
    finally:
        if old is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=old
        shutil.rmtree(tmp,ignore_errors=True)

    graph_keys={'next','next_contract','depends_on','dependencies','sequence','order','routes_to','delegate_to','on_success','on_failure'}
    for path in [ROOT/'core/process-map.json',*ROOT.glob('systems/*/process-map.json')]:
        data=json.loads(path.read_text(encoding='utf-8'))
        for activity in data.get('activities',[]):req(not (graph_keys & set(activity)),f'{path.relative_to(ROOT)} recreated execution-graph metadata on {activity.get("id")}')

    print(f'agent hardening regressions passed: {count} Workflows remain operating knowledge; AURA stays attached, tool/Skill neutral, and outside execution control')

if __name__=='__main__':main()
