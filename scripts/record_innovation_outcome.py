#!/usr/bin/env python3
from _common import *
from innovation_common import validate_schema
import argparse,json,hashlib,os

def _write(path,obj):
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');os.replace(tmp,path)

def record_outcome(business_id,entry_id,outcome,evidence_ref):
    if outcome not in {'supported','contradicted','neutral'}:raise ValueError('Outcome must be supported, contradicted, or neutral')
    idx=object_index(business_id)
    if evidence_ref not in idx or idx[evidence_ref][0].get('object_type')!='OutcomeEvaluation':raise ValueError('Community replication outcomes must cite an existing OutcomeEvaluation from the active business')
    entry=None;epath=None
    for obj,p in iter_instance_objects(business_id):
        if obj.get('object_type')=='InnovationExchangeEntry' and obj.get('id')==entry_id:entry=obj;epath=p;break
    if not entry:raise ValueError(f'Unknown InnovationExchangeEntry: {entry_id}')
    local=entry['local_evidence'];key=hashlib.sha256(f'{entry_id}|{outcome}|{evidence_ref}'.encode()).hexdigest()
    if key not in [x.get('event_key') for x in local.get('outcome_events',[])]:local['outcome_events'].append({'event_key':key,'outcome':outcome,'evidence_ref':evidence_ref,'recorded_at':now()});local[f'{outcome}_count']+=1
    entry['updated_at']=now();entry['last_activity_at']=entry['updated_at'];validate_schema('InnovationExchangeEntry',entry);_write(epath,entry);insight_ref=entry.get('insight_ref')
    if insight_ref and insight_ref in idx:
        insight,ipath=idx[insight_ref];rel={'supported':'supports','contradicted':'contradicts','neutral':'contextualizes'}[outcome]
        if evidence_ref not in [x.get('ref') for x in insight.get('evidence_links',[])]:insight.setdefault('evidence_links',[]).append({'ref':evidence_ref,'relationship':rel,'weight':None,'reason':'Active-business OutcomeEvaluation recorded as a local test of an imported BusinessOS innovation.'})
        insight['updated_at']=now();ext=insight.setdefault('extensions',{}).setdefault('community_evidence',{});ext['local_outcomes']={'supported':local['supported_count'],'contradicted':local['contradicted_count'],'neutral':local['neutral_count']};validate_schema('Insight',insight);_write(Path(ipath),insight)
    return entry

def main():
    ap=argparse.ArgumentParser(description='Record an active-business OutcomeEvaluation as local evidence for a community innovation.');ap.add_argument('business_id');ap.add_argument('entry_id');ap.add_argument('--outcome',required=True,choices=['supported','contradicted','neutral']);ap.add_argument('--evidence-ref',required=True);a=ap.parse_args()
    try:entry=record_outcome(a.business_id,a.entry_id,a.outcome,a.evidence_ref)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps({'exchange_entry_id':entry['id'],'local_evidence':entry['local_evidence']},indent=2))
if __name__=='__main__':main()
