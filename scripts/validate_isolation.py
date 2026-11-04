#!/usr/bin/env python3
from _common import *

def isolation_errors(business_id=None):
    errors=[];index={};owners={}
    for inst in (ROOT/'instances').iterdir():
        if not inst.is_dir() or inst.name.startswith('_'):continue
        for obj,p in iter_instance_objects(inst.name):
            index[(inst.name,obj['id'])]=(inst.name,obj,p)
            owners.setdefault(obj['id'],set()).add(inst.name)
    for (bid,oid),(_,obj,p) in index.items():
        if business_id is not None and bid!=business_id:continue
        for ref in refs_in_object(obj):
            if (bid,ref) not in index and ref in owners:
                errors.append(f'{p}: cross-business ref {ref} -> {", ".join(sorted(owners[ref]))}')
    return errors,index

def main():
    errors,index=isolation_errors()
    if errors:print('\n'.join(errors));raise SystemExit(1)
    print(f'isolation valid across {len(index)} indexed objects')
if __name__=='__main__':main()
