#!/usr/bin/env python3
from _common import *
import argparse,json


def status():
    root=workspace_root(); profile=workspace_profile(); businesses=[]
    ir=instances_root()
    if ir.exists():
        businesses=sorted([p.name for p in ir.iterdir() if p.is_dir() and p.name!='_template'])
    return {
        'product_root':str(PRODUCT_ROOT),
        'workspace_root':str(root),
        'external_state':workspace_is_external(),
        'workspace_config_source':str(workspace_config_path()) if workspace_config_path().exists() else ('BUSINESSOS_WORKSPACE' if os.environ.get('BUSINESSOS_WORKSPACE') else 'default_product_root'),
        'profile':profile.get('profile','simple'),
        'knowledge_enabled':profile.get('knowledge_enabled',True),
        'instances_root':str(instances_root()),
        'runtime_root':str(runtime_root()),
        'knowledge_root':str(knowledge_root()),
        'attachments_root':str(attachments_root()),
        'businesses':businesses
    }


def main():
    p=argparse.ArgumentParser();p.add_argument('--json',action='store_true');a=p.parse_args();r=status()
    if a.json: print(json.dumps(r,indent=2));return
    print(f"product_root={r['product_root']}")
    print(f"workspace_root={r['workspace_root']}")
    print(f"external_state={str(r['external_state']).lower()} profile={r['profile']} knowledge={str(r['knowledge_enabled']).lower()}")
    print(f"businesses={','.join(r['businesses']) if r['businesses'] else '(none)'}")

if __name__=='__main__':main()
