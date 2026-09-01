#!/usr/bin/env python3
from _common import *
import argparse,json


def status():
    root=workspace_root(); profile=workspace_profile(); directory=business_directory(); businesses=[row['id'] for row in directory]
    source=workspace_selection_source()
    source_detail='BUSINESSOS_WORKSPACE' if source=='environment' else (str(workspace_config_path()) if source=='local_link' else 'product root default')
    return {
        'product_root':str(PRODUCT_ROOT),
        'workspace_root':str(root),
        'external_state':workspace_is_external(),
        'workspace_config_source':source,
        'workspace_config_detail':source_detail,
        'profile':profile.get('profile','simple'),
        'knowledge_enabled':profile.get('knowledge_enabled',True),
        'instances_root':str(instances_root()),
        'runtime_root':str(runtime_root()),
        'knowledge_root':str(knowledge_root()),
        'attachments_root':str(attachments_root()),
        'businesses':businesses,
        'business_directory':directory,
    }


def main():
    p=argparse.ArgumentParser();p.add_argument('--json',action='store_true');a=p.parse_args();r=status()
    if a.json: print(json.dumps(r,indent=2,ensure_ascii=False));return
    print(f"product_root={r['product_root']}")
    print(f"workspace_root={r['workspace_root']}")
    print(f"selection={r['workspace_config_source']} ({r['workspace_config_detail']})")
    print(f"external_state={str(r['external_state']).lower()} profile={r['profile']} knowledge={str(r['knowledge_enabled']).lower()}")
    if r['business_directory']:
        print('businesses='+', '.join(f"{row['name']} ({row['id']})" for row in r['business_directory']))
    else:
        print('businesses=(none)')

if __name__=='__main__':main()
