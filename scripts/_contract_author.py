from pathlib import Path
import yaml
from _common import ROOT, os_version

BASE_META = {
    'version':os_version(),
    'risk':'low',
    'autonomy_ceiling':2,
}

def write_contract(system, relpath, cid, title, purpose, outcome, run_when, steps, *, reads=None, writes=None, capabilities=None, context=None, risk='low', autonomy=2, ctype='playbook', subcontracts=None, evidence_inputs=None, events=None, schedule=None, artifact_role=None):
    p=ROOT/'systems'/system/'contracts'/relpath/'CONTEXT.md'
    p.parent.mkdir(parents=True,exist_ok=True)
    meta={
        'id':cid,'type':ctype,'version':os_version(),'owner_system':system,
        'risk':risk,'autonomy_ceiling':autonomy,
        'reads':reads or [],'writes':writes or [],
        'capabilities':capabilities or {'required':['none'],'optional':[]},
    }
    if artifact_role: meta['artifact_role']=artifact_role
    if context: meta['context']=context
    if subcontracts: meta['subcontracts']=subcontracts
    if evidence_inputs: meta['evidence_inputs']=evidence_inputs
    if events: meta['events']=events
    if schedule: meta['schedule']=schedule
    fm=yaml.safe_dump(meta,sort_keys=False,width=1000).rstrip()
    body=[f'# {title}','','## Purpose',purpose,'','## Business Outcome',outcome,'','## Run When',run_when,'','## Process']
    body += [f'{i+1}. {s}' for i,s in enumerate(steps)]
    p.write_text('---\n'+fm+'\n---\n'+ '\n'.join(body).rstrip()+'\n',encoding='utf-8')
    return p

def add_subcontracts(system, relpath, required=None, conditional=None):
    p=ROOT/'systems'/system/'contracts'/relpath/'CONTEXT.md'
    text=p.read_text(encoding='utf-8')
    end=text.find('\n---\n',4)
    meta=yaml.safe_load(text[4:end]) or {}
    meta['version']=os_version()
    sc={}
    if required: sc['required']=required
    if conditional: sc['conditional']=conditional
    meta['subcontracts']=sc
    fm=yaml.safe_dump(meta,sort_keys=False,width=1000).rstrip()
    p.write_text('---\n'+fm+text[end:],encoding='utf-8')


def write_process_map(system, activities):
    import json
    p=ROOT/'systems'/system/'process-map.json'
    data={'version':os_version(),'system':system,'activities':activities}
    p.write_text(json.dumps(data,indent=2)+'\n')
