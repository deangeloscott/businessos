#!/usr/bin/env python3
"""Validate the portable AURA product and its installed operating knowledge.

This validator protects mechanics AURA actually owns: Workflow metadata, canonical
schemas/references, Playbook/Workflow navigation, organization-state primitives, product
integrity, and first-principles boundaries. Tool/provider discovery, execution capability
inventories, schedulers, orchestration, and other host-runtime concerns are outside AURA.
"""
from _common import *
import json,re

REQUIRED=['## Purpose','## Business Outcome','## Run When','## Process']
BAD_VENDOR=['HubSpot','Salesforce','Semrush','Ahrefs','Mailchimp','Klaviyo','OpenAI SDK','Anthropic SDK','Gemini SDK']
GENERIC=[r'Improve decisions by producing reliable, reusable .* intelligence or execution',r'Run when .* evidence is required for a current intelligence need, refresh, monitoring cycle, or decision',r'Improve valuable organic discovery and its contribution to business outcomes while preserving domain boundaries and evidence lineage']
RETIRED_WORKFLOW_METADATA={'version','risk','autonomy_ceiling','events','schedule','capabilities','subcontracts'}


def main():
    errors=[];warnings=[];ids={};types={};owners=installed_modules();declared=installation().get('installed_modules',[]);present={'core'} | ({p.name for p in (ROOT/'systems').iterdir() if p.is_dir()} if (ROOT/'systems').exists() else set())
    if set(declared)!=present:errors.append(f'INSTALLATION.json modules {sorted(declared)} do not match present modules {sorted(present)}')
    if 'core' not in owners:errors.append('Core must be installed')
    sreg={json.loads(p.read_text()).get('title') for p in schemas()}
    for p in contract_files():
        try:meta,body=read_frontmatter(p)
        except Exception as exc:errors.append(str(exc));continue
        rel=str(p.relative_to(ROOT));wid=meta.get('id');wtype=meta.get('type')
        for key in ['id','type','owner_system','reads','writes']:
            if key not in meta:errors.append(f'{rel}: missing metadata {key}')
        if wtype=='service':errors.append(f'{rel}: retired service framing; AURA operating knowledge is not an internal service')
        if wtype=='playbook':errors.append(f'{rel}: flattened playbook metadata remains; detailed procedures are Workflows and high-level Playbooks are separate')
        if wtype not in {None,'workflow'}:errors.append(f'{rel}: unsupported operating-knowledge type {wtype!r}')
        retired=sorted(RETIRED_WORKFLOW_METADATA&set(meta))
        if retired:errors.append(f'{rel}: retired/redundant Workflow metadata remains: {retired}')
        if wid:
            if wid in ids:errors.append(f'{rel}: duplicate id also at {ids[wid]}')
            ids[wid]=rel;types[wid]=wtype
        if meta.get('owner_system') not in owners:errors.append(f'{rel}: invalid owner {meta.get("owner_system")}')
        for section in REQUIRED:
            if section not in body:errors.append(f'{rel}: missing section {section}')
        proc=re.search(r'## Process\n(.*?)(?=\n## |\Z)',body,re.S)
        if proc is not None and not proc.group(1).strip():errors.append(f'{rel}: empty Process section')
        for sel in meta.get('reads',[]):
            typ=selector_type(sel)
            if typ not in sreg:errors.append(f'{rel}: non-canonical read selector {sel}')
            if isinstance(sel,dict) and set(sel)-{'type','owner_system','owner_scope'}:errors.append(f'{rel}: unsupported read selector keys {sel}')
        for typ in meta.get('writes',[]):
            if not isinstance(typ,str) or typ not in sreg:errors.append(f'{rel}: non-canonical write type {typ}')
        role=meta.get('artifact_role')
        if role not in {None,'customer_facing_production_root'}:errors.append(f'{rel}: unsupported artifact_role {role}')
        if role=='customer_facing_production_root':
            if meta.get('owner_system') not in {'content-synthesis','marketing-synthesis'}:errors.append(f'{rel}: customer-facing production root must belong to Content or Marketing')
            if 'Asset' not in meta.get('writes',[]):errors.append(f'{rel}: customer-facing production root must write Asset')
        for typ in meta.get('context',[]):
            if typ not in CONTEXT_TYPES:errors.append(f'{rel}: invalid context type {typ}')
        if re.search(r'\b(TODO|TBD|LOREM|PLACEHOLDER)\b',body,re.I):errors.append(f'{rel}: placeholder marker')
        for vendor in BAD_VENDOR:
            if vendor.lower() in body.lower():errors.append(f'{rel}: vendor coupling {vendor}')
        for pat in GENERIC:
            if re.search(pat,body,re.I):errors.append(f'{rel}: generic template language remains: {pat}')
        legacy_patterns=[r'_state/',r'_brand/',r'_system/',r'Route → `(?:0[1-9]|1[0-3])_',r'\bStrategyEvidence\b',r'\bCapabilityMatrix\b',r'ChangeEvent\.measured_effect',r'Opportunity\.learning',r'OrganicOrganic',r'StateState',r'\bSEOAsset\b',r'\bStage (?:[0-9]|1[0-3])(?:/[0-9]+)?\b',r'provider-neutral capability (?:need|needs|ID|IDs)']
        for pat in legacy_patterns:
            if re.search(pat,body,re.I):errors.append(f'{rel}: legacy artifact matches {pat}')

    all_ids=set(ids)
    for p in contract_files():
        meta,_=read_frontmatter(p);composition=meta.get('workflows') or {}
        for kind in ('required','conditional'):
            for item in composition.get(kind,[]) or []:
                ref=item.get('id') if isinstance(item,dict) else item
                if ref not in all_ids:errors.append(f'{p.relative_to(ROOT)}: unknown {kind} composed Workflow {ref}')
                elif types.get(ref)!='workflow':errors.append(f'{p.relative_to(ROOT)}: composed reference {ref} is not type workflow')

    from operating_knowledge import installed_playbooks
    registry_rows=[{'id':wid,'type':types[wid]} for wid in ids]
    for playbook in installed_playbooks(registry_rows):
        entry=playbook.get('entry_workflow')
        if entry and entry not in all_ids:errors.append(f"Playbook {playbook['id']}: unknown entry Workflow {entry}")
        elif entry and types.get(entry)!='workflow':errors.append(f"Playbook {playbook['id']}: entry {entry} is not type workflow")

    map_paths=[]
    if (ROOT/'core/process-map.json').exists():map_paths.append(ROOT/'core/process-map.json')
    map_paths+=sorted((ROOT/'systems').glob('*/process-map.json'))
    for mp in map_paths:
        try:data=json.loads(mp.read_text())
        except Exception as exc:errors.append(f'{mp.relative_to(ROOT)} invalid JSON: {exc}');continue
        if 'version' in data:errors.append(f'{mp.relative_to(ROOT)}: redundant process-map version; VERSION/INSTALLATION.json are product-version authority')
        seen=set()
        for activity in data.get('activities',[]):
            aid=activity.get('id');entry=activity.get('entry_workflow')
            if not aid or aid in seen:errors.append(f'{mp.relative_to(ROOT)}: missing/duplicate Workflow activity {aid}')
            seen.add(aid)
            if not entry:errors.append(f'{mp.relative_to(ROOT)}: activity {aid} missing entry_workflow')
            elif entry not in all_ids:errors.append(f'{mp.relative_to(ROOT)}: unknown Workflow {entry}')
            elif types.get(entry)!='workflow':errors.append(f'{mp.relative_to(ROOT)}: entry {entry} must resolve to type workflow, found {types.get(entry)!r}')
            if 'entry_contract' in activity:errors.append(f'{mp.relative_to(ROOT)}: retired entry_contract key; use entry_workflow')
            if 'supporting_contracts' in activity:errors.append(f'{mp.relative_to(ROOT)}: retired supporting_contracts key; use supporting_workflows')
            for ref in activity.get('supporting_workflows',[]):
                if ref not in all_ids:errors.append(f'{mp.relative_to(ROOT)}: unknown supporting Workflow {ref}')

    for p in schemas():
        try:
            schema=json.loads(p.read_text())
            if schema.get('type')=='object' and schema.get('additionalProperties') is not False:errors.append(f'{p.relative_to(ROOT)}: top-level schema must be strict')
        except Exception as exc:errors.append(f'{p.relative_to(ROOT)} invalid JSON: {exc}')

    if not (ROOT/'instances/_template/instance.json').exists():errors.append('missing instance template')
    for name in ['GLOSSARY.md','TASK-NAVIGATOR.md','PLAYBOOKS.md','WORKFLOW-INDEX.md']:
        if not (ROOT/name).exists():errors.append(f'missing human navigation {name}')
    installed=set(installation().get('installed_modules',[]));expected_pages={'core':ROOT/'docs/playbooks/core.md'}
    for module in installed-{'core'}:expected_pages[module]=ROOT/'docs/playbooks'/f'{module}.md'
    for module,page in expected_pages.items():
        if not page.exists():errors.append(f'missing Playbook/Workflow page for {module}: {page.relative_to(ROOT)}')
    if 'customer-intelligence' in installed and not (ROOT/'docs/playbooks/examples/research-public-reviews.md').exists():errors.append('missing human example docs/playbooks/examples/research-public-reviews.md')
    catalog_pages=[ROOT/'PLAYBOOKS.md',ROOT/'WORKFLOW-INDEX.md']+(list((ROOT/'docs/playbooks').rglob('*.md')) if (ROOT/'docs/playbooks').exists() else [])
    for page in catalog_pages:
        if not page.exists():continue
        try:text=page.read_text(encoding='utf-8')
        except UnicodeDecodeError as exc:errors.append(f'{page.relative_to(ROOT)}: invalid UTF-8: {exc}');continue
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
            clean=target.split('#',1)[0].strip()
            if not clean or clean.startswith(('http://','https://','mailto:','#')):continue
            if not (page.parent/clean).resolve().exists():errors.append(f'{page.relative_to(ROOT)}: broken local link {target}')

    required_core=['CONTEXT.md','AGENTS.md','AURA-ATTACHMENT.md','skills/viraltrac-aura/SKILL.md','docs/operating-knowledge.md','core/DEFAULTS.md','core/policies/agent-execution.md','core/policies/workflow-evolution.md','core/policies/active-business-truth.md','core/policies/evidence.md','core/policies/provenance.md','core/policies/preferences-and-adaptation.md','core/policies/business-isolation.md','core/policies/context-provenance-and-claims.md','core/policies/monitoring-continuity.md','core/schemas/context/preference-profile.schema.json','core/schemas/decision/decision-record.schema.json','core/schemas/learning/workflow-evolution-proposal.schema.json','scripts/enter.py','scripts/find_playbooks.py','scripts/find_workflows.py','scripts/remember.py','scripts/create_run.py','scripts/complete_run.py','scripts/canonical_store.py','scripts/persist_workflow_evolution.py','scripts/validate_business.py','scripts/resolve_workflow.py','scripts/bootstrap_explicit_context.py','scripts/resolve_preferences.py','scripts/upsert_preference_profile.py','BEGINNERS-GUIDE.md']
    for rel in required_core:
        if not (ROOT/rel).exists():errors.append(f'missing AURA core component {rel}')
    retired_paths=['core/capabilities/catalog.json','docs/adding-a-capability.md','generated/capability-usage-index.json','generated/playbook-candidate-index.json','PLAYBOOK-INDEX.md','core/schemas/learning/playbook-evolution-proposal.schema.json','scripts/persist_playbook_evolution.py','core/policies/playbook-evolution.md','scripts/resolve_contract.py','scripts/run_lifecycle.py','scripts/reconcile_runs.py','scripts/run_provenance.py','scripts/persist_run_results.py','scripts/finalize_run.py','scripts/finalize_work_receipt.py','scripts/finalize_sop_run.py','scripts/complete_sop_run.py','scripts/record_contract_completion.py','scripts/route_task.py','scripts/route_and_resolve.py','templates/manual-action.md','core/quality/action-quality.md']
    for rel in retired_paths:
        if (ROOT/rel).exists():errors.append(f'retired control/routing/capability/semantic artifact reappeared: {rel}')
    if installation().get('portable_first') is not True:errors.append('INSTALLATION.json must declare portable_first=true')
    print(f'Workflows checked: {sum(1 for value in types.values() if value=="workflow")}');print(f'Errors: {len(errors)}; Warnings: {len(warnings)}')
    for item in errors[:200]:print('ERROR',item)
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
