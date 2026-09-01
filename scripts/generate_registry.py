#!/usr/bin/env python3
"""Generate AURA knowledge/navigation registries without rebuilding a runtime control plane."""
from _common import *
import json,re

# Defensive exclusion for retired control/runtime metadata. validate_workspace.py rejects
# these keys in authored contracts; they must never become generated product semantics.
RETIRED_CONTRACT_METADATA={'risk','autonomy_ceiling','events','schedule'}


def _tokens(value):
    return sorted(set(re.findall(r'[a-z0-9]{3,}',str(value or '').lower())))


def _section(body,name):
    match=re.search(rf'^## {re.escape(name)}\n(.+?)(?=\n## |\Z)',body,re.M|re.S)
    return match.group(1).strip() if match else ''


def _write_task_navigator(process_maps,inst):
    cat=module_catalog();installed=sorted(installed_modules()-{'core'});maps={d.get('system'):d for d in process_maps if isinstance(d,dict)}
    lines=['# Task Navigator','',f"Installed edition: **{inst.get('display_name','ViralTrac AURA')}**.",'','ViralTrac AURA is an AI-native BusinessOS. Ask for an outcome in plain language; this file is a human browse view, not a requirement to select a playbook manually.','']
    for mid in installed:
        meta=cat.get(mid,{});lines += [f"## {meta.get('display_name',mid)}",'',meta.get('description',''),'','| Activity | Result | Entry contract |','|---|---|---|']
        for a in (maps.get(mid) or {}).get('activities',[]):lines.append(f"| `{a.get('id','')}` | {a.get('result','')} | `{a.get('entry_contract','')}` |")
        lines.append('')
    lines += ['## Core','','Core supplies organization-owned business context, evidence/provenance, decisions, optional continuity objects, measurement, Learning, reusable SOP knowledge, workspace integrity, and provider-neutral capability vocabulary.','','| Activity | Result | Entry contract |','|---|---|---|']
    for a in (maps.get('core') or {}).get('activities',[]):lines.append(f"| `{a.get('id','')}` | {a.get('result','')} | `{a.get('entry_contract','')}` |")
    lines += ['','See `DEPLOYMENT.md` for Simple / Power User / Organization deployment and `BRANDING.md` for public naming.',''];(ROOT/'TASK-NAVIGATOR.md').write_text('\n'.join(lines),encoding='utf-8')


def main():
    gen=ROOT/'generated';gen.mkdir(exist_ok=True);contracts=[];ids=set();caps={};deps={};routes=[]
    for p in contract_files():
        meta,body=read_frontmatter(p);cid=meta.get('id')
        if not cid:continue
        if cid in ids:raise SystemExit(f'Duplicate contract id: {cid}')
        ids.add(cid)
        title_match=re.search(r'^#\s+(.+)',body,re.M)
        title=title_match.group(1).strip() if title_match else cid
        purpose=_section(body,'Purpose')
        run_when=_section(body,'Run When')
        durable_meta={k:v for k,v in meta.items() if k not in RETIRED_CONTRACT_METADATA}
        rec={**durable_meta,'path':str(p.relative_to(ROOT)),'title':title,'purpose':purpose}
        rec['read_selectors']=[normalize_selector(x) for x in meta.get('reads',[])];rec['write_types']=[selector_type(x) for x in meta.get('writes',[])];rec['context_types']=meta.get('context',[]);contracts.append(rec)
        for c in meta.get('capabilities',{}).get('required',[])+meta.get('capabilities',{}).get('optional',[]):
            if c!='none':caps.setdefault(c,[]).append(cid)
        deps[cid]={'context':meta.get('context',[]),'reads':rec['read_selectors'],'writes':rec['write_types'],'evidence_inputs':meta.get('evidence_inputs',[])}
        title_tokens=_tokens(title);purpose_tokens=_tokens(purpose);run_when_tokens=_tokens(run_when);id_tokens=_tokens(cid.replace('.',' ').replace('-',' '))
        routes.append({
            'contract_id':cid,
            'owner_system':meta.get('owner_system'),
            'tokens':sorted(set(title_tokens+purpose_tokens+run_when_tokens+id_tokens)),
            'title_tokens':title_tokens,
            'purpose_tokens':purpose_tokens,
            'run_when_tokens':run_when_tokens,
        })
    (gen/'contract-registry.json').write_text(json.dumps({'version':os_version(),'contracts':contracts},indent=2)+'\n',encoding='utf-8')
    (gen/'system-registry.json').write_text(json.dumps({'systems':sorted(set(c.get('owner_system') for c in contracts if c.get('owner_system')))},indent=2)+'\n',encoding='utf-8')
    (gen/'capability-usage-index.json').write_text(json.dumps(caps,indent=2)+'\n',encoding='utf-8')
    (gen/'context-dependency-index.json').write_text(json.dumps(deps,indent=2)+'\n',encoding='utf-8')
    (gen/'route-index.json').write_text(json.dumps(routes,indent=2)+'\n',encoding='utf-8')
    for obsolete in ('event-subscription-index.json','schedule-index.json'):
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
    lines=['# Playbook Index','','Generated from contract frontmatter. Do not maintain a second manual list.','']
    for owner in sorted(by_system):
        lines += [f'## {owner}','']
        for c in sorted(by_system[owner],key=lambda x:x['id']):
            purpose=' '.join(c.get('purpose','').split());lines.append(f"- `{c['id']}` — {c.get('title',c['id'])}"+(f": {purpose}" if purpose else ''))
        lines.append('')
    (ROOT/'PLAYBOOK-INDEX.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    import generate_playbooks;generate_playbooks.main();inst=installation();_write_task_navigator(process_maps,inst);pub=publisher_metadata();publisher=pub.get('publisher',{}) if pub else {}
    manifest_root={
        'version':os_version(),'maturity':inst.get('maturity','alpha'),'edition':inst.get('edition','unmanaged'),'display_name':inst.get('display_name','ViralTrac AURA'),'public_name':inst.get('public_name',publisher.get('product_name','ViralTrac AURA')),'name_expansion':inst.get('name_expansion',publisher.get('product_name_expansion','Agentic Understanding and Reinforcement Architecture')),'descriptor':inst.get('descriptor',publisher.get('product_descriptor','AI-native BusinessOS')),'brand':inst.get('brand','ViralTrac'),'branding':'BRANDING.md','startup_message':inst.get('startup_message','BEGINNERS-GUIDE.md'),'publisher':{'id':publisher.get('id'),'name':publisher.get('name'),'metadata':'PUBLISHER.json'},'portable_first':bool(inst.get('portable_first',False)),'default_environment':inst.get('default_environment','local'),
        'workspace':{'default_root':'product_root','external_root_supported':True,'migration_helper':'scripts/migrate_workspace.py','selectors':['BUSINESSOS_WORKSPACE','.businessos/workspace.json'],'deployment_profiles':'distribution/deployment-profiles.json'},
        'state_locations':{'canonical_business':'instances/<business-id>/','run':'runtime/runs/<business-id>/<run-id>/','human_knowledge':'knowledge/<business-id>/','attachments':'attachments/'},
        'installed_modules':sorted(installed_modules()),'systems':sorted(by_system),'contract_count':len(contracts),'schema_count':len(sreg),'capability_count':len(json.loads((ROOT/'core/capabilities/catalog.json').read_text(encoding='utf-8')).get('capabilities',[])),'entrypoints':{'human':'BEGINNERS-GUIDE.md','deployment':'DEPLOYMENT.md','branding':'BRANDING.md','playbooks':'PLAYBOOKS.md','task_navigator':'TASK-NAVIGATOR.md','agent':'CONTEXT.md','glossary':'GLOSSARY.md'},'generated_from':'scripts/generate_registry.py'
    }
    (ROOT/'SYSTEM-MANIFEST.json').write_text(json.dumps(manifest_root,indent=2)+'\n',encoding='utf-8')
    manifest=[]
    for p in sorted([x for x in ROOT.rglob('*') if x.is_file() and 'generated/' not in x.as_posix() and '__pycache__' not in x.as_posix()]):manifest.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    (gen/'workspace-manifest.json').write_text(json.dumps({'version':os_version(),'edition':inst.get('edition','unmanaged'),'files':manifest},indent=2)+'\n',encoding='utf-8');(gen/'checksums.txt').write_text('\n'.join(f"{x['sha256']}  {x['path']}" for x in manifest)+'\n',encoding='utf-8');print(f'Generated registry for {len(contracts)} contracts, {len(sreg)} schemas, {len(caps)} used capabilities.')

if __name__=='__main__':main()
