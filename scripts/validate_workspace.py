#!/usr/bin/env python3
from _common import *
import json,re
from validate_provider_config import provider_config_errors
REQUIRED=['## Purpose','## Business Outcome','## Run When','## Process']
BAD_VENDOR=['HubSpot','Salesforce','Semrush','Ahrefs','Mailchimp','Klaviyo','OpenAI SDK','Anthropic SDK','Gemini SDK']
GENERIC=[r'Improve decisions by producing reliable, reusable .* intelligence or execution',r'Run when .* evidence is required for a current intelligence need, refresh, monitoring cycle, or decision',r'Improve valuable organic discovery and its contribution to business outcomes while preserving domain boundaries and evidence lineage']

def main():
    errors=[];warnings=[];ids={}
    capcat=json.loads((ROOT/'core/capabilities/catalog.json').read_text());validcaps={x['id'] for x in capcat['capabilities']}
    owners=installed_modules()
    declared=installation().get('installed_modules',[])
    present={'core'} | ({p.name for p in (ROOT/'systems').iterdir() if p.is_dir()} if (ROOT/'systems').exists() else set())
    if set(declared)!=present: errors.append(f'INSTALLATION.json modules {sorted(declared)} do not match present modules {sorted(present)}')
    if 'core' not in owners: errors.append('Core must be installed')
    sreg={json.loads(p.read_text()).get('title') for p in schemas()}
    for p in contract_files():
        try:meta,body=read_frontmatter(p)
        except Exception as e:errors.append(str(e));continue
        rel=str(p.relative_to(ROOT));cid=meta.get('id')
        for k in ['id','type','version','owner_system','risk','autonomy_ceiling','reads','writes','capabilities']:
            if k not in meta: errors.append(f'{rel}: missing metadata {k}')
        if cid:
            if cid in ids:errors.append(f'{rel}: duplicate id also at {ids[cid]}')
            ids[cid]=rel
        if meta.get('owner_system') not in owners:errors.append(f'{rel}: invalid owner {meta.get("owner_system")}')
        for sec in REQUIRED:
            if sec not in body:errors.append(f'{rel}: missing section {sec}')
        proc=re.search(r'## Process\n(.*?)(?=\n## |\Z)',body,re.S)
        if proc is not None and not proc.group(1).strip():errors.append(f'{rel}: empty Process section')
        for c in meta.get('capabilities',{}).get('required',[])+meta.get('capabilities',{}).get('optional',[]):
            if c!='none' and c not in validcaps:errors.append(f'{rel}: unknown capability {c}')
        for sel in meta.get('reads',[]):
            typ=selector_type(sel)
            if typ not in sreg:errors.append(f'{rel}: non-canonical read selector {sel}')
            if isinstance(sel,dict) and set(sel)-{'type','owner_system','owner_scope'}: errors.append(f'{rel}: unsupported read selector keys {sel}')
        for typ in meta.get('writes',[]):
            if not isinstance(typ,str) or typ not in sreg:errors.append(f'{rel}: non-canonical write type {typ}')
        role=meta.get('artifact_role')
        if role not in {None,'customer_facing_production_root'}: errors.append(f'{rel}: unsupported artifact_role {role}')
        if role=='customer_facing_production_root':
            if meta.get('owner_system') not in {'content-synthesis','marketing-synthesis'}: errors.append(f'{rel}: customer-facing production root must belong to Content or Marketing')
            if 'Asset' not in meta.get('writes',[]): errors.append(f'{rel}: customer-facing production root must write Asset')
        for typ in meta.get('context',[]):
            if typ not in CONTEXT_TYPES:errors.append(f'{rel}: invalid context type {typ}')
        if re.search(r'\b(TODO|TBD|LOREM|PLACEHOLDER)\b',body,re.I):errors.append(f'{rel}: placeholder marker')
        for v in BAD_VENDOR:
            if v.lower() in body.lower():errors.append(f'{rel}: vendor coupling {v}')
        for pat in GENERIC:
            if re.search(pat,body,re.I):errors.append(f'{rel}: generic template language remains: {pat}')
        legacy_patterns=[r'_state/',r'_brand/',r'_system/',r'Route → `(?:0[1-9]|1[0-3])_',r'\bStrategyEvidence\b',r'\bCapabilityMatrix\b',r'ChangeEvent\.measured_effect',r'Opportunity\.learning',r'OrganicOrganic',r'StateState',r'\bSEOAsset\b',r'\bStage (?:[0-9]|1[0-3])(?:/[0-9]+)?\b']
        for pat in legacy_patterns:
            if re.search(pat,body):errors.append(f'{rel}: legacy artifact matches {pat}')
    # Process-completeness references: all subcontracts and process-map entries must resolve.
    all_ids=set(ids)
    for p in contract_files():
        meta,_=read_frontmatter(p); sc=meta.get('subcontracts') or {}
        for kind in ('required','conditional'):
            for item in sc.get(kind,[]) or []:
                ref=item.get('id') if isinstance(item,dict) else item
                if ref not in all_ids: errors.append(f'{p.relative_to(ROOT)}: unknown {kind} subcontract {ref}')
    map_paths=[]
    if (ROOT/'core/process-map.json').exists(): map_paths.append(ROOT/'core/process-map.json')
    map_paths += sorted((ROOT/'systems').glob('*/process-map.json'))
    for mp in map_paths:
        try: d=json.loads(mp.read_text())
        except Exception as e: errors.append(f'{mp.relative_to(ROOT)} invalid JSON: {e}'); continue
        seen=set()
        for a in d.get('activities',[]):
            aid=a.get('id'); entry=a.get('entry_contract')
            if not aid or aid in seen: errors.append(f'{mp.relative_to(ROOT)}: missing/duplicate activity {aid}')
            seen.add(aid)
            if entry not in all_ids: errors.append(f'{mp.relative_to(ROOT)}: unknown entry contract {entry}')
            for ref in a.get('supporting_contracts',[]):
                if ref not in all_ids: errors.append(f'{mp.relative_to(ROOT)}: unknown supporting contract {ref}')
    for p in schemas():
        try:
            s=json.loads(p.read_text())
            if s.get('type')=='object' and s.get('additionalProperties') is not False:errors.append(f'{p.relative_to(ROOT)}: top-level schema must be strict')
        except Exception as e:errors.append(f'{p.relative_to(ROOT)} invalid JSON: {e}')
    # Reactive/event interoperability profiles are machine contracts and must remain edition-safe.
    ep=ROOT/'core/monitoring/event-consumer-profile.json'
    if ep.exists():
        try:
            ed=json.loads(ep.read_text())
            es=json.loads((ROOT/'core/schemas/runtime/businessos-event-consumer-profile.schema.json').read_text())
            for e in __import__('jsonschema').Draft202012Validator(es).iter_errors(ed): errors.append(f'{ep.relative_to(ROOT)}: {e.message}')
            for fam in ed.get('event_families',[]):
                if fam.get('owner_system') not in owners: errors.append(f'{ep.relative_to(ROOT)}: event family {fam.get("id")} references omitted owner {fam.get("owner_system")}')
                for ref in fam.get('preferred_contracts',[]):
                    if ref not in all_ids: errors.append(f'{ep.relative_to(ROOT)}: event family {fam.get("id")} references unknown contract {ref}')
        except Exception as e: errors.append(f'{ep.relative_to(ROOT)} invalid: {e}')
    rmp=ROOT/'instances/_template/config/reactive-monitoring.json'
    if rmp.exists():
        try:
            rd=json.loads(rmp.read_text()); rs=json.loads((ROOT/'core/schemas/runtime/reactive-monitoring-profile.schema.json').read_text())
            for e in __import__('jsonschema').Draft202012Validator(rs).iter_errors(rd): errors.append(f'{rmp.relative_to(ROOT)}: {e.message}')
        except Exception as e: errors.append(f'{rmp.relative_to(ROOT)} invalid: {e}')
    if not (ROOT/'instances/_template/instance.json').exists():errors.append('missing instance template')
    for f in ['GLOSSARY.md','TASK-NAVIGATOR.md','PLAYBOOKS.md']:
        if not (ROOT/f).exists():errors.append(f'missing human navigation {f}')

    # Human playbook catalog is generated from the canonical contract/process metadata.
    installed=set(installation().get('installed_modules',[]))
    expected_pages={'core': ROOT/'docs/playbooks/core.md'}
    for mid in installed - {'core'}:
        expected_pages[mid]=ROOT/'docs/playbooks'/f'{mid}.md'
    for mid,page in expected_pages.items():
        if not page.exists(): errors.append(f'missing human playbook page for {mid}: {page.relative_to(ROOT)}')
    if 'customer-intelligence' in installed and not (ROOT/'docs/playbooks/examples/research-public-reviews.md').exists():
        errors.append('missing human playbook example docs/playbooks/examples/research-public-reviews.md')
    catalog_pages=[ROOT/'PLAYBOOKS.md'] + (list((ROOT/'docs/playbooks').rglob('*.md')) if (ROOT/'docs/playbooks').exists() else [])
    for page in catalog_pages:
        if not page.exists(): continue
        try: page_text=page.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            errors.append(f'{page.relative_to(ROOT)}: invalid UTF-8: {e}')
            continue
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',page_text):
            clean=target.split('#',1)[0].strip()
            if not clean or clean.startswith(('http://','https://','mailto:','#')): continue
            resolved=(page.parent/clean).resolve()
            if not resolved.exists(): errors.append(f'{page.relative_to(ROOT)}: broken local link {target}')
    for f in ['core/policies/portable-first.md','core/policies/local-state-and-recovery.md','core/policies/capability-preflight.md','core/policies/host-capability-discovery.md','scripts/bootstrap_environment.py','WELCOME.md','scripts/preflight_capabilities.py','deployment/environments/local/tool-inventory.json','deployment/environments/local/capability-bindings.json','deployment/environments/local/provider-preferences.json','core/policies/external-research-interaction.md','core/policies/context-reuse-and-question-minimization.md','instances/_template/config/external-research-profile.json','core/schemas/runtime/external-research-profile.schema.json','deployment/operator-profile.json','core/schemas/runtime/operator-profile.schema.json','scripts/update_research_profile.py','scripts/resolve_research_profile.py','core/policies/viraltrac-native-companion.md','core/providers/viraltrac/companion-profile.json','core/providers/viraltrac/object-mapping.json','core/schemas/runtime/provider-companion-profile.schema.json','core/schemas/runtime/provider-capability-snapshot.schema.json','scripts/sync_viraltrac_capabilities.py','core/providers/viraltrac/event-interoperability.json','core/schemas/runtime/provider-event-interoperability.schema.json','core/monitoring/event-consumer-profile.json','core/schemas/runtime/businessos-event-consumer-profile.schema.json','core/schemas/runtime/event-reaction-decision.schema.json','core/schemas/runtime/reactive-monitoring-profile.schema.json','instances/_template/config/reactive-monitoring.json','scripts/activate_viraltrac_event_plane.py','scripts/event_reaction_key.py','core/policies/agent-execution.md','core/policies/active-business-truth.md','core/policies/preferences-and-adaptation.md','core/policies/shared-workspace-coordination.md','core/schemas/context/preference-profile.schema.json','scripts/resolve_preferences.py','scripts/upsert_preference_profile.py','scripts/migrate_preference_profiles.py','scripts/resolve_contract.py','scripts/bootstrap_explicit_context.py','scripts/canonical_store.py','scripts/persist_run_results.py','scripts/validate_business.py','core/policies/attention-lifecycle.md','core/policies/platform-intelligence.md','core/schemas/action/attention-item.schema.json','core/schemas/intelligence/platform-change.schema.json','scripts/upsert_attention.py','scripts/list_attention.py','scripts/set_attention_status.py','scripts/record_platform_change.py','scripts/list_platform_state.py','scripts/maintain_lifecycle.py','scripts/validate_attention_lifecycle.py']:
        if not (ROOT/f).exists(): errors.append(f'missing portable-first component {f}')
    if installation().get('portable_first') is not True: errors.append('INSTALLATION.json must declare portable_first=true')
    if installation().get('default_environment')!='local': errors.append('INSTALLATION.json default_environment must be local')
    errors.extend(provider_config_errors())
    print(f'Contracts checked: {len(ids)}');print(f'Errors: {len(errors)}; Warnings: {len(warnings)}')
    for x in errors[:150]:print('ERROR',x)
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
