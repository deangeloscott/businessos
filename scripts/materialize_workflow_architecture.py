#!/usr/bin/env python3
"""One-time local development helper for the canonical AURA Workflow refactor.

Run this only on `refactor/aura-playbook-workflow-skill-1`. It materializes the new
Playbook → Workflow → Step architecture directly in the repository, regenerates every
canonical derived navigation/index artifact, and then removes the one-time migration
machinery. It is development tooling, not a product migration feature.
"""
from pathlib import Path
import ast,re,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
EXPECTED_BRANCH='refactor/aura-playbook-workflow-skill-1'
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

QUALIFICATION_REPLACEMENTS=[
    ('contract_tests','workflow_tests'),
    ('contract_count','workflow_count'),
    ('contract_path','workflow_path'),
    ('contract_ids','workflow_ids'),
    ('contract_acceptance','workflow_acceptance'),
    ('event_from_contract','event_from_workflow'),
    ('CONTRACT_ID','WORKFLOW_ID'),
]

DUPLICATE_WORKFLOW_KEYS=('workflow_id','workflow_path','workflow_count','workflow_tests')


def _git(*args,check=True):
    return subprocess.run(['git',*args],cwd=ROOT,text=True,capture_output=True,check=check)


def guard_refactor_branch():
    try:branch=_git('branch','--show-current').stdout.strip()
    except (subprocess.CalledProcessError,FileNotFoundError) as exc:
        raise RuntimeError('Run this helper from a normal Git checkout with Git available.') from exc
    if branch!=EXPECTED_BRANCH:
        raise RuntimeError(f'Refusing destructive materialization on {branch!r}; expected {EXPECTED_BRANCH!r}.')
    if _git('diff','--quiet',check=False).returncode or _git('diff','--cached','--quiet',check=False).returncode:
        raise RuntimeError('Tracked local changes are present. Commit or stash them before materialization.')


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


def _collapse_duplicate_workflow_keys(text):
    """Collapse transitional adjacent aliases after both names become Workflow-native."""
    out=text
    for key in DUPLICATE_WORKFLOW_KEYS:
        # Handles values such as wid, c['workflow_id'], len(tests), and tests. The old
        # compatibility fields are adjacent in the authored qualification dictionaries.
        pattern=rf"(['\"]{re.escape(key)}['\"]\s*:\s*([^,\n]+)\s*,)\s*['\"]{re.escape(key)}['\"]\s*:\s*\2\s*,"
        out=re.sub(pattern,r'\1',out)
    return out


def _rewrite_python_architecture(path):
    text=path.read_text(encoding='utf-8');new=text
    new=new.replace(".get('contracts',[])",".get('workflows',[])")
    new=new.replace(".get('contracts', [])",".get('workflows', [])")
    new=new.replace("['contracts']","['workflows']")
    new=new.replace('["contracts"]','["workflows"]')
    # Path components written as ROOT/'...'/ 'contracts' /... move with the authored tree.
    new=re.sub(r"(?<=/)'contracts'(?=/)","'workflows'",new)
    new=re.sub(r'(?<=/)"contracts"(?=/)',r'"workflows"',new)
    new=new.replace('RETIRED_CONTRACT_METADATA','RETIRED_WORKFLOW_METADATA')
    new=new.replace('contract_id','workflow_id')
    new=_collapse_duplicate_workflow_keys(new)
    if new!=text:path.write_text(new,encoding='utf-8')


def rewrite_architecture_terms():
    changed=[]
    for path in text_files():
        if rewrite(path,COMMON_REPLACEMENTS):changed.append(str(path.relative_to(ROOT)))

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

    for path in text_files():
        if path.suffix.lower()=='.py':_rewrite_python_architecture(path)

    # Qualification should expose one Workflow vocabulary, not compatibility aliases.
    qroot=ROOT/'qualification'
    if qroot.exists():
        for path in qroot.rglob('*.py'):
            text=path.read_text(encoding='utf-8');new=text
            for old,replacement in QUALIFICATION_REPLACEMENTS:new=new.replace(old,replacement)
            for old,replacement in [('load_contracts','load_workflows'),('parse_contract','parse_workflow'),('contract_id','workflow_id'),('contract_files','workflow_files')]:new=new.replace(old,replacement)
            new=re.sub(r'\bcontracts\b','workflows',new)
            new=re.sub(r'\bcontract\b','workflow',new)
            new=re.sub(r'\bContract\b','Workflow',new)
            new=re.sub(r'\bcid\b','wid',new)
            new=_collapse_duplicate_workflow_keys(new)
            if new!=text:path.write_text(new,encoding='utf-8')
    return changed


def assert_python_integrity():
    problems=[]
    for path in ROOT.rglob('*.py'):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):continue
        try:tree=ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
        except SyntaxError as exc:
            problems.append(f'{path.relative_to(ROOT)}: Python syntax error at {exc.lineno}: {exc.msg}');continue
        for node in ast.walk(tree):
            if not isinstance(node,ast.Dict):continue
            seen=set()
            for key in node.keys:
                if isinstance(key,ast.Constant) and isinstance(key.value,str):
                    if key.value in seen:problems.append(f'{path.relative_to(ROOT)}:{getattr(node,"lineno",0)} duplicate dict key {key.value!r}')
                    seen.add(key.value)
    if problems:raise RuntimeError('Python integrity failed after Workflow rewrite:\n'+'\n'.join(problems[:200]))


def assert_qualification_shape():
    qroot=ROOT/'qualification'
    if not qroot.exists():return
    forbidden=('contract_id','contract_tests','contract_count','contract_path','contract_acceptance','event_from_contract','load_contracts','parse_contract','contract_files','--contract')
    problems=[]
    for path in qroot.rglob('*.py'):
        text=path.read_text(encoding='utf-8')
        for token in forbidden:
            if token in text:problems.append(f'{path.relative_to(ROOT)}: retired qualification architecture token remains: {token}')
    if problems:raise RuntimeError('Qualification Workflow cleanup incomplete:\n'+'\n'.join(problems[:200]))


def remove_stale_derived_state():
    generated=ROOT/'generated'
    if generated.exists():shutil.rmtree(generated)
    old=ROOT/'PLAYBOOK-INDEX.md'
    if old.exists():old.unlink()


def assert_canonical_shape(allow_one_time_helpers=False):
    problems=[]
    for path in ROOT.rglob('*'):
        if not path.exists():continue
        rel=path.relative_to(ROOT).as_posix()
        if '/contracts/' in f'/{rel}/' or rel.endswith('/contracts') or rel=='core/contracts':problems.append(f'legacy authored path: {rel}')

    forbidden={
        'contract_files':'retired Workflow loader name',
        'contract-registry.json':'retired registry filename',
        'resolve_contract':'retired Workflow resolver name',
        'target_contract_id':'retired ProcessExtension field',
        'local_contract_id':'retired ProcessExtension field',
        'proposed_local_contract_id':'retired evolution field',
    }
    helper_names={'validate_workspace.py'}
    if allow_one_time_helpers:helper_names|={'migrate_workflow_semantics.py','materialize_workflow_architecture.py'}
    for path in (ROOT/'scripts').glob('*.py'):
        if path.name in helper_names:continue
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

    schema_forbidden=['contract_id','target_contract_id','local_contract_id','proposed_local_contract_id','required_capabilities','optional_capabilities','PlaybookEvolutionProposal']
    for path in ROOT.rglob('*.schema.json'):
        text=path.read_text(encoding='utf-8');rel=path.relative_to(ROOT)
        for token in schema_forbidden:
            if f'"{token}"' in text:problems.append(f'{rel}: retired schema field/type remains: {token}')
    if problems:raise RuntimeError('Canonical Workflow materialization incomplete:\n'+'\n'.join(problems[:300]))


def run_python(rel):
    subprocess.run([sys.executable,str(ROOT/rel)],cwd=ROOT,check=True)


def regenerate_derived_state():
    run_python('scripts/generate_registry.py')
    required=[
        'generated/workflow-registry.json','generated/workflow-candidate-index.json',
        'generated/process-map-registry.json','generated/schema-registry.json',
        'generated/object-type-registry.json','generated/context-dependency-index.json',
        'generated/system-registry.json','generated/workspace-manifest.json','generated/checksums.txt',
        'WORKFLOW-INDEX.md','PLAYBOOKS.md','TASK-NAVIGATOR.md','SYSTEM-MANIFEST.json',
    ]
    missing=[rel for rel in required if not (ROOT/rel).exists()]
    if missing:raise RuntimeError('Derived regeneration incomplete: '+', '.join(missing))
    retired=ROOT/'generated/contract-registry.json'
    if retired.exists():raise RuntimeError('Retired contract registry was regenerated')
    registry=__import__('json').loads((ROOT/'generated/workflow-registry.json').read_text(encoding='utf-8'))
    if 'workflows' not in registry or 'contracts' in registry:raise RuntimeError('Workflow registry did not regenerate with one canonical workflows collection')
    return required


def retire_development_fossils():
    paths=[
        'scripts/_contract_author.py',
        'scripts/resolve_effective_contract.py',
        'scripts/resolve_contract.py',
        'tests/run_playbook_evolution_exchange.py',
        'scripts/migrate_workflow_semantics.py',
        'scripts/materialize_workflow_architecture.py',
    ]
    removed=[]
    for rel in paths:
        path=ROOT/rel
        if path.exists():path.unlink();removed.append(rel)
    return removed


def main():
    guard_refactor_branch()
    result=migrate(False)
    moved=rename_workflow_trees()
    rewrite_architecture_terms()
    remove_stale_derived_state()

    # Prove the transformed authored/code shape before deleting the recovery helpers.
    assert_python_integrity()
    assert_qualification_shape()
    assert_canonical_shape(allow_one_time_helpers=True)
    regenerate_derived_state()

    # The migration has served its only purpose. Remove it and regenerate once more so
    # manifests/checksums describe the final product tree rather than development tooling.
    removed=retire_development_fossils()
    remove_stale_derived_state()
    derived=regenerate_derived_state()
    assert_python_integrity()
    assert_qualification_shape()
    assert_canonical_shape(allow_one_time_helpers=False)

    print('Workflow semantic migration:',result)
    print('Workflow trees moved:',moved)
    print('Retired development artifacts:',removed)
    print('Regenerated derived artifacts:',len(derived))
    print('Canonical Workflow architecture materialized through step 5 successfully.')

if __name__=='__main__':main()
