#!/usr/bin/env python3
from _common import *
import argparse,collections

def lifecycle_errors(bid,objects=None):
    pairs=objects if objects is not None else [(o,str(p.relative_to(ROOT))) for o,p in iter_instance_objects(bid)]
    idx={o.get('id'):(o,p) for o,p in pairs if o.get('id')}
    errors=[]; active=collections.defaultdict(list); current=collections.defaultdict(list)
    for o,p in pairs:
        typ=o.get('object_type')
        if typ=='AttentionItem':
            if o.get('status') in {'open','acknowledged'}:active[o.get('dedupe_key')].append((o,p))
            if o.get('status')=='resolved' and not o.get('resolved_at'):errors.append(f'{p} resolved AttentionItem requires resolved_at')
            sb=o.get('superseded_by')
            if o.get('status')=='superseded' and not sb:errors.append(f'{p} superseded AttentionItem requires superseded_by')
            if sb:
                if sb==o.get('id'):errors.append(f'{p} AttentionItem cannot supersede itself')
                elif sb not in idx:errors.append(f'{p} superseded_by {sb} does not exist')
        elif typ=='PlatformChange':
            key=o.get('semantic_key')
            if o.get('status')=='current':
                if o.get('authority')=='unknown': errors.append(f'{p} current PlatformChange requires non-unknown authority')
                refs=(o.get('source_refs') or [])+(o.get('evidence_refs') or [])
                if not refs: errors.append(f'{p} current PlatformChange requires source/evidence provenance')
                for ref in o.get('source_refs') or []:
                    if ref not in idx or idx[ref][0].get('object_type')!='SourceRecord': errors.append(f'{p} source_ref {ref} must reference an existing SourceRecord')
            if o.get('status')=='current':current[key].append((o,p))
            sb=o.get('superseded_by');sup=o.get('supersedes')
            if o.get('status')=='superseded' and not sb:errors.append(f'{p} superseded PlatformChange requires superseded_by')
            if o.get('status')=='current' and sb:errors.append(f'{p} current PlatformChange may not have superseded_by')
            if sb:
                if sb==o.get('id'):errors.append(f'{p} PlatformChange cannot supersede itself')
                elif sb not in idx:errors.append(f'{p} superseded_by {sb} does not exist')
                else:
                    n=idx[sb][0]
                    if n.get('object_type')!='PlatformChange' or n.get('semantic_key')!=key:errors.append(f'{p} superseded_by must reference the same PlatformChange semantic_key')
                    elif n.get('supersedes')!=o.get('id'):errors.append(f'{p} supersession link is not reciprocal with {sb}')
            if sup and sup not in idx:errors.append(f'{p} supersedes {sup} does not exist')
    for key,vals in active.items():
        if key and len(vals)>1:errors.append(f'multiple active AttentionItems share dedupe_key {key!r}: '+', '.join(o['id'] for o,_ in vals))
    for key,vals in current.items():
        if key and len(vals)>1:errors.append(f'multiple current PlatformChanges share semantic_key {key!r}: '+', '.join(o['id'] for o,_ in vals))
    return errors

def main():
    ap=argparse.ArgumentParser();ap.add_argument('business_id');a=ap.parse_args();e=lifecycle_errors(a.business_id)
    if e:print('\n'.join(e));raise SystemExit(1)
    print('attention/platform lifecycle validation passed')
if __name__=='__main__':main()
