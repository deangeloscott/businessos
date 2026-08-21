#!/usr/bin/env python3
from _common import *
import argparse,json
from jsonschema import Draft202012Validator
p=argparse.ArgumentParser();p.add_argument('schema_title');p.add_argument('object_path');a=p.parse_args()
sreg=json.loads((ROOT/'generated/schema-registry.json').read_text());m=next((x for x in sreg if x.get('title')==a.schema_title),None)
if not m: raise SystemExit('Unknown schema title')
schema=json.loads((ROOT/m['path']).read_text());obj=json.loads(Path(a.object_path).read_text());errs=sorted(Draft202012Validator(schema).iter_errors(obj),key=lambda e:list(e.path))
for e in errs: print('ERROR',list(e.path),e.message)
if errs: raise SystemExit(1)
print('valid')
