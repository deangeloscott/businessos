#!/usr/bin/env python3
"""Regressions for semantic PlatformChange re-verification across wording changes."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'
BID='platform-semantic-reverification-regression'; BASE=ROOT/'instances'/BID

def req(c,m):
    if not c: raise AssertionError(m)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def jrun(*args): return json.loads(run(*args).stdout)
def write(p,o): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')

def main():
    if BASE.exists(): shutil.rmtree(BASE)
    try:
        run(S/'init_business.py',BID,'--name','Platform Semantic Reverification Regression')
        src1={'id':f'src_{BID}_one','object_type':'SourceRecord','schema_version':'1.0.0','business_id':BID,'created_at':'2026-01-01T00:00:00+00:00','updated_at':'2026-01-01T00:00:00+00:00','lineage':[],'source_type':'official_platform_documentation','source_reference':'https://example.test/one','origin':'Official platform','retrieved_at':'2026-01-01T00:00:00+00:00','published_at':None,'content_hash':None,'access_scope':'public','extensions':{}}
        src2=dict(src1);src2.update(id=f'src_{BID}_two',source_reference='https://example.test/two',created_at='2026-02-01T00:00:00+00:00',updated_at='2026-02-01T00:00:00+00:00',retrieved_at='2026-02-01T00:00:00+00:00')
        write(BASE/'intelligence/sources'/f"{src1['id']}.json",src1);write(BASE/'intelligence/sources'/f"{src2['id']}.json",src2)

        original='Events API v1 remains supported through November 30; v2 requires events.read and grants are not migrated automatically.'
        restated='Reminder: the November 30 support end is unchanged. Version 2 still requires events.read, and existing grants still do not move automatically.'
        p1=jrun(S/'record_platform_change.py',BID,'--platform','SignalPort','--topic','Events API v1 lifecycle','--state',original,'--authority','official_platform','--materiality','high','--source-ref',src1['id'],'--verified-at','2026-01-01T00:00:00+00:00')
        p1b=jrun(S/'record_platform_change.py',BID,'--platform','SignalPort','--topic','Events API v1 lifecycle','--state',restated,'--authority','official_platform','--materiality','high','--source-ref',src2['id'],'--verified-at','2026-02-01T00:00:00+00:00','--change-summary','Official reminder semantically restates the same material state.','--reverify-current')
        req(p1b['platform_change_id']==p1['platform_change_id'],'semantic re-verification must preserve PlatformChange identity')
        req(p1b['result']=='reverified' and p1b['verification_count']==2,'semantic re-verification must increment count without versioning')
        files=list((BASE/'intelligence/platform-changes').glob('plc_*.json'));req(len(files)==1,'semantic re-verification must not create another PlatformChange file')
        obj=json.loads(files[0].read_text())
        req(obj['state_summary']==original,'canonical state summary must remain stable on semantic re-verification')
        req(src2['id'] in obj['source_refs'] and src2['id'] in obj['lineage'],'later provenance must be retained')
        hist=obj.get('extensions',{}).get('verification_history',[]);req(len(hist)==1 and hist[0]['observed_state_summary']==restated,'later wording must be retained as verification history')

        changed='Events API v1 support now ends October 15; v2 still requires events.read and grants are not migrated automatically.'
        p2=jrun(S/'record_platform_change.py',BID,'--platform','SignalPort','--topic','Events API v1 lifecycle','--state',changed,'--authority','official_platform','--materiality','critical','--source-ref',src2['id'],'--verified-at','2026-03-01T00:00:00+00:00','--change-summary','Shutdown deadline moved earlier.')
        req(p2['platform_change_id']!=p1['platform_change_id'] and p2['result']=='changed','material state change must still create a superseding version')
        old=json.loads((BASE/'intelligence/platform-changes'/f"{p1['platform_change_id']}.json").read_text());new=json.loads((BASE/'intelligence/platform-changes'/f"{p2['platform_change_id']}.json").read_text())
        req(old['status']=='superseded' and old['superseded_by']==new['id'] and new['supersedes']==old['id'],'material change must preserve reciprocal supersession')

        # Explicit no-change mode cannot fabricate a current object when none exists.
        other='platform-semantic-no-current-regression'; otherbase=ROOT/'instances'/other
        if otherbase.exists(): shutil.rmtree(otherbase)
        run(S/'init_business.py',other,'--name','No Current Platform State')
        r=run(S/'record_platform_change.py',other,'--platform','SignalPort','--topic','Events API v1 lifecycle','--state',restated,'--authority','official_platform','--source-ref',src2['id'],'--reverify-current',check=False)
        req(r.returncode!=0 and '--reverify-current requires an existing current PlatformChange' in (r.stdout+r.stderr),'reverify-current must fail closed without a current state')
        shutil.rmtree(otherbase)
        print('platform semantic re-verification regressions passed')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
        r=ROOT/'runtime'/BID
        if r.exists(): shutil.rmtree(r)

if __name__=='__main__': main()
