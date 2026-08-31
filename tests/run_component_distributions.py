#!/usr/bin/env python3
"""Regression that every named non-full AURA edition packages against the current Core."""
from pathlib import Path
import json,shutil,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from package_edition import build_distribution,editions,resolve_modules
from _common import os_version


def req(cond,msg):
    if not cond:raise AssertionError(msg)


def main():
    eds=editions();targets=[eid for eid in eds if eid not in {'full','content'}]
    tmp=Path(tempfile.mkdtemp(prefix='aura-component-distributions-'))
    try:
        for eid in targets:
            pkg=build_distribution(eid,output_dir=tmp,keep_folder=True);pdir=Path(pkg['folder'])
            expected=resolve_modules(eds[eid]['modules'])
            inst=json.loads((pdir/'INSTALLATION.json').read_text())
            actual={'core'}|{p.name for p in (pdir/'systems').iterdir() if p.is_dir()}
            req(inst.get('standalone_distribution') is True,f'{eid} was not marked standalone')
            req(set(inst.get('installed_modules',[]))==expected,f'{eid} INSTALLATION modules mismatch: {inst.get("installed_modules")} vs {sorted(expected)}')
            req(actual==expected,f'{eid} filesystem modules mismatch: {sorted(actual)} vs {sorted(expected)}')
            req((pdir/'VERSION').read_text().strip()==os_version(),f'{eid} did not inherit current AURA version')
            defaults=(pdir/'core/DEFAULTS.md').read_text()
            for phrase in [
                'AURA is organizational memory and operational knowledge, not the model, harness, permission system, scheduler, or execution-control plane.',
                'Installed modules are packages of AURA operational knowledge, not limits on what a capable human, model, or harness may do.',
                'A missing module means its reusable AURA SOP knowledge is unavailable.',
                'does **not** prohibit the active model/user from completing that work',
                'An uninstalled optional module is never a hidden hard dependency.'
            ]:
                req(phrase in defaults,f'{eid} lost current Core invariant: {phrase}')
            req((pdir/'generated/contract-registry.json').exists(),f'{eid} registry was not generated')
            req((pdir/'PLAYBOOKS.md').exists(),f'{eid} human playbook catalog missing')
        print(f'AURA component distribution regressions passed: {len(targets)} named editions package with current Core; content is exercised by workspace/human-knowledge regression')
    finally:
        shutil.rmtree(tmp,ignore_errors=True)


if __name__=='__main__':main()
