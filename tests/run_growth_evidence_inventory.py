#!/usr/bin/env python3
"""Regression: broad-growth evidence inventory informs judgment without becoming a semantic gate."""
from pathlib import Path
import json, os, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts'


def req(cond,msg):
    if not cond: raise AssertionError(msg)


def run(args,env,check=True):
    p=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,env=env,capture_output=True,text=True)
    if check and p.returncode!=0:
        raise AssertionError(f'command failed: {args}\nstdout={p.stdout}\nstderr={p.stderr}')
    return p


def inventory(bid,workspace,env):
    p=run([S/'growth_baseline_gate.py',bid],env)
    return json.loads(p.stdout)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-growth-inventory-') as td:
        ws=Path(td).resolve(); env=os.environ.copy(); env['BUSINESSOS_WORKSPACE']=str(ws)
        bid='growth-inventory'
        run([S/'init_business.py',bid,'--name','Growth Inventory'],env)

        # Missing structured metric/economic objects is a representation fact, not a stop signal.
        empty=inventory(bid,ws,env)
        req(empty.get('status')=='evidence_inventory_ready',f'inventory should always return advisory context: {empty}')
        req(empty.get('mode')=='advisory_evidence_inventory','inventory must identify itself as advisory')
        req(empty.get('hard_gate') is False,'growth inventory must not be a deterministic permission gate')
        req(empty.get('decision_authority')=='model_or_human','semantic evidence sufficiency belongs to capable intelligence')
        req(empty.get('structured_baseline_state')=='not_recorded','new business should report structured baseline as not recorded')
        req('baseline_required' not in json.dumps(empty),'legacy hard-gate outcome must not survive in normal output')
        req('does not establish that usable first-party evidence is absent' in empty.get('reason',''),'absence of structured types must not be equated with no usable evidence')

        # Rich first-party evidence represented as Sources/Observations remains visible even
        # when the dedicated metric/economic object types are absent.
        inst=ws/'instances'/bid
        evidence_dir=inst/'intelligence'/'evidence'; evidence_dir.mkdir(parents=True,exist_ok=True)
        (evidence_dir/'src_first_party.json').write_text(json.dumps({
            'id':'src_growth_first_party','object_type':'SourceRecord','business_id':bid,
            'source_type':'first_party_export','title':'Funnel export','extensions':{}
        },indent=2)+'\n')
        (evidence_dir/'obs_funnel.json').write_text(json.dumps({
            'id':'obs_growth_funnel','object_type':'Observation','business_id':bid,
            'statement':'The supplied funnel export contains conversion-stage counts.','source_refs':['src_growth_first_party'],'extensions':{}
        },indent=2)+'\n')
        observed=inventory(bid,ws,env)
        req(observed.get('structured_baseline_state')=='not_recorded','Source/Observation evidence must not be mislabeled as dedicated metric objects')
        req(observed.get('related_evidence_counts',{}).get('SourceRecord',0)>=1,'inventory should surface recorded Source evidence')
        req(observed.get('related_evidence_counts',{}).get('Observation',0)>=1,'inventory should surface recorded Observation evidence')
        req(observed.get('hard_gate') is False,'rich alternate evidence representation still must not trigger a hard gate')

        # Adding a structured metric changes only the inventory state, not who decides sufficiency.
        metrics=inst/'metrics'; metrics.mkdir(parents=True,exist_ok=True)
        (metrics/'metric_conversion.json').write_text(json.dumps({
            'id':'met_growth_conversion','object_type':'MetricObservation','business_id':bid,
            'metric_name':'demo_booking_rate','value':0.02,'extensions':{}
        },indent=2)+'\n')
        structured=inventory(bid,ws,env)
        req(structured.get('structured_baseline_state')=='present','structured metric should be inventoried as present')
        req(structured.get('structured_baseline_counts',{}).get('MetricObservation')==1,'metric count should be exact')
        req(structured.get('decision_authority')=='model_or_human' and structured.get('hard_gate') is False,'structured evidence presence still must not become deterministic semantic sufficiency')

        # Product source remains untouched by the external-workspace regression.
        req(not (ROOT/'instances'/bid).exists(),'growth inventory regression leaked business state into product instances/')

    print('growth evidence inventory regressions passed: structured state informs judgment without becoming a permission-to-act gate')


if __name__=='__main__': main()
