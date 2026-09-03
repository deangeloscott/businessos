#!/usr/bin/env python3
"""Validate the portable AURA product and its authored operating knowledge.

This validator protects mechanics AURA actually owns: module/product integrity, canonical
schemas, Workflow metadata, Playbook/process-map references, navigation, and the absence
of retired control-plane artifacts. It intentionally does not judge business semantics,
model strategy, tool/provider choice, execution capability, or natural-language quality
through keyword/regex heuristics.
"""
from _common import *
import json,re

REQUIRED_SECTIONS=['## Purpose','## Business Outcome','## Run When','## Process']
RETIRED_WORKFLOW_METADATA={'version','risk','autonomy_ceiling','events','schedule','capabilities','subcontracts','artifact_role','workflows','action','intent','requires_capabilities','preferred_capabilities','route_when','required_companions','boundaries'}
RETIRED_PATHS=['core/DEFAULTS.md','core/policies/agent-execution.md','core/policies/business-isolation.md','core/capabilities/catalog.json','docs/adding-a-capability.md','generated/capability-usage-index.json','generated/playbook-candidate-index.json','PLAYBOOK-INDEX.md','core/schemas/learning/playbook-evolution-proposal.schema.json','scripts/persist_playbook_evolution.py','core/policies/playbook-evolution.md','core/schemas/learning/workflow-evolution-proposal.schema.json','scripts/persist_workflow_evolution.py','scripts/adopt_process_extension.py','core/workflows/learning/adopt-process-extension/CONTEXT.md','scripts/run_lifecycle.py','scripts/reconcile_runs.py','scripts/run_provenance.py','scripts/persist_run_results.py','scripts/finalize_run.py','scripts/finalize_work_receipt.py','scripts/finalize_sop_run.py','scripts/complete_sop_run.py','scripts/record_contract_completion.py','scripts/route_task.py','scripts/route_and_resolve.py','templates/manual-action.md','core/quality/action-quality.md','core/contracts']
REQUIRED_CORE=['CONTEXT.md','AGENTS.md','AURA-ATTACHMENT.md','skills/viraltrac-aura/SKILL.md','docs/operating-knowledge.md','core/policies/workflow-evolution.md','core/policies/active-business-truth.md','core/policies/evidence.md','core/policies/provenance.md','core/policies/preferences-and-adaptation.md','core/policies/context-provenance-and-claims.md','core/policies/monitoring-continuity.md','core/schemas/context/preference-profile.schema.json','core/schemas/decision/decision-record.schema.json','core/schemas/learning/process-extension.schema.json','scripts/enter.py','scripts/find_playbooks.py','scripts/find_workflows.py','scripts/remember.py','scripts/create_run.py','scripts/complete_run.py','scripts/canonical_store.py','scripts/persist_process_extension.py','scripts/process_extensions.py','scripts/validate_business.py','scripts/resolve_workflow.py','scripts/bootstrap_explicit_context.py','scripts/resolve_preferences.py','scripts/upsert_preference_profile.py','BEGINNERS-GUIDE.md']


def _validate_workflows(errors,owners,schema_titles):
    ids={};types={}
    for path in workflow_files():
        try:meta,body=read_frontmatter(path)
        except Exception as exc:errors.append(str(exc));continue
        rel=str(path.relative_to(ROOT));wid=meta.get('id');wtype=meta.get('type')
        for key in ('id','type','owner_system','reads','writes'):
            if key not in meta:errors.append(f'{rel}: missing metadata {key}')
        if wtype!='workflow':
            if wtype=='service':errors.append(f'{rel}: retired service framing; AURA operating knowledge is not an internal service')
            elif wtype=='playbook':errors.append(f'{rel}: flattened Playbook metadata remains; detailed procedures are Workflows and Playbooks are separate product knowledge')
            else:errors.append(f'{rel}: unsupported operating-knowledge type {wtype!r}')
        retired=sorted(RETIRED_WORKFLOW_METADATA&set(meta))
        if retired:errors.append(f'{rel}: retired/redundant Workflow metadata remains: {retired}')
        if wid:
            if wid in ids:errors.append(f'{rel}: duplicate id also at {ids[wid]}')
            ids[wid]=rel;types[wid]=wtype
        if meta.get('owner_system') not in owners:errors.append(f'{rel}: invalid operating-knowledge area {meta.get("owner_system")}')
        for section in REQUIRED_SECTIONS:
            if section not in body:errors.append(f'{rel}: missing section {section}')
        process=re.search(r'## Process\n(.*?)(?=\n## |\Z)',body,re.S)
        if process is not None and not process.group(1).strip():errors.append(f'{rel}: empty Process section')
        for selector in meta.get('reads',[]):
            typ=selector_type(selector)
            if typ not in schema_titles:errors.append(f'{rel}: non-canonical read selector {selector}')
            if isinstance(selector,dict) and set(selector)-{'type','domain','scope'}:errors.append(f'{rel}: unsupported read selector keys {selector}')
        for typ in meta.get('writes',[]):
            if not isinstance(typ,str) or typ not in schema_titles:errors.append(f'{rel}: non-canonical write type {typ}')
        for typ in meta.get('context',[]):
            if typ not in CONTEXT_TYPES:errors.append(f'{rel}: invalid context type {typ}')
    return ids,types

def _validate_playbooks_and_maps(errors,ids,types):
    all_ids=set(ids);from operating_knowledge import installed_playbooks;registry_rows=[{'id':wid,'type':types[wid]} for wid in ids]
    for playbook in installed_playbooks(registry_rows):
        entry=playbook.get('entry_workflow')
        if entry and entry not in all_ids:errors.append(f"Playbook {playbook['id']}: unknown entry Workflow {entry}")
        elif entry and types.get(entry)!='workflow':errors.append(f"Playbook {playbook['id']}: entry {entry} is not type workflow")
    map_paths=[]
    if (ROOT/'core/process-map.json').exists():map_paths.append(ROOT/'core/process-map.json')
    map_paths+=sorted((ROOT/'systems').glob('*/process-map.json'))
    for map_path in map_paths:
        try:data=json.loads(map_path.read_text())
        except Exception as exc:errors.append(f'{map_path.relative_to(ROOT)} invalid JSON: {exc}');continue
        if 'version' in data:errors.append(f'{map_path.relative_to(ROOT)}: redundant process-map version; VERSION/INSTALLATION.json are product-version authority')
        seen=set()
        for activity in data.get('activities',[]):
            aid=activity.get('id');entry=activity.get('entry_workflow')
            if not aid or aid in seen:errors.append(f'{map_path.relative_to(ROOT)}: missing/duplicate activity {aid}')
            seen.add(aid)
            if not entry:errors.append(f'{map_path.relative_to(ROOT)}: activity {aid} missing entry_workflow')
            elif entry not in all_ids:errors.append(f'{map_path.relative_to(ROOT)}: unknown Workflow {entry}')
            elif types.get(entry)!='workflow':errors.append(f'{map_path.relative_to(ROOT)}: entry {entry} must resolve to type workflow, found {types.get(entry)!r}')
            for ref in activity.get('supporting_workflows',[]) or []:
                if ref not in all_ids:errors.append(f'{map_path.relative_to(ROOT)}: unknown supporting Workflow {ref}')
                elif types.get(ref)!='workflow':errors.append(f'{map_path.relative_to(ROOT)}: supporting reference {ref} is not type workflow')

def _validate_schemas(errors):
    titles=set()
    for path in schemas():
        try:schema=json.loads(path.read_text())
        except Exception as exc:errors.append(f'{path.relative_to(ROOT)} invalid JSON: {exc}');continue
        title=schema.get('title')
        if title:titles.add(title)
        if schema.get('type')=='object' and schema.get('additionalProperties') is not False:errors.append(f'{path.relative_to(ROOT)}: top-level schema must be strict')
    return titles

def _validate_navigation(errors,installed):
    for name in ('GLOSSARY.md','TASK-NAVIGATOR.md','PLAYBOOKS.md','WORKFLOW-INDEX.md'):
        if not (ROOT/name).exists():errors.append(f'missing human navigation {name}')
    expected={'core':ROOT/'docs/playbooks/core.md'}
    for module in installed-{'core'}:expected[module]=ROOT/'docs/playbooks'/f'{module}.md'
    for module,page in expected.items():
        if not page.exists():errors.append(f'missing Playbook/Workflow page for {module}: {page.relative_to(ROOT)}')
    if 'customer-intelligence' in installed and not (ROOT/'docs/playbooks/examples/research-public-reviews.md').exists():errors.append('missing human example docs/playbooks/examples/research-public-reviews.md')
    pages=[ROOT/'PLAYBOOKS.md',ROOT/'WORKFLOW-INDEX.md']+(list((ROOT/'docs/playbooks').rglob('*.md')) if (ROOT/'docs/playbooks').exists() else [])
    for page in pages:
        if not page.exists():continue
        try:text=page.read_text(encoding='utf-8')
        except UnicodeDecodeError as exc:errors.append(f'{page.relative_to(ROOT)}: invalid UTF-8: {exc}');continue
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
            clean=target.split('#',1)[0].strip()
            if not clean or clean.startswith(('http://','https://','mailto:','#')):continue
            if not (page.parent/clean).resolve().exists():errors.append(f'{page.relative_to(ROOT)}: broken local link {target}')

def main():
    errors=[];warnings=[];declared=set(installation().get('installed_modules',[]));present={'core'}|({p.name for p in (ROOT/'systems').iterdir() if p.is_dir()} if (ROOT/'systems').exists() else set());owners=installed_modules()
    if declared!=present:errors.append(f'INSTALLATION.json modules {sorted(declared)} do not match present modules {sorted(present)}')
    if 'core' not in owners:errors.append('Core must be installed')
    schema_titles=_validate_schemas(errors);ids,types=_validate_workflows(errors,owners,schema_titles);_validate_playbooks_and_maps(errors,ids,types)
    if not (ROOT/'instances/_template/instance.json').exists():errors.append('missing instance template')
    _validate_navigation(errors,declared)
    for rel in REQUIRED_CORE:
        if not (ROOT/rel).exists():errors.append(f'missing AURA core component {rel}')
    for rel in RETIRED_PATHS:
        if (ROOT/rel).exists():errors.append(f'retired/redundant AURA artifact reappeared: {rel}')
    for path in sorted((ROOT/'systems').glob('*/contracts')):
        if path.exists():errors.append(f'retired contract tree reappeared: {path.relative_to(ROOT)}')
    if installation().get('portable_first') is not True:errors.append('INSTALLATION.json must declare portable_first=true')
    print(f'Workflows checked: {sum(1 for value in types.values() if value=="workflow")}');print(f'Errors: {len(errors)}; Warnings: {len(warnings)}')
    for item in errors[:200]:print('ERROR',item)
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
