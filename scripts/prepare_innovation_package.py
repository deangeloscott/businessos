#!/usr/bin/env python3
from _common import *
from process_extensions import get_extension
from innovation_common import validate_package,bounded_summary,innovation_fingerprint,find_identifying_keys
import argparse,json,hashlib


def _sharing_config(business_id):
    path=ROOT/'instances'/business_id/'config'/'innovation-sharing.json'
    if path.exists():
        try:return json.loads(path.read_text())
        except Exception:pass
    return {'format_version':'1.0','prompt_mode':'ask_when_noteworthy','default_detail_level':'workflow_only','default_identity_level':'anonymous','exchange_discovery_enabled':False,'exchange_sources':[],'notes':None}

def _evidence_counts(summary):
    if summary is None:return
    for key in ['replication_count','supported_count','contradicted_count','neutral_count']:
        if key in summary and (not isinstance(summary[key],int) or summary[key]<0):raise ValueError(f'evidence_summary.{key} must be a non-negative integer')


def prepare_package(business_id,extension_id,detail=None,identity=None,evidence_summary=None,case_study=None,display_name=None,pseudonym=None,output=None):
    extension=get_extension(business_id,extension_id);config=_sharing_config(business_id);detail=detail or config.get('default_detail_level') or 'workflow_only';identity=identity or config.get('default_identity_level') or 'anonymous'
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
    else:
        if evidence_summary is None or case_study is None:raise ValueError('full_case_study requires bounded evidence summary and case study')
    _evidence_counts(evidence_summary)
    if identity!='named':
        identifying=find_identifying_keys(evidence_summary)+find_identifying_keys(case_study)
        if identifying:raise ValueError('Anonymous/pseudonymous package summary contains direct identifying field(s): '+', '.join(identifying))

    process={'mode':extension['mode'],'owner_system':extension['owner_system'],'target_contract_id':extension.get('target_contract_id'),'local_contract_id':extension.get('local_contract_id'),'title':extension['title'],'purpose':extension['purpose'],'route_terms':extension.get('route_terms') or [],'reads':extension.get('reads') or [],'writes':extension.get('writes') or [],'required_capabilities':extension.get('required_capabilities') or [],'optional_capabilities':extension.get('optional_capabilities') or [],'applies_when':extension.get('applies_when') or [],'does_not_apply_when':extension.get('does_not_apply_when') or [],'instructions':extension.get('instructions') or [],'verification':extension.get('verification') or [],'compatibility':extension.get('compatibility') or {'aura_min':os_version(),'aura_max':None}}
    fingerprint=innovation_fingerprint(process);timestamp=now();package_id='ipkg_'+hashlib.sha256(f'{fingerprint}|{business_id}|{timestamp}'.encode()).hexdigest()[:20]
    package={'format_version':'1.0','package_id':package_id,'created_at':timestamp,'aura_version':os_version(),'innovation_fingerprint':fingerprint,'detail_level':detail,'identity_level':identity,'contributor':{'display_name':display_name,'pseudonym':pseudonym},'process':process,'evidence_summary':evidence_summary,'case_study':case_study,'privacy':{'raw_private_state_included':False,'secrets_included':False,'source_business_identity_included':identity=='named','user_approved_export':False,'approved_at':None},'integrity':{'algorithm':'sha256','content_hash':None}}
    validate_package(package);path=Path(output) if output else ROOT/'runtime'/'innovation'/business_id/f'{package_id}.draft.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(package,indent=2)+'\n');return package,path


def main():
    parser=argparse.ArgumentParser(description='Prepare a local InnovationPackage draft. This does not approve or submit sharing.');parser.add_argument('business_id');parser.add_argument('extension_id');parser.add_argument('--detail',choices=['workflow_only','anonymized_evidence','full_case_study']);parser.add_argument('--identity',choices=['anonymous','pseudonymous','named']);parser.add_argument('--display-name');parser.add_argument('--pseudonym');parser.add_argument('--evidence-summary-file');parser.add_argument('--case-study-file');parser.add_argument('--output');args=parser.parse_args()
    try:
        evidence=json.loads(Path(args.evidence_summary_file).read_text()) if args.evidence_summary_file else None;case=json.loads(Path(args.case_study_file).read_text()) if args.case_study_file else None;package,path=prepare_package(args.business_id,args.extension_id,args.detail,args.identity,evidence,case,args.display_name,args.pseudonym,args.output)
    except (ValueError,json.JSONDecodeError) as exc:raise SystemExit(str(exc))
    print(json.dumps({'package_id':package['package_id'],'draft_path':str(path),'approved_for_export':False},indent=2))

if __name__=='__main__':main()
