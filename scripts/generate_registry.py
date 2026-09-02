#!/usr/bin/env python3
"""Generate AURA knowledge/navigation registries without rebuilding a runtime control plane."""
from _common import *
import json,re

# Authored workflow metadata is operating knowledge only. Product version belongs to
# VERSION / INSTALLATION.json; runtime/control metadata belongs to the host.
RETIRED_CONTRACT_METADATA={'version','risk','autonomy_ceiling','events','schedule','capabilities'}


def _tokens(value):
    return sorted(set(re.findall(r'[a-z0-9]{3,}',str(value or '').lower())))


def _section(body,name):
    match=re.search(rf'^## {re.escape(name)}\n(.+?)(?=\n## |\Z)',body,re.M|re.S)
    return match.group(1).strip() if match else ''


def _write_task_navigator(process_maps,inst):
    from operating_knowledge import PLAYBOOK_BY_SYSTEM
    cat=module_catalog();installed=sorted(installed_modules()-{'core'});maps={d.get('system'):d for d in process_maps if isinstance(d,dict)}
    lines=['# Task Navigator','',f"Installed edition: **{inst.get('display_name','ViralTrac AURA')}**.",'','Ask for the business outcome in normal language. AURA may surface a high-level Playbook and useful Workflows; this file is only a human browse view.','']
    for mid in installed:
        meta=cat.get(mid,{});playbook=PLAYBOOK_BY_SYSTEM.get(mid)
        title=playbook.get('title') if playbook else meta.get('display_name',mid)
        summary=playbook.get('summary') if playbook else meta.get('description','')
        lines += [f"## {title}",'',summary,'','| Workflow | Result | Workflow ID |','|---|---|---|']
        for a in (maps.get(mid) or {}).get('activities',[]):lines.append(f"| {a.get('id','').replace('-',' ').title()} | {a.get('result','')} | `{a.get('entry_contract','')}` |")
        lines.append('')
    lines += ['## AURA Core','','Core supplies shared organization memory, truth/evidence rules, decisions, continuity, measurement, Learning, and workspace integrity. It supports the business Playbooks rather than acting as another business Playbook.','','| Workflow | Result | Workflow ID |','|---|---|---|']
    for a in (maps.get('core') or {}).get('activities',[]):lines.append(f"| {a.get('id','').replace('-',' ').title()} | {a.get('result','')} | `{a.get('entry_contract','')}` |")
    lines += ['','See `PLAYBOOKS.md` for the high-level business jobs and `WORKFLOW-INDEX.md` for the detailed reusable procedures.',''];(ROOT/'TASK-NAVIGATOR.md').write_text('\n'.join(lines),encoding='utf-8')


def main():
    gen=ROOT/'generated';gen.mkdir(exist_ok=True);contracts=[];ids=set();deps={};candidate_rows=[]
    for p in contract_files():
        meta,body=read_frontmatter(p);cid=meta.get('id')
        if not cid:continue
        if cid in ids:raise SystemExit(f'Duplicate contract id: {cid}')
        ids.add(cid)
        title_match=re.search(r'^#\s+(.+)',body,re.M);title=title_match.group(1).strip() if title_match else cid
        purpose=_section(body,'Purpose');run_when=_section(body,'Run When')
        durable_meta={k:v for k,v in meta.items() if k not in RETIRED_CONTRACT_METADATA}
        rec={**durable_meta,'path':str(p.relative_to(ROOT)),'title':title,'purpose':purpose}
        rec['read_selectors']=[normalize_selector(x) for x in meta.get('reads',[])];rec['write_types']=[selector_type(x) for x in meta.get('writes',[])];rec['context_types']=meta.get('context',[]);contracts.append(rec)
        deps[cid]={'context':meta.get('context',[]),'reads':rec['read_selectors'],'writes':rec['write_types'],'evidence_inputs':meta.get('evidence_inputs',[])}
        if meta.get('type')=='workflow':
            title_tokens=_tokens(title);purpose_tokens=_tokens(purpose);run_when_tokens=_tokens(run_when);id_tokens=_tokens(cid.replace('.',' ').replace('-',' '))
            candidate_rows.append({'workflow_id':cid,'contract_id':cid,'owner_system':meta.get('owner_system'),'artifact_role':meta.get('artifact_role'),'tokens':sorted(set(title_tokens+purpose_tokens+run_when_tokens+id_tokens)),'title_tokens':title_tokens,'purpose_tokens':purpose_tokens,'run_when_tokens':run_when_tokens})
    (gen/'contract-registry.json').write_text(json.dumps({'version':os_version(),'contracts':contracts},indent=2)+'\n',encoding='utf-8')
    (gen/'system-registry.json').write_text(json.dumps({'systems':sorted(set(c.get('owner_system') for c in contracts if c.get('owner_system')))},indent=2)+'\n',encoding='utf-8')
    (gen/'context-dependency-index.json').write_text(json.dumps(deps,indent=2)+'\n',encoding='utf-8')
    (gen/'workflow-candidate-index.json').write_text(json.dumps(candidate_rows,indent=2)+'\n',encoding='utf-8')
    for obsolete in ('capability-usage-index.json','playbook-candidate-index.json','event-subscription-index.json','schedule-index.json','route-index.json'):
        op=gen/obsolete
        if op.exists():op.unlink()
    process_maps=[];map_paths=[]
    if (ROOT/'core/process-map.json').exists():map_paths.append(ROOT/'core/process-map.json')
    map_paths+=sorted((ROOT/'systems').glob('*/process-map.json'))
    for pp in map_paths:
        try:process_maps.append(json.loads(pp.read_text(encoding='utf-8')))
        except Exception as e:raise SystemExit(f'Invalid process map {pp}: {e}')
    (gen/'process-map-registry.json').write_text(json.dumps({'version':os_version(),'systems':process_maps},indent=2)+'\n',encoding='utf-8')
    sreg=[]
    for p in schemas():
        d=json.loads(p.read_text(encoding='utf-8'));sreg.append({'title':d.get('title'),'path':str(p.relative_to(ROOT))})
    (gen/'schema-registry.json').write_text(json.dumps(sreg,indent=2)+'\n',encoding='utf-8');(gen/'object-type-registry.json').write_text(json.dumps({x.get('title'):x.get('path') for x in sreg if x.get('title')},indent=2)+'\n',encoding='utf-8')
    by_system={}
    for c in contracts:by_system.setdefault(c.get('owner_system','unknown'),[]).append(c)
    lines=['# Workflow Index','','Generated from AURA workflow frontmatter. These are reusable procedures, not a tool registry or execution graph.','']
    for owner in sorted(by_system):
        workflows=[c for c in by_system[owner] if c.get('type')=='workflow']
        if not workflows:continue
        lines += [f'## {owner}','']
        for c in sorted(workflows,key=lambda x:x['id']):
            purpose=' '.join(c.get('purpose','').split());lines.append(f"- `{c['id']}` — {c.get('title',c['id'])}"+(f": {purpose}" if purpose else ''))
        lines.append('')
    (ROOT/'WORKFLOW-INDEX.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    old=ROOT/'PLAYBOOK-INDEX.md'
    if old.exists():old.unlink()
    import generate_playbooks;generate_playbooks.main();inst=installation();_write_task_navigator(process_maps,inst);pub=publisher_metadata();publisher=pub.get('publisher',{}) if pub else {}
    from operating_knowledge import installed_playbooks
    workflow_count=sum(1 for c in contracts if c.get('type')=='workflow')
    manifest_root={
        'version':os_version(),'maturity':inst.get('maturity','alpha'),'edition':inst.get('edition','unmanaged'),'display_name':inst.get('display_name','ViralTrac AURA'),'public_name':inst.get('public_name',publisher.get('product_name','ViralTrac AURA')),'name_expansion':inst.get('name_expansion',publisher.get('product_name_expansion','Agentic Understanding and Reinforcement Architecture')),'descriptor':inst.get('descriptor',publisher.get('product_descriptor','AI-native BusinessOS')),'brand':inst.get('brand','ViralTrac'),'branding':'BRANDING.md','startup_message':inst.get('startup_message','BEGINNERS-GUIDE.md'),'publisher':{'id':publisher.get('id'),'name':publisher.get('name'),'metadata':'PUBLISHER.json'},'portable_first':bool(inst.get('portable_first',False)),'default_environment':inst.get('default_environment','local'),
        'workspace':{'default_root':'product_root','external_root_supported':True,'migration_helper':'scripts/migrate_workspace.py','selectors':['BUSINESSOS_WORKSPACE','.businessos/workspace.json'],'deployment_profiles':'distribution/deployment-profiles.json'},
        'state_locations':{'canonical_business':'instances/<business-id>/','run':'runtime/runs/<business-id>/<run-id>/','human_knowledge':'knowledge/<business-id>/','attachments':'attachments/'},
        'installed_modules':sorted(installed_modules()),'systems':sorted(by_system),'playbook_count':len(installed_playbooks()),'workflow_count':workflow_count,'contract_count':len(contracts),'schema_count':len(sreg),'entrypoints':{'human':'BEGINNERS-GUIDE.md','deployment':'DEPLOYMENT.md','branding':'BRANDING.md','playbooks':'PLAYBOOKS.md','workflows':'WORKFLOW-INDEX.md','task_navigator':'TASK-NAVIGATOR.md','agent':'CONTEXT.md','skill':'skills/viraltrac-aura/SKILL.md','glossary':'GLOSSARY.md'},'generated_from':'scripts/generate_registry.py'
    }
    (ROOT/'SYSTEM-MANIFEST.json').write_text(json.dumps(manifest_root,indent=2)+'\n',encoding='utf-8')
    manifest=[]
    for p in sorted([x for x in ROOT.rglob('*') if x.is_file() and 'generated/' not in x.as_posix() and '__pycache__' not in x.as_posix()]):manifest.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    (gen/'workspace-manifest.json').write_text(json.dumps({'version':os_version(),'edition':inst.get('edition','unmanaged'),'files':manifest},indent=2)+'\n',encoding='utf-8');(gen/'checksums.txt').write_text('\n'.join(f"{x['sha256']}  {x['path']}" for x in manifest)+'\n',encoding='utf-8');print(f'Generated registry for {len(contracts)} contracts, {workflow_count} workflows, {len(installed_playbooks())} playbooks, {len(sreg)} schemas.')

if __name__=='__main__':main()
