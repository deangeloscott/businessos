#!/usr/bin/env python3
from _common import *

def isolation_errors():
    errors=[];index={}
    for inst in (ROOT/'instances').iterdir():
        if not inst.is_dir() or inst.name.startswith('_'):continue
        for obj,p in iter_instance_objects(inst.name):index[obj['id']]=(inst.name,obj,p)
    for oid,(bid,obj,p) in index.items():
        for ref in refs_in_object(obj):
            if ref in index and index[ref][0]!=bid:errors.append(f'{p}: cross-business ref {ref} -> {index[ref][0]}')
    return errors,index

def main():
    errors,index=isolation_errors()
    if errors:print('\n'.join(errors));raise SystemExit(1)
    print(f'isolation valid across {len(index)} indexed objects')
if __name__=='__main__':main()
