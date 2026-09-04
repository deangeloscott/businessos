#!/usr/bin/env python3
"""Qualification product-integrity regression using only current snapshot primitives."""
from pathlib import Path
import shutil,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qualification'))
from common import product_snapshot,snapshot_diff
from prepare_run import copy_product


def req(cond,msg):
    if not cond:raise AssertionError(msg)


def changed(before,after):
    diff=snapshot_diff(before,after)
    return diff,any(diff.values())


def main():
    temp_root=Path(tempfile.mkdtemp(prefix='aura-qual-product-integrity-'))
    try:
        product=copy_product(ROOT,temp_root/'product')
        workspace=temp_root/'workspace';workspace.mkdir()
        baseline=product_snapshot(product)
        req(baseline.get('digest') and baseline.get('file_count',0)>0,'staged product integrity baseline missing')

        # Organization/runtime state lives outside the staged product and must not alter
        # the protected product snapshot.
        (workspace/'runtime').mkdir(parents=True)
        (workspace/'runtime'/'host-owned-note.json').write_text('{"note":"runtime state belongs to the active host"}\n')
        diff,mutated=changed(baseline,product_snapshot(product))
        req(not mutated,f'external workspace state was falsely classified as staged product mutation: {diff}')

        # AURA-generated registries/manifests are disposable derived views. Normal use may
        # regenerate them, so they must not be mistaken for candidate mutation of product source.
        generated=product/'generated';generated.mkdir(parents=True,exist_ok=True)
        (generated/'workspace-manifest.json').write_text('{"derived":true}\n')
        (generated/'checksums.txt').write_text('derived\n')
        diff,mutated=changed(baseline,product_snapshot(product))
        req(not mutated,f'derived generated views were falsely classified as staged product mutation: {diff}')
        shutil.rmtree(generated)

        # The portable AURA Skill is product source and therefore protected just like
        # policies, Workflows, schemas, scripts, and human docs.
        protected=product/'skills/viraltrac-aura/SKILL.md';original=protected.read_text()
        protected.write_text(original+'\n')
        diff,mutated=changed(baseline,product_snapshot(product))
        req(mutated,'actual staged product mutation was not detected')
        req('skills/viraltrac-aura/SKILL.md' in diff.get('modified',[]),'protected Skill path absent from mutation diff')
        protected.write_text(original)
        diff,mutated=changed(baseline,product_snapshot(product))
        req(not mutated,f'restored staged product remained marked mutated: {diff}')

        readme=product/'README.md';readme_original=readme.read_text();readme.write_text(readme_original+'\n')
        diff,mutated=changed(baseline,product_snapshot(product))
        req(mutated and 'README.md' in diff.get('modified',[]),'ordinary staged product source mutation was not detected')
        readme.write_text(readme_original)
        diff,mutated=changed(baseline,product_snapshot(product))
        req(not mutated,f'clean staged product did not return to baseline: {diff}')

        retired=[
            'core/capabilities/catalog.json','docs/adding-a-capability.md',
            'scripts/bootstrap_environment.py','scripts/resolve_capability.py','scripts/preflight_capabilities.py',
            'core/providers/registry.json','core/schemas/runtime/capability-binding.schema.json',
            'core/schemas/runtime/scheduler-bindings.schema.json'
        ]
        for rel in retired:req(not (product/rel).exists(),f'staged AURA product still ships retired runtime/provider/capability machinery: {rel}')
        print('qualification product-integrity regression passed: external workspace and derived generated state allowed, staged source mutation detected, retired capability/runtime machinery absent, source checkout untouched')
    finally:
        shutil.rmtree(temp_root,ignore_errors=True)

if __name__=='__main__':main()
