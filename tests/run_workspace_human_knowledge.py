#!/usr/bin/env python3
"""End-to-end regression for external workspace resolution, deployment profiles, and human knowledge views."""
from pathlib import Path
import json,os,shutil,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

import _common as common
from configure_workspace import configure
from init_business import init_business
from configure_innovation_sharing import configure as configure_innovation
from generate_knowledge_layer import generate
from workspace_status import status
from route_and_resolve import route_and_resolve

BID='test-workspace-deployment'

def fail(msg): raise AssertionError(msg)

def main():
    required=[
        'DEPLOYMENT.md','distribution/deployment-profiles.json','core/policies/workspace-and-human-knowledge.md',
        'core/contracts/workspace/configure/CONTEXT.md','core/contracts/knowledge/refresh-human-layer/CONTEXT.md',
        'core/schemas/runtime/workspace-profile.schema.json','scripts/configure_workspace.py','scripts/workspace_status.py','scripts/generate_knowledge_layer.py'
    ]
    for rel in required:
        if not (ROOT/rel).exists(): fail(f'missing {rel}')
    profiles=json.loads((ROOT/'distribution/deployment-profiles.json').read_text())
    ids=[x['id'] for x in profiles.get('profiles',[])]
    if ids!=['simple','power_user','organization']: fail(f'unexpected deployment profiles: {ids}')
    if 'optional' not in profiles.get('invariant','').lower(): fail('deployment profiles do not preserve optional adapter invariant')
    prior=os.environ.get('BUSINESSOS_WORKSPACE'); tmp=Path(tempfile.mkdtemp(prefix='businessos-workspace-regression-'))
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
        logical=str((dest/'instance.json').relative_to(common.ROOT))
        if logical!=f'instances/{BID}/instance.json': fail(f'external state did not preserve portable logical ref: {logical}')
        # Existing stateful helper should inherit workspace redirection without special knowledge of the deployment.
        innovation,innovation_path=configure_innovation(BID,'ask_when_noteworthy','workflow_only','anonymous',True,[],None)
        if innovation_path.resolve()!=dest.joinpath('config/innovation-sharing.json').resolve() or innovation.get('exchange_discovery_enabled') is not True: fail('existing stateful helper did not write into external workspace')
        learning={'id':'lrn_workspace_regression','object_type':'Learning','schema_version':'1.0.0','business_id':BID,'owner_scope':'business','owner_system':'core','statement':'A generated human view should remain derived from canonical state.','maturity':'validated','status':'active','evidence_refs':[],'confidence':0.9,'system_learning_eligible':False,'extensions':{}}
        lp=dest/'learning/business/lrn_workspace_regression.json';lp.parent.mkdir(parents=True,exist_ok=True);lp.write_text(json.dumps(learning,indent=2)+'\n')
        notes=tmp/'knowledge'/BID/'notes';notes.mkdir(parents=True,exist_ok=True);human_note=notes/'keep-me.md';human_note.write_text('# Human note\nDo not overwrite me.\n')
        out=generate(BID)
        home=Path(out['generated_root'])/'Home.md';learn=Path(out['generated_root'])/'Learning.md'
        if not home.exists() or not learn.exists(): fail('human knowledge pages were not generated')
        text=learn.read_text()
        if 'businessos_generated: true' not in text or 'canonical: false' not in text or 'lrn_workspace_regression' not in text: fail('generated Learning view lacks derived-state/source markers')
        generate(BID)
        if human_note.read_text()!='# Human note\nDo not overwrite me.\n': fail('knowledge refresh overwrote human-authored notes')
        if common.PRODUCT_ROOT.joinpath('knowledge',BID).exists(): fail('human knowledge leaked into product tree during external deployment')
        ref=common.storage_ref(lp)
        if ref!=f'instances/{BID}/learning/business/lrn_workspace_regression.json': fail(f'nonportable external state ref: {ref}')
        if common.resolve_storage_ref(ref).resolve()!=lp.resolve(): fail('workspace-relative state ref did not resolve back to external workspace')
        product_ref=common.storage_ref(common.PRODUCT_ROOT/'core/policies/portable-first.md')
        if not product_ref.startswith('product:') or common.resolve_storage_ref(product_ref).resolve()!=common.PRODUCT_ROOT.joinpath('core/policies/portable-first.md').resolve(): fail('product reference boundary failed')
        st=status()
        if st['workspace_root']!=str(tmp.resolve()) or BID not in st['businesses']: fail('workspace status did not reflect external business state')
        if route_and_resolve('Configure BusinessOS for a private GitHub organization workspace')['contract_id']!='core.workspace.configure': fail('workspace deployment natural-language route missing')
        if route_and_resolve('Refresh our BusinessOS human knowledge layer for Obsidian',BID)['contract_id']!='core.knowledge.refresh-human-layer': fail('human knowledge natural-language route missing')
        print('workspace + human knowledge deployment regressions passed end to end')
    finally:
        if prior is None: os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else: os.environ['BUSINESSOS_WORKSPACE']=prior
        shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__':main()
