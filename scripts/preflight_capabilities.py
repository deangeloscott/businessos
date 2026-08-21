#!/usr/bin/env python3
from _common import *
from resolve_capability import resolve
import argparse,json


def _recommendations(capabilities):
    path=ROOT/'distribution/provider-recommendations.json'
    if not path.exists(): return []
    data=json.loads(path.read_text())
    reg={p['id']:p for p in provider_registry().get('providers',[])}
    out=[]
    for rec in data.get('recommendations',[]):
        p=reg.get(rec.get('provider_id'))
        if not p: continue
        if capabilities and not set(capabilities).intersection(p.get('capabilities',[])): continue
        out.append(rec)
    return out

def preflight(business_id,contract_id,environment=None,include_optional=False,use_declared_environment=False):
    environment=environment or installation().get('default_environment') or 'local'
    if not (ROOT/'instances'/business_id).exists():
        raise ValueError(f'Unknown business: {business_id}')
    reg=load_registry(); match=next((x for x in reg['contracts'] if x['id']==contract_id),None)
    if not match: raise ValueError(f'Unknown contract: {contract_id}')
    required=[c for c in match.get('capabilities',{}).get('required',[]) if c!='none']
    optional=[c for c in match.get('capabilities',{}).get('optional',[]) if c!='none']
    profile_path=ROOT/'deployment/environments'/environment/'host-profile.json'
    profile=json.loads(profile_path.read_text()) if profile_path.exists() else {}
    discovery_complete=profile.get('discovery_status')=='completed'
    if not discovery_complete and not use_declared_environment:
        return {
            'version':os_version(),'business_id':business_id,'contract_id':contract_id,'environment':environment,
            'status':'host_discovery_required','automated_ready':False,'required':[],'optional':[],'optional_checked':include_optional,
            'host_discovery':{'completed':False,'policy':'core/policies/host-capability-discovery.md'},
            'recommendations':_recommendations(required+optional),
            'next_action':'Inspect the current host tools, conservatively map clear capabilities, run scripts/bootstrap_environment.py, then rerun preflight. If discovery is impossible, rerun with --use-declared-environment.',
            'rule':'Do not recommend/acquire a provider merely because the fresh local profile has not yet discovered tools the host already supplies.'
        }

    def check(cap):
        r=resolve(environment,cap,business_id)
        row={'capability':cap,'resolution':r}
        if r['status']=='available':
            row['execution_state']='available'
            row['decision_required']=False
        elif r['status']=='provider_refresh_required':
            row['execution_state']='provider_discovery'
            row['decision_required']=False
            row['next_action']='refresh_existing_provider_capability_discovery'
        elif r['status']=='provider_recommended':
            row['execution_state']='provider_decision'
            row['decision_required']=True
            row['fallback_if_not_authorized']='manual_or_assisted_if_safe'
        else:
            row['execution_state']='manual_or_assisted_fallback'
            row['decision_required']=False
        return row

    req=[check(c) for c in required]
    opt=[check(c) for c in optional] if include_optional else []
    if not req or all(x['execution_state']=='available' for x in req):
        status='ready'
    elif any(x['execution_state']=='provider_discovery' for x in req):
        status='provider_discovery_required'
    elif any(x['execution_state']=='provider_decision' for x in req):
        status='decision_required'
    else:
        status='ready_with_fallback'
    return {
        'version':os_version(),
        'business_id':business_id,
        'contract_id':contract_id,
        'environment':environment,
        'status':status,
        'automated_ready':all(x['execution_state']=='available' for x in req),
        'required':req,
        'optional':opt,
        'optional_checked':include_optional,
        'host_discovery':{'completed':discovery_complete,'profile':profile},
        'recommendations':_recommendations(required+optional),
        'rule':'Missing automation changes the executor, not the required process. Execution resolution and provider recommendation are separate; any new connection requires authorization.'
    }


def main():
    p=argparse.ArgumentParser(description='Preflight one atomic contract against the active deployment capabilities before execution.')
    p.add_argument('business_id');p.add_argument('contract_id');p.add_argument('--environment');p.add_argument('--include-optional',action='store_true');p.add_argument('--use-declared-environment',action='store_true',help='Proceed from declared bindings even if host discovery could not be completed.');p.add_argument('--output')
    a=p.parse_args()
    try:r=preflight(a.business_id,a.contract_id,a.environment,a.include_optional,a.use_declared_environment)
    except ValueError as e:raise SystemExit(str(e))
    out=json.dumps(r,indent=2)+'\n'
    if a.output:Path(a.output).write_text(out)
    else:print(out,end='')
if __name__=='__main__':main()
