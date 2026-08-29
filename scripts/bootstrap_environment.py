#!/usr/bin/env python3
from _common import *
import argparse, json, sys
from datetime import datetime, timezone


def _now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')


def _load(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def _manifest(path):
    if path=='-':
        return json.loads(sys.stdin.read())
    return json.loads(resolve_storage_ref(path).read_text())


def _host_connection_refs(host_data):
    refs=set()
    for t in (host_data or {}).get('tools',[]) or []:
        tid=t.get('id') or t.get('name')
        if not tid:continue
        refs.add(t.get('connection_ref') or f'host:{tid}')
    return refs


def bootstrap(environment, manifest=None, host_id=None, host_name=None, mark_welcome=False):
    if not environment_exists(environment):
        raise ValueError(f'Unknown environment: {environment}')
    env=environment_overlay_dir(environment,create=True)
    caps={x['id'] for x in json.loads((ROOT/'core/capabilities/catalog.json').read_text()).get('capabilities',[])}
    data={'format_version':'1.0','tools':[]}
    if manifest:
        data=_manifest(manifest)
    tools=data.get('tools',[])
    unknown=[]; inventory=[]; bindings=[]
    for t in tools:
        tid=t.get('id') or t.get('name')
        if not tid: continue
        enabled=t.get('enabled',True)
        declared=t.get('capabilities',[]) or []
        for cap in declared:
            if cap not in caps: unknown.append(f'{tid}:{cap}')
        inventory.append({
            'id':tid,
            'description':t.get('description'),
            'enabled':enabled,
            'provider_id':t.get('provider_id'),
            'capabilities':[c for c in declared if c in caps],
            'source':'host_discovery'
        })
        if enabled:
            for cap in declared:
                if cap not in caps: continue
                bindings.append({
                    'capability':cap,
                    'provider_id':t.get('provider_id'),
                    'provider_action':t.get('provider_action') or tid,
                    'connection_ref':t.get('connection_ref') or f'host:{tid}',
                    'permissions':t.get('permissions',[]),
                    'limitations':t.get('limitations',[]),
                    'coverage':t.get('coverage'),
                    'reliability':t.get('reliability'),
                    'freshness':t.get('freshness'),
                    'enabled':True
                })
    if unknown:
        raise ValueError('Unknown capability mapping(s): '+', '.join(unknown))

    inv_path=env/'tool-inventory.json';bindings_path=env/'capability-bindings.json';host_path=env/'host-tools.json'
    previous_inventory=_load(inv_path,{'tools':[]}).get('tools',[]) if inv_path.exists() else []
    previous_bindings=_load(bindings_path,{'bindings':[]}).get('bindings',[]) if bindings_path.exists() else []
    previous_host=_load(host_path,{'tools':[]}) if host_path.exists() else {'tools':[]}
    old_host_refs=_host_connection_refs(previous_host)

    # Host refresh owns only host-discovery entries. Preserve optional local packs,
    # connected-provider bindings, and other non-host environment state.
    preserved_inventory=[row for row in previous_inventory if row.get('source')!='host_discovery']
    preserved_bindings=[row for row in previous_bindings if row.get('connection_ref') not in old_host_refs]

    host_path.write_text(json.dumps(data,indent=2)+'\n')
    inv_path.write_text(json.dumps({'tools':[ *preserved_inventory, *inventory ]},indent=2)+'\n')
    bindings_path.write_text(json.dumps({'bindings':[ *preserved_bindings, *bindings ]},indent=2)+'\n')
    pref=environment_file(environment,'provider-preferences.json',writable=True)
    if not pref.exists(): pref.write_text(json.dumps({'format_version':'1.0','preferences':[]},indent=2)+'\n')
    sched=environment_file(environment,'scheduler-bindings.json',writable=True)
    if not sched.exists(): sched.write_text(json.dumps({'format_version':'1.0','bindings':[]},indent=2)+'\n')
    profile={'format_version':'1.0','environment':environment,'host_id':host_id or data.get('host_id'),'host_name':host_name or data.get('host_name'),'discovery_status':'completed','discovered_at':_now(),'tool_count':len(inventory),'binding_count':len(bindings),'preserved_non_host_tool_count':len(preserved_inventory),'preserved_non_host_binding_count':len(preserved_bindings)}
    (env/'host-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
    state=_load(env/'bootstrap-state.json',{'format_version':'1.0','welcome_shown':False,'host_discovery_completed':False,'last_bootstrap_at':None})
    state['host_discovery_completed']=True; state['last_bootstrap_at']=_now()
    if mark_welcome: state['welcome_shown']=True
    (env/'bootstrap-state.json').write_text(json.dumps(state,indent=2)+'\n')
    return {'environment':environment,'environment_state_root':storage_ref(env),'host':profile,'bindings':bindings,'preserved_non_host_bindings':len(preserved_bindings),'welcome_shown':state.get('welcome_shown',False)}


def main():
    p=argparse.ArgumentParser(description='Compile visible host tools into workspace-owned AURA environment state while keeping shipped product defaults immutable and preserving unrelated local/provider bindings.')
    p.add_argument('environment',nargs='?',default='local')
    p.add_argument('--manifest',help="Host-tool manifest path. Workspace-relative state refs such as runtime/host-tools.json resolve through the active workspace; use '-' for stdin.")
    p.add_argument('--host-id')
    p.add_argument('--host-name')
    p.add_argument('--mark-welcome-shown',action='store_true')
    a=p.parse_args()
    try: out=bootstrap(a.environment,a.manifest,a.host_id,a.host_name,a.mark_welcome_shown)
    except (ValueError,json.JSONDecodeError) as e: raise SystemExit(str(e))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
