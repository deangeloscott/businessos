#!/usr/bin/env python3
"""Validate claim-safe mutations of existing customer-facing text surfaces."""
from _common import ROOT, object_index
from build_mutation_claim_manifest import build as rebuild_delta, FORMAT as DELTA_FORMAT
from capture_customer_facing_state import TEXT_EXT
from validate_business_claims import validate_manifest_sentences, business_name
from pathlib import Path
import argparse, json

ACTIVE_STATUSES={'applied','verifying','verified','closed','partially_applied'}
CUSTOMER_FACING_OWNERS={'seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}
PROTECTED_PREFIXES=('core/','systems/','scripts/','tests/','docs/','generated/','runtime/','instances/','deployment/')


def _file_path(ref):
    if not isinstance(ref,str) or not ref.startswith('file:'): return None
    raw=ref[5:]
    p=Path(raw); return p if p.is_absolute() else ROOT/p

def _rel(p:Path):
    try:return p.resolve().relative_to(ROOT.resolve()).as_posix()
    except Exception:return p.resolve().as_posix()

def _is_customer_facing_target(ref,owner):
    p=_file_path(ref)
    if p is None:return False
    ext=p.suffix.lower()
    if ext in {'.html','.htm'}: return True
    if ext not in {'.md','.txt'}: return False
    rel=_rel(p)
    if rel.startswith(PROTECTED_PREFIXES): return False
    return owner in CUSTOMER_FACING_OWNERS

def _under(path:Path,root:Path):
    try:path.resolve().relative_to(root.resolve());return True
    except Exception:return path.resolve()==root.resolve()

def mutation_errors(business_id,objects=None):
    idx=object_index(business_id); errors=[]; name=business_name(business_id)
    if objects is None: objects=list(idx.values())
    else: objects=[(o,ROOT/p) if isinstance(p,str) else (o,p) for o,p in objects]
    byid={o.get('id'):o for o,_ in objects if o.get('id')}
    for chg,path in objects:
        if chg.get('object_type')!='ChangeEvent' or chg.get('status') not in ACTIVE_STATUSES: continue
        ap=byid.get(chg.get('action_packet_ref'))
        owner=ap.get('owner_system') if isinstance(ap,dict) else None
        targets=[r for r in chg.get('target_refs',[]) if _is_customer_facing_target(r,owner)]
        if not targets: continue
        relpath=str(path.relative_to(ROOT)) if isinstance(path,Path) and path.is_absolute() else str(path)
        ext=chg.get('extensions') if isinstance(chg.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        if bos.get('customer_facing') is False:
            errors.append(f'{relpath} cannot opt out of claim governance for customer-facing file targets')
            continue
        entries=bos.get('customer_facing_mutations')
        if not isinstance(entries,list) or not entries:
            errors.append(f'{relpath} mutates customer-facing file(s) but has no extensions.businessos.customer_facing_mutations evidence; capture before state with scripts/capture_customer_facing_state.py and build the post-change claim delta with scripts/build_mutation_claim_manifest.py')
            continue
        covered=set()
        for i,entry in enumerate(entries):
            ctx=f'{relpath} customer_facing_mutations[{i}]'
            if not isinstance(entry,dict): errors.append(f'{ctx} must be an object');continue
            root_raw=entry.get('surface_root'); before_raw=entry.get('before_capture'); delta_raw=entry.get('claim_delta')
            if not root_raw or not before_raw or not delta_raw:
                errors.append(f'{ctx} requires surface_root, before_capture, and claim_delta');continue
            root=Path(root_raw); root=root if root.is_absolute() else ROOT/root
            bp=Path(before_raw); bp=bp if bp.is_absolute() else ROOT/bp
            dp=Path(delta_raw); dp=dp if dp.is_absolute() else ROOT/dp
            if not bp.exists() or not dp.exists():
                errors.append(f'{ctx} referenced before_capture/claim_delta does not exist');continue
            try: stored=json.loads(dp.read_text())
            except Exception as e: errors.append(f'{ctx} claim_delta is invalid JSON: {e}');continue
            if stored.get('format')!=DELTA_FORMAT or stored.get('business_id')!=business_id:
                errors.append(f'{ctx} claim_delta is not a matching BusinessOS customer-facing mutation manifest');continue
            try: current=rebuild_delta(business_id,bp,root)
            except Exception as e: errors.append(f'{ctx} could not reproduce mutation delta: {e}');continue
            for k in ('source_root','source_identity','before_snapshot_hash','after_snapshot_hash','changed_customer_facing_files','added_customer_facing_files','removed_customer_facing_files'):
                if stored.get(k)!=current.get(k): errors.append(f'{ctx} {k} does not match reproduced before/after state')
            expected={(x.get('file'),x.get('text')) for x in current.get('introduced_claims',[])}
            actual={(x.get('file'),x.get('text')) for x in stored.get('introduced_claims',[]) if isinstance(x,dict)}
            if actual!=expected:
                errors.append(f'{ctx} introduced_claims do not exactly match the reproduced customer-facing claim delta')
            # Every changed/added/removed customer-facing file must be represented in ChangeEvent.target_refs.
            changed=set(current.get('changed_customer_facing_files',[]))
            for rel in changed:
                fp=(root/rel) if root.is_dir() else root
                ref='file:'+_rel(fp)
                if ref not in chg.get('target_refs',[]):
                    errors.append(f'{ctx} changed customer-facing file is missing from ChangeEvent.target_refs: {ref}')
                covered.add(ref)
            claims=stored.get('introduced_claims',[])
            errors.extend(validate_manifest_sentences(claims,[x[1] for x in sorted(expected)],idx,name,ctx))
            for ref in targets:
                p=_file_path(ref)
                if p is not None and _under(p,root):
                    try: target_rel=p.resolve().relative_to(root.resolve()).as_posix() if root.is_dir() else p.name
                    except Exception: target_rel=p.name
                    if target_rel not in changed:
                        errors.append(f'{ctx} customer-facing target is not shown as changed relative to the declared before capture: {ref}; capture the surface before editing rather than post-hoc')
                    else:
                        covered.add(ref)
        missing=[r for r in targets if r not in covered]
        if missing: errors.append(f'{relpath} customer-facing mutation evidence does not cover target(s): {missing}')
    return errors

def main():
    ap=argparse.ArgumentParser(description='Validate that existing customer-facing asset mutations did not introduce unsupported active-business claims.')
    ap.add_argument('business_id'); a=ap.parse_args()
    errors=mutation_errors(a.business_id)
    print(f'business={a.business_id} customer_facing_mutation_errors={len(errors)}')
    for e in errors: print('ERROR',e)
    if errors: raise SystemExit(1)
    print('customer-facing mutation validation passed')
if __name__=='__main__':main()
