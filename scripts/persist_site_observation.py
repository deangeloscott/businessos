#!/usr/bin/env python3
from _common import ROOT, object_index, now, slug, storage_ref
from inspect_site_evidence import build_manifest, render_observation_statement, LOCAL_EVIDENCE_METHOD, source_identity
import argparse, json

PERSIST_MARKER='scripts/persist_site_observation.py'

def load_source(bid,source_ref):
    idx=object_index(bid)
    if source_ref not in idx or idx[source_ref][0].get('object_type')!='SourceRecord': raise ValueError(f'unknown SourceRecord: {source_ref}')
    src=idx[source_ref][0]; ext=src.get('extensions',{}).get('businessos_local_evidence',{})
    if ext.get('evidence_type')!='local_site_inspection': raise ValueError(f'{source_ref} is not a deterministic local-site evidence source; run inspect_site_evidence.py first')
    mp=ROOT/ext.get('manifest_path','')
    if not mp.exists(): raise ValueError(f'missing local evidence manifest: {ext.get("manifest_path")}')
    manifest=json.loads(mp.read_text());source_root=ROOT/manifest['source_root'];manifest_root=manifest.get('source_root','');expected_identity=source_identity(manifest_root)
    if manifest.get('source_identity') and manifest.get('source_identity')!=expected_identity:raise ValueError('local evidence source identity does not match its source_root')
    if src.get('source_reference')!=manifest_root:raise ValueError('local evidence SourceRecord source_reference does not match its manifest source_root')
    current=build_manifest(source_root,bid,captured_at=manifest.get('captured_at'),source_locator=manifest_root)
    if current['snapshot_hash']!=manifest.get('snapshot_hash'):raise ValueError('local site changed after evidence capture; capture the current source state before persisting a new direct observation')
    return src,manifest,mp

def persist(bid,source_ref,fact_ids,observation_type,subject_refs=None,id_suffix=None):
    src,manifest,mp=load_source(bid,source_ref);byid={f['id']:f for f in manifest.get('facts',[])};missing=[x for x in fact_ids if x not in byid]
    if missing:raise ValueError('unknown fact id(s): '+', '.join(missing))
    facts=[byid[x] for x in fact_ids];ts=now();suffix=id_suffix or slug(observation_type+'-'+fact_ids[0][-8:]);oid=f'obs_{bid}_{suffix}'
    obs={
        'id':oid,'object_type':'Observation','schema_version':'1.0.0','business_id':bid,'created_at':ts,'updated_at':ts,
        'lineage':[source_ref],'observation_type':observation_type,'subject_refs':subject_refs or [],
        'statement':render_observation_statement(facts),'source_refs':[source_ref],'observed_at':ts,'method':LOCAL_EVIDENCE_METHOD,'extraction_confidence':1.0,
        'extensions':{'businessos_local_evidence':{'persisted_by':PERSIST_MARKER,'manifest_path':storage_ref(mp),'snapshot_hash':manifest['snapshot_hash'],'source_identity':manifest.get('source_identity') or source_identity(manifest.get('source_root','')),'fact_refs':fact_ids}}
    }
    out=ROOT/'instances'/bid/'intelligence/observations'/f'{oid}.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(obs,indent=2,ensure_ascii=False)+'\n');return obs,out

def main():
    ap=argparse.ArgumentParser(description='Persist a direct SEO/site Observation only from deterministic facts captured by inspect_site_evidence.py.')
    ap.add_argument('business_id');ap.add_argument('--source-ref',required=True);ap.add_argument('--fact-id',action='append',required=True);ap.add_argument('--observation-type',required=True);ap.add_argument('--subject-ref',action='append',default=[]);ap.add_argument('--id-suffix');a=ap.parse_args()
    obs,path=persist(a.business_id,a.source_ref,a.fact_id,a.observation_type,a.subject_ref,a.id_suffix)
    print(json.dumps({'object_written':storage_ref(path),'observation_id':obs['id'],'statement':obs['statement']},indent=2,ensure_ascii=False))

if __name__=='__main__':main()
