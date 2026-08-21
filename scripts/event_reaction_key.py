#!/usr/bin/env python3
import argparse, hashlib, json

def key(parts):
    payload=json.dumps(parts,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def main():
    p=argparse.ArgumentParser(description='Create a deterministic BusinessOS event-reaction idempotency key from authoritative event/reaction identity.')
    p.add_argument('--business-id',required=True)
    p.add_argument('--provider-id',required=True)
    p.add_argument('--event-id',required=True)
    p.add_argument('--subscription-ref',default='')
    p.add_argument('--evaluation-version',default='')
    p.add_argument('--reaction-scope',default='core.monitoring.react-to-business-event')
    a=p.parse_args()
    parts={'business_id':a.business_id,'provider_id':a.provider_id,'event_id':a.event_id,'subscription_ref':a.subscription_ref or None,'evaluation_version':a.evaluation_version or None,'reaction_scope':a.reaction_scope}
    print(json.dumps({'idempotency_key':key(parts),'identity':parts},indent=2))
if __name__=='__main__': main()
