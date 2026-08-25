#!/usr/bin/env python3
from _common import *
from innovation_common import validate_schema
import argparse,json,os

def configure(business_id,prompt_mode='ask_when_noteworthy',detail='workflow_only',identity='anonymous',discovery=False,sources=None,notes=None):
    base=ROOT/'instances'/business_id
    if not base.exists():raise ValueError(f'Unknown business: {business_id}')
    obj={'format_version':'1.0','prompt_mode':prompt_mode,'default_detail_level':detail,'default_identity_level':identity,'exchange_discovery_enabled':bool(discovery),'exchange_sources':list(dict.fromkeys(sources or [])),'notes':notes}
    validate_schema('InnovationSharingConfig',obj); path=base/'config'/'innovation-sharing.json';path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,path);return obj,path

def main():
    ap=argparse.ArgumentParser(description='Configure Innovation Exchange prompting/defaults. This never grants standing permission to share data.');ap.add_argument('business_id');ap.add_argument('--prompt-mode',choices=['never_ask','ask_when_noteworthy','prepare_draft_only'],default='ask_when_noteworthy');ap.add_argument('--detail',choices=['workflow_only','anonymized_evidence','full_case_study'],default='workflow_only');ap.add_argument('--identity',choices=['anonymous','pseudonymous','named'],default='anonymous');ap.add_argument('--enable-discovery',action='store_true');ap.add_argument('--source',action='append',default=[]);ap.add_argument('--notes');a=ap.parse_args()
    try:obj,path=configure(a.business_id,a.prompt_mode,a.detail,a.identity,a.enable_discovery,a.source,a.notes)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps({'path':str(path.relative_to(ROOT)),**obj},indent=2))
if __name__=='__main__':main()
