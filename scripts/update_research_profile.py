#!/usr/bin/env python3
from _common import *
import argparse, json
from jsonschema import Draft202012Validator
BUSINESS_FIELDS=('name','organization','email','phone','location','website')
OPERATOR_FIELDS=('name','email','phone','location')
def validate_file(data,schema_path):
    schema=json.loads(schema_path.read_text()); errs=sorted(Draft202012Validator(schema).iter_errors(data),key=lambda e:list(e.path))
    if errs: raise ValueError('; '.join((('/'.join(map(str,e.path)) or '<root>')+': '+e.message) for e in errs[:10]))
def supplied(args,fields): return {f:getattr(args,f) for f in fields if getattr(args,f) is not None}
def update_business(business_id,vals):
    path=ROOT/'instances'/business_id/'config/external-research-profile.json'
    if not path.exists(): raise ValueError('Unknown business or missing research profile')
    data=json.loads(path.read_text()); ident=data.setdefault('identity',{})
    for k,v in vals.items(): ident[k]=v
    validate_file(data,ROOT/'core/schemas/runtime/external-research-profile.schema.json'); path.write_text(json.dumps(data,indent=2)+'\n'); return path
def update_operator(vals):
    path=ROOT/'deployment/operator-profile.json'
    if not path.exists(): raise ValueError('Missing deployment/operator-profile.json')
    data=json.loads(path.read_text()); ident=data.setdefault('identity',{}); reuse=set(data.get('reuse_across_businesses') or [])
    for k,v in vals.items(): ident[k]=v; reuse.add(k)
    data['reuse_across_businesses']=sorted(reuse)
    validate_file(data,ROOT/'core/schemas/runtime/operator-profile.schema.json'); path.write_text(json.dumps(data,indent=2)+'\n'); return path
def main():
    p=argparse.ArgumentParser(); p.add_argument('business_id'); p.add_argument('--scope',choices=['business','operator'],default='business')
    for f in BUSINESS_FIELDS: p.add_argument('--'+f)
    a=p.parse_args(); vals=supplied(a,BUSINESS_FIELDS)
    if not vals: raise SystemExit('Provide at least one identity field')
    try:
        if a.scope=='operator':
            invalid=sorted(set(vals)-set(OPERATOR_FIELDS))
            if invalid: raise ValueError('Operator scope cannot store brand-specific field(s): '+', '.join(invalid))
            path=update_operator(vals)
        else: path=update_business(a.business_id,vals)
    except ValueError as e: raise SystemExit(str(e))
    print(path)
if __name__=='__main__': main()
