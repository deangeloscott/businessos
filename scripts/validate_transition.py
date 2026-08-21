#!/usr/bin/env python3
from _common import *
import argparse,json
p=argparse.ArgumentParser();p.add_argument('object_type');p.add_argument('from_state');p.add_argument('to_state');a=p.parse_args()
m=json.loads((ROOT/'core/references/state-machines.json').read_text())
if a.object_type not in m: raise SystemExit('Unknown state machine')
allowed=m[a.object_type]['transitions'].get(a.from_state,[])
if a.to_state not in allowed: raise SystemExit(f'Invalid transition {a.object_type}: {a.from_state} -> {a.to_state}; allowed={allowed}')
print('valid')
