#!/usr/bin/env python3
"""Protect durable attention/platform history without making age or attention an execution gate."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from context_plan import build_plan
from validate_business import validate_business

BID='attention-platform-regression';BASE=ROOT/'instances'/BID


def req(c,m):
    if not c:raise AssertionError(m)

def run(*args,check=True):return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def jrun(*args):return json.loads(run(*args).stdout)

def write(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')


def main():
    if BASE.exists():shutil.rmtree(BASE)
    try:
        run(S/'init_business.py',BID,'--name','Attention Platform Regression')

        # Repeated material conditions update one durable attention item rather than
        # manufacturing a runtime queue entry for every observation.
        args=[
            S/'upsert_attention.py',BID,
            '--dedupe-key','google-search:faq-rich-results:review',
            '--type','material_change','--severity','medium',
            '--title','Review changed search guidance',
            '--reason','Verified platform guidance changed and may affect current organizational guidance.',
            '--recommended-action','Review affected guidance and decide whether any organizational update is warranted.',
            '--seen-at','2026-01-01T00:00:00+00:00'
        ]
        a1=jrun(*args);a2=jrun(*args)
        req(a1['attention_id']==a2['attention_id'] and a2['occurrence_count']==2,'repeated attention should reuse one durable item')
        req(len(list((BASE/'operations/attention').glob('att_*.json')))==1,'repeated attention must not multiply canonical files')

        run(S/'set_attention_status.py',BID,a1['attention_id'],'acknowledged','--at','2026-01-02T00:00:00+00:00')
        a3=jrun(*args)
        req(a3['status']=='acknowledged' and a3['occurrence_count']==3,'re-observation should preserve acknowledged active state')
        run(S/'set_attention_status.py',BID,a1['attention_id'],'resolved','--note','Review completed.','--at','2026-01-03T00:00:00+00:00')
        req(jrun(S/'list_attention.py',BID,'--json')['count']==0,'resolved attention should leave the active view')
        a4=jrun(*args)
        req(a4['attention_id']==a1['attention_id'] and a4['reopened'],'a genuine recurrence should reopen the same semantic item')

        # Archival is an explicit semantic retention decision, never an age threshold.
        active_archive=run(S/'archive_history.py',BID,a1['attention_id'],'--reason','Historical review complete. Keep for audit only.',check=False)
        req(active_archive.returncode!=0 and 'only after status=resolved' in active_archive.stderr,'active attention was archived without prior resolution')
        run(S/'set_attention_status.py',BID,a1['attention_id'],'resolved','--note','Recurrence reviewed and closed.','--at','2026-01-04T00:00:00+00:00')
        archived=jrun(S/'archive_history.py',BID,a1['attention_id'],'--reason','Historical review complete. Keep for audit only.','--at','2026-01-05T00:00:00+00:00')
        req(archived['archived_count']==1 and archived['selection_authority'] is False,'explicit attention archive did not preserve authority boundary')
        hist_attention=BASE/'history'/'AttentionItem'/f"{a1['attention_id']}.json"
        req(hist_attention.exists(),'resolved attention was not moved to history')
        hist_obj=json.loads(hist_attention.read_text())
        req(hist_obj['status']=='archived' and hist_obj['extensions']['archive_reason']=='Historical review complete. Keep for audit only.','historical attention lost explicit archive meaning')
        req(not (BASE/'operations/attention'/f"{a1['attention_id']}.json").exists(),'archived attention remained in active canonical path')

        # Platform knowledge is organization-owned evidence/history. Attention may point
        # to it, but neither object needs a Run or implies a scheduler/notification task.
        src={
            'id':f'src_{BID}_google-search-docs','object_type':'SourceRecord','schema_version':'1.0.0','business_id':BID,
            'created_at':'2026-01-01T00:00:00+00:00','updated_at':'2026-01-01T00:00:00+00:00','lineage':[],
            'source_type':'official_platform_documentation','source_reference':'https://developers.google.com/search/',
            'origin':'Google Search documentation','retrieved_at':'2026-01-01T00:00:00+00:00','published_at':None,
            'content_hash':None,'access_scope':'public','extensions':{}
        }
        write(BASE/'intelligence/sources'/f"{src['id']}.json",src)
        change=jrun(
            S/'record_platform_change.py',BID,'--platform','Google Search','--topic','FAQ rich results',
            '--state','FAQ rich-result guidance materially changed.','--authority','official_platform','--materiality','high',
            '--source-ref',src['id'],'--verified-at','2026-03-01T00:00:00+00:00'
        )
        pa=jrun(
            S/'upsert_attention.py',BID,'--dedupe-key','google-search:faq-rich-results:business-review',
            '--type','material_change','--severity','medium','--title','Review FAQ rich-result guidance change',
            '--reason','Current verified platform knowledge changed and may affect existing guidance.',
            '--recommended-action','Evaluate the affected organizational guidance before deciding whether to change anything.',
            '--lineage-ref',change['platform_change_id'],'--seen-at','2026-03-01T00:00:00+00:00'
        )
        req(pa['created'],'material platform change should support one durable attention item')

        current_archive=run(S/'archive_history.py',BID,change['platform_change_id'],'--reason','Old platform state.',check=False)
        req(current_archive.returncode!=0 and 'only after status=superseded' in current_archive.stderr,'current platform state was archiveable')
        replacement=jrun(
            S/'record_platform_change.py',BID,'--platform','Google Search','--topic','FAQ rich results',
            '--state','FAQ rich-result guidance changed again and supersedes the prior verified state.','--authority','official_platform','--materiality','high',
            '--source-ref',src['id'],'--verified-at','2026-04-01T00:00:00+00:00'
        )
        req(replacement['platform_change_id']!=change['platform_change_id'],'materially changed platform state did not create a new current version')
        platform_archive=jrun(S/'archive_history.py',BID,change['platform_change_id'],'--reason','Superseded platform state retained only for history.','--at','2026-04-02T00:00:00+00:00')
        req(platform_archive['archived_count']==1,'superseded platform state was not explicitly archivable')
        req((BASE/'history'/'PlatformChange'/f"{change['platform_change_id']}.json").exists(),'superseded platform state did not move to history')
        current=json.loads((BASE/'intelligence/platform-changes'/f"{replacement['platform_change_id']}.json").read_text())
        req(current['status']=='current','explicit history archival disturbed current platform state')

        errors,_,counts=validate_business(BID)
        req(not errors,f'attention/platform organizational state should validate without Run provenance: {errors}')
        req(counts.get('AttentionItem')==1 and counts.get('PlatformChange')==1,f'active view should contain only current organizational state after explicit archival: {counts}')
        for p in (BASE/'operations/attention').glob('att_*.json'):
            bos=(json.loads(p.read_text()).get('extensions') or {}).get('businessos',{})
            req('run_ref' not in bos and 'run_id' not in bos,'AttentionItem became Run-bound again')

        # Retention classification belonged to the retired age-based lifecycle. Explicit
        # status + explicit archive choice is sufficient; no dead retention class should return.
        attention_schema=json.loads((ROOT/'core/schemas/action/attention-item.schema.json').read_text())
        platform_schema=json.loads((ROOT/'core/schemas/intelligence/platform-change.schema.json').read_text())
        req('retention_class' not in attention_schema.get('properties',{}),'AttentionItem regained obsolete retention_class')
        req('retention_class' not in platform_schema.get('properties',{}),'PlatformChange regained obsolete retention_class')
        req('retention_class' not in (S/'upsert_attention.py').read_text(),'attention creation regained retention-class plumbing')
        req('retention_class' not in (S/'record_platform_change.py').read_text(),'platform-change creation regained retention-class plumbing')

        plan=build_plan(BID,'core.attention.manage')
        req('core/policies/attention-lifecycle.md' in plan['files'],'attention SOP should load attention continuity policy')
        policy=(ROOT/'core/policies/attention-lifecycle.md').read_text()
        req('Attention is organizational memory' in policy and 'proof that a background task exists' in policy and 'not execution authority' in policy,'attention policy lost the runtime boundary')
        req('elapsed time is not semantic authority' in policy.lower(),'attention policy reintroduced age as semantic retention authority')
        req('90 days' not in policy and '180 days' not in policy,'attention policy retained arbitrary age-based archival thresholds')
        workflow=(ROOT/'core/workflows/attention/manage/CONTEXT.md').read_text()
        req('archive_history.py' in workflow and 'Elapsed time alone is not a retention decision' in workflow,'attention Workflow did not preserve explicit archival boundary')
        req(not (S/'maintain_lifecycle.py').exists(),'retired age-based lifecycle helper still exists')

        print('attention/platform continuity regression passed with explicit history retention and no Run, approval, scheduler, delivery-channel, age-based, or retention-class semantic authority')
    finally:
        if BASE.exists():shutil.rmtree(BASE)
        runtime=ROOT/'runtime'/BID
        if runtime.exists():shutil.rmtree(runtime)


if __name__=='__main__':main()
