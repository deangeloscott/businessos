#!/usr/bin/env python3
from _common import ROOT, object_index
from inspect_site_evidence import build_manifest, render_observation_statement, LOCAL_EVIDENCE_METHOD, source_identity
import argparse, json

PERSIST_MARKER='scripts/persist_site_observation.py'
LOCAL_SITE_SOURCE_TYPES={'first_party_website_export','website_export','local_site_export','first_party_site_export'}

def _local_ext(src):
    ext=src.get('extensions') if isinstance(src.get('extensions'),dict) else {}
    le=ext.get('businessos_local_evidence') if isinstance(ext.get('businessos_local_evidence'),dict) else {}
    return le

def _manifest_identity(manifest):
    root=manifest.get('source_root','')
    return manifest.get('source_identity') or source_identity(root)

def local_evidence_errors(business_id):
    idx=object_index(business_id); errors=[]; warnings=[]
    sources={k:v[0] for k,v in idx.items() if v[0].get('object_type')=='SourceRecord'}
    observations={k:v[0] for k,v in idx.items() if v[0].get('object_type')=='Observation'}
    local_candidates={sid for sid,src in sources.items() if src.get('source_type') in LOCAL_SITE_SOURCE_TYPES}
    manifests={}; identity_keys={}
    for sid,src in sources.items():
        le=_local_ext(src)
        if le.get('evidence_type')!='local_site_inspection': continue
        mp=ROOT/le.get('manifest_path','')
        if not mp.exists(): errors.append(f'{sid} local-site evidence manifest is missing: {le.get("manifest_path")!r}'); continue
        try: manifest=json.loads(mp.read_text())
        except Exception as e: errors.append(f'{sid} local-site evidence manifest is invalid JSON: {e}'); continue
        manifest_root=manifest.get('source_root','')
        if not manifest_root:
            errors.append(f'{sid} local-site evidence manifest has no source_root'); continue
        expected_identity=source_identity(manifest_root)
        actual_identity=_manifest_identity(manifest)
        if actual_identity!=expected_identity:
            errors.append(f'{sid} local-site evidence source_identity does not match normalized source_root')
        if src.get('source_reference')!=manifest_root:
            errors.append(f'{sid} source_reference does not match local evidence manifest source_root')
        if le.get('source_root') and le.get('source_root')!=manifest_root:
            errors.append(f'{sid} extensions.businessos_local_evidence.source_root does not match manifest')
        if le.get('source_identity') and le.get('source_identity')!=actual_identity:
            errors.append(f'{sid} extensions.businessos_local_evidence.source_identity does not match manifest')
        if str(manifest.get('format_version','1.0'))>='1.1':
            if not manifest.get('source_identity') or not le.get('source_identity'):
                errors.append(f'{sid} RC6 local-site evidence is missing source_identity')
        source_root=ROOT/manifest_root
        if not source_root.exists():
            # Historical evidence remains valid even if the original locator is later removed.
            # It cannot support a new current Observation until recaptured.
            current=None
        else:
            try: current=build_manifest(source_root,business_id,captured_at=manifest.get('captured_at'),source_locator=manifest_root)
            except Exception as e: errors.append(f'{sid} local-site evidence could not inspect current source state: {e}'); current=None
        if current is not None and current.get('source_identity')!=actual_identity:
            errors.append(f'{sid} current local-site locator identity does not match captured evidence identity')
        # A changed source does not invalidate historical evidence. Freshness is checked by
        # persist_site_observation.py when a workflow tries to create a new direct Observation.
        if src.get('content_hash')!=manifest.get('snapshot_hash'):
            errors.append(f'{sid} content_hash does not match deterministic local-site snapshot hash')
        if le.get('snapshot_hash')!=manifest.get('snapshot_hash'):
            errors.append(f'{sid} extensions.businessos_local_evidence.snapshot_hash does not match manifest')
        key=(actual_identity,manifest.get('snapshot_hash'))
        prior=identity_keys.get(key)
        if prior and prior!=mp:
            errors.append(f'{sid} duplicate local evidence capture identity for the same source locator and snapshot: {prior.relative_to(ROOT)} and {mp.relative_to(ROOT)}')
        else: identity_keys[key]=mp
        manifests[sid]=(manifest,mp)

    for oid,obs in observations.items():
        candidate_refs=[r for r in (obs.get('source_refs') or []) if r in local_candidates]
        uncaptured=[r for r in candidate_refs if r not in manifests]
        if uncaptured:
            errors.append(f'{oid} relies on local website/export source(s) {", ".join(uncaptured)} without deterministic capture; run scripts/inspect_site_evidence.py and use its SourceRecord before persisting direct site observations')
            continue
        local_refs=[r for r in candidate_refs if r in manifests]
        if not local_refs: continue
        if len(local_refs)!=1:
            errors.append(f'{oid} direct local-site Observation must use exactly one deterministic local-site SourceRecord')
            continue
        sid=local_refs[0]; manifest,mp=manifests[sid]
        ext=obs.get('extensions') if isinstance(obs.get('extensions'),dict) else {}
        le=ext.get('businessos_local_evidence') if isinstance(ext.get('businessos_local_evidence'),dict) else {}
        if obs.get('method')!=LOCAL_EVIDENCE_METHOD or le.get('persisted_by')!=PERSIST_MARKER:
            errors.append(f'{oid} directly observes a local site export but was not persisted through {PERSIST_MARKER}; model-written direct site facts are not sufficient evidence')
            continue
        if le.get('manifest_path')!=mp.relative_to(ROOT).as_posix() or le.get('snapshot_hash')!=manifest.get('snapshot_hash'):
            errors.append(f'{oid} local evidence manifest/snapshot reference does not match its SourceRecord')
        if le.get('source_identity') and le.get('source_identity')!=_manifest_identity(manifest):
            errors.append(f'{oid} local evidence source_identity does not match its SourceRecord')
        fact_refs=le.get('fact_refs') if isinstance(le.get('fact_refs'),list) else []
        if not fact_refs:
            errors.append(f'{oid} local-site Observation has no deterministic fact_refs'); continue
        byid={f['id']:f for f in manifest.get('facts',[])}
        missing=[x for x in fact_refs if x not in byid]
        if missing:
            errors.append(f'{oid} references unknown deterministic site fact(s): {", ".join(missing)}'); continue
        facts=[byid[x] for x in fact_refs]
        expected=render_observation_statement(facts)
        if obs.get('statement')!=expected:
            errors.append(f'{oid} statement does not exactly match its deterministic fact_refs; direct local observations may not add or alter site facts outside the evidence manifest')
    return errors,warnings

def main():
    ap=argparse.ArgumentParser(description='Validate deterministic first-party/local evidence support for direct website observations.')
    ap.add_argument('business_id'); a=ap.parse_args()
    errors,warnings=local_evidence_errors(a.business_id)
    print(f'business={a.business_id} local_evidence_errors={len(errors)} warnings={len(warnings)}')
    for w in warnings: print('WARNING',w)
    for e in errors: print('ERROR',e)
    if errors: raise SystemExit(1)
    print('local evidence validation passed')

if __name__=='__main__': main()
