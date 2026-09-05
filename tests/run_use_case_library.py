#!/usr/bin/env python3
"""Regression checks for the maintainer-only real-world qualification library and focused Workflow diagnostic entry."""
from pathlib import Path
import json, os, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'qualification/use-cases'
LIB=json.loads((BASE/'library.json').read_text())


def req(cond,msg):
    if not cond:raise AssertionError(msg)


def run_prepare(args,prefix):
    with tempfile.TemporaryDirectory(prefix=f'aura-{prefix}-evaluator-') as td, tempfile.TemporaryDirectory(prefix=f'aura-{prefix}-candidate-') as cd:
        cmd=[sys.executable,str(ROOT/'qualification/prepare_run.py'),*args,'--run-root',td,'--candidate-root',cd,'--run-id','smoke']
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'})
        req(p.returncode==0,f"qualification preparation failed:\n{p.stdout}\n{p.stderr}")
        rd=Path(td)/'smoke';run=json.loads((rd/'run.json').read_text());queue=json.loads((rd/'evaluator/queue.json').read_text());product=Path(run['product_root']);workspace=Path(run['workspace']);surface=Path(run['candidate_surface_root'])
        req(run.get('candidate_blind') is True,'blind-candidate mode not recorded')
        req(product.parent==surface and workspace.parent==surface,'candidate product/workspace should share only the neutral candidate surface')
        req(rd not in product.parents and rd not in workspace.parents,'candidate and evaluator trees must remain physically separate')
        req(not (surface/'evaluator').exists() and not (surface/'checkpoints').exists(),'evaluator state leaked into candidate surface')
        req('qualification' not in product.as_posix().lower() and 'qualification' not in workspace.as_posix().lower(),'candidate-visible paths reveal benchmark intent')
        req(not (product/'qualification').exists() and not (product/'tests').exists(),'developer/evaluator machinery leaked into staged product')
        pointer=product/'.businessos/workspace.json';req(pointer.exists(),'staged product lost persistent external-workspace binding')
        req(Path(json.loads(pointer.read_text()).get('workspace_root','')).resolve()==workspace.resolve(),'staged workspace pointer mismatch')
        req(not (rd/'evaluator/suite.json').exists(),'retired generated qualification suite returned')
        return rd,run,queue


def main():
    cases=LIB.get('cases',[]);req(cases,'real-world use-case library is empty')
    ids=[c.get('id') for c in cases];req(len(ids)==len(set(ids)),'duplicate use-case ids')
    required_industries={'b2b-saas','local-services','ecommerce','creator-media','professional-services'}
    industries={c.get('industry') for c in cases};req(required_industries<=industries,f'missing representative industries: {required_industries-industries}')
    required_domains={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}
    domains={d for c in cases for d in c.get('domains',[])};req(required_domains<=domains,f'missing operating-area coverage: {required_domains-domains}')
    kinds={c.get('kind') for c in cases};req({'composed','cross-domain','longitudinal'}<=kinds,'use-case library lost composition/cross-domain/longitudinal coverage')
    forbidden=('qualification rubric','qualification score','qualification checkpoint','qualification receipt','target workflow','judge criteria')
    longitudinal=0
    for c in cases:
        fixture=ROOT/'qualification/fixtures'/f"{c['fixture']}.json";req(fixture.is_file(),f"missing fixture for {c['id']}: {fixture.name}")
        pairs=c.get('stages') or [c]
        if c.get('stages'):longitudinal+=1
        for pair in pairs:
            for key in ('request','judge'):
                path=BASE/pair[key];req(path.is_file(),f"missing {key} for {c['id']}: {pair[key]}")
            request=(BASE/pair['request']).read_text(encoding='utf-8').strip();req(request,f"empty request: {c['id']}")
            lower=request.lower();req(not any(x in lower for x in forbidden),f"candidate request leaks evaluator framing: {c['id']}")
            judge=(BASE/pair['judge']).read_text(encoding='utf-8');req('# Expected' in judge,f"judge guidance lacks outcome framing: {c['id']}")
    req(longitudinal>=1,'real-world library needs at least one longitudinal/change-oriented case')

    coverage=subprocess.run([sys.executable,str(ROOT/'qualification/use_case_coverage.py')],cwd=ROOT,capture_output=True,text=True)
    req(coverage.returncode==0,f'use-case coverage validation failed:\n{coverage.stdout}\n{coverage.stderr}')
    summary=json.loads(coverage.stdout);req(summary['use_cases']==len(cases),'coverage helper case count mismatch');req(summary['domain_count']>=len(required_domains),'coverage helper lost operating-area breadth')
    req(summary['authored_playbooks']>0,'authored Playbook inventory unexpectedly empty')
    req(summary['playbooks_remaining']==0 and summary['playbooks_covered']==summary['authored_playbooks'],'real-world library no longer covers every authored Playbook')

    rd,run,queue=run_prepare(['--case','saas-positioning-page'],'usecase-smoke')
    events=queue.get('events',[]);req(run.get('mode')=='use-case' and queue.get('case_filter')=='saas-positioning-page','use-case identity not retained evaluator-side');req(len(events)==1 and events[0].get('kind')=='use_case','use-case event preparation failed');req(events[0].get('event_id')=='TASK-0001','candidate-facing task id is not opaque')
    judge=rd/'evaluator/judges/TASK-0001.md';req(judge.is_file() and 'Expected outcome' in judge.read_text(),'hidden use-case judge guidance was not staged evaluator-side')
    start=subprocess.run([sys.executable,str(ROOT/'qualification/task_controller.py'),'start',str(rd)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    req(start.returncode==0,f'use-case controller start failed: {start.stdout}\n{start.stderr}');msg=json.loads(start.stdout).get('candidate_message','').strip();expected=(BASE/'requests/saas-positioning-page.md').read_text().strip();req(msg==expected,'candidate did not receive ordinary request verbatim');req('saas-positioning-page' not in msg.lower() and 'expected outcome' not in msg.lower(),'candidate request leaked use-case/judge metadata')

    rd,run,queue=run_prepare(['--case','saas-memory-evolution'],'longitudinal-smoke')
    events=queue.get('events',[]);req(len(events)==3,'longitudinal case did not produce expected staged requests');req(len({e.get('business_id') for e in events})==1,'longitudinal stages lost shared organization workspace');req(events[1].get('fresh_model_context') is True and events[2].get('fresh_model_context') is True,'longitudinal fresh-context intent missing evaluator-side');req(events[2].get('release_fixture')=='later_period','longitudinal contradictory/new evidence release missing');req(all((rd/'evaluator/judges'/f"{e['event_id']}.md").is_file() for e in events),'longitudinal judge guidance not isolated per stage')

    workflow_id='content.production.article';ordinary='Create the strongest useful article this organization needs from the evidence available, and make it genuinely publication-ready.'
    rd,run,queue=run_prepare(['--workflow',workflow_id,'--fixture','atlasops-saas','--request',ordinary],'workflow-diagnostic-smoke')
    events=queue.get('events',[]);req(run.get('mode')=='workflow-diagnostic' and len(events)==1,'focused Workflow diagnostic did not remain one explicit diagnostic');event=events[0];req(event.get('kind')=='workflow_diagnostic' and event.get('workflow_id')==workflow_id,'focused Workflow target was not retained evaluator-side');req(event.get('task')==ordinary,'focused diagnostic did not preserve maintainer-authored ordinary request');req(event.get('claim_under_test') and event.get('workflow_process_steps'),'focused diagnostic lost authored Workflow knowledge for professional review')

    for retired in ('qualification/build_suite.py','qualification/missions','qualification/cases'):
        req(not (ROOT/retired).exists(),f'retired qualification machinery still exists: {retired}')

    print(f"real-world qualification library regressions passed: {len(cases)} cases, {len(industries)} industries, {len(domains)} operating areas, {summary['playbooks_covered']}/{summary['authored_playbooks']} Playbooks; focused Workflow diagnostics remain available without a generated all-Workflow suite")

if __name__=='__main__':main()
