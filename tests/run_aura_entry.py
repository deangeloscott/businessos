#!/usr/bin/env python3
"""Focused regression for the harness-neutral AURA business-work front door."""
from pathlib import Path
import json, os, shutil, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'


def require(cond,msg):
    if not cond:raise AssertionError(msg)


def run(args,env,check=True):
    p=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,env=env,capture_output=True,text=True)
    if check and p.returncode!=0:raise AssertionError(f"command failed: {args}\nstdout={p.stdout}\nstderr={p.stderr}")
    return p


def init_business(bid,env):
    run([SCRIPTS/'init_business.py',bid,'--name',bid.replace('-',' ').title()],env)


def enter(request,bid,workspace,env,*extra):
    p=run([SCRIPTS/'enter.py',request,'--business-id',bid,'--workspace',workspace,*extra],env)
    return json.loads(p.stdout)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-entry-regression-') as td:
        ws=Path(td).resolve();env=os.environ.copy();env['BUSINESSOS_WORKSPACE']=str(ws)
        bid='entry-regression'
        init_business(bid,env)
        request='Create a presentation for this business.'
        first=enter(request,bid,ws,env)
        require(first.get('status')=='ready',f'entry should be ready: {first}')
        require(first.get('handoff_format')=='compact','ordinary CLI entry should return the compact agent handoff')
        require(first.get('business_id')==bid,'explicit business should resolve')
        require(first.get('original_request')==request,'original request must be preserved')
        require(first.get('root_contract',{}).get('contract_id')=='content.production.presentation',f'expected presentation route, got {first.get("root_contract")}')
        rid=first.get('run',{}).get('run_id');require(rid and rid.startswith('run_'),'entry should create a bounded Run')
        work=ws/'runtime/runs'/bid/rid/'work';require(work.is_dir(),'entry Run must expose workspace-owned work/')
        require(Path(first['run']['work_dir']).resolve()==work.resolve(),'returned work_dir should be the actual Run work directory')
        require(first['run'].get('resumed') is False,'first entry should create, not resume')
        require(first.get('execution_env',{}).get('BUSINESSOS_RUN_ID')==rid,'execution envelope should identify the Run')
        require('CONTEXT.md' in first.get('context',{}).get('contract_and_policy_refs',[]),'compact handoff should preserve material context references without duplicating object/schema refs')
        require(first.get('process',{}).get('entry_contract')=='content.production.presentation','process plan should use routed root contract')
        require(first.get('process',{}).get('required_subcontracts'),'compact handoff should preserve required downstream contract information')
        require('status' in first.get('capabilities',{}),'compact handoff should preserve material capability state')
        require(first.get('completion',{}).get('interface')=='scripts/finalize_run.py','compact handoff should expose the ordinary finalization interface')

        envelope_ref=first.get('execution_envelope_ref');require(envelope_ref,'compact handoff should reference the complete envelope')
        envelope_path=ws/envelope_ref;require(envelope_path.exists(),'complete execution envelope should be durable inside the Run')
        durable=json.loads(envelope_path.read_text())
        require(durable.get('original_request')==request,'durable full envelope must preserve the original request')
        require(durable.get('route',{}).get('contract_id')=='content.production.presentation','durable full envelope must preserve resolved routing')
        require(durable.get('context_plan',{}).get('run_id')==rid,'durable context plan must be bound to the Run')
        require(durable.get('process_plan',{}).get('entry_contract')=='content.production.presentation','durable process plan should use the routed root contract')
        require(len(json.dumps(first))<len(json.dumps(durable)),'ordinary handoff should be smaller than the complete durable envelope')

        sys.path.insert(0,str(SCRIPTS))
        from enter import enter as library_enter
        library=library_enter(request,bid,ws)
        require(library.get('process_plan',{}).get('entry_contract')=='content.production.presentation','programmatic enter() consumers should retain the complete envelope')
        require(library.get('execution_envelope_ref')==envelope_ref,'programmatic enter() should reference the same durable envelope artifact')

        second=enter(request,bid,ws,env,'--full')
        require(second.get('status')=='ready','repeat entry should remain ready')
        require(second.get('run',{}).get('run_id')==rid,'exact active request should resume the existing Run')
        require(second.get('run',{}).get('resumed') is True,'repeat entry should report resumed')
        require(second.get('route',{}).get('contract_id')=='content.production.presentation','--full should preserve the prior complete CLI envelope for compatibility')
        require(second.get('context_plan',{}).get('run_id')==rid,'--full should expose the complete context plan')

        third=enter(request,bid,ws,env,'--new-run')
        require(third.get('run',{}).get('run_id')!=rid,'--new-run should force a distinct Run')
        require(third.get('run',{}).get('resumed') is False,'forced new Run should not report resumed')

        # The high-level finalizer should resolve exact Run-labelled evidence, bind provenance,
        # validate the active business, complete the root, and refresh human knowledge without
        # requiring the caller to sequence low-level completion helpers.
        detector=enter('Check whether our website has an indexing problem.',bid,ws,env)
        drid=detector['run']['run_id'];ddir=ws/'runtime/runs'/bid/drid
        inspected=ddir/'artifacts'/'index-inspection.txt';inspected.write_text('Deterministic fixture inspection found no supplied indexable pages to evaluate.\n')
        nofinding=ddir/'artifacts'/'indexing-no-finding.json'
        nofinding.write_text(json.dumps({
            'contract_id':'seo.diagnosis.detectors.indexing','status':'completed','result':'no_finding',
            'checks_performed':[{'check':'bounded indexing-state inspection','status':'pass'}],
            'evidence_refs':[f'runtime/runs/{bid}/{drid}/artifacts/index-inspection.txt']
        },indent=2)+'\n')
        finalized=run([SCRIPTS/'finalize_run.py',bid,drid,'--workspace',ws],env)
        final=json.loads(finalized.stdout)
        require(final.get('status')=='completed' and final.get('category')=='mechanically_repaired',f'ordinary finalization failed: {final}')
        require(final.get('validation',{}).get('status')=='clean','finalizer should aggregate the green business validation')
        require(final.get('root_evidence_refs')==[f'runtime/runs/{bid}/{drid}/artifacts/indexing-no-finding.json'],'finalizer should normalize exact workspace-relative root evidence')
        require(json.loads((ddir/'run.json').read_text()).get('status')=='completed','finalizer should complete the Run')
        require((ws/'knowledge'/bid/'_generated'/'Home.md').exists(),'finalizer should refresh enabled human knowledge in the organization workspace')

        second_bid='entry-regression-two';init_business(second_bid,env)
        ambiguous=run([SCRIPTS/'enter.py','Analyze our business.','--workspace',ws],env,check=False)
        require(ambiguous.returncode==2,'ambiguous business entry should be non-ready')
        payload=json.loads(ambiguous.stdout)
        require(payload.get('status')=='needs_input' and 'active_business' in payload.get('missing',[]),f'multiple businesses must not be silently selected: {payload}')
        require(sorted(payload.get('available_business_ids',[]))==sorted([bid,second_bid]),'ambiguous response should expose available business IDs')

        # External-workspace entry must not create corresponding business state under product root.
        require(not (ROOT/'instances'/bid).exists(),'entry regression leaked business state into product instances/')
        require(not (ROOT/'runtime/runs'/bid).exists(),'entry regression leaked Run state into product runtime/')
        require(not (ROOT/'knowledge'/bid).exists(),'entry/finalization regression leaked human knowledge into product root')

    print('aura entry regressions passed')


if __name__=='__main__':main()
