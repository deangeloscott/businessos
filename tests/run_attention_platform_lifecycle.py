#!/usr/bin/env python3
"""RC8 regressions for portable attention, platform freshness, dedupe, supersession, and archive lifecycle."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts';sys.path.insert(0,str(S))
from validate_business import validate_business
from validate_attention_lifecycle import lifecycle_errors
from context_plan import build_plan
from _common import iter_instance_objects

BID='attention-platform-regression';BASE=ROOT/'instances'/BID

def req(c,m):
    if not c:raise AssertionError(m)
def run(*args,check=True):return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def jrun(*args):return json.loads(run(*args).stdout)
def write(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')
def mark_preexisting_run_bound():
    run_bound={'AttentionItem','PlatformChange'}
    for obj,p in iter_instance_objects(BID):
        if obj.get('object_type') not in run_bound: continue
        bos=obj.setdefault('extensions',{}).setdefault('businessos',{})
        bos['origin']='preexisting'
        p.write_text(json.dumps(obj,indent=2)+'\n')


def main():
    if BASE.exists():shutil.rmtree(BASE)
    try:
        run(S/'init_business.py',BID,'--name','Attention Platform Regression')

        # Repeated detection must update one semantic attention item, not multiply files.
        args=[S/'upsert_attention.py',BID,'--dedupe-key','google-search:approval:publish-fix','--type','approval_required','--severity','high','--title','Approve search fix','--reason','A verified search remediation is ready but external write approval is missing.','--recommended-action','Approve or reject the bounded website update','--seen-at','2026-01-01T00:00:00+00:00']
        a1=jrun(*args);a2=jrun(*args)
        req(a1['attention_id']==a2['attention_id'],'repeated attention must reuse one id')
        req(a2['occurrence_count']==2,'repeated attention must increment occurrence_count')
        req(len(list((BASE/'operations/attention').glob('att_*.json')))==1,'repeated attention must not create files')
        run(S/'set_attention_status.py',BID,a1['attention_id'],'acknowledged','--at','2026-01-02T00:00:00+00:00')
        a3=jrun(*args);req(a3['status']=='acknowledged' and a3['occurrence_count']==3,'recheck should retain acknowledged active state and increment count')
        active=jrun(S/'list_attention.py',BID,'--json');req(active['count']==1,'active queue should contain one deduped item')

        run(S/'set_attention_status.py',BID,a1['attention_id'],'resolved','--note','Approval no longer required; work was cancelled.','--at','2026-01-03T00:00:00+00:00')
        active=jrun(S/'list_attention.py',BID,'--json');req(active['count']==0,'resolved attention must leave active queue')
        a4=jrun(*args);req(a4['attention_id']==a1['attention_id'] and a4['reopened'] and a4['occurrence_count']==4,'genuine recurrence should reopen same semantic item rather than create duplicate')
        run(S/'set_attention_status.py',BID,a1['attention_id'],'resolved','--note','Resolved again.','--at','2026-01-04T00:00:00+00:00')

        # Verified platform state must retain source provenance.
        src={'id':f'src_{BID}_google-search-docs','object_type':'SourceRecord','schema_version':'1.0.0','business_id':BID,'created_at':'2026-01-01T00:00:00+00:00','updated_at':'2026-01-01T00:00:00+00:00','lineage':[],'source_type':'official_platform_documentation','source_reference':'https://developers.google.com/search/','origin':'Google Search documentation','retrieved_at':'2026-01-01T00:00:00+00:00','published_at':None,'content_hash':None,'access_scope':'public','extensions':{}}
        write(BASE/'intelligence/sources'/f"{src['id']}.json",src)

        # Platform state: unchanged verification refreshes current object; material change creates a superseding version.
        p1=jrun(S/'record_platform_change.py',BID,'--platform','Google Search','--topic','FAQ rich results','--state','FAQ rich results are supported for eligible pages.','--authority','official_platform','--materiality','medium','--source-ref',src['id'],'--verified-at','2026-01-01T00:00:00+00:00')
        p1b=jrun(S/'record_platform_change.py',BID,'--platform','Google Search','--topic','FAQ rich results','--state','FAQ rich results are supported for eligible pages.','--authority','official_platform','--materiality','medium','--source-ref',src['id'],'--verified-at','2026-02-01T00:00:00+00:00')
        req(p1['platform_change_id']==p1b['platform_change_id'] and p1b['result']=='refreshed' and p1b['verification_count']==2,'unchanged platform state should refresh one object')
        req(len(list((BASE/'intelligence/platform-changes').glob('plc_*.json')))==1,'unchanged platform checks must not create files')
        p2=jrun(S/'record_platform_change.py',BID,'--platform','Google Search','--topic','FAQ rich results','--state','FAQ rich results are deprecated and no longer shown.','--authority','official_platform','--materiality','high','--change-summary','Support was deprecated.','--source-ref',src['id'],'--verified-at','2026-03-01T00:00:00+00:00')
        req(p2['platform_change_id']!=p1['platform_change_id'] and p2['result']=='changed','material platform change should create new version')
        current=jrun(S/'list_platform_state.py',BID,'--json');req(current['count']==1 and current['items'][0]['id']==p2['platform_change_id'],'normal platform retrieval should expose one current state')
        old=json.loads((BASE/'intelligence/platform-changes'/f"{p1['platform_change_id']}.json").read_text());new=json.loads((BASE/'intelligence/platform-changes'/f"{p2['platform_change_id']}.json").read_text())
        req(old['status']=='superseded' and old['superseded_by']==new['id'] and new['supersedes']==old['id'],'platform versions must have reciprocal supersession lineage')

        # A material platform change can be referenced by one attention item without coupling to delivery channel.
        pa=jrun(S/'upsert_attention.py',BID,'--dedupe-key','google-search:faq-rich-results:business-review','--type','material_change','--severity','medium','--title','Review deprecated FAQ rich-result dependency','--reason','Current verified Google Search state changed and may affect existing implementation guidance.','--recommended-action','Evaluate affected BusinessOS/site state before changing anything','--lineage-ref',new['id'],'--seen-at','2026-03-01T00:00:00+00:00')
        req(pa['created'],'first material change attention should create one item')

        mark_preexisting_run_bound()
        errors,warnings,counts=validate_business(BID)
        req(not errors,f'valid attention/platform state should pass business validation: {errors}')
        req(counts.get('AttentionItem')==2 and counts.get('PlatformChange')==2,f'expected canonical types missing: {counts}')

        # Validator rejects duplicate active semantic state even if an agent hand-writes it.
        orig=json.loads((BASE/'operations/attention'/f"{pa['attention_id']}.json").read_text());dup=dict(orig);dup['id']=orig['id']+'dup';write(BASE/'operations/attention'/f"{dup['id']}.json",dup)
        mark_preexisting_run_bound();errs,_,_=validate_business(BID);req(any('multiple active AttentionItems share dedupe_key' in e for e in errs),f'duplicate active attention should fail: {errs}')
        (BASE/'operations/attention'/f"{dup['id']}.json").unlink()
        dup=dict(new);dup['id']=new['id']+'dup';dup['supersedes']=None;write(BASE/'intelligence/platform-changes'/f"{dup['id']}.json",dup)
        mark_preexisting_run_bound();errs,_,_=validate_business(BID);req(any('multiple current PlatformChanges share semantic_key' in e for e in errs),f'duplicate current platform state should fail: {errs}')
        (BASE/'intelligence/platform-changes'/f"{dup['id']}.json").unlink()

        # Old terminal state moves out of active folders; it remains canonical history and references remain valid.
        arch=jrun(S/'maintain_lifecycle.py',BID,'--attention-days','30','--platform-days','30','--apply','--as-of','2026-08-24T00:00:00+00:00')
        req(arch['eligible_count']>=2,'old resolved attention and superseded platform version should be archive eligible')
        req((BASE/'history/attention/2026'/f"{a1['attention_id']}.json").exists(),'resolved attention should move to history')
        req((BASE/'history/platform-changes/2026'/f"{p1['platform_change_id']}.json").exists(),'superseded platform state should move to history')
        active=jrun(S/'list_attention.py',BID,'--json');req(active['count']==1 and active['items'][0]['id']==pa['attention_id'],'archive maintenance must leave only genuinely active attention')
        current=jrun(S/'list_platform_state.py',BID,'--json');req(current['count']==1 and current['items'][0]['id']==p2['platform_change_id'],'archive maintenance must leave current platform state')
        mark_preexisting_run_bound();errs,_,_=validate_business(BID);req(not errs,f'archived history must preserve valid references: {errs}')

        # Archived resolved semantic attention can recur without creating a second historical/active copy.
        a5=jrun(*args);req(a5['attention_id']==a1['attention_id'] and a5['reopened'],'archived recurring condition should restore the same semantic item')
        req(not (BASE/'history/attention/2026'/f"{a1['attention_id']}.json").exists(),'reopening archived item should move it back to active state, not duplicate it')
        req((BASE/'operations/attention'/f"{a1['attention_id']}.json").exists(),'reopened item should exist in active attention path')
        mark_preexisting_run_bound();errs,_,_=validate_business(BID);req(not errs,f'reopened archived state should validate: {errs}')

        # Policies must be loaded by the contracts that own these semantics.
        plan=build_plan(BID,'core.attention.manage');req('core/policies/attention-lifecycle.md' in plan['files'],'attention contract must load attention lifecycle policy')
        plan=build_plan(BID,'core.intelligence.record-platform-change');req('core/policies/platform-intelligence.md' in plan['files'],'platform record contract must load platform intelligence policy')
        plan=build_plan(BID,'industry.monitoring.technology');req('core/policies/platform-intelligence.md' in plan['files'],'industry platform monitoring must load shared platform policy')
        text=(ROOT/'core/policies/attention-lifecycle.md').read_text();req('Repetition updates state; meaningful change creates history.' in text and 'list_attention.py' in text,'attention policy must specify dedupe/harness boundary')
        text=(ROOT/'core/policies/platform-intelligence.md').read_text();req('does **not** authorize BusinessOS to rewrite its own product logic' in text,'platform policy must prohibit uncontrolled self-modification')
        print('attention/platform lifecycle regressions passed')
    finally:
        if BASE.exists():shutil.rmtree(BASE)
        r=ROOT/'runtime'/BID
        if r.exists():shutil.rmtree(r)
if __name__=='__main__':main()
