#!/usr/bin/env python3
"""Describe an explicitly selected AURA Playbook or Workflow as a browse view.

This helper resolves authored navigation only. It does not construct an execution graph,
select supporting methods, prescribe order, schedule work, delegate, or create receipts.
The active model/user decides which knowledge and methods are useful for the real task.
"""
from _common import *
from operating_knowledge import get_playbook
import argparse,json


def workflow_map():
    out={}
    for path in workflow_files():
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
    return maps[system][activity]['entry_workflow']


def workflow_view(workflow_id,workflows=None):
    workflows=workflows or workflow_map()
    if workflow_id not in workflows:raise ValueError(f'Unknown Workflow {workflow_id}')
    workflow=workflows[workflow_id]
    return {'workflow_id':workflow_id,'owner_system':workflow.get('owner_system'),'path':next((str(p.relative_to(ROOT)) for p in workflow_files() if read_frontmatter(p)[0].get('id')==workflow_id),None)}


def build_process_plan(system=None,activity=None,workflow_id=None,playbook_id=None):
    workflows=workflow_map()
    if playbook_id:
        playbook=get_playbook(playbook_id)
        if not playbook:raise ValueError(f'Unknown Playbook {playbook_id}')
        entry=playbook.get('entry_workflow')
        return {
            'playbook':playbook,
            'entry_workflow':entry,
            'entry_workflow_view':workflow_view(entry,workflows) if entry else None,
            'rule':'Playbook browse view only. Use the smallest useful set of Workflows or other methods for the real request; the active model/user owns semantic selection, ordering, parallelism, adaptation, tools, external Skills, and execution.'
        }
    entry=resolve_entry(system,activity,workflow_id)
    return {'entry_workflow':entry,'system':system,'activity':activity,'workflow_view':workflow_view(entry,workflows),'rule':'Workflow browse view only. AURA does not construct a supporting-method or execution graph.'}


def main():
    ap=argparse.ArgumentParser(description='Describe an AURA Playbook/Workflow entry without creating an execution plan.');ap.add_argument('--playbook');ap.add_argument('--system');ap.add_argument('--activity');ap.add_argument('--workflow');ap.add_argument('--output');a=ap.parse_args()
    try:data=build_process_plan(a.system,a.activity,a.workflow,a.playbook)
    except ValueError as e:raise SystemExit(str(e))
    text=json.dumps(data,indent=2)+'\n'
    if a.output:Path(a.output).write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
