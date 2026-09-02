#!/usr/bin/env python3
"""One-time development helper that materializes AURA's Workflow-native source tree.

This is intentionally not a product migration feature. It is used once on the refactor
branch, validates that legacy operating-knowledge architecture is gone, and then deletes
itself together with the older semantic migration helper and temporary CI runner.
"""
from pathlib import Path
import re,shutil,sys

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
if str(SCRIPTS) not in sys.path:sys.path.insert(0,str(SCRIPTS))

from migrate_workflow_semantics import migrate

TEXT_SUFFIXES={'.py','.md','.json','.yaml','.yml','.txt'}
SKIP_DIRS={'.git','dist','__pycache__','.pytest_cache','.venv','venv'}

COMMON_REPLACEMENTS=[
    ('contract_files','workflow_files'),
    ('entry_contract','entry_workflow'),
    ('supporting_contracts','supporting_workflows'),
    ('contract-registry.json','workflow-registry.json'),
    ('resolve_contract','resolve_workflow'),
    ('target_contract_id','target_workflow_id'),
    ('local_contract_id','local_workflow_id'),
    ('proposed_local_contract_id','proposed_local_workflow_id'),
    ('_canonical_contract','_canonical_workflow'),
    ('contract_map','workflow_map'),
    ('contract_index','workflow_index'),
    ('parse_contract','parse_workflow'),
    ('load_contracts','load_workflows'),
    ('/contracts/','/workflows/'),
    ('core/contracts','core/workflows'),
]


def text_files():
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):continue
        yield path


def rewrite(path,replacements):
    try:text=path.read_text(encoding='utf-8')
    except UnicodeDecodeError:return False
    new=text
    for old,replacement in replacements:new=new.replace(old,replacement)
    if new==text:return False
    path.write_text(new,encoding='utf-8');return True


def rename_workflow_trees():
    roots=[ROOT/'core']+sorted(p for p in (ROOT/'systems').iterdir() if p.is_dir())
    moved=[]
    for root in roots:
        old=root/'contracts';new=root/'workflows'
        if not old.exists():continue
        if new.exists():raise RuntimeError(f'Workflow target already exists: {new.relative_to(ROOT)}')
        old.rename(new);moved.append(str(new.relative_to(ROOT)))
    return moved


def rewrite_architecture_terms():
    changed=[]
    for path in text_files():
        if rewrite(path,COMMON_REPLACEMENTS):changed.append(str(path.relative_to(ROOT)))

    # Registry generation is the only place where the old plural collection name itself
    # represented the operating-knowledge model. Make the derived format Workflow-native.
    registry_script=ROOT/'scripts/generate_registry.py'
    if registry_script.exists():
        text=registry_script.read_text(encoding='utf-8')
        text=re.sub(r'\bcontracts\b','workflows',text)
        text=text.replace('RETIRED_CONTRACT_METADATA','RETIRED_WORKFLOW_METADATA')
        text=text.replace(
            '# workflow-registry.json is retained as an internal v0.1.x storage filename only. Its\n    # records are Workflow metadata and it is not a model-facing hierarchy concept.\n',
            '# The Workflow registry is a derived navigation view; authored Workflow files remain the source of truth.\n'
        )
        registry_script.write_text(text,encoding='utf-8')

    # Consumers of the derived registry should use the Workflow collection directly.
    for path in text_files():
        if path.suffix.lower()!='.py':continue
        text=path.read_text(encoding='utf-8');new=text
        new=new.replace(".get('contracts',[])",".get('workflows',[])")
        new=new.replace(".get('contracts', [])",".get('workflows', [])")
        new=new.replace('[\'contracts\']','[\'workflows\']')
        new=new.replace('["contracts"]','["workflows"]')
        new=new.replace('RETIRED_CONTRACT_METADATA','RETIRED_WORKFLOW_METADATA')
        new=new.replace('contract_id','workflow_id')
        if new!=text:path.write_text(new,encoding='utf-8')

    # Qualification is entirely about authored operating knowledge, so its local naming
    # should not preserve the retired Contract model either.
    qroot=ROOT/'qualification'
    if qroot.exists():
        for path in qroot.rglob('*.py'):
            text=path.read_text(encoding='utf-8');new=text
            for old,replacement in [('load_contracts','load_workflows'),('parse_contract','parse_workflow'),('contract_id','workflow_id'),('contract_files','workflow_files')]:new=new.replace(old,replacement)
            new=re.sub(r'\bcontracts\b','workflows',new)
            new=re.sub(r'\bcontract\b','workflow',new)
            new=re.sub(r'\bcid\b','wid',new)
            if new!=text:path.write_text(new,encoding='utf-8')
    return changed


def retire_development_fossils():
    paths=[
        'scripts/_contract_author.py',
        'scripts/resolve_effective_contract.py',
        'scripts/resolve_contract.py',
        'tests/run_playbook_evolution_exchange.py',
        'scripts/migrate_workflow_semantics.py',
        'scripts/materialize_workflow_architecture.py',
        '.github/workflows/aura-materialize-workflows.yml',
    ]
    removed=[]
    for rel in paths:
        path=ROOT/rel
        if path.exists():path.unlink();removed.append(rel)
    return removed


def remove_stale_derived_state():
    generated=ROOT/'generated'
    if generated.exists():shutil.rmtree(generated)
    old=ROOT/'PLAYBOOK-INDEX.md'
    if old.exists():old.unlink()


def assert_canonical_shape():
    problems=[]
    for path in ROOT.rglob('*'):
        if not path.exists():continue
        rel=path.relative_to(ROOT).as_posix()
        if '/contracts/' in f'/{rel}/' or rel.endswith('/contracts') or rel=='core/contracts':problems.append(f'legacy authored path: {rel}')

    # Active implementation may not depend on retired operating-knowledge identifiers.
    # Validators/tests are allowed to name retired concepts when asserting they stay gone.
    forbidden={
        'contract_files':'retired Workflow loader name',
        'contract-registry.json':'retired registry filename',
        'resolve_contract':'retired Workflow resolver name',
        'target_contract_id':'retired ProcessExtension field',
        'local_contract_id':'retired ProcessExtension field',
        'proposed_local_contract_id':'retired evolution field',
    }
    for path in (ROOT/'scripts').glob('*.py'):
        if path.name in {'validate_workspace.py'}:continue
        text=path.read_text(encoding='utf-8');rel=path.relative_to(ROOT).as_posix()
        for token,meaning in forbidden.items():
            if token in text:problems.append(f'{rel}: {meaning}: {token}')

    workflow_paths=list((ROOT/'core/workflows').rglob('CONTEXT.md'))+list((ROOT/'systems').glob('*/workflows/**/CONTEXT.md'))
    if not workflow_paths:problems.append('no authored Workflow source found after materialization')
    for path in workflow_paths:
        text=path.read_text(encoding='utf-8');rel=path.relative_to(ROOT)
        if re.search(r'^type:\s*playbook\s*$',text,re.M):problems.append(f'{rel}: flattened type: playbook remains')
        if re.search(r'^capabilities:\s*$',text,re.M):problems.append(f'{rel}: capability metadata remains')
        if re.search(r'^subcontracts:\s*$',text,re.M):problems.append(f'{rel}: subcontract composition remains')
        if 'PlaybookEvolutionProposal' in text:problems.append(f'{rel}: old Playbook evolution semantics remain')
        if 'core.learning.playbook-evolution' in text:problems.append(f'{rel}: old Playbook evolution id remains')
    if problems:raise RuntimeError('Canonical Workflow materialization incomplete:\n'+'\n'.join(problems[:300]))


def main():
    result=migrate(False)
    moved=rename_workflow_trees()
    rewrite_architecture_terms()
    remove_stale_derived_state()
    # Delete one-time development machinery before validating the final product tree.
    removed=retire_development_fossils()
    assert_canonical_shape()
    print('Workflow semantic migration:',result)
    print('Workflow trees moved:',moved)
    print('Retired development artifacts:',removed)
    print('Canonical Workflow architecture materialized successfully.')

if __name__=='__main__':main()
