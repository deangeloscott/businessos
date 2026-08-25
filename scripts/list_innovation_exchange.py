#!/usr/bin/env python3
from _common import *
import argparse,json

def list_entries(business_id,owner_system=None,status=None,compatible_only=False):
    rows=[]
    for obj,p in iter_instance_objects(business_id):
        if obj.get('object_type')!='InnovationExchangeEntry':continue
        if owner_system and obj.get('owner_system')!=owner_system:continue
        if status and obj.get('status')!=status:continue
        if compatible_only and obj.get('compatibility_status')!='compatible':continue
        rep=obj.get('reported_evidence') or {};loc=obj.get('local_evidence') or {};rows.append({'id':obj['id'],'title':obj['title'],'owner_system':obj['owner_system'],'status':obj['status'],'compatibility_status':obj['compatibility_status'],'contributions':rep.get('contribution_count',0),'reported_supported':rep.get('reported_supported_count',0),'reported_contradicted':rep.get('reported_contradicted_count',0),'local_supported':loc.get('supported_count',0),'local_contradicted':loc.get('contradicted_count',0),'last_activity_at':obj.get('last_activity_at')})
    rows.sort(key=lambda x:(x['local_supported']-x['local_contradicted'],x['contributions'],x.get('last_activity_at') or ''),reverse=True);return rows

def main():
    ap=argparse.ArgumentParser(description='List/search the active business local Innovation Exchange feed.');ap.add_argument('business_id');ap.add_argument('--owner-system');ap.add_argument('--status');ap.add_argument('--compatible-only',action='store_true');a=ap.parse_args();print(json.dumps(list_entries(a.business_id,a.owner_system,a.status,a.compatible_only),indent=2))
if __name__=='__main__':main()
