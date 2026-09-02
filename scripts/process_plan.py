#!/usr/bin/env python3
"""Describe AURA Playbook/Workflow composition without constructing an execution graph.

`workflows` metadata identifies reusable supporting knowledge that is normally or
conditionally useful to an authored Workflow. It does not specify runtime order,
scheduling, delegation, tool calls, or receipt requirements. The active model/user chooses
how to apply, sequence, parallelize, adapt, or replace relevant knowledge.
"""
from _common import *
from operating_knowledge import get_playbook
import argparse,json


def workflow_map():
    out={}
    for path in contract_files():
        meta,_=read_frontmatter(path);wid=meta.get('id')
        if wid:out[wid]=meta
    return out


def process_maps():
    out={};paths=[];cp=ROOT/'core/process-map.json'
    if cp.exists():paths.append(cp)
    paths+=sorted((ROOT/'systems').glob('*/process-map.json'))
    for p in paths:
        data=json.loads(p.read_text());out[data['system']]={a['id']:a for a in data.get('activities',[])}
    return out


def resolve_entry(system=None,activity=None,workflow_id=None):
    if workflow_id:return workflow_id
    maps=process_maps()
    if not system or not activity:raise ValueError('Provide --workflow or both --system and --activity')
    if system not in maps or activity not in maps[system]:raise ValueError('Unknown system/activity')
    return maps[system][activity]['entry_contract']


def workflow_composition(workflow_id,workflows=None,stack=None):
    workflows=workflows or workflow_map();stack=stack or []
    if workflow_id not in workflows:raise ValueError(f'Unknown Workflow {workflow_id}')
    if workflow_id in stack:raise ValueError('Workflow composition cycle: '+' -> '.join(stack+[workflow_id]))
    workflow=workflows[workflow_id];refs=workflow.get('workflows') or {};nstack=stack+[workflow_id];normally=[];conditional=[]
    for child in refs.get('required',[]) or []:
        wid=child.get('id') if isinstance(child,dict) else child
        normally.append(workflow_composition(wid,workflows,nstack))
    for child in refs.get('conditional',[]) or []:
        if isinstance(child,str):wid,when=child,'when relevant to the actual request'
        else:wid,when=child.get('id'),child.get('when','when relevant to the actual request')
        conditional.append({'when':when,'workflow':workflow_composition(wid,workflows,nstack)})
    return {'workflow_id':workflow_id,'owner_system':workflow.get('owner_system'),'normally_use':normally,'conditionally_use':conditional}


def build_process_plan(system=None,activity=None,workflow_id=None,playbook_id=None):
    workflows=workflow_map()
    if playbook_id:
        playbook=get_playbook(playbook_id)
        if not playbook:raise ValueError(f'Unknown Playbook {playbook_id}')
        entry=playbook.get('entry_workflow')
        return {
            'playbook':playbook,
            'entry_workflow':entry,
            'workflow_composition':workflow_composition(entry,workflows) if entry else None,
            'rule':'Playbook browse view only. Use the smallest useful set of Workflows for the real request; the active model/user owns semantic selection, ordering, parallelism, adaptation, tools, external Skills, and execution.'
        }
    entry=resolve_entry(system,activity,workflow_id)
    return {'entry_workflow':entry,'system':system,'activity':activity,'workflow_composition':workflow_composition(entry,workflows),'rule':'Workflow browse view only. Composition describes reusable knowledge, not an execution graph or orchestration authority.'}


def main():
    ap=argparse.ArgumentParser(description='Describe AURA Playbook/Workflow composition without creating an execution plan.');ap.add_argument('--playbook');ap.add_argument('--system');ap.add_argument('--activity');ap.add_argument('--workflow');ap.add_argument('--contract',help=argparse.SUPPRESS);ap.add_argument('--output');a=ap.parse_args()
    try:data=build_process_plan(a.system,a.activity,a.workflow or a.contract,a.playbook)
    except ValueError as e:raise SystemExit(str(e))
    text=json.dumps(data,indent=2)+'\n'
    if a.output:Path(a.output).write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
