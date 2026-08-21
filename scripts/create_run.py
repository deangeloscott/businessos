#!/usr/bin/env python3
from _common import *
import argparse,json,secrets
p=argparse.ArgumentParser();p.add_argument('business_id');p.add_argument('contract_id');p.add_argument('task');p.add_argument('--focus',action='append',default=[]);a=p.parse_args()
reg=load_registry();valid={x['id'] for x in reg['contracts']}
if a.contract_id not in valid: raise SystemExit('Unknown contract')
if not (ROOT/'instances'/a.business_id).exists(): raise SystemExit('Unknown business')
rid='run_'+secrets.token_hex(8);corr='cor_'+secrets.token_hex(8);ts=now();d=ROOT/'runtime/runs'/a.business_id/rid;d.mkdir(parents=True)
obj={'run_id':rid,'business_id':a.business_id,'task':a.task,'contract_id':a.contract_id,'status':'active','focus_refs':a.focus,'correlation_id':corr,'causation_id':None,'created_at':ts,'updated_at':ts}
(d/'run.json').write_text(json.dumps(obj,indent=2)+'\n');(d/'artifacts').mkdir();(d/'checkpoints').mkdir();(d/'logs').mkdir();(d/'README.md').write_text('Run-local working/recovery state. Preserve validated outputs and resume according to core/policies/local-state-and-recovery.md.\n');print(rid)
