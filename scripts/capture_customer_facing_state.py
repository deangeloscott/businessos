#!/usr/bin/env python3
"""Capture pre-mutation customer-facing text state for later claim-delta validation."""
from _common import ROOT, now
from build_claim_manifest import scan_claims
from pathlib import Path
import argparse, hashlib, json

TEXT_EXT={'.html','.htm','.md','.txt'}
CAPTURE_VERSION='1.0'


def _sha(data:bytes): return hashlib.sha256(data).hexdigest()

def _rel_locator(path:Path):
    p=path.resolve()
    try:return p.relative_to(ROOT.resolve()).as_posix()
    except Exception:return p.as_posix()

def _source_identity(locator:str):
    return 'sha256:'+_sha(locator.rstrip('/').encode('utf-8'))

def _files(root:Path):
    if root.is_file(): return [root] if root.suffix.lower() in TEXT_EXT else []
    return sorted(p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in TEXT_EXT)

def capture(business_id,source):
    src=Path(source)
    if not src.is_absolute(): src=ROOT/src
    src=src.resolve()
    if not src.exists(): raise ValueError(f'customer-facing source not found: {source}')
    locator=_rel_locator(src)
    rows=[]; snapshot_parts=[]
    for p in _files(src):
        rel=p.name if src.is_file() else p.relative_to(src).as_posix()
        data=p.read_bytes(); digest='sha256:'+_sha(data)
        rows.append({'path':rel,'sha256':digest,'candidates':scan_claims(business_id,p)})
        snapshot_parts.append(f'{rel}\0{digest}\n')
    snap='sha256:'+_sha(''.join(snapshot_parts).encode('utf-8'))
    return {
        'format':'businessos.customer_facing_state',
        'format_version':CAPTURE_VERSION,
        'business_id':business_id,
        'captured_at':now(),
        'source_root':locator,
        'source_identity':_source_identity(locator),
        'snapshot_hash':snap,
        'files':rows,
    }

def main():
    ap=argparse.ArgumentParser(description='Capture customer-facing text state before an authorized mutation.')
    ap.add_argument('business_id'); ap.add_argument('source'); ap.add_argument('--output',required=True); a=ap.parse_args()
    try:d=capture(a.business_id,a.source)
    except ValueError as e:raise SystemExit(str(e))
    out=Path(a.output); out=out if out.is_absolute() else ROOT/out; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps({'output':str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else str(out),'source_identity':d['source_identity'],'snapshot_hash':d['snapshot_hash'],'files':len(d['files'])},indent=2))
if __name__=='__main__':main()
