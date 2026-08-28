#!/usr/bin/env python3
from _common import *
import argparse, json, sys
from datetime import datetime, timezone
from jsonschema import Draft202012Validator

PROVIDER_ID='viraltrac'
INTEROP=ROOT/'core/providers/viraltrac/event-interoperability.json'
REACTIVE_SCHEMA=ROOT/'core/schemas/runtime/reactive-monitoring-profile.schema.json'
BINDING_SCHEMA=ROOT/'core/schemas/runtime/capability-binding.schema.json'
RECOGNIZED={'off','publish_shadow','evaluate_shadow','allowlisted_actions','broad','degraded'}

def now(): return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')

def load_source(path):
    raw=sys.stdin.read() if path=='-' else resolve_storage_ref(path).read_text()
    return json.loads(raw)

def walk_modes(v, out):
    if isinstance(v,dict):
        for k,x in v.items():
            if str(k).lower() in {'mode','operational_mode','event_mode','event_fabric_mode'} and isinstance(x,str) and x in RECOGNIZED: out.add(x)
            walk_modes(x,out)
    elif isinstance(v,list):
        for x in v: walk_modes(x,out)

def resolve_mode(data, explicit=None):
    if explicit:
        if explicit not in RECOGNIZED: raise ValueError('Unknown event operational mode: '+explicit)
        return explicit
    found=set(); walk_modes(data,found)
    if len(found)==1: return next(iter(found))
    if not found: raise ValueError('Could not determine current event operational mode; supply --mode from the authenticated ViralTrac operations response.')
    raise ValueError('Multiple event mode values found; supply --mode explicitly: '+', '.join(sorted(found)))

def validate(schema_path,obj,label):
    errs=list(Draft202012Validator(json.loads(schema_path.read_text())).iter_errors(obj))
    if errs: raise ValueError(label+': '+'; '.join(e.message for e in errs))

def upsert_binding(bindings, binding, remove=False):
    key=(binding['capability'],binding.get('provider_id'),binding['connection_ref'])
    out=[]
    for b in bindings:
        if (b.get('capability'),b.get('provider_id'),b.get('connection_ref'))==key: continue
        out.append(b)
    if not remove: out.append(binding)
    return out

def activate(environment,business_id,operations,mode=None,delivery_mode='none',subscription_ref=None,connection_ref='provider:viraltrac'):
    if not environment_exists(environment): raise ValueError('Unknown environment: '+environment)
    biz=ROOT/'instances'/business_id
    if not biz.exists(): raise ValueError('Unknown business: '+business_id)
    ops=load_source(operations); opmode=resolve_mode(ops,mode)
    interop=json.loads(INTEROP.read_text())
    bp=environment_file(environment,'capability-bindings.json',writable=True); bindings=json.loads(bp.read_text()).get('bindings',[]) if bp.exists() else []
    has_vt=any(b.get('provider_id')==PROVIDER_ID and b.get('enabled',True) for b in bindings)
    if not has_vt: raise ValueError('No enabled ViralTrac binding exists in this environment; connect/synchronize ViralTrac first.')

    live_possible=opmode in set(interop['activation']['evaluation_modes']) and delivery_mode in {'push','poll'} and bool(subscription_ref)
    subscribe_binding={
      'capability':'business.event.subscribe','provider_id':PROVIDER_ID,'provider_action':'viraltrac:event_subscription_runtime',
      'connection_ref':connection_ref,'permissions':[],'limitations':[],
      'coverage':f'runtime_mode:{opmode};delivery:{delivery_mode}','reliability':None,'freshness':now(),'enabled':True
    }
    host_binding={
      'capability':'business.event.delivery.receive','provider_id':None,'provider_action':f'host:event_delivery:{delivery_mode}',
      'connection_ref':f'host:event_delivery:{delivery_mode}','permissions':[],'limitations':[],
      'coverage':'declared_by_current_host_or_harness','reliability':None,'freshness':now(),'enabled':True
    }
    if opmode=='evaluate_shadow': subscribe_binding['limitations']=['evaluation_only','event_triggered_external_effects_disabled']
    elif opmode=='degraded': subscribe_binding['limitations']=['degraded_mode','critical_or_required_reactions_only','optional_work_uses_fallback']
    elif opmode=='allowlisted_actions': subscribe_binding['limitations']=['only_separately_eligible_allowlisted_actions_may_execute']
    elif opmode=='broad': subscribe_binding['limitations']=['event_delivery_still_does_not_authorize_actions']

    bindings=[b for b in bindings if not (b.get('capability')=='business.event.subscribe' and b.get('provider_id')==PROVIDER_ID and b.get('connection_ref')==connection_ref)]
    bindings=[b for b in bindings if not (b.get('capability')=='business.event.delivery.receive' and str(b.get('connection_ref','')).startswith('host:event_delivery:'))]
    if live_possible:
        validate(BINDING_SCHEMA,subscribe_binding,'Invalid subscription binding'); validate(BINDING_SCHEMA,host_binding,'Invalid host delivery binding')
        bindings += [subscribe_binding,host_binding]
    bp.write_text(json.dumps({'bindings':bindings},indent=2)+'\n')

    rp=biz/'config/reactive-monitoring.json'
    profile=json.loads(rp.read_text()) if rp.exists() else {
      'format_version':'1.0','enabled':True,'provider_preference':'viraltrac','delivery_preference':'event_when_ready_else_poll','materiality_mode':'adaptive',
      'event_family_allowlist':[],'event_family_blocklist':[],'coalesce_window_seconds':300,'max_reaction_depth':8,'status':'not_configured','subscription_ref':None,'last_configured_at':None,'notes':None
    }
    if not profile.get('enabled',True): status='disabled'
    elif live_possible and opmode=='degraded': status='degraded'
    elif live_possible: status='ready'
    else: status='fallback'
    profile.update({'provider_preference':PROVIDER_ID,'status':status,'subscription_ref':subscription_ref if live_possible else None,'last_configured_at':now()})
    reason=[]
    if opmode in {'off','publish_shadow'}: reason.append('provider_mode_not_live_for_businessos_reaction')
    if delivery_mode=='none': reason.append('host_delivery_unavailable')
    if delivery_mode in {'push','poll'} and not subscription_ref: reason.append('subscription_ref_required_for_live_activation')
    if opmode=='degraded': reason.append('provider_degraded')
    profile['notes']='; '.join(reason) if reason else None
    validate(REACTIVE_SCHEMA,profile,'Invalid reactive monitoring profile')
    rp.parent.mkdir(parents=True,exist_ok=True); rp.write_text(json.dumps(profile,indent=2)+'\n')

    sp=environment_file(environment,'providers/viraltrac-capabilities.json')
    if sp.exists():
        writable_sp=environment_file(environment,'providers/viraltrac-capabilities.json',writable=True)
        snap=json.loads(writable_sp.read_text())
        for row in snap.get('capabilities',[]):
            if row.get('capability')=='business.event.subscribe':
                row['status']='bound' if live_possible else ('candidate' if opmode not in {'off','publish_shadow'} else 'not_detected')
                row['notes']=f'runtime mode={opmode}; host delivery={delivery_mode}; '+('subscription active' if live_possible else 'fallback active')
        writable_sp.write_text(json.dumps(snap,indent=2)+'\n')
    return {'provider_id':PROVIDER_ID,'environment':environment,'business_id':business_id,'operational_mode':opmode,'delivery_mode':delivery_mode,'live_reactive_enabled':live_possible,'status':status,'subscription_ref':subscription_ref if live_possible else None,'reason_codes':reason or ['reactive_event_path_ready']}

def main():
    p=argparse.ArgumentParser(description='Activate/deactivate the ViralTrac Event / Reactive Plane BusinessOS event path from current runtime mode/readiness evidence. This helper never creates credentials or invents a delivery endpoint.')
    p.add_argument('environment',nargs='?',default='local'); p.add_argument('--business-id',required=True)
    p.add_argument('--operations',required=True,help="Authenticated /v1/events/operations (or equivalent normalized runtime state) JSON, workspace-relative state ref, or '-' for stdin")
    p.add_argument('--mode',choices=sorted(RECOGNIZED),help='Explicit current runtime mode when the response contains multiple mode-like values.')
    p.add_argument('--delivery-mode',choices=['push','poll','none'],default='none',help='Current host/harness event-delivery mechanism. Use none when unavailable.')
    p.add_argument('--subscription-ref',help='Authoritative ViralTrac subscription/managed-binding reference. Required for live activation.')
    p.add_argument('--connection-ref',default='provider:viraltrac')
    a=p.parse_args()
    try: out=activate(a.environment,a.business_id,a.operations,a.mode,a.delivery_mode,a.subscription_ref,a.connection_ref)
    except (ValueError,json.JSONDecodeError) as e: raise SystemExit(str(e))
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
