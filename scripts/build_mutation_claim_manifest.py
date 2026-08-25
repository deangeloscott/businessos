#!/usr/bin/env python3
"""Build a claim-delta manifest after mutating a customer-facing text surface."""
from _common import ROOT, now
from build_claim_manifest import scan_claims
from capture_customer_facing_state import TEXT_EXT, _files, _rel_locator, _source_identity, _sha
from pathlib import Path
import argparse, json, re

FORMAT='businessos.customer_facing_mutation_claims'
VERSION='1.0'

def _norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9\[\]#]+',' ',(s or '').lower())).strip()

def _state(business_id,src:Path):
    locator=_rel_locator(src); rows=[]; parts=[]
    for p in _files(src):
        rel=p.name if src.is_file() else p.relative_to(src).as_posix(); data=p.read_bytes(); digest='sha256:'+_sha(data)
        rows.append({'path':rel,'sha256':digest,'candidates':scan_claims(business_id,p)})
        parts.append(f'{rel}\0{digest}\n')
    return locator,_source_identity(locator),'sha256:'+_sha(''.join(parts).encode()),rows

def build(business_id,before_capture,after_source):
    bp=Path(before_capture); bp=bp if bp.is_absolute() else ROOT/bp
    before=json.loads(bp.read_text())
    if before.get('format')!='businessos.customer_facing_state' or before.get('business_id')!=business_id:
        raise ValueError('before capture is not a matching BusinessOS customer-facing state capture')
    src=Path(after_source); src=src if src.is_absolute() else ROOT/src; src=src.resolve()
    if not src.exists(): raise ValueError(f'after source not found: {after_source}')
    locator,sid,snapshot,after_rows=_state(business_id,src)
    if locator!=before.get('source_root') or sid!=before.get('source_identity'):
        raise ValueError('after source locator differs from before capture; customer-facing mutations must compare the same target surface')
    bmap={x['path']:x for x in before.get('files',[])}; amap={x['path']:x for x in after_rows}
    changed=sorted(p for p in set(bmap)|set(amap) if bmap.get(p,{}).get('sha256')!=amap.get(p,{}).get('sha256'))
    added=sorted(set(amap)-set(bmap)); removed=sorted(set(bmap)-set(amap))
    introduced=[]
    for p,row in amap.items():
        old={_norm(x) for x in bmap.get(p,{}).get('candidates',[]) if x}
        for sent in row.get('candidates',[]):
            if _norm(sent) not in old:
                introduced.append({'file':p,'text':sent,'classification':'unclassified','support_refs':[]})
    relbp=str(bp.relative_to(ROOT)) if bp.is_relative_to(ROOT) else str(bp)
    return {
        'format':FORMAT,'format_version':VERSION,'business_id':business_id,'generated_at':now(),
        'before_capture':relbp,'source_root':locator,'source_identity':sid,
        'before_snapshot_hash':before.get('snapshot_hash'),'after_snapshot_hash':snapshot,
        'changed_customer_facing_files':changed,'added_customer_facing_files':added,'removed_customer_facing_files':removed,
        'introduced_claims':introduced,
    }

def main():
    ap=argparse.ArgumentParser(description='Compare before/after customer-facing text and create the claim-delta manifest required for governed mutations.')
    ap.add_argument('business_id'); ap.add_argument('before_capture'); ap.add_argument('after_source'); ap.add_argument('--output',required=True); a=ap.parse_args()
    try:d=build(a.business_id,a.before_capture,a.after_source)
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))
    out=Path(a.output);out=out if out.is_absolute() else ROOT/out;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps({'output':str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else str(out),'changed_files':d['changed_customer_facing_files'],'introduced_claim_count':len(d['introduced_claims'])},indent=2))
if __name__=='__main__':main()
