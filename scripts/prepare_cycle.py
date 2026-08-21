#!/usr/bin/env python3
from _common import *
import argparse,json
p=argparse.ArgumentParser();p.add_argument('cadence',choices=['daily','weekly','monthly','quarterly']);p.add_argument('--owner');a=p.parse_args()
idx=json.loads((ROOT/'generated/schedule-index.json').read_text())
rows=[x for x in idx if x.get('default')==a.cadence and (not a.owner or x.get('owner_system')==a.owner)]
print(json.dumps({'cadence':a.cadence,'contracts':rows},indent=2))
