#!/usr/bin/env python3
"""Regression: workspace migration must reject overlapping source/target roots."""
from pathlib import Path
import os, shutil, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from configure_workspace import configure
from migrate_workspace import migrate


def expect_reject(target):
    try:
        migrate(target,'organization',True,activate=False,write_link=False)
    except ValueError as e:
        if 'non-nested' not in str(e):
            raise AssertionError(f'unexpected rejection: {e}')
        return
    raise AssertionError(f'nested workspace migration was not rejected: {target}')


def main():
    prior=os.environ.get('BUSINESSOS_WORKSPACE')
    tmp=Path(tempfile.mkdtemp(prefix='aura-workspace-path-guard-'))
    source=tmp/'source'
    try:
        configure(source,'organization',True,write_link=False,force=True,allow_state_switch=True)
        (source/'instances/acme').mkdir(parents=True,exist_ok=True)
        (source/'instances/acme/state.txt').write_text('preserve me\n')
        os.environ['BUSINESSOS_WORKSPACE']=str(source)

        expect_reject(source/'nested-target')
        expect_reject(tmp)

        if not (source/'instances/acme/state.txt').exists():
            raise AssertionError('rejected migration modified source state')
        if (source/'nested-target').exists():
            raise AssertionError('rejected nested migration created target state')
        print('workspace migration path-overlap regression passed')
    finally:
        if prior is None: os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else: os.environ['BUSINESSOS_WORKSPACE']=prior
        shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__': main()
