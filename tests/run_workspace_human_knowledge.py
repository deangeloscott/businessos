#!/usr/bin/env python3
"""End-to-end regression for AURA external workspaces, human knowledge, migration, and component packaging."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

import _common as common
from configure_workspace import configure
from migrate_workspace import migrate
from init_business import init_business
from configure_innovation_sharing import configure as configure_innovation
from generate_knowledge_layer import generate
from register_human_note import register_note
from workspace_status import status
from route_and_resolve import route_and_resolve
from package_edition import build_distribution

BID='test-workspace-deployment'
EXPECTED_NAME='ViralTrac AURA'
EXPECTED_EXPANSION='Agentic Understanding and Reinforcement Architecture'

def fail(msg): raise AssertionError(msg)

def main():
    required=[
        'BRANDING.md','DEPLOYMENT.md','distribution/deployment-profiles.json','core/policies/workspace-and-human-knowledge.md',
        'core/contracts/workspace/configure/CONTEXT.md','core/contracts/knowledge/refresh-human-layer/CONTEXT.md','core/contracts/knowledge/ingest-human-note/CONTEXT.md',
        'core/schemas/runtime/workspace-profile.schema.json','scripts/configure_workspace.py','scripts/migrate_workspace.py','scripts/workspace_status.py','scripts/generate_knowledge_layer.py','scripts/register_human_note.py'
    ]
    for rel in required:
        if not (ROOT/rel).exists(): fail(f'missing {rel}')
    inst=json.loads((ROOT/'INSTALLATION.json').read_text())
    if inst.get('display_name')!=EXPECTED_NAME or inst.get('name_expansion')!=EXPECTED_EXPANSION: fail('root AURA installation branding is incorrect')
    profiles=json.loads((ROOT/'distribution/deployment-profiles.json').read_text())
    ids=[x['id'] for x in profiles.get('profiles',[])]
    if ids!=['simple','power_user','organization']: fail(f'unexpected deployment profiles: {ids}')
    if 'optional' not in profiles.get('invariant','').lower(): fail('deployment profiles do not preserve optional adapter invariant')
    for rel in ['core/contracts/workspace/configure/CONTEXT.md','core/contracts/knowledge/refresh-human-layer/CONTEXT.md','core/contracts/knowledge/ingest-human-note/CONTEXT.md']:
        text=(ROOT/rel).read_text()
        for section in ['## Purpose','## Business Outcome','## Run When','## Process']:
            if section not in text: fail(f'{rel} missing {section}')
        if text.count('\n1. [')<1 or sum(text.count(f'\n{i}. [') for i in range(1,10))<5: fail(f'{rel} lacks five labeled process steps')
    prior=os.environ.get('BUSINESSOS_WORKSPACE');prior_cfg=os.environ.get('BUSINESSOS_WORKSPACE_CONFIG');tmp=Path(tempfile.mkdtemp(prefix='aura-workspace-regression-'))
    migrated=tmp.parent/(tmp.name+'-migrated')
    try:
        cfg=configure(tmp,'organization',knowledge_enabled=True,write_link=False,force=True)
        if not cfg['external_state'] or cfg['profile']!='organization': fail('external organization workspace was not configured')
        if not (tmp/'.businessos/workspace.json').exists() or not (tmp/'WORKSPACE.md').exists(): fail('portable workspace metadata missing')
        os.environ['BUSINESSOS_WORKSPACE']=str(tmp)
        if common.workspace_root().resolve()!=tmp.resolve(): fail('BUSINESSOS_WORKSPACE did not select external root')
        if Path(common.ROOT/'instances').resolve()!=tmp.joinpath('instances').resolve(): fail('legacy ROOT/instances did not redirect to external workspace')
        if Path(common.ROOT/'runtime').resolve()!=tmp.joinpath('runtime').resolve(): fail('legacy ROOT/runtime did not redirect to external workspace')
        if Path(common.ROOT/'core').resolve()!=common.PRODUCT_ROOT.joinpath('core').resolve(): fail('product core path was incorrectly redirected')
        dest=init_business(BID,'Workspace Regression Business')
        if dest.resolve()!=tmp.joinpath('instances',BID).resolve(): fail('business initialized outside selected workspace')
        if common.PRODUCT_ROOT.joinpath('instances',BID).exists(): fail('external initialization leaked business state into product tree')
        logical=(dest/'instance.json').relative_to(common.ROOT).as_posix()
        if logical!=f'instances/{BID}/instance.json': fail(f'external state did not preserve portable logical ref: {logical}')

        innovation,innovation_path=configure_innovation(BID,'ask_when_noteworthy','workflow_only','anonymous',True,[],None)
        if innovation_path.resolve()!=dest.joinpath('config/innovation-sharing.json').resolve() or innovation.get('exchange_discovery_enabled') is not True: fail('existing stateful helper did not write into external workspace')
        learning={'id':'lrn_workspace_regression','object_type':'Learning','schema_version':'1.0.0','business_id':BID,'owner_scope':'business','owner_system':'core','statement':'A generated human view should remain derived from canonical state.','maturity':'validated','status':'active','evidence_refs':[],'confidence':0.9,'system_learning_eligible':False,'extensions':{}}
        lp=dest/'learning/business/lrn_workspace_regression.json';lp.parent.mkdir(parents=True,exist_ok=True);lp.write_text(json.dumps(learning,indent=2)+'\n')
        notes=tmp/'knowledge'/BID/'notes';notes.mkdir(parents=True,exist_ok=True);human_note=notes/'keep-me.md';human_note.write_text('# Human note\nPossible customer concern: handoff time may be too long.\n')
        out=generate(BID)
        home=Path(out['generated_root'])/'Home.md';learn=Path(out['generated_root'])/'Learning.md'
        if not home.exists() or not learn.exists(): fail('human knowledge pages were not generated')
        text=learn.read_text()
        if 'businessos_generated: true' not in text or 'canonical: false' not in text or 'product: ViralTrac AURA' not in text or 'lrn_workspace_regression' not in text: fail('generated Learning view lacks AURA/derived-state/source markers')
        before_note=human_note.read_text();generate(BID)
        if human_note.read_text()!=before_note: fail('knowledge refresh overwrote human-authored notes')
        if common.PRODUCT_ROOT.joinpath('knowledge',BID).exists(): fail('human knowledge leaked into product tree during external deployment')
        src,src_path,created=register_note(BID,'keep-me.md')
        if not created or src.get('source_type')!='human_knowledge_note' or src.get('source_reference')!=f'knowledge/{BID}/notes/keep-me.md': fail('human note was not registered as portable source material')
        if (src.get('extensions') or {}).get('businessos',{}).get('canonical_truth') is not False: fail('human note registration did not preserve noncanonical truth boundary')
        src2,_,created2=register_note(BID,'keep-me.md')
        if created2 or src2['id']!=src['id']: fail('identical human note registration was not idempotent')
        if any(obj.get('object_type') in {'Observation','Insight','Business'} and obj.get('lineage')==[src['id']] for obj,_ in common.iter_instance_objects(BID)): fail('note registration silently promoted note contents to canonical truth')
        ref=common.storage_ref(lp)
        if ref!=f'instances/{BID}/learning/business/lrn_workspace_regression.json': fail(f'nonportable external state ref: {ref}')
        if common.resolve_storage_ref(ref).resolve()!=lp.resolve(): fail('workspace-relative state ref did not resolve back to external workspace')
        product_ref=common.storage_ref(common.PRODUCT_ROOT/'core/policies/portable-first.md')
        if not product_ref.startswith('product:') or common.resolve_storage_ref(product_ref).resolve()!=common.PRODUCT_ROOT.joinpath('core/policies/portable-first.md').resolve(): fail('product reference boundary failed')
        st=status()
        if st['workspace_root']!=str(tmp.resolve()) or BID not in st['businesses']: fail('workspace status did not reflect external business state')
        deployment_requests=[
            'Configure ViralTrac AURA for a private GitHub organization workspace',
            'Set up AURA with an external workspace for our team',
            'Store BusinessOS state in a private GitLab workspace',
            'We want a Forgejo-hosted organization workspace for ViralTrac AURA'
        ]
        for request in deployment_requests:
            if route_and_resolve(request)['contract_id']!='core.workspace.configure': fail(f'workspace deployment natural-language route missing: {request}')
        if route_and_resolve('Refresh our AURA human knowledge layer for Obsidian',BID)['contract_id']!='core.knowledge.refresh-human-layer': fail('human knowledge natural-language route missing')
        if route_and_resolve('Use my Obsidian note in AURA',BID)['contract_id']!='core.knowledge.ingest-human-note': fail('human note ingestion natural-language route missing')

        # Customize a workspace-level human knowledge file to reproduce the migration
        # conflict that would occur if target defaults were created before source state copied.
        knowledge_readme=tmp/'knowledge/README.md';custom_knowledge='# Custom organization knowledge index\nKeep this exact content during migration.\n';knowledge_readme.write_text(custom_knowledge)

        if migrated.exists(): shutil.rmtree(migrated)
        mig=migrate(migrated,'organization',True,activate=False,write_link=False)
        if not mig.get('verified') or not mig.get('source_retained') or mig.get('activated'): fail('copy-only workspace migration result is incorrect')
        if mig.get('file_count',0)<4 or not (migrated/'instances'/BID/'instance.json').exists(): fail('workspace migration did not copy canonical business state')
        if not (migrated/'knowledge'/BID/'notes/keep-me.md').exists(): fail('workspace migration did not preserve human knowledge notes')
        if (migrated/'knowledge/README.md').read_text()!=custom_knowledge: fail('workspace migration replaced customized human knowledge README with target default')
        if not (tmp/'instances'/BID/'instance.json').exists() or not human_note.exists() or knowledge_readme.read_text()!=custom_knowledge: fail('workspace migration modified/deleted source state')
        mig2=migrate(migrated,'organization',True,activate=False,write_link=False)
        if not mig2.get('verified') or mig2.get('copied_file_count')!=0 or mig2.get('identical_existing_file_count')!=mig2.get('file_count'): fail('repeat workspace migration was not idempotent')
        os.environ['BUSINESSOS_WORKSPACE']=str(migrated)
        if common.workspace_root().resolve()!=migrated.resolve() or BID not in status()['businesses']: fail('migrated workspace could not be selected and resumed')
        if common.resolve_storage_ref(ref).resolve()!=migrated.joinpath(ref).resolve(): fail('portable state reference did not survive workspace migration')
        os.environ['BUSINESSOS_WORKSPACE']=str(tmp)

        # Prove standalone/component packaging preserves Core deployment and AURA branding.
        pkg=build_distribution('content',output_dir=tmp/'packages',keep_folder=True)
        pdir=Path(pkg['folder']);pinst=json.loads((pdir/'INSTALLATION.json').read_text())
        if not pinst.get('display_name','').startswith(EXPECTED_NAME) or pinst.get('public_name')!=pinst.get('display_name') or pinst.get('name_expansion')!=EXPECTED_EXPANSION: fail('component edition lost AURA family branding')
        if pinst.get('configurable_workspace_root') is not True or pinst.get('human_knowledge_layer') is not True: fail('component edition lost workspace/knowledge installation declarations')
        if pinst.get('deployment_profiles')!='distribution/deployment-profiles.json': fail('component edition lost deployment profile reference')
        for rel in ['BRANDING.md','DEPLOYMENT.md','scripts/configure_workspace.py','scripts/migrate_workspace.py','scripts/generate_knowledge_layer.py','scripts/register_human_note.py','core/policies/workspace-and-human-knowledge.md','core/contracts/workspace/configure/CONTEXT.md','core/contracts/knowledge/refresh-human-layer/CONTEXT.md','core/contracts/knowledge/ingest-human-note/CONTEXT.md']:
            if not (pdir/rel).exists(): fail(f'component edition lost deployment component: {rel}')
        if (pdir/'.businessos/workspace.json').exists(): fail('component package leaked a local workspace pointer/profile')
        if 'ViralTrac AURA' not in (pdir/'README.md').read_text() or 'migrate_workspace.py' not in (pdir/'START-HERE.md').read_text(): fail('component navigation does not expose AURA branding/migration architecture')
        cws=tmp/'component-workspace';env=dict(os.environ);env['BUSINESSOS_WORKSPACE']=str(cws);env['PYTHONDONTWRITEBYTECODE']='1'
        subprocess.run([sys.executable,str(pdir/'scripts/configure_workspace.py'),str(cws),'--profile','power_user','--no-link'],cwd=pdir,env=env,check=True,capture_output=True,text=True)
        subprocess.run([sys.executable,str(pdir/'scripts/init_business.py'),'component-workspace-test','--name','Component Workspace Test'],cwd=pdir,env=env,check=True,capture_output=True,text=True)
        if not (cws/'instances/component-workspace-test/instance.json').exists(): fail('component edition did not initialize into external workspace')
        subprocess.run([sys.executable,str(pdir/'scripts/generate_knowledge_layer.py'),'component-workspace-test'],cwd=pdir,env=env,check=True,capture_output=True,text=True)
        if not (cws/'knowledge/component-workspace-test/_generated/Home.md').exists(): fail('component edition did not generate external human knowledge layer')
        if (pdir/'instances/component-workspace-test').exists(): fail('component edition external state leaked into product package')
        print('AURA workspace + human knowledge deployment regressions passed end to end, including verified migration, governed notes, branding, and component edition')
    finally:
        if prior is None: os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else: os.environ['BUSINESSOS_WORKSPACE']=prior
        if prior_cfg is None: os.environ.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
        else: os.environ['BUSINESSOS_WORKSPACE_CONFIG']=prior_cfg
        shutil.rmtree(migrated,ignore_errors=True)
        shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__':main()
