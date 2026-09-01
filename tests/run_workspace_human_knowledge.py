#!/usr/bin/env python3
"""Regression for AURA external workspaces, human knowledge, migration and component packaging."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import _common as common
from configure_workspace import configure
from migrate_workspace import migrate
from init_business import init_business
from generate_knowledge_layer import generate
from register_human_note import register_note
from workspace_status import status
from package_edition import build_distribution

BID='test-workspace-deployment'

def fail(msg):raise AssertionError(msg)

def req(cond,msg):
    if not cond:fail(msg)

def main():
    required=['BRANDING.md','OPERATOR-GUIDE.md','distribution/deployment-profiles.json','core/policies/workspace-and-human-knowledge.md','core/schemas/config/workspace-profile.schema.json','scripts/configure_workspace.py','scripts/migrate_workspace.py','scripts/workspace_status.py','scripts/generate_knowledge_layer.py','scripts/register_human_note.py']
    for rel in required:req((ROOT/rel).exists(),f'missing {rel}')
    retired=['core/schemas/runtime/workspace-profile.schema.json','deployment/operator-profile.json','scripts/preflight_capabilities.py','scripts/resolve_capability.py','core/providers/registry.json']
    for rel in retired:req(not (ROOT/rel).exists(),f'retired runtime/provider artifact still shipped: {rel}')
    prior=os.environ.get('BUSINESSOS_WORKSPACE');tmp=Path(tempfile.mkdtemp(prefix='aura-workspace-regression-'));migrated=tmp.parent/(tmp.name+'-migrated')
    try:
        cfg=configure(tmp,'organization',knowledge_enabled=True,write_link=False,force=True);req(cfg['external_state'] and cfg['profile']=='organization','external organization workspace not configured')
        req((tmp/'.businessos/workspace.json').exists() and (tmp/'WORKSPACE.md').exists(),'portable workspace metadata missing')
        req(not (tmp/'.businessos/environments').exists(),'workspace created deprecated runtime environment overlays')
        os.environ['BUSINESSOS_WORKSPACE']=str(tmp);req(common.workspace_root().resolve()==tmp.resolve(),'workspace selection failed')
        dest=init_business(BID,'Workspace Regression Business');req(dest.resolve()==tmp.joinpath('instances',BID).resolve(),'business initialized outside workspace')
        learning={'id':'lrn_workspace_regression','object_type':'Learning','schema_version':'1.0.0','business_id':BID,'owner_scope':'business','owner_system':'core','statement':'Generated human views remain derived from canonical state.','maturity':'validated','status':'active','evidence_refs':[],'confidence':0.9,'extensions':{}}
        lp=dest/'learning/business/lrn_workspace_regression.json';lp.parent.mkdir(parents=True,exist_ok=True);lp.write_text(json.dumps(learning,indent=2)+'\n')
        notes=tmp/'knowledge'/BID/'notes';notes.mkdir(parents=True,exist_ok=True);note=notes/'keep-me.md';note.write_text('# Human note\nPossible customer concern.\n')
        out=generate(BID);generated=Path(out['generated_root']);req((generated/'Home.md').exists() and (generated/'Learning.md').exists(),'human knowledge pages missing')
        text=(generated/'Learning.md').read_text();req('aura_generated: true' in text and 'canonical: false' in text and 'lrn_workspace_regression' in text,'generated knowledge markers/content missing')
        before=note.read_text();generate(BID);req(note.read_text()==before,'knowledge refresh overwrote human note')
        src,_,created=register_note(BID,'keep-me.md');req(created and src.get('source_type')=='human_knowledge_note','human note not registered as source material')
        src2,_,created2=register_note(BID,'keep-me.md');req(not created2 and src2['id']==src['id'],'human note registration not idempotent')
        req(status()['workspace_root']==str(tmp.resolve()) and BID in status()['businesses'],'workspace status incorrect')
        custom='# Custom organization knowledge index\n';(tmp/'knowledge/README.md').write_text(custom)
        if migrated.exists():shutil.rmtree(migrated)
        mig=migrate(migrated,'organization',True,activate=False,write_link=False);req(mig.get('verified') and (migrated/'instances'/BID/'instance.json').exists(),'workspace migration failed')
        req((migrated/'knowledge'/BID/'notes/keep-me.md').exists() and (migrated/'knowledge/README.md').read_text()==custom,'migration lost human knowledge')
        pkg=build_distribution('content',output_dir=tmp/'packages',keep_folder=True);pdir=Path(pkg['folder'])
        for rel in ['OPERATOR-GUIDE.md','scripts/configure_workspace.py','scripts/migrate_workspace.py','scripts/generate_knowledge_layer.py','core/schemas/config/workspace-profile.schema.json']:
            req((pdir/rel).exists(),f'component edition lost {rel}')
        for rel in retired:req(not (pdir/rel).exists(),f'component edition restored retired runtime machinery: {rel}')
        cws=tmp/'component-workspace';env={**os.environ,'BUSINESSOS_WORKSPACE':str(cws),'PYTHONDONTWRITEBYTECODE':'1'}
        subprocess.run([sys.executable,str(pdir/'scripts/configure_workspace.py'),str(cws),'--profile','power_user','--no-link'],cwd=pdir,env=env,check=True,capture_output=True,text=True)
        subprocess.run([sys.executable,str(pdir/'scripts/init_business.py'),'component-workspace-test','--name','Component Workspace Test'],cwd=pdir,env=env,check=True,capture_output=True,text=True)
        subprocess.run([sys.executable,str(pdir/'scripts/generate_knowledge_layer.py'),'component-workspace-test'],cwd=pdir,env=env,check=True,capture_output=True,text=True)
        req((cws/'knowledge/component-workspace-test/_generated/Home.md').exists(),'component edition human knowledge generation failed')
        print('AURA workspace + human knowledge regressions passed: portable state, migration, notes and component packaging without runtime/provider coupling')
    finally:
        if prior is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior
        shutil.rmtree(migrated,ignore_errors=True);shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__':main()
