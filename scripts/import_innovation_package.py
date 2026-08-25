#!/usr/bin/env python3
from _common import *
from innovation_common import load_package,validate_package,validate_schema,compatibility_status
import argparse,json,hashlib,os

def _write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,path)

def _counts(summary):
    summary=summary or {};return {k:int(summary.get(k,0) or 0) for k in ['replication_count','supported_count','contradicted_count','neutral_count']}

def import_package(business_id,package_path):
    base=ROOT/'instances'/business_id
    if not base.exists():raise ValueError(f'Unknown business: {business_id}')
    pkg=load_package(package_path);validate_package(pkg,require_export_approval=True);proc=pkg['process'];fp=pkg['innovation_fingerprint'];ts=now();compat=compatibility_status(proc.get('compatibility') or {},os_version(),proc.get('target_contract_id'))
    pkgdir=base/'intelligence'/'innovation-exchange'/'packages';pkgdir.mkdir(parents=True,exist_ok=True);stored=pkgdir/f"{pkg['package_id']}.json";_write_json(stored,pkg)
    srid='src_iex_'+hashlib.sha256(f"{business_id}|{pkg['package_id']}".encode()).hexdigest()[:18]
    source={'id':srid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,'lineage':[],'source_type':'businessos_innovation_package','source_reference':pkg['package_id'],'origin':pkg.get('contributor',{}).get('display_name') or pkg.get('contributor',{}).get('pseudonym') or 'BusinessOS Innovation Exchange','retrieved_at':ts,'published_at':pkg.get('created_at'),'content_hash':pkg.get('integrity',{}).get('content_hash'),'access_scope':'shared_contribution','extensions':{'businessos_evidence':{'capture_status':'captured','capture_method':'structured_record','acquisition_method':'user_provided','title':proc.get('title'),'context':'Portable BusinessOS InnovationPackage; reported outcomes are not independent proof.'},'innovation_fingerprint':fp,'detail_level':pkg['detail_level']}}
    validate_schema('SourceRecord',source);spath=base/'intelligence'/'sources'/f'{srid}.json'
    if spath.exists():source['created_at']=json.loads(spath.read_text()).get('created_at') or ts
    _write_json(spath,source)
    iid='ins_iex_'+hashlib.sha256(f"{business_id}|{fp}".encode()).hexdigest()[:18];ipath=base/'intelligence'/'insights'/f'{iid}.json';existing_ins=json.loads(ipath.read_text()) if ipath.exists() else None;links=list(existing_ins.get('evidence_links',[])) if existing_ins else []
    if srid not in [x.get('ref') for x in links]:links.append({'ref':srid,'relationship':'contextualizes','weight':None,'reason':'Community contribution establishes the proposed workflow/report, not independent effectiveness.'})
    confidence={'workflow_only':0.15,'anonymized_evidence':0.25,'full_case_study':0.3}[pkg['detail_level']]
    insight={'id':iid,'object_type':'Insight','schema_version':'1.0.0','business_id':business_id,'created_at':existing_ins.get('created_at') if existing_ins else ts,'updated_at':ts,'lineage':[],'owner_system':proc['owner_system'],'insight_type':'community_process_candidate','statement':f"Community-contributed BusinessOS process candidate: {proc['title']} — {proc['purpose']}",'subject_refs':[],'evidence_links':links,'confidence':existing_ins.get('confidence',confidence) if existing_ins else confidence,'scope':{'source':'businessos_innovation_exchange','innovation_fingerprint':fp},'status':existing_ins.get('status','candidate') if existing_ins else 'candidate','reviewed_at':None,'extensions':{'external_learning':{'discovery_source':'businessos_innovation_exchange','innovation_fingerprint':fp,'reported_evidence':pkg.get('evidence_summary'),'requires_triangulation':True}}}
    validate_schema('Insight',insight);_write_json(ipath,insight)
    eid='iex_'+hashlib.sha256(f"{business_id}|{fp}".encode()).hexdigest()[:20];epath=base/'intelligence'/'innovation-exchange'/'entries'/f'{eid}.json';old=json.loads(epath.read_text()) if epath.exists() else None;package_ids=list(old.get('package_ids',[])) if old else [];source_refs=list(old.get('source_record_refs',[])) if old else [];new_package=pkg['package_id'] not in package_ids
    if new_package:package_ids.append(pkg['package_id'])
    if srid not in source_refs:source_refs.append(srid)
    reported=dict(old.get('reported_evidence',{})) if old else {'contribution_count':0,'reported_replication_count':0,'reported_supported_count':0,'reported_contradicted_count':0,'reported_neutral_count':0}
    if new_package:
        c=_counts(pkg.get('evidence_summary'));reported['contribution_count']+=1;reported['reported_replication_count']+=c['replication_count'];reported['reported_supported_count']+=c['supported_count'];reported['reported_contradicted_count']+=c['contradicted_count'];reported['reported_neutral_count']+=c['neutral_count']
    local=dict(old.get('local_evidence',{})) if old else {'supported_count':0,'contradicted_count':0,'neutral_count':0,'outcome_events':[]}
    entry={'id':eid,'object_type':'InnovationExchangeEntry','schema_version':'1.0.0','business_id':business_id,'created_at':old.get('created_at') if old else ts,'updated_at':ts,'innovation_fingerprint':fp,'owner_system':proc['owner_system'],'title':proc['title'],'target_contract_id':proc.get('target_contract_id'),'local_contract_id':proc.get('local_contract_id'),'compatibility_status':compat,'status':old.get('status','candidate') if old else 'candidate','package_ids':package_ids,'source_record_refs':source_refs,'insight_ref':iid,'reported_evidence':reported,'local_evidence':local,'last_activity_at':ts,'extensions':{'package_paths':sorted(set((old.get('extensions',{}).get('package_paths',[]) if old else [])+[str(stored.relative_to(ROOT))])),'latest_detail_level':pkg['detail_level']}}
    validate_schema('InnovationExchangeEntry',entry);_write_json(epath,entry);return entry,source,insight,stored

def main():
    ap=argparse.ArgumentParser(description='Import an approved portable InnovationPackage into one business as external/community evidence.');ap.add_argument('business_id');ap.add_argument('package_path');a=ap.parse_args()
    try:entry,source,insight,stored=import_package(a.business_id,a.package_path)
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))
    print(json.dumps({'exchange_entry_id':entry['id'],'compatibility_status':entry['compatibility_status'],'source_record_ref':source['id'],'insight_ref':insight['id'],'stored_package':str(stored.relative_to(ROOT))},indent=2))
if __name__=='__main__':main()
