#!/usr/bin/env python3
from _common import *
import json, re

RISK_ORDER={'low':0,'medium':1,'high':2}
SCOPE_ORDER={'business':0,'team':1,'role':2,'operator':3}

def _version_tuple(value):
    try:
        parts=[int(x) for x in str(value).split('.')]
        if len(parts)!=3: raise ValueError
        return tuple(parts)
    except Exception:
        raise ValueError(f'Invalid semantic version: {value!r}')

def version_compatible(compatibility, version=None):
    version=_version_tuple(version or os_version()); compatibility=compatibility or {}
    minv=compatibility.get('businessos_min'); maxv=compatibility.get('businessos_max')
    if minv and version < _version_tuple(minv): return False
    if maxv and version > _version_tuple(maxv): return False
    return True

def _scope_applies(ext, team_ref=None, role_ref=None, operator_ref=None):
    scope=ext.get('scope'); ref=ext.get('scope_ref')
    if scope=='business': return True
    if scope=='team': return bool(team_ref) and ref==team_ref
    if scope=='role': return bool(role_ref) and ref==role_ref
    if scope=='operator': return bool(operator_ref) and ref==operator_ref
    return False

def all_extensions(business_id):
    return [obj for obj,_ in iter_instance_objects(business_id) if obj.get('object_type')=='ProcessExtension']

def active_extensions(business_id, team_ref=None, role_ref=None, operator_ref=None):
    out=[]
    for ext in all_extensions(business_id):
        if ext.get('status')!='active': continue
        if not version_compatible(ext.get('compatibility') or {}): continue
        if not _scope_applies(ext,team_ref,role_ref,operator_ref): continue
        out.append(ext)
    return sorted(out,key=lambda x:(SCOPE_ORDER.get(x.get('scope'),99),int(x.get('priority',0)),x.get('id','')))

def get_extension(business_id, extension_id):
    for ext in all_extensions(business_id):
        if ext.get('id')==extension_id: return ext
    raise ValueError(f'Unknown ProcessExtension for {business_id}: {extension_id}')

def _canonical_contract(contract_id):
    matches=[]
    for p in contract_files():
        try: meta,body=read_frontmatter(p)
        except Exception: continue
        if meta.get('id')==contract_id: matches.append((p,meta,body))
    if not matches: return None
    if len(matches)>1: raise ValueError(f'Duplicate contract id: {contract_id}')
    return matches[0]

def local_playbooks(business_id, team_ref=None, role_ref=None, operator_ref=None):
    return [x for x in active_extensions(business_id,team_ref,role_ref,operator_ref) if x.get('mode')=='local_playbook']

def route_local_playbook(task,business_id,team_ref=None,role_ref=None,operator_ref=None):
    q=task.strip().lower(); words=set(re.findall(r'[a-z0-9]{2,}',q)); scored=[]
    for ext in local_playbooks(business_id,team_ref,role_ref,operator_ref):
        cid=(ext.get('local_contract_id') or '').lower(); title=(ext.get('title') or '').lower()
        if q==cid or (title and title in q): score=100
        else:
            score=0
            for term in ext.get('route_terms') or []:
                t=term.lower().strip()
                if t and t in q: score+=4
            tokens=set(re.findall(r'[a-z0-9]{2,}',' '.join([cid,title,ext.get('purpose') or ''])))
            score+=len(words & tokens)
        if score: scored.append((score,ext))
    scored.sort(key=lambda x:(x[0],x[1].get('local_contract_id','')),reverse=True)
    if not scored: return None
    top=scored[0][0]; second=scored[1][0] if len(scored)>1 else 0
    if top<4 or (top<100 and second and top-second<2): return None
    ext=scored[0][1]
    return {'score':top,'system_score':top,'contract_id':ext['local_contract_id'],'owner_system':ext['owner_system'],'status':'available','reason':'matched active business local playbook','process_extension_id':ext['id']}

def _merge_metadata(base_meta, extensions):
    meta=json.loads(json.dumps(base_meta)); caps=meta.setdefault('capabilities',{})
    req=[x for x in caps.get('required',[]) if x!='none']; opt=[x for x in caps.get('optional',[]) if x!='none']
    reads=[selector_type(x) for x in meta.get('reads',[])]; writes=[selector_type(x) for x in meta.get('writes',[])]
    risk=meta.get('risk','low'); ceiling=int(meta.get('autonomy_ceiling',4))
    for ext in extensions:
        req += ext.get('required_capabilities') or []; opt += ext.get('optional_capabilities') or []
        reads += ext.get('reads') or []; writes += ext.get('writes') or []
        erisk=ext.get('risk','low')
        if RISK_ORDER.get(erisk,0)>RISK_ORDER.get(risk,0): risk=erisk
        ceiling=min(ceiling,int(ext.get('autonomy_ceiling',ceiling)))
    req=list(dict.fromkeys(req)); opt=[x for x in dict.fromkeys(opt) if x not in req]
    meta['capabilities']={'required':req or ['none'],'optional':opt or ['none']}
    meta['reads']=list(dict.fromkeys(reads)); meta['writes']=list(dict.fromkeys(writes)); meta['risk']=risk; meta['autonomy_ceiling']=ceiling
    meta['process_extension_ids']=[x['id'] for x in extensions]
    return meta

def _extension_markdown(ext):
    lines=[f"### {ext.get('title')} (`{ext.get('id')}`)",'',f"Scope: `{ext.get('scope')}`. This extension adds requirements; canonical BusinessOS policy remains authoritative.",'']
    if ext.get('applies_when'): lines+=['**Applies when**']+[f"- {x}" for x in ext['applies_when']]+['']
    if ext.get('does_not_apply_when'): lines+=['**Does not apply when**']+[f"- {x}" for x in ext['does_not_apply_when']]+['']
    lines+=['**Additional operating instructions**']+[f"{i+1}. {x}" for i,x in enumerate(ext.get('instructions') or [])]+['']
    lines+=['**Additional verification**']+[f"- {x}" for x in ext.get('verification') or []]+['']
    return '\n'.join(lines)

def resolve_effective(contract_id,business_id,team_ref=None,role_ref=None,operator_ref=None):
    local=next((x for x in local_playbooks(business_id,team_ref,role_ref,operator_ref) if x.get('local_contract_id')==contract_id),None)
    if local:
        meta={'id':local['local_contract_id'],'type':'playbook','version':local.get('extension_version','1.0.0'),'owner_system':local['owner_system'],'risk':local.get('risk','medium'),'autonomy_ceiling':local.get('autonomy_ceiling',2),'reads':local.get('reads') or [],'writes':local.get('writes') or [],'capabilities':{'required':local.get('required_capabilities') or ['none'],'optional':local.get('optional_capabilities') or ['none']},'process_extension_ids':[local['id']],'local_playbook':True}
        body=['---']
        for key in ['id','type','version','owner_system','risk','autonomy_ceiling']: body.append(f"{key}: {meta[key]}")
        body += ['---',f"# {local['title']}",'','## Purpose',local['purpose'],'','## Applicability']
        body += [f"- Applies when: {x}" for x in local.get('applies_when') or []]; body += [f"- Does not apply when: {x}" for x in local.get('does_not_apply_when') or []]
        body += ['','## Process']+[f"{i+1}. {x}" for i,x in enumerate(local.get('instructions') or [])]
        body += ['','## Verification']+[f"- {x}" for x in local.get('verification') or []]
        body += ['','## Extension Boundary','This is a business-scoped local playbook. Core BusinessOS policies, truth/approval/evidence boundaries, and supported deterministic helpers remain authoritative.','']
        return None,meta,'\n'.join(body),[local]
    canonical=_canonical_contract(contract_id)
    if not canonical: raise ValueError(f'Unknown contract id for {business_id}: {contract_id}')
    path,meta,_=canonical
    exts=[x for x in active_extensions(business_id,team_ref,role_ref,operator_ref) if x.get('mode')=='augment_contract' and x.get('target_contract_id')==contract_id]
    effective_meta=_merge_metadata(meta,exts); content=path.read_text()
    if exts:
        content += '\n\n## Active Business Process Extensions\n\nThese business-scoped extensions are additive. They do not replace or weaken the canonical contract above.\n\n'
        content += '\n'.join(_extension_markdown(x) for x in exts)
    return path,effective_meta,content,exts

def effective_capabilities(contract_id,business_id,team_ref=None,role_ref=None,operator_ref=None):
    _,meta,_,exts=resolve_effective(contract_id,business_id,team_ref,role_ref,operator_ref); caps=meta.get('capabilities') or {}
    return {'required':[x for x in caps.get('required',[]) if x!='none'],'optional':[x for x in caps.get('optional',[]) if x!='none'],'process_extension_ids':[x['id'] for x in exts]}
