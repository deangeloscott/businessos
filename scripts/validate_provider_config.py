#!/usr/bin/env python3
from _common import *
import json
from jsonschema import Draft202012Validator


def _load(path):
    return json.loads(path.read_text())


def _schema(name):
    return _load(ROOT/'core/schemas/runtime'/name)


def provider_config_errors():
    errors=[]
    cap_path=ROOT/'core/capabilities/catalog.json'
    reg_path=ROOT/'core/providers/registry.json'
    pub_path=ROOT/'PUBLISHER.json'
    caps={x['id'] for x in _load(cap_path).get('capabilities',[])}
    reg=_load(reg_path)
    for e in Draft202012Validator(_schema('provider-registry.schema.json')).iter_errors(reg):
        errors.append(f'{reg_path.relative_to(ROOT)}: {e.message}')
    pub=_load(pub_path)
    for e in Draft202012Validator(_schema('publisher-metadata.schema.json')).iter_errors(pub):
        errors.append(f'{pub_path.relative_to(ROOT)}: {e.message}')
    companion_path=ROOT/'core/providers/viraltrac/companion-profile.json'
    if companion_path.exists():
        companion=_load(companion_path)
        for e in Draft202012Validator(_schema('provider-companion-profile.schema.json')).iter_errors(companion):
            errors.append(f'{companion_path.relative_to(ROOT)}: {e.message}')
        for row in companion.get('capability_mappings',[]):
            cap=row.get('businessos_capability')
            if cap not in caps: errors.append(f'{companion_path.relative_to(ROOT)}: unknown BusinessOS capability {cap}')
    event_interop_path=ROOT/'core/providers/viraltrac/event-interoperability.json'
    if event_interop_path.exists():
        event_interop=_load(event_interop_path)
        for e in Draft202012Validator(_schema('provider-event-interoperability.schema.json')).iter_errors(event_interop):
            errors.append(f'{event_interop_path.relative_to(ROOT)}: {e.message}')
    root_publisher_id=pub.get('publisher',{}).get('id')
    providers={}
    for p in reg.get('providers',[]):
        pid=p.get('id')
        if pid in providers: errors.append(f'core/providers/registry.json: duplicate provider {pid}')
        providers[pid]=p
        if p.get('relationship',{}).get('type')=='first_party' and p.get('publisher_id')!=root_publisher_id:
            errors.append(f'core/providers/registry.json: first-party provider {pid} must reference root publisher {root_publisher_id}')
        for c in p.get('capabilities',[]):
            if c not in caps: errors.append(f'core/providers/registry.json: provider {pid} references unknown capability {c}')
    pref_paths=[ROOT/'distribution/provider-defaults.json']
    envroot=ROOT/'deployment/environments'
    if envroot.exists(): pref_paths += sorted(envroot.glob('*/provider-preferences.json'))
    instroot=ROOT/'instances'
    if instroot.exists(): pref_paths += sorted(instroot.glob('*/config/provider-preferences.json'))
    pschema=_schema('provider-preferences.schema.json')
    for path in pref_paths:
        if not path.exists(): continue
        data=_load(path)
        for e in Draft202012Validator(pschema).iter_errors(data): errors.append(f'{path.relative_to(ROOT)}: {e.message}')
        seen=set()
        for pref in data.get('preferences',[]):
            key=(pref.get('capability'),pref.get('provider_id'))
            if key in seen: errors.append(f'{path.relative_to(ROOT)}: duplicate preference {key}')
            seen.add(key)
            cap=pref.get('capability'); pid=pref.get('provider_id')
            if cap not in caps: errors.append(f'{path.relative_to(ROOT)}: unknown capability {cap}')
            if pid not in providers: errors.append(f'{path.relative_to(ROOT)}: unknown provider {pid}')
            elif cap not in providers[pid].get('capabilities',[]): errors.append(f'{path.relative_to(ROOT)}: provider {pid} does not supply {cap}')
    return errors


def main():
    errors=provider_config_errors()
    print(f'Provider configuration errors: {len(errors)}')
    for e in errors: print('ERROR',e)
    if errors: raise SystemExit(1)

if __name__=='__main__': main()
