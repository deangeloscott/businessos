#!/usr/bin/env python3
from _common import *
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from jsonschema import Draft202012Validator

PROVIDER_ID='viraltrac'
PROFILE=ROOT/'core/providers/viraltrac/companion-profile.json'
SNAPSHOT_SCHEMA=ROOT/'core/schemas/runtime/provider-capability-snapshot.schema.json'


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')


def load_json_source(path):
    if path == '-':
        raw=sys.stdin.read().encode('utf-8')
    else:
        raw=resolve_storage_ref(path).read_bytes()
    return raw, json.loads(raw.decode('utf-8'))


def flatten_strings(value):
    out=[]
    def walk(v):
        if isinstance(v,dict):
            for k,x in v.items():
                out.append(str(k)); walk(x)
        elif isinstance(v,list):
            for x in v: walk(x)
        elif v is not None:
            out.append(str(v))
    walk(value)
    return out


def explicit_capabilities(data):
    vals=[]
    if isinstance(data,dict):
        for key in ('businessos_capabilities','business_os_capabilities'):
            x=data.get(key)
            if isinstance(x,list): vals.extend(str(v) for v in x)
    return set(vals)


def sync(environment, manifest_path, connection_ref='provider:viraltrac', source_kind='auto', allow_preview=False):
    if not environment_exists(environment): raise ValueError(f'Unknown environment: {environment}')
    profile=json.loads(PROFILE.read_text())
    catalog={x['id'] for x in json.loads((ROOT/'core/capabilities/catalog.json').read_text()).get('capabilities',[])}
    raw,data=load_json_source(manifest_path)
    haystack='\n'.join(flatten_strings(data)).lower()
    explicit=explicit_capabilities(data)
    unknown=sorted(explicit-catalog)
    if unknown: raise ValueError('Descriptor declares unknown BusinessOS capability(s): '+', '.join(unknown))

    snapshot_rows=[]; new_bindings=[]
    for row in profile['capability_mappings']:
        cap=row['businessos_capability']
        if cap not in catalog: raise ValueError(f'Companion profile references unknown capability: {cap}')
        matches=[s for s in row['signals_any'] if s.lower() in haystack]
        detected=(cap in explicit) or bool(matches)
        if not detected:
            status='not_detected'
        elif row['auto_bind'] or allow_preview:
            status='bound'
            new_bindings.append({
                'capability':cap,
                'provider_id':PROVIDER_ID,
                'provider_action':row['provider_action'],
                'connection_ref':connection_ref,
                'permissions':[],
                'limitations':row.get('limits',[]),
                'coverage':'discovered_from_provider_descriptor',
                'reliability':None,
                'freshness':utc_now(),
                'enabled':True
            })
        else:
            status='candidate'
        snapshot_rows.append({
            'capability':cap,
            'status':status,
            'provider_action':row['provider_action'],
            'matched_signals':sorted(set(matches + ([f'explicit:{cap}'] if cap in explicit else []))),
            'auto_bind':row['auto_bind'],
            'notes':'; '.join(row.get('limits',[])) or None
        })

    snap={
        'format_version':'1.0','provider_id':PROVIDER_ID,'environment':environment,
        'connection_ref':connection_ref,'discovered_at':utc_now(),'source_kind':source_kind,
        'source_sha256':hashlib.sha256(raw).hexdigest(),'capabilities':snapshot_rows
    }
    errors=list(Draft202012Validator(json.loads(SNAPSHOT_SCHEMA.read_text())).iter_errors(snap))
    if errors: raise ValueError('Invalid provider snapshot: '+'; '.join(e.message for e in errors))

    sp=environment_file(environment,'providers/viraltrac-capabilities.json',writable=True,seed_product_default=False)
    sp.parent.mkdir(parents=True,exist_ok=True); sp.write_text(json.dumps(snap,indent=2)+'\n')

    bp=environment_file(environment,'capability-bindings.json',writable=True)
    bindings=json.loads(bp.read_text()).get('bindings',[]) if bp.exists() else []
    auto_mapped_caps={row['businessos_capability'] for row in profile['capability_mappings'] if row.get('auto_bind') or allow_preview}
    kept=[b for b in bindings if not (b.get('provider_id')==PROVIDER_ID and b.get('connection_ref')==connection_ref and b.get('capability') in auto_mapped_caps)]
    merged=kept+new_bindings
    bp.write_text(json.dumps({'bindings':merged},indent=2)+'\n')
    return {
        'provider_id':PROVIDER_ID,'environment':environment,'connection_ref':connection_ref,
        'bound_capabilities':[b['capability'] for b in new_bindings],
        'candidate_capabilities':[r['capability'] for r in snapshot_rows if r['status']=='candidate'],
        'not_detected':[r['capability'] for r in snapshot_rows if r['status']=='not_detected'],
        'snapshot':storage_ref(sp)
    }


def main():
    p=argparse.ArgumentParser(description="Synchronize non-secret ViralTrac capability discovery into workspace-owned AURA environment bindings. The harness retrieves the authenticated descriptor; this helper does not store credentials or require network access.")
    p.add_argument('environment',nargs='?',default='local')
    p.add_argument('--manifest',required=True,help="JSON from ViralTrac capability discovery/external-harness/MCP tooling, workspace-relative state ref, or '-' for stdin")
    p.add_argument('--connection-ref',default='provider:viraltrac')
    p.add_argument('--source-kind',default='auto')
    p.add_argument('--allow-preview',action='store_true',help='Also bind mappings marked candidate/preview-only. Use only after explicit operational/readiness verification.')
    a=p.parse_args()
    try: out=sync(a.environment,a.manifest,a.connection_ref,a.source_kind,a.allow_preview)
    except (ValueError,json.JSONDecodeError) as e: raise SystemExit(str(e))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
