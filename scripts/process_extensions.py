#!/usr/bin/env python3
"""Resolve organization-scoped AURA Workflow knowledge without runtime authority.

ProcessExtensions are organization-owned reusable operating knowledge. Deterministic code
may list/filter them and provide bounded lexical candidates; the active model/user decides
semantic applicability, conflicts, sequencing, and execution method.
"""
from _common import *
import json,re

SCOPE_ORDER={'business':0,'team':1,'role':2,'operator':3}


def _scope_applies(extension,team_ref=None,role_ref=None,operator_ref=None):
    scope=extension.get('scope');ref=extension.get('scope_ref')
    if scope=='business':return True
    if scope=='team':return bool(team_ref) and ref==team_ref
    if scope=='role':return bool(role_ref) and ref==role_ref
    if scope=='operator':return bool(operator_ref) and ref==operator_ref
    return False


def _is_local(extension):return str(extension.get('workflow_id') or '').startswith('custom.')

def all_extensions(business_id):return [obj for obj,_ in iter_instance_objects(business_id) if obj.get('object_type')=='ProcessExtension']

def active_extensions(business_id,team_ref=None,role_ref=None,operator_ref=None):
    out=[]
    for extension in all_extensions(business_id):
        if extension.get('status')!='active' or not _scope_applies(extension,team_ref,role_ref,operator_ref):continue
        out.append(extension)
    return sorted(out,key=lambda extension:(SCOPE_ORDER.get(extension.get('scope'),99),extension.get('id','')))
def get_extension(business_id,extension_id):
    for extension in all_extensions(business_id):
        if extension.get('id')==extension_id:return extension
    raise ValueError(f'Unknown ProcessExtension for {business_id}: {extension_id}')


def _canonical_workflow(workflow_id):
    matches=[]
    for path in workflow_files():
        try:meta,body=read_frontmatter(path)
        except Exception:continue
        if meta.get('id')==workflow_id:matches.append((path,meta,body))
    if not matches:return None
    if len(matches)>1:raise ValueError(f'Duplicate Workflow id: {workflow_id}')
    if matches[0][1].get('type')!='workflow':raise ValueError(f'{workflow_id} is not an AURA Workflow')
    return matches[0]


def local_workflows(business_id,team_ref=None,role_ref=None,operator_ref=None):
    return [extension for extension in active_extensions(business_id,team_ref,role_ref,operator_ref) if _is_local(extension)]


def local_workflow_candidates(task,business_id,team_ref=None,role_ref=None,operator_ref=None,top=6):
    query=str(task or '').strip().lower()
    if not query:return []
    words=set(re.findall(r'[a-z0-9]{2,}',query));rows=[]
    for extension in local_workflows(business_id,team_ref,role_ref,operator_ref):
        workflow_id=str(extension.get('workflow_id') or '');title=str(extension.get('title') or '');purpose=str(extension.get('purpose') or '')
        text=' '.join([workflow_id,title,purpose,*[str(term) for term in extension.get('discovery_terms') or []]]).lower();score=10000 if query==workflow_id.lower() else len(words & set(re.findall(r'[a-z0-9]{2,}',text)))*3
        if title and title.lower() in query:score+=6
        if score<=0:continue
        rows.append((score,{'score':score,'workflow_id':workflow_id,'status':'available','local_workflow':True,'process_extension_id':extension.get('id'),'selection_authority':False,'reason':'organization-local Workflow candidate only; the active model/user judges semantic applicability'}))
    rows.sort(key=lambda item:(item[0],item[1]['workflow_id']),reverse=True)
    return [row for _,row in rows[:max(1,int(top))]]


def _merge_metadata(base_meta,extensions):
    meta=json.loads(json.dumps(base_meta));meta['process_extension_ids']=[extension['id'] for extension in extensions];return meta


def _extension_markdown(extension):
    lines=[f"### {extension.get('title')} (`{extension.get('id')}`)",'',f"Scope: `{extension.get('scope')}`. This is organization-owned Workflow knowledge, not authority over the active model/harness/user.",'']
    if extension.get('applies_when'):lines+=['**Applies when**']+[f"- {item}" for item in extension['applies_when']]+['']
    if extension.get('does_not_apply_when'):lines+=['**Does not apply when**']+[f"- {item}" for item in extension['does_not_apply_when']]+['']
    lines+=['**Additional operating instructions**']+[f"{index+1}. {item}" for index,item in enumerate(extension.get('instructions') or [])]+['']
    if extension.get('verification'):lines+=['**Useful verification guidance**']+[f"- {item}" for item in extension.get('verification') or []]+['']
    return '\n'.join(lines)


def resolve_effective(workflow_id,business_id,team_ref=None,role_ref=None,operator_ref=None):
    local=next((extension for extension in local_workflows(business_id,team_ref,role_ref,operator_ref) if extension.get('workflow_id')==workflow_id),None)
    if local:
        meta={'id':local['workflow_id'],'type':'workflow','process_extension_ids':[local['id']],'local_workflow':True}
        body=['---',f"id: {meta['id']}",'type: workflow','---',f"# {local['title']}",'','## Purpose',local['purpose'],'','## Applicability']+[f"- Applies when: {item}" for item in local.get('applies_when') or []]+[f"- Does not apply when: {item}" for item in local.get('does_not_apply_when') or []]+['','## Process']+[f"{index+1}. {item}" for index,item in enumerate(local.get('instructions') or [])]
        if local.get('verification'):body+=['','## Verification']+[f"- {item}" for item in local.get('verification') or []]
        body+=['','## Extension Boundary','This is organization-scoped Workflow knowledge. The active model/harness/user may adapt it or choose another sound method; AURA truth, provenance, persistence, and organization-isolation integrity still apply.','']
        return None,meta,'\n'.join(body),[local]
    canonical=_canonical_workflow(workflow_id)
    if not canonical:raise ValueError(f'Unknown Workflow id for {business_id}: {workflow_id}')
    path,meta,_=canonical;extensions=[extension for extension in active_extensions(business_id,team_ref,role_ref,operator_ref) if not _is_local(extension) and extension.get('workflow_id')==workflow_id];effective_meta=_merge_metadata(meta,extensions);content=path.read_text()
    if extensions:content+='\n\n## Active Organization Workflow Extensions\n\nThese organization-scoped extensions add relevant operating knowledge to this AURA Workflow. They do not create runtime authority or prevent the active intelligence from choosing another valid method. If applicable extensions conflict semantically, the model/user resolves that conflict from actual organization context.\n\n'+'\n'.join(_extension_markdown(extension) for extension in extensions)
    return path,effective_meta,content,extensions
