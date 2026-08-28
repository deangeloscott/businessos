#!/usr/bin/env python3
from _common import *
import argparse,json
p=argparse.ArgumentParser();p.add_argument('environment');p.add_argument('--business');a=p.parse_args()
if not environment_exists(a.environment): raise SystemExit('Unknown environment')
cat={x['id'] for x in json.loads((ROOT/'core/capabilities/catalog.json').read_text())['capabilities']}
bp=environment_file(a.environment,'capability-bindings.json')
binds=json.loads(bp.read_text()).get('bindings',[]) if bp.exists() else []
out={c:{'status':'unavailable'} for c in cat}
for b in binds:
 c=b.get('capability')
 if c in out and b.get('enabled',True): out[c]={'status':'available','binding':b}
print(json.dumps({'environment':a.environment,'business_id':a.business,'capabilities':out},indent=2))
