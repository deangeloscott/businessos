from pathlib import Path
import yaml
from _common import ROOT


def write_contract(system,relpath,cid,title,purpose,outcome,run_when,steps,*,reads=None,writes=None,context=None,ctype='workflow',subcontracts=None,evidence_inputs=None,artifact_role=None,completion_evidence=None,references=None):
    """Author one AURA Workflow without runtime/tool/provider/version metadata.

    Reads/writes/subcontracts/completion evidence describe reusable operating knowledge;
    they do not create a runtime graph or permission model. Describe real work in natural
    language inside the Workflow. The active model/harness chooses actual tools, Skills,
    providers, orchestration, and implementation details.
    """
    p=ROOT/'systems'/system/'contracts'/relpath/'CONTEXT.md';p.parent.mkdir(parents=True,exist_ok=True)
    meta={'id':cid,'type':ctype,'owner_system':system,'reads':reads or [],'writes':writes or []}
    if artifact_role:meta['artifact_role']=artifact_role
    if completion_evidence:meta['completion_evidence']=completion_evidence
    if context:meta['context']=context
    if subcontracts:meta['subcontracts']=subcontracts
    if evidence_inputs:meta['evidence_inputs']=evidence_inputs
    if references:meta['references']=references
    fm=yaml.safe_dump(meta,sort_keys=False,width=1000).rstrip()
    body=[f'# {title}','','## Purpose',purpose,'','## Business Outcome',outcome,'','## Run When',run_when,'','## Process']
    body += [f'{i+1}. {s}' for i,s in enumerate(steps)]
    p.write_text('---\n'+fm+'\n---\n'+'\n'.join(body).rstrip()+'\n',encoding='utf-8');return p


def add_subcontracts(system,relpath,required=None,conditional=None):
    """Add Workflow-composition references without introducing execution semantics."""
    p=ROOT/'systems'/system/'contracts'/relpath/'CONTEXT.md';text=p.read_text(encoding='utf-8');end=text.find('\n---\n',4)
    meta=yaml.safe_load(text[4:end]) or {};meta.pop('version',None);meta.pop('capabilities',None)
    sc={}
    if required:sc['required']=required
    if conditional:sc['conditional']=conditional
    meta['subcontracts']=sc
    fm=yaml.safe_dump(meta,sort_keys=False,width=1000).rstrip();p.write_text('---\n'+fm+text[end:],encoding='utf-8')


def write_process_map(system,activities):
    """Write a human/model navigation map of common Workflows, never an execution graph."""
    import json
    p=ROOT/'systems'/system/'process-map.json';data={'system':system,'activities':activities}
    p.write_text(json.dumps(data,indent=2)+'\n')
