#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'qualification'))
from build_suite import build

def req(c,m):
    if not c: raise AssertionError(m)

def main():
    suite=build(); manifest=json.loads((ROOT/'SYSTEM-MANIFEST.json').read_text())
    expected=manifest.get('counts',{}).get('contract_count') or manifest.get('contract_count'); expected_caps=manifest.get('capability_count')
    req(suite['contract_count']==expected,f"qualification coverage {suite['contract_count']} != manifest {expected}")
    ids=[t['contract_id'] for t in suite['contract_tests']]; req(suite['capability_count']==expected_caps,f"qualification capability coverage {suite['capability_count']} != manifest {expected_caps}")
    req(len(suite['capability_coverage'])==expected_caps,'every declared capability needs a qualification mapping')
    req(len(ids)==len(set(ids)),'duplicate contract qualification tests')
    req(all(not t['unknown_required_subcontracts'] for t in suite['contract_tests']),'unknown required subcontracts in qualification suite')
    req(all(t['hard_gates'] and t['rubric_dimensions'] and t['candidate_task'] for t in suite['contract_tests']),'every contract needs gates, rubric, and candidate task')
    customer=[t for t in suite['contract_tests'] if t.get('artifact_role')=='customer_facing_production_root']
    req(customer,'expected customer-facing production contracts')
    req(all(t['output_policy']['artifact_required'] and 'actual_artifact_exists' in t['hard_gates'] for t in customer),'customer-facing roots must require actual artifacts')
    owners={m['owner_system'] for m in suite['domain_missions']}; required={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}
    req(owners==required,f'domain mission coverage mismatch: {owners ^ required}')
    req(len(suite['cross_domain_missions'])>=5,'cross-domain mission coverage too small')
    req(len(suite['marathon_missions'])>=2,'marathon mission coverage too small')
    req(len(suite.get('concurrency_missions',[]))>=4,'concurrency mission coverage too small')
    live=[t for t in suite['contract_tests'] if t['competitive_profile']=='search_live_field']; req(live,'SEO/AEO live-field tests missing')
    ads=[t for t in suite['contract_tests'] if t['competitive_profile']=='paid_and_persuasion_field']; req(ads,'competitive marketing tests missing')
    print(f"qualification framework regressions passed: {suite['contract_count']} contract tests, {suite['capability_count']} capability mappings, {len(suite['domain_missions'])} domain missions, {len(suite['cross_domain_missions'])} cross-domain missions, {len(suite['marathon_missions'])} marathon missions, {len(suite.get('concurrency_missions',[]))} concurrency missions")
if __name__=='__main__': main()
