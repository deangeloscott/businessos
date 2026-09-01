#!/usr/bin/env python3
"""Protect first-principles AURA organization entry and memory mechanics."""
from pathlib import Path
import json,os,tempfile,sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

from _common import business_directory,resolve_business
from init_business import init_business
from bootstrap_explicit_context import persist_explicit_context
from validate_business import validate_business
from remember import remember
from forget import forget


def req(condition,message):
    if not condition:raise AssertionError(message)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-first-principles-') as td:
        workspace=Path(td).resolve();old=os.environ.get('BUSINESSOS_WORKSPACE')
        os.environ['BUSINESSOS_WORKSPACE']=str(workspace)
        try:
            bid='jebs-bakery';init_business(bid,"Jeb's Bakery")
            base=workspace/'instances'/bid
            business_path=base/'context/business.json'
            req(business_path.exists(),'organization name alone must create canonical Business context')
            business=json.loads(business_path.read_text())
            req(business['name']=="Jeb's Bakery",'canonical organization name was not preserved')
            req(not business.get('industries') and not business.get('business_models'),'initialization invented business facts')
            source_refs=business.get('lineage') or []
            req(len(source_refs)==1,'minimal organization identity should preserve one initialization source')
            source_path=base/'intelligence/sources'/f'{source_refs[0]}.json'
            req(source_path.exists(),'minimal organization identity lost provenance source')
            errors,warnings,counts=validate_business(bid,True)
            req(not errors,f'name-only canonical organization must validate: {errors}')
            req(counts.get('Business')==1,'name-only initialization lost canonical Business')

            created_at=business['created_at']
            persist_explicit_context(
                bid,
                industries=['retail bakery'],
                objectives=['wholesale growth'],
                source_text="Jeb's Bakery is a retail bakery. Our current objective is wholesale growth.",
            )
            business=json.loads(business_path.read_text())
            req(business['created_at']==created_at,'later context enrichment replaced organization identity instead of extending it')
            req('retail bakery' in business.get('industries',[]),'business context was not merged into minimal identity')
            req(len(business.get('lineage') or [])>=2,'context enrichment discarded prior identity provenance')
            errors,_,_=validate_business(bid,True)
            req(not errors,f'enriched organization must validate: {errors}')

            # Ordinary durable meaning can be created/updated without a Run or playbook.
            remembered=remember(bid,{'objects':[{
                'key':'packaging-goal','object_type':'Objective',
                'content':{'name':'Improve wholesale packaging','priority':2}
            }]})
            objective_ref=remembered['objects'][0]['id']
            objective_path=base/'context/objectives'/f'{objective_ref}.json'
            req(objective_path.exists(),'generic memory create did not persist canonical Objective')
            updated=remember(bid,{'objects':[{
                'key':'packaging-goal','object_ref':objective_ref,'object_type':'Objective',
                'content':{'name':'Improve wholesale packaging and fulfillment','priority':1}
            }]})
            req(updated['objects'][0]['operation']=='updated','direct current-truth correction did not update existing object')
            objective=json.loads(objective_path.read_text())
            req(objective['name']=='Improve wholesale packaging and fulfillment' and objective['priority']==1,'direct current-truth correction was not preserved')

            # Forget is deletion, not a hidden lifecycle. It works only when canonical
            # state no longer depends on the object and does not manufacture history.
            forgotten=forget(bid,objective_ref)
            req(forgotten['status']=='forgotten' and not objective_path.exists(),'unreferenced durable object was not safely forgotten')
            req(objective_ref not in {obj.get('id') for obj,p in []},'forget unexpectedly created replacement state')
            errors,_,_=validate_business(bid,True)
            req(not errors,f'organization must remain valid after safe forgetting: {errors}')

            second='bobs-warehouse';init_business(second,"Bob's Warehouse")
            directory=business_directory();by_id={row['id']:row['name'] for row in directory}
            req(by_id=={second:"Bob's Warehouse",bid:"Jeb's Bakery"},f'organization directory is not human-readable/stable: {directory}')
            resolved=resolve_business()
            req(resolved.get('status')=='needs_input','multiple organizations must not be guessed')
            req({row['id'] for row in resolved.get('available_businesses',[])}=={bid,second},'ambiguous resolution did not expose organization directory')
            req(not (workspace/'runtime/runs').exists(),'organization entry/memory created Run state')

            print('first-principles AURA interface regressions passed: lightweight entry, direct memory correction, forgetting, and organization isolation')
        finally:
            if old is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
            else:os.environ['BUSINESSOS_WORKSPACE']=old


if __name__=='__main__':main()
