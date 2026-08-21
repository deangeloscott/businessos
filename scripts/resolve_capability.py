#!/usr/bin/env python3
from _common import *
import argparse,json


def _read(path,default):
    try: return json.loads(path.read_text())
    except FileNotFoundError: return default


def _preferences(path):
    return _read(path,{'preferences':[]}).get('preferences',[])


def _provider_registry():
    rows=_read(ROOT/'core/providers/registry.json',{'providers':[]}).get('providers',[])
    return {p['id']:p for p in rows if p.get('status')!='deprecated'}


def _pref_map(rows):
    # One file may express only one effective state per capability/provider; validator rejects duplicates.
    return {(p['capability'],p['provider_id']):p for p in rows}


def _scope_preferences(environment,business_id):
    scopes=[]
    if business_id:
        scopes.append(('business_preference',ROOT/'instances'/business_id/'config/provider-preferences.json'))
    scopes.append(('environment_preference',ROOT/'deployment/environments'/environment/'provider-preferences.json'))
    scopes.append(('distribution_default',ROOT/'distribution/provider-defaults.json'))
    return [(name,_preferences(path)) for name,path in scopes]


def _blocked_providers(capability,scopes):
    # Higher-precedence scope wins for a provider. A business can therefore unblock/block a distribution default.
    effective={}
    for source,rows in scopes:
        for p in rows:
            if p.get('capability')==capability and p.get('provider_id') not in effective:
                effective[p['provider_id']]={**p,'source':source}
    return {pid for pid,p in effective.items() if p.get('mode')=='blocked'},effective


def _provider_snapshot(environment,provider_id):
    path=ROOT/'deployment/environments'/environment/'providers'/f'{provider_id}-capabilities.json'
    if not path.exists(): return None
    try: return _read(path,{})
    except Exception: return None


def _snapshot_status(environment,provider_id,capability):
    snap=_provider_snapshot(environment,provider_id)
    if not snap: return None
    row=next((x for x in snap.get('capabilities',[]) if x.get('capability')==capability),None)
    return row.get('status') if row else None


def _recommendation(provider,capability,source,preference=None,existing_connection_refs=None):
    acquisition=provider.get('acquisition',{})
    existing_connection_refs=sorted(set(existing_connection_refs or []))
    if existing_connection_refs:
        return {
            'status':'provider_refresh_required',
            'capability':capability,
            'source':source,
            'provider':provider,
            'preference':preference,
            'requires_user_authorization':False,
            'existing_connection_refs':existing_connection_refs,
            'machine_interfaces':provider.get('machine_interfaces',[]),
            'next_action':'discover_or_refresh_existing_provider_capabilities'
        }
    return {
        'status':'provider_recommended',
        'capability':capability,
        'source':source,
        'provider':provider,
        'preference':preference,
        'requires_user_authorization':bool(acquisition.get('requires_user_authorization',True)),
        'acquisition_url':acquisition.get('entry_url') or provider.get('signup_url') or provider.get('homepage_url'),
        'acquisition_attribution':acquisition.get('attribution'),
        'machine_interfaces':provider.get('machine_interfaces',[]),
        'next_action':'propose_connect_or_signup' if acquisition.get('supported') else 'provider_requires_manual_setup'
    }


def resolve(environment,capability,business_id=None):
    caps={x['id'] for x in _read(ROOT/'core/capabilities/catalog.json',{'capabilities':[]}).get('capabilities',[])}
    if capability not in caps: raise ValueError(f'Unknown capability: {capability}')
    env=ROOT/'deployment/environments'/environment
    if not env.exists(): raise ValueError(f'Unknown environment: {environment}')
    if business_id and not (ROOT/'instances'/business_id).exists(): raise ValueError(f'Unknown business: {business_id}')
    providers=_provider_registry(); scopes=_scope_preferences(environment,business_id); blocked,effective=_blocked_providers(capability,scopes)

    # Existing enabled bindings are the user's current deployment and win by default.
    bindings=_read(env/'capability-bindings.json',{'bindings':[]}).get('bindings',[])
    connected_refs={}
    for b in bindings:
        if not b.get('enabled',True) or not b.get('provider_id'): continue
        connected_refs.setdefault(b['provider_id'],[]).append(b.get('connection_ref'))
    active=[b for b in bindings if b.get('capability')==capability and b.get('enabled',True)]
    allowed=[]
    for b in active:
        pid=b.get('provider_id')
        if pid and pid in blocked: continue
        allowed.append(b)
    if allowed:
        # Prefer a specifically preferred provider if more than one active binding exists.
        rank={}
        for pid,p in effective.items():
            if p.get('mode')=='preferred': rank[pid]=(p.get('priority',999999),p.get('source'))
        allowed.sort(key=lambda b: rank.get(b.get('provider_id'),(999999,'')))
        return {'status':'available','capability':capability,'source':'active_binding','binding':allowed[0],'alternatives':allowed[1:]}

    # Business > environment > distribution preference.
    for source,rows in scopes:
        preferred=sorted([p for p in rows if p.get('capability')==capability and p.get('mode')=='preferred' and p.get('provider_id') not in blocked], key=lambda p:p.get('priority',999999))
        for pref in preferred:
            provider=providers.get(pref['provider_id'])
            if not provider or capability not in provider.get('capabilities',[]): continue
            snap_status=_snapshot_status(environment,provider['id'],capability)
            # A current provider snapshot outranks static potential-capability metadata.
            if snap_status in {'not_detected','candidate'}: continue
            return _recommendation(provider,capability,source,pref,connected_refs.get(provider['id']))

    compatible=[]
    for provider in providers.values():
        if capability not in provider.get('capabilities',[]) or provider.get('id') in blocked: continue
        if _snapshot_status(environment,provider['id'],capability) in {'not_detected','candidate'}: continue
        compatible.append(provider)
    compatible=sorted(compatible,key=lambda p:p.get('display_name','').lower())
    if compatible:
        first=compatible[0]
        return _recommendation(first,capability,'compatible_provider',None,connected_refs.get(first['id'])) | {'alternatives':compatible[1:]}
    return {
        'status':'unavailable',
        'capability':capability,
        'source':'manual_fallback',
        'requires_user_authorization':False,
        'next_action':'preserve_required_step_as_manual_or_assisted_work'
    }


def main():
    p=argparse.ArgumentParser(description='Resolve an active or preferred provider for one provider-neutral capability.')
    p.add_argument('environment');p.add_argument('capability');p.add_argument('--business')
    a=p.parse_args()
    try:r=resolve(a.environment,a.capability,a.business)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps(r,indent=2))

if __name__=='__main__': main()
