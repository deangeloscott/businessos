#!/usr/bin/env python3
"""Validate integrity of optional deterministic local-site captures.

This validator applies only when evidence declares AURA's deterministic local-site capture
metadata. Other sound model/harness first-party evidence paths remain valid and are governed
by normal provenance/truth policy rather than this helper-specific format.
"""
from _common import ROOT,object_index
from inspect_site_evidence import source_identity
import argparse,json


def _local_ext(obj):
    ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
    return ext.get('businessos_local_evidence') if isinstance(ext.get('businessos_local_evidence'),dict) else {}


def _manifest_identity(manifest):
    root=manifest.get('source_root','')
    return manifest.get('source_identity') or source_identity(root)


def local_evidence_errors(business_id):
    idx=object_index(business_id);errors=[];warnings=[]
    sources={k:v[0] for k,v in idx.items() if v[0].get('object_type')=='SourceRecord'}
    manifests={}

    # Validate only SourceRecords that explicitly claim this deterministic capture format.
    for sid,src in sources.items():
        le=_local_ext(src)
        if le.get('evidence_type')!='local_site_inspection':continue
        raw_path=le.get('manifest_path')
        if not raw_path:
            errors.append(f'{sid} deterministic local-site evidence is missing manifest_path');continue
        mp=ROOT/raw_path
        if not mp.exists():errors.append(f'{sid} local-site evidence manifest is missing: {raw_path!r}');continue
        try:manifest=json.loads(mp.read_text())
        except Exception as exc:errors.append(f'{sid} local-site evidence manifest is invalid JSON: {exc}');continue
        manifest_root=manifest.get('source_root','')
        if not manifest_root:
            errors.append(f'{sid} local-site evidence manifest has no source_root');continue
        expected_identity=source_identity(manifest_root);actual_identity=_manifest_identity(manifest)
        if actual_identity!=expected_identity:errors.append(f'{sid} local-site evidence source_identity does not match normalized source_root')
        if src.get('source_reference')!=manifest_root:errors.append(f'{sid} source_reference does not match local evidence manifest source_root')
        if le.get('source_root') and le.get('source_root')!=manifest_root:errors.append(f'{sid} local evidence source_root does not match manifest')
        if le.get('source_identity') and le.get('source_identity')!=actual_identity:errors.append(f'{sid} local evidence source_identity does not match manifest')
        if src.get('content_hash')!=manifest.get('snapshot_hash'):errors.append(f'{sid} content_hash does not match deterministic local-site snapshot hash')
        if le.get('snapshot_hash')!=manifest.get('snapshot_hash'):errors.append(f'{sid} local evidence snapshot_hash does not match manifest')
        manifests[sid]=(manifest,mp)

    # If an Observation voluntarily preserves deterministic fact_refs, verify those refs are
    # real facts from its declared capture. Do not require this capture format or rewrite the
    # model's natural-language Observation into a canned sentence.
    for oid,(obs,path) in idx.items():
        if obs.get('object_type')!='Observation':continue
        le=_local_ext(obs);fact_refs=le.get('fact_refs') if isinstance(le.get('fact_refs'),list) else []
        if not fact_refs:continue
        local_sources=[ref for ref in (obs.get('source_refs') or []) if ref in manifests]
        if len(local_sources)!=1:
            errors.append(f'{oid} declares deterministic local fact_refs but does not reference exactly one matching deterministic local-site SourceRecord');continue
        sid=local_sources[0];manifest,mp=manifests[sid];byid={f.get('id'):f for f in manifest.get('facts',[]) if isinstance(f,dict) and f.get('id')}
        missing=[ref for ref in fact_refs if ref not in byid]
        if missing:errors.append(f'{oid} references unknown deterministic site fact(s): '+', '.join(missing))
        if le.get('manifest_path') and le.get('manifest_path')!=mp.relative_to(ROOT).as_posix():errors.append(f'{oid} local evidence manifest_path does not match its SourceRecord')
        if le.get('snapshot_hash') and le.get('snapshot_hash')!=manifest.get('snapshot_hash'):errors.append(f'{oid} local evidence snapshot_hash does not match its SourceRecord')
        if le.get('source_identity') and le.get('source_identity')!=_manifest_identity(manifest):errors.append(f'{oid} local evidence source_identity does not match its SourceRecord')
    return errors,warnings


def main():
    ap=argparse.ArgumentParser(description='Validate optional deterministic local-site capture integrity without gating other first-party evidence methods.')
    ap.add_argument('business_id');a=ap.parse_args();errors,warnings=local_evidence_errors(a.business_id)
    print(f'business={a.business_id} local_evidence_errors={len(errors)} warnings={len(warnings)}')
    for w in warnings:print('WARNING',w)
    for e in errors:print('ERROR',e)
    if errors:raise SystemExit(1)
    print('local evidence validation passed')

if __name__=='__main__':main()
