#!/usr/bin/env python3
"""Import an approved InnovationPackage without manufacturing organizational conclusions."""
from _common import *
from innovation_common import load_package,validate_package,validate_schema,innovation_package_dir,innovation_entry_path
import argparse,json,hashlib,os


def _write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);temporary=path.with_suffix(path.suffix+'.tmp');temporary.write_text(json.dumps(obj,indent=2)+'\n');os.replace(temporary,path)
def _counts(summary):
    summary=summary or {};return {key:int(summary.get(key,0) or 0) for key in ['replication_count','supported_count','contradicted_count','neutral_count']}


def import_package(business_id,package_path):
    base=instance_dir(business_id)
    if not base.exists():raise ValueError(f'Unknown business: {business_id}')
    package=load_package(package_path);validate_package(package,require_export_approval=True);process=package['process'];fingerprint=package['innovation_fingerprint'];timestamp=now()

    package_dir=innovation_package_dir(business_id);package_dir.mkdir(parents=True,exist_ok=True);stored=package_dir/f"{package['package_id']}.json";_write_json(stored,package)
    source_id='src_iex_'+hashlib.sha256(f"{business_id}|{package['package_id']}".encode()).hexdigest()[:18];source_path=base/'intelligence'/'sources'/f'{source_id}.json';existing_source=json.loads(source_path.read_text()) if source_path.exists() else {};source_reference=storage_ref(stored)
    source={
        'id':source_id,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,
        'created_at':existing_source.get('created_at') or timestamp,'updated_at':timestamp,'lineage':[],
        'source_type':'aura_innovation_package','source_reference':source_reference,
        'origin':package.get('contributor',{}).get('display_name') or package.get('contributor',{}).get('pseudonym') or 'ViralTrac AURA Innovation Exchange',
        'retrieved_at':timestamp,'published_at':package.get('created_at'),'content_hash':package.get('integrity',{}).get('content_hash'),'access_scope':'shared_contribution',
        'extensions':{'businessos_evidence':{'capture_status':'captured','capture_method':'structured_record','acquisition_method':'user_provided','title':process.get('title'),'context':'Portable AURA InnovationPackage; reported outcomes are contribution claims, not independent proof.'},'innovation_fingerprint':fingerprint,'package_id':package['package_id'],'detail_level':package['detail_level']}
    }
    validate_schema('SourceRecord',source);_write_json(source_path,source)

    entry_id='iex_'+hashlib.sha256(f"{business_id}|{fingerprint}".encode()).hexdigest()[:20];entry_path=innovation_entry_path(business_id,entry_id);old=json.loads(entry_path.read_text()) if entry_path.exists() else None;package_ids=list(old.get('package_ids',[])) if old else [];source_refs=list(old.get('source_record_refs',[])) if old else [];new_package=package['package_id'] not in package_ids
    if new_package:package_ids.append(package['package_id'])
    if source_id not in source_refs:source_refs.append(source_id)
    reported=dict(old.get('reported_evidence',{})) if old else {'contribution_count':0,'reported_replication_count':0,'reported_supported_count':0,'reported_contradicted_count':0,'reported_neutral_count':0}
    if new_package:
        counts=_counts(package.get('evidence_summary'));reported['contribution_count']+=1;reported['reported_replication_count']+=counts['replication_count'];reported['reported_supported_count']+=counts['supported_count'];reported['reported_contradicted_count']+=counts['contradicted_count'];reported['reported_neutral_count']+=counts['neutral_count']
    local=dict(old.get('local_evidence',{})) if old else {'supported_count':0,'contradicted_count':0,'neutral_count':0,'outcome_events':[]}
    entry={
        'id':entry_id,'business_id':business_id,'created_at':old.get('created_at') if old else timestamp,'updated_at':timestamp,
        'innovation_fingerprint':fingerprint,'mode':process['mode'],'workflow_id':process['workflow_id'],'title':process['title'],
        'package_ids':package_ids,'source_record_refs':source_refs,'reported_evidence':reported,'local_evidence':local,'last_activity_at':timestamp,
        'extensions':{'package_paths':sorted(set((old.get('extensions',{}).get('package_paths',[]) if old else [])+[source_reference])),'latest_detail_level':package['detail_level']}
    }
    validate_schema('InnovationExchangeEntry',entry);_write_json(entry_path,entry);return entry,source,stored


def main():
    parser=argparse.ArgumentParser(description='Import an approved portable InnovationPackage as organization-local support data plus a canonical SourceRecord. The importer does not create an Insight or adopt the Workflow.');parser.add_argument('business_id');parser.add_argument('package_path');args=parser.parse_args()
    try:entry,source,stored=import_package(args.business_id,args.package_path)
    except (ValueError,json.JSONDecodeError) as exc:raise SystemExit(str(exc))
    print(json.dumps({'exchange_entry_id':entry['id'],'workflow_id':entry['workflow_id'],'source_record_ref':source['id'],'stored_package':storage_ref(stored),'rule':'Imported package is evidence of contributed operating knowledge, not proof of effectiveness or an organizational Insight.'},indent=2))


if __name__=='__main__':main()
