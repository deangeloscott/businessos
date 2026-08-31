#!/usr/bin/env python3
"""Regression for qualification product-integrity snapshots without runtime/provider machinery."""
from pathlib import Path
import json,os,shutil,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'qualification'))
from common import ensure_run_dir,write_json,write_text,product_integrity_snapshot,detect_product_integrity_mutation,finalize_product_integrity_snapshot


def req(cond,msg):
    if not cond:raise AssertionError(msg)

def main():
    temp_root=Path(tempfile.mkdtemp(prefix='businessos-qual-product-integrity-'))
    prior_workspace=os.environ.get('BUSINESSOS_WORKSPACE');workspace=temp_root/'workspace';os.environ['BUSINESSOS_WORKSPACE']=str(workspace)
    try:
        run_dir=ensure_run_dir(temp_root/'qualification-runs'/'product-integrity')
        bundle=run_dir/'bundle';bundle.mkdir(parents=True,exist_ok=True);input_file=bundle/'request.txt';input_file.write_text('test input\n')
        startup=product_integrity_snapshot(run_dir,bundle,[input_file]);req(startup.get('hash'),'startup product integrity hash missing')
        write_json(run_dir/'run.json',{'id':'product-integrity-regression','status':'running'});write_text(run_dir/'notes.md','run-local qualification state\n')
        workspace.mkdir(parents=True,exist_ok=True);(workspace/'runtime').mkdir(parents=True,exist_ok=True);(workspace/'runtime'/'host-owned-note.json').write_text('{"note":"runtime state belongs to the active host"}\n')
        req(detect_product_integrity_mutation(startup).get('mutated') is False,'workspace/run-local qualification state was falsely classified as product mutation')
        protected=ROOT/'core/capabilities/catalog.json';original=protected.read_text()
        try:
            protected.write_text(original+'\n')
            diff=detect_product_integrity_mutation(startup);req(diff.get('mutated') is True,'actual staged product mutation was not detected');req(any('core/capabilities/catalog.json' in x for x in diff.get('changed_paths',[])),'protected product path absent from mutation diff')
        finally:protected.write_text(original)
        req(detect_product_integrity_mutation(startup).get('mutated') is False,'restored product tree remained falsely marked mutated')
        readme=ROOT/'README.md';readme_original=readme.read_text()
        try:
            readme.write_text(readme_original+'\n')
            final=finalize_product_integrity_snapshot(run_dir,startup);req(final.get('status')=='invalid_product_mutation','finalization did not reject product-tree mutation')
        finally:readme.write_text(readme_original)
        clean=finalize_product_integrity_snapshot(run_dir,startup);req(clean.get('status')=='valid','clean product tree did not validate after restore')
        retired=['scripts/bootstrap_environment.py','scripts/resolve_capability.py','scripts/preflight_capabilities.py','core/providers/registry.json','core/schemas/runtime/capability-binding.schema.json','core/schemas/runtime/scheduler-bindings.schema.json']
        for rel in retired:req(not (ROOT/rel).exists(),f'qualification still ships retired runtime/provider machinery: {rel}')
        print('qualification product-integrity regression passed: workspace state allowed, AURA product mutation detected, retired runtime machinery absent')
    finally:
        if prior_workspace is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior_workspace
        shutil.rmtree(temp_root,ignore_errors=True)

if __name__=='__main__':main()
