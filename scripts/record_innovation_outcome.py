#!/usr/bin/env python3
"""Attach a real local OutcomeEvaluation to imported innovation support state."""
from _common import *
from innovation_common import validate_schema,iter_innovation_entries
import argparse,json,hashlib,os


def _write(path,obj):
    temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(obj,indent=2)+'\n');os.replace(temporary,path)


def record_outcome(business_id,entry_id,outcome,evidence_ref):
    if outcome not in {'supported','contradicted','neutral'}:raise ValueError('Outcome must be supported, contradicted, or neutral')
    index=object_index(business_id)
    if evidence_ref not in index or index[evidence_ref][0].get('object_type')!='OutcomeEvaluation':raise ValueError('Local innovation evidence must cite an existing OutcomeEvaluation from the active organization')
    entry=None;entry_path=None
    for candidate,path in iter_innovation_entries(business_id):
        if candidate.get('id')==entry_id:entry=candidate;entry_path=path;break
    if not entry:raise ValueError(f'Unknown innovation exchange entry: {entry_id}')
    local=entry['local_evidence'];event_key=hashlib.sha256(f'{entry_id}|{outcome}|{evidence_ref}'.encode()).hexdigest()
    if event_key not in [event.get('event_key') for event in local.get('outcome_events',[])]:
        local['outcome_events'].append({'event_key':event_key,'outcome':outcome,'evidence_ref':evidence_ref,'recorded_at':now()});local[f'{outcome}_count']+=1
    entry['updated_at']=now();entry['last_activity_at']=entry['updated_at'];validate_schema('InnovationExchangeEntry',entry);_write(entry_path,entry);return entry


def main():
    parser=argparse.ArgumentParser(description='Record an organization OutcomeEvaluation as local evidence about an imported innovation. This updates support evidence only; it does not create an Insight or auto-adopt the method.');parser.add_argument('business_id');parser.add_argument('entry_id');parser.add_argument('--outcome',required=True,choices=['supported','contradicted','neutral']);parser.add_argument('--evidence-ref',required=True);args=parser.parse_args()
    try:entry=record_outcome(args.business_id,args.entry_id,args.outcome,args.evidence_ref)
    except ValueError as exc:raise SystemExit(str(exc))
    print(json.dumps({'exchange_entry_id':entry['id'],'local_evidence':entry['local_evidence']},indent=2))

if __name__=='__main__':main()
