#!/usr/bin/env python3
from _common import *
import json, re

def main():
    gen=ROOT/'generated'; gen.mkdir(exist_ok=True)
    contracts=[]; ids=set(); event_consumers={}; caps={}; deps={}; routes=[]; schedules=[]
    for p in contract_files():
        meta,body=read_frontmatter(p)
        cid=meta.get('id')
        if not cid: continue
        if cid in ids: raise SystemExit(f'Duplicate contract id: {cid}')
        ids.add(cid)
        title=re.search(r'^#\s+(.+)',body,re.M)
        purpose=re.search(r'^## Purpose\n(.+?)(?=\n## |\Z)',body,re.M|re.S)
        rec={**meta,'path':str(p.relative_to(ROOT)),'title':title.group(1).strip() if title else cid,'purpose':purpose.group(1).strip() if purpose else ''}
        rec['read_selectors']=[normalize_selector(x) for x in meta.get('reads',[])]
        rec['write_types']=[selector_type(x) for x in meta.get('writes',[])]
        rec['context_types']=meta.get('context',[])
        contracts.append(rec)
        for c in meta.get('capabilities',{}).get('required',[]) + meta.get('capabilities',{}).get('optional',[]):
            if c!='none': caps.setdefault(c,[]).append(cid)
        for e in meta.get('events',{}).get('consumes',[]):
            if e!='none': event_consumers.setdefault(e,[]).append(cid)
        deps[cid]={'context':meta.get('context',[]),'reads':rec['read_selectors'],'writes':rec['write_types'],'evidence_inputs':meta.get('evidence_inputs',[])}
        token_source=' '.join([rec['title'],rec['purpose'],cid]).lower()
        tokens=sorted(set(re.findall(r'[a-z0-9]{3,}',token_source)))
        routes.append({'contract_id':cid,'owner_system':meta.get('owner_system'),'tokens':tokens})
        if meta.get('schedule'): schedules.append({'contract_id':cid,'owner_system':meta.get('owner_system'),**meta.get('schedule')})
    (gen/'contract-registry.json').write_text(json.dumps({'version':os_version(),'contracts':contracts},indent=2)+'\n')
    (gen/'system-registry.json').write_text(json.dumps({'systems':sorted(set(c.get('owner_system') for c in contracts if c.get('owner_system')))},indent=2)+'\n')
    (gen/'event-subscription-index.json').write_text(json.dumps(event_consumers,indent=2)+'\n')
    (gen/'capability-usage-index.json').write_text(json.dumps(caps,indent=2)+'\n')
    (gen/'context-dependency-index.json').write_text(json.dumps(deps,indent=2)+'\n')
    (gen/'route-index.json').write_text(json.dumps(routes,indent=2)+'\n')
    (gen/'schedule-index.json').write_text(json.dumps(schedules,indent=2)+'\n')
    process_maps=[]
    map_paths=[]
    if (ROOT/'core/process-map.json').exists(): map_paths.append(ROOT/'core/process-map.json')
    map_paths += sorted((ROOT/'systems').glob('*/process-map.json'))
    for pp in map_paths:
        try: process_maps.append(json.loads(pp.read_text()))
        except Exception as e: raise SystemExit(f'Invalid process map {pp}: {e}')
    (gen/'process-map-registry.json').write_text(json.dumps({'version':os_version(),'systems':process_maps},indent=2)+'\n')
    sreg=[]
    for p in schemas():
        d=json.loads(p.read_text());sreg.append({'title':d.get('title'),'path':str(p.relative_to(ROOT))})
    (gen/'schema-registry.json').write_text(json.dumps(sreg,indent=2)+'\n')
    (gen/'object-type-registry.json').write_text(json.dumps({x.get('title'):x.get('path') for x in sreg if x.get('title')},indent=2)+'\n')
    # Human-readable index and root manifest are generated from the same authored contract metadata to prevent drift.
    by_system={}
    for c in contracts: by_system.setdefault(c.get('owner_system','unknown'),[]).append(c)
    lines=['# Playbook Index','','Generated from contract frontmatter. Do not maintain a second manual list.','']
    for owner in sorted(by_system):
        lines += [f'## {owner}','']
        for c in sorted(by_system[owner], key=lambda x:x['id']):
            purpose=' '.join(c.get('purpose','').split())
            lines.append(f"- `{c['id']}` — {c.get('title',c['id'])}" + (f": {purpose}" if purpose else ''))
        lines.append('')
    (ROOT/'PLAYBOOK-INDEX.md').write_text('\n'.join(lines).rstrip()+'\n')
    # Build the plain-language human catalog from the same contract/process metadata.
    import generate_playbooks
    generate_playbooks.main()
    inst=installation();pub=publisher_metadata();publisher=pub.get('publisher',{}) if pub else {}
    manifest_root={
        'version':os_version(),
        'edition':inst.get('edition','unmanaged'),
        'display_name':inst.get('display_name','ViralTrac AURA'),
        'public_name':inst.get('public_name',publisher.get('product_name','ViralTrac AURA')),
        'name_expansion':inst.get('name_expansion',publisher.get('product_name_expansion','Agentic Understanding and Reinforcement Architecture')),
        'descriptor':inst.get('descriptor',publisher.get('product_descriptor','AI-native BusinessOS')),
        'brand':inst.get('brand','ViralTrac'),
        'branding':'BRANDING.md',
        'startup_message':inst.get('startup_message','WELCOME.md'),
        'host_capability_discovery':bool(inst.get('host_capability_discovery',True)),
        'publisher':{'id':publisher.get('id'),'name':publisher.get('name'),'metadata':'PUBLISHER.json'},
        'portable_first':bool(inst.get('portable_first',False)),
        'default_environment':inst.get('default_environment','local'),
        'workspace':{
            'default_root':'product_root',
            'external_root_supported':True,
            'migration_helper':'scripts/migrate_workspace.py',
            'selectors':['BUSINESSOS_WORKSPACE','.businessos/workspace.json'],
            'deployment_profiles':'distribution/deployment-profiles.json'
        },
        'state_locations':{
            'canonical_business':'instances/<business-id>/',
            'run':'runtime/runs/<business-id>/<run-id>/',
            'human_knowledge':'knowledge/<business-id>/',
            'attachments':'attachments/'
        },
        'installed_modules':sorted(installed_modules()),
        'systems':sorted(by_system),
        'contract_count':len(contracts),
        'schema_count':len(sreg),
        'capability_count':len(json.loads((ROOT/'core/capabilities/catalog.json').read_text()).get('capabilities',[])),
        'scheduled_contract_count':len(schedules),
        'entrypoints':{'welcome':'WELCOME.md','human':'START-HERE.md','deployment':'DEPLOYMENT.md','branding':'BRANDING.md','playbooks':'PLAYBOOKS.md','task_navigator':'TASK-NAVIGATOR.md','agent':'CONTEXT.md','glossary':'GLOSSARY.md'},
        'generated_from':'scripts/generate_registry.py'
    }
    (ROOT/'SYSTEM-MANIFEST.json').write_text(json.dumps(manifest_root,indent=2)+'\n')
    manifest=[]
    for p in sorted([x for x in ROOT.rglob('*') if x.is_file() and 'generated/' not in x.as_posix() and '__pycache__' not in x.as_posix()]):
        manifest.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    (gen/'workspace-manifest.json').write_text(json.dumps({'version':os_version(),'edition':inst.get('edition','unmanaged'),'files':manifest},indent=2)+'\n')
    (gen/'checksums.txt').write_text('\n'.join(f"{x['sha256']}  {x['path']}" for x in manifest)+'\n')
    print(f'Generated registry for {len(contracts)} contracts, {len(sreg)} schemas, {len(caps)} used capabilities.')
if __name__=='__main__': main()
