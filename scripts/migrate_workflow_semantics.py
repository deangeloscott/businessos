#!/usr/bin/env python3
"""One-time source migration for the Playbook → Workflow semantic refactor.

This migration intentionally changes authored operating-knowledge metadata, not business
meaning. Existing contract procedures become Workflows; high-level Playbooks are generated
from installed AURA operating areas. The retired AURA capability vocabulary is removed
because execution/tool choice belongs to the active model/harness.
"""
from pathlib import Path
import argparse
import yaml

from _common import ROOT,contract_files,read_frontmatter

RETIRE_PATHS = [
    'core/capabilities/catalog.json',
    'docs/adding-a-capability.md',
    'generated/capability-usage-index.json',
    'generated/playbook-candidate-index.json',
    'PLAYBOOK-INDEX.md',
]


def render(meta,body):
    front=yaml.safe_dump(meta,sort_keys=False,width=1000).rstrip()
    return '---\n'+front+'\n---\n'+body.lstrip('\n')


def migrate(dry_run=False):
    changed=[];retyped=0;capability_blocks=0
    for path in contract_files():
        meta,body=read_frontmatter(path);before=dict(meta);dirty=False
        if meta.get('type')=='playbook':
            meta['type']='workflow';retyped+=1;dirty=True
        if 'capabilities' in meta:
            meta.pop('capabilities',None);capability_blocks+=1;dirty=True
        if dirty:
            changed.append(str(path.relative_to(ROOT)))
            if not dry_run:path.write_text(render(meta,body),encoding='utf-8')

    removed=[]
    for rel in RETIRE_PATHS:
        path=ROOT/rel
        if path.exists():
            removed.append(rel)
            if not dry_run:path.unlink()
    return {
        'changed_contracts':len(changed),'retyped_playbook_metadata':retyped,
        'removed_capability_blocks':capability_blocks,'retired_files':removed,
        'dry_run':dry_run,
    }


def main():
    p=argparse.ArgumentParser(description='Convert flattened AURA contract metadata into Workflow semantics and retire the invented capability vocabulary.')
    p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    result=migrate(a.dry_run)
    for key,value in result.items():print(f'{key}: {value}')

if __name__=='__main__':main()
