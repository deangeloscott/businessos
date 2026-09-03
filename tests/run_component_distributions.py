#!/usr/bin/env python3
"""Regression that every named non-full AURA edition packages current Core through a relative output path."""
from pathlib import Path
import json,os,shutil,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from package_edition import build_distribution,editions,resolve_modules
from _common import os_version


def req(cond,msg):
    if not cond:raise AssertionError(msg)


def main():
    eds=editions();targets=[eid for eid in eds if eid not in {'full','content'}];tmp=Path(tempfile.mkdtemp(prefix='aura-component-distributions-'));prior_cwd=Path.cwd();relative_tmp=Path(os.path.relpath(tmp,ROOT))
    try:
        os.chdir(ROOT)
        for eid in targets:
            pkg=build_distribution(eid,output_dir=relative_tmp,keep_folder=True);pdir=Path(pkg['folder']);expected=resolve_modules(eds[eid]['modules']);inst=json.loads((pdir/'INSTALLATION.json').read_text());actual={'core'}|{p.name for p in (pdir/'systems').iterdir() if p.is_dir()}
            req(inst.get('standalone_distribution') is True,f'{eid} was not marked standalone');req(set(inst.get('installed_modules',[]))==expected,f'{eid} INSTALLATION modules mismatch: {inst.get("installed_modules")} vs {sorted(expected)}');req(actual==expected,f'{eid} filesystem modules mismatch: {sorted(actual)} vs {sorted(expected)}');req((pdir/'VERSION').read_text().strip()==os_version(),f'{eid} did not inherit current AURA version');req(Path(pkg['zip']).is_absolute(),f'{eid} relative output path was not resolved safely: {pkg["zip"]}')
            defaults=(pdir/'core/DEFAULTS.md').read_text()
            for phrase in [
                'AURA is organization-owned memory and reusable operating knowledge, not the model, harness, permission system, scheduler, or execution-control plane.',
                'AURA uses **Playbook → Workflow → Step**.',
                'AURA does not define a universal capability vocabulary or tool allowlist.',
                'Installed modules are bodies of AURA operating knowledge, not limits on what capable intelligence may do.',
                'A missing module means its AURA guidance is unavailable. It does **not** prohibit another sound method.',
                'An uninstalled optional module is never a hidden hard dependency.',
            ]:req(phrase in defaults,f'{eid} lost current Core invariant: {phrase}')
            req((pdir/'generated/workflow-registry.json').exists(),f'{eid} Workflow registry was not generated');req(not (pdir/'generated/contract-registry.json').exists(),f'{eid} packaged retired contract registry');req((pdir/'generated/workflow-candidate-index.json').exists(),f'{eid} Workflow discovery index missing');req((pdir/'PLAYBOOKS.md').exists(),f'{eid} high-level Playbook catalog missing');req((pdir/'WORKFLOW-INDEX.md').exists(),f'{eid} Workflow index missing');req((pdir/'skills/viraltrac-aura/SKILL.md').exists(),f'{eid} AURA awareness Skill missing');req(not (pdir/'core/capabilities/catalog.json').exists(),f'{eid} packaged retired capability ontology')
        print(f'AURA component distribution regressions passed: {len(targets)} named editions package Playbooks, Workflows, Skill attachment, and current Core through relative output paths')
    finally:
        os.chdir(prior_cwd);shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__':main()
