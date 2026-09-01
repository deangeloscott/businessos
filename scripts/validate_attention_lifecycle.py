#!/usr/bin/env python3
"""Validate small semantic invariants for durable AttentionItem and PlatformChange state."""
from _common import *
import argparse,collections


def lifecycle_errors(business_id,objects=None):
    pairs=objects if objects is not None else [(obj,str(path.relative_to(ROOT))) for obj,path in iter_instance_objects(business_id)]
    index={obj.get('id'):(obj,path) for obj,path in pairs if obj.get('id')};errors=[];active_attention=collections.defaultdict(list);current_platform=collections.defaultdict(list)
    for obj,path in pairs:
        typ=obj.get('object_type')
        if typ=='AttentionItem':
            if obj.get('status') in {'open','acknowledged'}:active_attention[obj.get('dedupe_key')].append((obj,path))
            if obj.get('status')=='resolved' and not obj.get('resolved_at'):errors.append(f'{path} resolved AttentionItem requires resolved_at')
        elif typ=='PlatformChange':
            key=obj.get('semantic_key')
            if obj.get('status')=='current':
                current_platform[key].append((obj,path))
                if obj.get('authority')=='unknown':errors.append(f'{path} current PlatformChange requires non-unknown authority')
                refs=(obj.get('source_refs') or [])+(obj.get('evidence_refs') or [])
                if not refs:errors.append(f'{path} current PlatformChange requires source/evidence provenance')
                for ref in obj.get('source_refs') or []:
                    if ref not in index or index[ref][0].get('object_type')!='SourceRecord':errors.append(f'{path} source_ref {ref} must reference an existing SourceRecord')
                if obj.get('superseded_by'):errors.append(f'{path} current PlatformChange may not have superseded_by')
            replacement=obj.get('superseded_by');prior=obj.get('supersedes')
            if obj.get('status')=='superseded' and not replacement:errors.append(f'{path} superseded PlatformChange requires superseded_by')
            if replacement:
                if replacement==obj.get('id'):errors.append(f'{path} PlatformChange cannot supersede itself')
                elif replacement not in index:errors.append(f'{path} superseded_by {replacement} does not exist')
                else:
                    current=index[replacement][0]
                    if current.get('object_type')!='PlatformChange' or current.get('semantic_key')!=key:errors.append(f'{path} superseded_by must reference the same PlatformChange semantic_key')
                    elif current.get('supersedes')!=obj.get('id'):errors.append(f'{path} supersession link is not reciprocal with {replacement}')
            if prior and prior not in index:errors.append(f'{path} supersedes {prior} does not exist')
    for key,values in active_attention.items():
        if key and len(values)>1:errors.append(f'multiple active AttentionItems share dedupe_key {key!r}: '+', '.join(obj['id'] for obj,_ in values))
    for key,values in current_platform.items():
        if key and len(values)>1:errors.append(f'multiple current PlatformChanges share semantic_key {key!r}: '+', '.join(obj['id'] for obj,_ in values))
    return errors


def main():
    parser=argparse.ArgumentParser();parser.add_argument('business_id');args=parser.parse_args();errors=lifecycle_errors(args.business_id)
    if errors:print('\n'.join(errors));raise SystemExit(1)
    print('attention/platform semantic validation passed')

if __name__=='__main__':main()
