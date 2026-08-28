#!/usr/bin/env python3
from pathlib import Path
import json, os, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qualification'))
from common import product_snapshot, read_json
from evaluate_run import qualification_status, staged_product_integrity_flags


def req(cond,msg):
    if not cond: raise AssertionError(msg)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-product-integrity-') as td:
        root=Path(td)
        prep=subprocess.run([sys.executable,str(ROOT/'qualification/prepare_run.py'),'--profile','atomic','--domain','core','--run-root',str(root),'--run-id','product-integrity-smoke'],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        req(prep.returncode==0,f'qualification preparation failed:\n{prep.stdout}\n{prep.stderr}')
        rd=root/'product-integrity-smoke'; run=read_json(rd/'run.json'); product=Path(run['product_root']); workspace=Path(run['workspace']); baseline=read_json(rd/'evaluator/product-snapshot.json')
        req(isinstance(baseline,dict) and baseline.get('digest'),'prepared qualification must persist staged product snapshot')
        req(run.get('product_snapshot_digest')==baseline.get('digest'),'run metadata must bind staged product snapshot digest')
        req(run.get('qualification_status')=='NOT_EVALUATED','prepared work must not imply qualification success')
        req(run.get('candidate_blind') is True,'prepared work must use blind candidate mode')

        req(not (product/'qualification').exists(),'staged product leaked qualification directory')
        req(not (product/'tests').exists(),'staged product leaked developer tests')
        req(not (rd/'candidate').exists(),'qualification run created candidate-facing test directory')
        req(not (workspace/'qualification').exists(),'workspace leaked qualification directory')
        req(not (workspace/'attachments/qualification-inputs').exists(),'workspace leaked qualification-named inputs')
        evaluator_queue=read_json(rd/'evaluator/queue.json'); req((evaluator_queue or {}).get('events'),'evaluator must retain hidden target metadata externally')
        req(all(x.get('contract_id') for x in evaluator_queue.get('events',[]) if x.get('kind')=='contract_acceptance'),'evaluator contract events must retain hidden target contracts')
        start=subprocess.run([sys.executable,str(ROOT/'qualification/task_controller.py'),'start',str(rd)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        req(start.returncode==0,f'blind controller start failed:\n{start.stdout}\n{start.stderr}')
        candidate=json.loads(start.stdout).get('candidate_message',''); lower=candidate.lower()
        req(candidate and all(term not in lower for term in ('qualification','checkpoint','receipt','evaluator','rubric','scoring rule','hidden target')),'candidate message contains test-taking metadata')
        req(not staged_product_integrity_flags(rd,product,run),'untouched staged product must pass product-integrity check')

        transient=product/'__pycache__'/'scratch.cpython-313.pyc'; transient.parent.mkdir(); transient.write_bytes(b'transient'); ds=product/'.DS_Store'; ds.write_bytes(b'transient')
        req(not staged_product_integrity_flags(rd,product,run),'ignored interpreter/editor transients must not invalidate qualification')

        # A real host discovery pass with a non-empty manifest must write only workspace-owned
        # environment state. This is the condition that an empty-manifest smoke test used to miss.
        env={**os.environ,'BUSINESSOS_WORKSPACE':str(workspace),'PYTHONDONTWRITEBYTECODE':'1'}
        configure=subprocess.run([sys.executable,str(product/'scripts/configure_workspace.py'),str(workspace)],cwd=product,capture_output=True,text=True,env=env)
        req(configure.returncode==0,f'normal external workspace configuration failed:\n{configure.stdout}\n{configure.stderr}')
        shipped_bindings=product/'deployment/environments/local/capability-bindings.json'; shipped_before=shipped_bindings.read_text(encoding='utf-8')
        manifest=workspace/'runtime/host-tools.json'; manifest.parent.mkdir(parents=True,exist_ok=True)
        manifest.write_text(json.dumps({'format_version':'1.0','host_id':'qualification-host','tools':[{
            'id':'generate_image','description':'host image generation','enabled':True,
            'capabilities':['creative.image.generate'],'provider_action':'generate_image'
        }]},indent=2)+'\n',encoding='utf-8')
        bootstrap=subprocess.run([sys.executable,str(product/'scripts/bootstrap_environment.py'),'local','--manifest','runtime/host-tools.json','--mark-welcome-shown'],cwd=product,capture_output=True,text=True,env=env)
        req(bootstrap.returncode==0,f'normal host environment bootstrap failed:\n{bootstrap.stdout}\n{bootstrap.stderr}')
        overlay=workspace/'.businessos/environments/local'
        for name in ('host-profile.json','bootstrap-state.json','host-tools.json','tool-inventory.json','capability-bindings.json','provider-preferences.json','scheduler-bindings.json'):
            req((overlay/name).exists(),f'workspace environment overlay missing {name}')
        req(shipped_bindings.read_text(encoding='utf-8')==shipped_before,'host discovery modified shipped environment defaults')
        req(not (product/'runtime/host-tools.json').exists(),'workspace host manifest leaked into staged product runtime')
        req(not (product/'.businessos/environments').exists(),'external-workspace host overlay leaked into staged product')
        resolved=subprocess.run([sys.executable,str(product/'scripts/resolve_capability.py'),'local','creative.image.generate'],cwd=product,capture_output=True,text=True,env=env)
        req(resolved.returncode==0,f'overlay capability resolution failed:\n{resolved.stdout}\n{resolved.stderr}')
        resolved_json=json.loads(resolved.stdout); req(resolved_json.get('status')=='available','discovered workspace binding was not used by capability resolution')
        req(not staged_product_integrity_flags(rd,product,run),'official host discovery with real bindings must leave protected product source unchanged')

        # Shipped deployment defaults/templates remain protected. Host state belongs in the overlay,
        # so changing either a template or the local shipped default is a true product mutation.
        template=product/'deployment/environments/_template/host-profile.json'
        template_original=template.read_text(encoding='utf-8')
        template.write_text(template_original+'\n',encoding='utf-8')
        flags=staged_product_integrity_flags(rd,product,run); mutation=next((x for x in flags if x.get('type')=='staged_product_mutation'),None)
        req(mutation and 'deployment/environments/_template/host-profile.json' in mutation.get('modified',[]),'deployment template mutation must remain protected')
        template.write_text(template_original,encoding='utf-8')
        req(not staged_product_integrity_flags(rd,product,run),'restoring deployment template must clear product-integrity flag')
        shipped_bindings.write_text(shipped_before+'\n',encoding='utf-8')
        flags=staged_product_integrity_flags(rd,product,run); mutation=next((x for x in flags if x.get('type')=='staged_product_mutation'),None)
        req(mutation and 'deployment/environments/local/capability-bindings.json' in mutation.get('modified',[]),'shipped local environment default mutation must remain protected')
        shipped_bindings.write_text(shipped_before,encoding='utf-8')
        req(not staged_product_integrity_flags(rd,product,run),'restoring shipped local environment default must clear product-integrity flag')

        helper=product/'run_all_events.py'; helper.write_text("print('private qualification solver')\n",encoding='utf-8')
        flags=staged_product_integrity_flags(rd,product,run); mutation=next((x for x in flags if x.get('type')=='staged_product_mutation'),None)
        req(mutation and 'run_all_events.py' in mutation.get('created',[]),f'candidate-created product helper must be a critical product mutation: {flags}')
        helper.unlink(); req(not staged_product_integrity_flags(rd,product,run),'restoring exact protected product source should clear current-state mutation flag')

        target=product/'README.md'; original=target.read_text(encoding='utf-8'); target.write_text(original+'\nqualification mutation\n',encoding='utf-8')
        flags=staged_product_integrity_flags(rd,product,run); mutation=next((x for x in flags if x.get('type')=='staged_product_mutation'),None); req(mutation and 'README.md' in mutation.get('modified',[]),'modified staged source must fail product integrity'); target.write_text(original,encoding='utf-8')
        req(not staged_product_integrity_flags(rd,product,run),'restoring protected source must leave only workspace-owned runtime state')
        target.unlink(); flags=staged_product_integrity_flags(rd,product,run); mutation=next((x for x in flags if x.get('type')=='staged_product_mutation'),None); req(mutation and 'README.md' in mutation.get('deleted',[]),'deleted staged source must fail product integrity')

        run_bad={**run,'product_snapshot_digest':'tampered'}; mismatch=staged_product_integrity_flags(rd,product,run_bad); req(mismatch and mismatch[0].get('type')=='product_integrity_baseline_mismatch','run metadata snapshot tampering must fail integrity')
        snapshot_path=rd/'evaluator/product-snapshot.json'; saved=snapshot_path.read_text(encoding='utf-8'); snapshot_path.unlink(); missing=staged_product_integrity_flags(rd,product,run); req(missing and missing[0].get('type')=='product_integrity_baseline_missing','missing product integrity baseline must fail closed'); snapshot_path.write_text(saved,encoding='utf-8')

    req(qualification_status({'FAIL':1})=='FAILED','any evaluator FAIL must set qualification status FAILED')
    req(qualification_status({'HARD-PASS / REVIEW-PENDING':2})=='REVIEW_REQUIRED','hard-pass without professional review must not be called qualified')
    req(qualification_status({'BLOCKED-EXTERNAL':1})=='INCOMPLETE','blocked qualification must be incomplete')
    req(qualification_status({'ACCEPTABLE':2,'COMPETITIVE':1,'EXCEPTIONAL':1})=='QUALIFIED','only fully reviewed acceptable-or-better events may be qualified')
    print('qualification staged-product integrity regressions passed with blind candidate exposure, workspace-owned host environment state, and protected deployment defaults')

if __name__=='__main__': main()
