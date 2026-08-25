#!/usr/bin/env python3
from _common import *
from process_extensions import get_extension
from innovation_common import validate_package,bounded_summary,innovation_fingerprint,find_identifying_keys
import argparse,json,hashlib,os

def _sharing_config(business_id):
    path=ROOT/'instances'/business_id/'config'/'innovation-sharing.json'
    if path.exists():
        try:return json.loads(path.read_text())
        except Exception:pass
    return {'format_version':'1.0','prompt_mode':'ask_when_noteworthy','default_detail_level':'workflow_only','default_identity_level':'anonymous','exchange_discovery_enabled':False,'exchange_sources':[],'notes':None}

def _evidence_counts(summary):
    if summary is None:return
    for k in ['replication_count','supported_count','contradicted_count','neutral_count']:
        if k in summary and (not isinstance(summary[k],int) or summary[k]<0):raise ValueError(f'evidence_summary.{k} must be a non-negative integer')

def prepare_package(business_id,extension_id,detail=None,identity=None,evidence_summary=None,case_study=None,display_name=None,pseudonym=None,output=None):
    ext=get_extension(business_id,extension_id);cfg=_sharing_config(business_id);detail=detail or cfg.get('default_detail_level') or 'workflow_only';identity=identity or cfg.get('default_identity_level') or 'anonymous'
    if detail not in {'workflow_only','anonymized_evidence','full_case_study'}:raise ValueError('Unknown detail level')
    if identity not in {'anonymous','pseudonymous','named'}:raise ValueError('Unknown identity level')
    if identity=='anonymous':display_name=None;pseudonym=None
    elif identity=='pseudonymous':
        if not pseudonym:raise ValueError('pseudonymous identity requires --pseudonym')
        display_name=None
    elif identity=='named':
        if not display_name:raise ValueError('named identity requires --display-name')
        pseudonym=None
    evidence_summary=bounded_summary(evidence_summary,'evidence_summary');case_study=bounded_summary(case_study,'case_study')
    if detail=='workflow_only':evidence_summary=None;case_study=None
    elif detail=='anonymized_evidence':
        if evidence_summary is None:raise ValueError('anonymized_evidence requires a bounded evidence summary')
        case_study=None
    elif detail=='full_case_study':
        if evidence_summary is None or case_study is None:raise ValueError('full_case_study requires bounded evidence summary and case study')
    _evidence_counts(evidence_summary)
    if identity!='named':
        id_hits=find_identifying_keys(evidence_summary)+find_identifying_keys(case_study)
        if id_hits:raise ValueError('Anonymous/pseudonymous package summary contains direct identifying field(s): '+', '.join(id_hits))
    process={'mode':ext['mode'],'owner_system':ext['owner_system'],'target_contract_id':ext.get('target_contract_id'),'local_contract_id':ext.get('local_contract_id'),'title':ext['title'],'purpose':ext['purpose'],'route_terms':ext.get('route_terms') or [],'reads':ext.get('reads') or [],'writes':ext.get('writes') or [],'required_capabilities':ext.get('required_capabilities') or [],'optional_capabilities':ext.get('optional_capabilities') or [],'applies_when':ext.get('applies_when') or [],'does_not_apply_when':ext.get('does_not_apply_when') or [],'instructions':ext.get('instructions') or [],'verification':ext.get('verification') or [],'compatibility':ext.get('compatibility') or {'businessos_min':os_version(),'businessos_max':None}}
    fp=innovation_fingerprint(process);ts=now();pid='ipkg_'+hashlib.sha256(f'{fp}|{business_id}|{ts}'.encode()).hexdigest()[:20]
    pkg={'format_version':'1.0','package_id':pid,'created_at':ts,'businessos_version':os_version(),'innovation_fingerprint':fp,'detail_level':detail,'identity_level':identity,'contributor':{'display_name':display_name,'pseudonym':pseudonym},'process':process,'evidence_summary':evidence_summary,'case_study':case_study,'privacy':{'raw_private_state_included':False,'secrets_included':False,'source_business_identity_included':False,'user_approved_export':False,'approved_at':None},'integrity':{'algorithm':'sha256','content_hash':None}}
    validate_package(pkg);out=Path(output) if output else ROOT/'runtime'/'innovation'/business_id/f'{pid}.draft.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(pkg,indent=2)+'\n');return pkg,out

def main():
    ap=argparse.ArgumentParser(description='Prepare a local InnovationPackage draft. This does not approve or submit sharing.');ap.add_argument('business_id');ap.add_argument('extension_id');ap.add_argument('--detail',choices=['workflow_only','anonymized_evidence','full_case_study']);ap.add_argument('--identity',choices=['anonymous','pseudonymous','named']);ap.add_argument('--display-name');ap.add_argument('--pseudonym');ap.add_argument('--evidence-summary-file');ap.add_argument('--case-study-file');ap.add_argument('--output');a=ap.parse_args()
    try:
        ev=json.loads(Path(a.evidence_summary_file).read_text()) if a.evidence_summary_file else None;cs=json.loads(Path(a.case_study_file).read_text()) if a.case_study_file else None;pkg,path=prepare_package(a.business_id,a.extension_id,a.detail,a.identity,ev,cs,a.display_name,a.pseudonym,a.output)
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))
    print(json.dumps({'package_id':pkg['package_id'],'draft_path':str(path),'approved_for_export':False},indent=2))
if __name__=='__main__':main()
