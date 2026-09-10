#!/usr/bin/env python3
"""Prove that AURA can resolve, retrieve, persist, read back, clean up, and validate."""
from pathlib import Path
import argparse,json,subprocess,sys

from _common import PRODUCT_ROOT,object_index,resolve_business,workspace_root
from enter import prepare_work
from forget import forget
from remember import remember
from validate_business import validate_business


def _workspace_validation():
    completed=subprocess.run([sys.executable,str(PRODUCT_ROOT/'scripts/validate_workspace.py')],cwd=PRODUCT_ROOT,capture_output=True,text=True)
    return {'ok':completed.returncode==0,'returncode':completed.returncode,'summary':(completed.stdout or completed.stderr).strip().splitlines()[-1:]}


def doctor(business_id=None):
    checks=[]
    try:root=str(workspace_root())
    except Exception as exc:
        return {'format_version':'1.0','status':'not_ready','workspace_root':None,'business_id':None,'checks':[{'name':'workspace_resolution','ok':False,'detail':str(exc)}],'reason':str(exc)}
    try:resolved=resolve_business(business_id)
    except Exception as exc:
        return {'format_version':'1.0','status':'not_ready','workspace_root':root,'business_id':None,'checks':[{'name':'organization_resolution','ok':False,'detail':str(exc)}],'reason':str(exc)}
    if resolved.get('status')!='resolved':
        return {'format_version':'1.0','status':'not_ready','workspace_root':str(workspace_root()),'business_id':None,'checks':[{'name':'organization_resolution','ok':False,'detail':resolved.get('reason')}],'reason':resolved.get('reason'),'available_businesses':resolved.get('available_businesses',[])}
    bid=resolved['business_id'];checks.append({'name':'organization_resolution','ok':True,'detail':resolved.get('resolution')})
    try:
        retrieval=prepare_work('AURA readiness probe: retrieve minimal organization context only.',bid)
        retrieval_ok=retrieval.get('status')=='ready' and retrieval.get('business_id')==bid
        retrieval_detail=f"baseline={len((retrieval.get('retrieval') or {}).get('baseline_context') or [])}"
    except (Exception,SystemExit) as exc:
        retrieval_ok=False;retrieval_detail=str(exc)
    checks.append({'name':'retrieval','ok':retrieval_ok,'detail':retrieval_detail})

    probe_id=None;probe_ok=False;cleanup_ok=True
    try:
        persisted=remember(bid,{'objects':[{'object_type':'Asset','content':{'asset_type':'aura_doctor_probe','business_role':'temporary AURA readiness probe','version':'1','status':'active'}}]})
        row=persisted['objects'][0];probe_id=row['id'];probe_path=Path(workspace_root())/row['path']
        current=object_index(bid).get(probe_id)
        probe_ok=bool(current and current[0].get('asset_type')=='aura_doctor_probe' and probe_path.exists())
    except Exception as exc:
        checks.append({'name':'persistence_readback','ok':False,'detail':str(exc)})
    else:
        checks.append({'name':'persistence_readback','ok':probe_ok,'detail':'temporary canonical probe created and read back' if probe_ok else 'temporary canonical probe was not readable'})
    finally:
        if probe_id:
            try:forget(bid,probe_id)
            except Exception as exc:
                cleanup_ok=False;checks.append({'name':'probe_cleanup','ok':False,'detail':str(exc)})
            else:checks.append({'name':'probe_cleanup','ok':probe_id not in object_index(bid),'detail':'temporary probe removed'})

    try:
        errors,warnings,_=validate_business(bid,True);business_ok=not errors;business_detail=f'errors={len(errors)} warnings={len(warnings)}'
    except Exception as exc:
        business_ok=False;business_detail=str(exc)
    checks.append({'name':'organization_validation','ok':business_ok,'detail':business_detail})
    try:workspace_check=_workspace_validation()
    except Exception as exc:workspace_check={'ok':False,'returncode':None,'summary':[str(exc)]}
    checks.append({'name':'workspace_validation','ok':workspace_check['ok'],'detail':'; '.join(workspace_check['summary']) or f"exit={workspace_check['returncode']}"})
    ready=all(row['ok'] for row in checks) and probe_ok and cleanup_ok
    return {'format_version':'1.0','status':'ready' if ready else 'not_ready','workspace_root':root,'business_id':bid,'checks':checks,'receipt':'AURA local retrieval, persistence, and validation checks passed. Host attachment is not verified by this check.' if ready else 'AURA local readiness check found a problem.'}


def main():
    p=argparse.ArgumentParser(description='Verify the active AURA organization can be retrieved, written, read back, cleaned up, and validated.')
    p.add_argument('--business-id');p.add_argument('--json',action='store_true');a=p.parse_args();r=doctor(a.business_id)
    if a.json:print(json.dumps(r,indent=2,ensure_ascii=False))
    else:
        print(f"AURA local readiness: {r['status'].upper()} (host attachment not checked)")
        if r.get('business_id'):print(f"organization={r['business_id']}")
        for row in r.get('checks',[]):print(('✓' if row['ok'] else '✗')+f" {row['name']}: {row.get('detail') or ''}")
    raise SystemExit(0 if r['status']=='ready' else 1)

if __name__=='__main__':main()
