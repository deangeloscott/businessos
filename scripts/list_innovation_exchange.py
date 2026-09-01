#!/usr/bin/env python3
"""List imported organization-local InnovationPackage support state without ranking effectiveness."""
from innovation_common import iter_innovation_entries
import argparse,json


def list_entries(business_id,owner_system=None,compatible_only=False):
    rows=[]
    for entry,_ in iter_innovation_entries(business_id):
        if owner_system and entry.get('owner_system')!=owner_system:continue
        if compatible_only and entry.get('compatibility_status')!='compatible':continue
        reported=entry.get('reported_evidence') or {};local=entry.get('local_evidence') or {}
        rows.append({'id':entry['id'],'title':entry['title'],'owner_system':entry['owner_system'],'compatibility_status':entry['compatibility_status'],'contributions':reported.get('contribution_count',0),'reported_supported':reported.get('reported_supported_count',0),'reported_contradicted':reported.get('reported_contradicted_count',0),'local_supported':local.get('supported_count',0),'local_contradicted':local.get('contradicted_count',0),'last_activity_at':entry.get('last_activity_at')})
    # Freshness is a stable browse order, not a quality/effectiveness score.
    rows.sort(key=lambda row:(row.get('last_activity_at') or '',row.get('title') or ''),reverse=True);return rows


def main():
    parser=argparse.ArgumentParser(description='List imported InnovationPackage support data. Evidence counts are shown but AURA does not rank methods as better/worse from them.');parser.add_argument('business_id');parser.add_argument('--owner-system');parser.add_argument('--compatible-only',action='store_true');args=parser.parse_args();print(json.dumps(list_entries(args.business_id,args.owner_system,args.compatible_only),indent=2))

if __name__=='__main__':main()
