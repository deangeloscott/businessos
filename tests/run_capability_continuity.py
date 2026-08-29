#!/usr/bin/env python3
"""Regression checks for AURA monitoring continuity, human UX, and trusted optional local capability packs."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

import _common as common
from manage_local_capabilities import packs,_system_action
from resolve_capability import resolve
from list_due_monitoring import summarize
from generate_knowledge_layer import generate

BID='continuity-regression'

def fail(msg):raise AssertionError(msg)

def run(cmd,env,ok=True):
    p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
    if ok and p.returncode!=0:fail(f"command failed: {' '.join(map(str,cmd))}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p

def main():
    required=[
        'core/policies/monitoring-continuity.md','core/policies/local-capability-packs.md',
        'core/schemas/runtime/capability-pack.schema.json','core/schemas/runtime/scheduler-bindings.schema.json',
        'core/capability-packs/local-media.json','core/capability-packs/local-automation.json',
        'scripts/manage_local_capabilities.py','scripts/register_scheduler_binding.py','scripts/list_due_monitoring.py','scripts/monitoring_status.py'
    ]
    for rel in required:
        if not (ROOT/rel).exists():fail(f'missing continuity component {rel}')

    catalog={x['id'] for x in json.loads((ROOT/'core/capabilities/catalog.json').read_text()).get('capabilities',[])}
    expected={'media.video.acquire','media.transcript.acquire','media.metadata.inspect','media.video.process','media.audio.extract','media.frame.extract','automation.schedule.manage'}
    if not expected<=catalog:fail(f'capability catalog missing continuity capabilities: {sorted(expected-catalog)}')

    allpacks=packs()
    if set(allpacks)!={'local-automation','local-media'}:fail(f'unexpected capability packs: {sorted(allpacks)}')
    media=allpacks['local-media'];automation=allpacks['local-automation']
    if not {'yt-dlp','ffmpeg','ffprobe'}<={t['id'] for t in media['tools']}:fail('local media pack lost yt-dlp/ffmpeg/ffprobe')
    if 'ffmpeg-full' not in json.dumps(media):fail('local media pack lost enhanced Homebrew ffmpeg-full path')
    if not any('automation.schedule.manage' in t.get('capabilities',[]) for t in automation['tools']):fail('local automation pack does not map schedule mechanics')
    if 'allowed to access' not in media.get('responsibility_note',''):fail('local media responsibility note should remain short and permission-oriented')
    try:_system_action(media,'install',False)
    except ValueError as e:
        if 'requires explicit --approve' not in str(e):fail(f'unapproved system action rejected for wrong reason: {e}')
    else:fail('local pack system install was allowed without explicit approval')

    policy=(ROOT/'core/policies/local-capability-packs.md').read_text()
    for phrase in ['not another AURA edition','Never search the web for an arbitrary executable','Installing, upgrading, reinstalling, or changing system software requires explicit user authorization','does not mean AURA has "watched" or understood a video']:
        if phrase not in policy:fail(f'local capability policy missing invariant: {phrase}')
    continuity=(ROOT/'core/policies/monitoring-continuity.md').read_text()
    for phrase in ['semantic cadence is not the same thing as an active background schedule','User-specified cadence wins','Due-on-next-start','Missing background automation changes the executor, not the monitoring plan','Default to **material changes only**','Do not create or send a new notification merely to say that nothing changed','scripts/monitoring_status.py']:
        if phrase not in continuity:fail(f'monitoring continuity policy missing invariant: {phrase}')

    src_schema=json.loads((ROOT/'core/schemas/intelligence/source-profile.schema.json').read_text())
    for field in ['monitoring_cadence','monitoring_signal_cadences','monitoring_notification']:
        if field not in src_schema.get('properties',{}):fail(f'SourceProfile missing {field}')
        if field in src_schema.get('required',[]):fail(f'{field} must remain backward-compatible/optional')
    signal_props=src_schema['properties']['monitoring_signal_cadences']['items']['properties']
    if 'notification_mode' not in signal_props:fail('per-signal cadence cannot customize notification behavior')

    for rel in [
        'systems/content-synthesis/contracts/intelligence/creator-monitoring/CONTEXT.md',
        'systems/competitor-intelligence/contracts/analysis/advertising/CONTEXT.md',
        'systems/competitor-intelligence/contracts/analysis/content-strategy/CONTEXT.md'
    ]:
        text=(ROOT/rel).read_text()
        for cap in ['media.video.acquire','media.transcript.acquire','media.frame.extract']:
            if cap not in text:fail(f'{rel} does not expose optional local media capability {cap}')

    subject=(ROOT/'core/contracts/intelligence/subject-monitoring/CONTEXT.md').read_text()
    for phrase in ['monitoring_signal_cadences','material_changes_only','scripts/monitoring_status.py','one concise digest']:
        if phrase not in subject:fail(f'subject monitoring missing user-control/noise behavior: {phrase}')

    manager=ROOT/'scripts/manage_local_capabilities.py'
    p=subprocess.run([sys.executable,str(manager),'status','--pack','definitely-not-a-real-pack'],cwd=ROOT,capture_output=True,text=True)
    if p.returncode==0 or 'Unknown capability pack' not in (p.stderr+p.stdout):fail('unknown local pack does not fail cleanly')
    if 'KeyError' in (p.stderr+p.stdout):fail('unknown local pack leaked an implementation exception')

    prior_ws=os.environ.get('BUSINESSOS_WORKSPACE');prior_path=os.environ.get('PATH');tmp=Path(tempfile.mkdtemp(prefix='aura-continuity-regression-'))
    env=dict(os.environ);env['BUSINESSOS_WORKSPACE']=str(tmp);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1'
    try:
        os.environ['BUSINESSOS_WORKSPACE']=str(tmp)
        (tmp/'instances'/BID).mkdir(parents=True)

        # A missing media capability should route to the trusted local pack before generic/manual fallback.
        local=resolve('local','media.video.acquire',BID)
        if local.get('status')!='local_pack_check_required' or (local.get('pack') or {}).get('id')!='local-media':fail(f'local media capability did not resolve to trusted pack: {local}')

        upsert=[sys.executable,str(ROOT/'scripts/upsert_source_profile.py'),BID]
        pricing=json.dumps({'signal':'pricing changes','mode':'recurring','expression':'monthly','source':'user','next_check_at':'2026-09-15T00:00:00Z','notification_mode':'material_changes_only'})
        first=run(upsert+[
            '--source-reference','https://example.com/creator','--display-name','Example Creator Channel',
            '--subject-key','example_creator','--subject-name','Example Creator','--subject-kind','creator','--subject-relationship','thought_leader',
            '--watch-status','active','--source-modality','video','--monitoring-question','What materially changed?',
            '--cadence-mode','recurring','--cadence-expression','weekly','--cadence-source','user',
            '--notification-mode','material_changes_only','--notification-source','user',
            '--signal-cadence-json',pricing,
            '--last-checked-at','2026-08-20T00:00:00Z','--next-check-at','2026-08-28T00:00:00Z'
        ],env)
        created=json.loads(first.stdout)
        if created.get('schedule_execution','').startswith('active'):fail('SourceProfile helper falsely equated cadence with active scheduling')
        if not any(x.get('signal')=='pricing changes' and x.get('expression')=='monthly' for x in created.get('monitoring_signal_cadences',[])):fail('per-signal user cadence was not persisted')

        # Later inferred defaults may not silently override explicit user cadence/notification choices.
        blocked=run(upsert+[
            '--source-reference','https://example.com/creator','--cadence-mode','recurring','--cadence-expression','monthly','--cadence-source','inferred'
        ],env,ok=False)
        if blocked.returncode==0 or 'user-specified' not in (blocked.stderr+blocked.stdout):fail('inferred cadence silently replaced explicit user cadence')
        blocked_notice=run(upsert+[
            '--source-reference','https://example.com/creator','--notification-mode','all_checks','--notification-source','inferred'
        ],env,ok=False)
        if blocked_notice.returncode==0 or 'user-specified' not in (blocked_notice.stderr+blocked_notice.stdout):fail('inferred notification mode silently replaced explicit user preference')
        inferred_pricing=json.dumps({'signal':'pricing changes','mode':'recurring','expression':'weekly','source':'inferred','notification_mode':'all_checks'})
        blocked_signal=run(upsert+['--source-reference','https://example.com/creator','--signal-cadence-json',inferred_pricing],env,ok=False)
        if blocked_signal.returncode==0 or 'user-specified' not in (blocked_signal.stderr+blocked_signal.stdout):fail('inferred signal cadence silently replaced explicit user signal cadence')

        run(upsert+[
            '--source-reference','https://example.com/creator/newsletter','--display-name','Example Creator Newsletter',
            '--subject-key','example_creator','--subject-name','Example Creator','--subject-kind','creator','--subject-relationship','thought_leader',
            '--watch-status','active','--source-modality','text','--cadence-mode','recurring','--cadence-expression','monthly','--cadence-source','inferred',
            '--next-check-at','2026-09-15T00:00:00Z'
        ],env)

        # Default/material-change-only monitoring can be due without spamming the user.
        due=summarize(BID,'local','2026-08-29T00:00:00Z')
        if due.get('due_unbound_count')!=1:fail(f'due-on-next-start fallback did not find overdue unbound subject: {due}')
        if due.get('proactive_due_notice_count')!=0:fail(f'material-changes-only default allowed a routine due notification: {due}')
        subject_row=next(x for x in due['subjects'] if x.get('subject_key')=='example_creator')
        if subject_row.get('execution_status')!='planned_unbound' or not subject_row.get('needs_refresh_on_start'):fail(f'unbound cadence was represented as scheduled: {subject_row}')
        if subject_row.get('proactive_due_notice_allowed'):fail('material-changes-only monitor would proactively nag merely because it is due')
        if not any(x.get('signal')=='pricing changes' and x.get('notification_mode')=='material_changes_only' for x in subject_row.get('signal_cadences',[])):fail('combined monitoring view lost per-signal controls')

        # A user can opt into due notices for a specific signal without making every monitor noisy.
        hiring=json.dumps({'signal':'hiring/layoffs','mode':'recurring','expression':'weekly','source':'user','next_check_at':'2026-08-28T12:00:00Z','notification_mode':'due_and_material_changes'})
        run(upsert+['--source-reference','https://example.com/creator','--signal-cadence-json',hiring],env)
        due2=summarize(BID,'local','2026-08-29T00:00:00Z')
        if due2.get('proactive_due_notice_count')!=1:fail('explicit per-signal due notification preference was not represented')

        # Seed a local-pack binding, then refresh host discovery. Host discovery must replace only its own entries.
        overlay=tmp/'.businessos/environments/local';overlay.mkdir(parents=True,exist_ok=True)
        (overlay/'tool-inventory.json').write_text(json.dumps({'tools':[{'id':'local-pack:local-media:yt-dlp','description':'yt-dlp','enabled':True,'provider_id':None,'capabilities':['media.video.acquire'],'source':'local_capability_pack'}]},indent=2)+'\n')
        local_binding={'capability':'media.video.acquire','provider_id':None,'provider_action':'/trusted/yt-dlp','connection_ref':'local-pack:local-media:yt-dlp','permissions':['local_process'],'limitations':[],'coverage':'local_machine','reliability':1.0,'freshness':'2026.08.19','enabled':True}
        (overlay/'capability-bindings.json').write_text(json.dumps({'bindings':[local_binding]},indent=2)+'\n')
        manifest=tmp/'host.json';manifest.write_text(json.dumps({'format_version':'1.0','tools':[{'id':'host-doc-reader','description':'Host document reader','enabled':True,'capabilities':['document.read']}]},indent=2)+'\n')
        run([sys.executable,str(ROOT/'scripts/bootstrap_environment.py'),'local','--manifest',str(manifest)],env)
        merged=json.loads((overlay/'capability-bindings.json').read_text()).get('bindings',[])
        refs={x.get('connection_ref') for x in merged}
        if 'local-pack:local-media:yt-dlp' not in refs or 'host:host-doc-reader' not in refs:fail(f'host refresh did not preserve unrelated local-pack binding: {refs}')

        # A real externally-created schedule becomes automatic only after a verified binding receipt is recorded.
        register=run([
            sys.executable,str(ROOT/'scripts/register_scheduler_binding.py'),'local','sched_example_creator',
            '--business-id',BID,'--target-kind','subject','--subject-key','example_creator',
            '--executor-kind','harness_scheduler','--executor-ref','harness-task-123','--cadence-expression','weekly',
            '--verified-at','2026-08-29T00:00:00Z','--next-run-at','2026-09-04T00:00:00Z'
        ],env)
        receipt=json.loads(register.stdout)
        if receipt.get('binding',{}).get('status')!='active':fail('verified scheduler binding was not recorded active')
        active=summarize(BID,'local','2026-08-29T00:00:00Z')
        subject_row=next(x for x in active['subjects'] if x.get('subject_key')=='example_creator')
        if subject_row.get('execution_status')!='active_automatic' or subject_row.get('needs_refresh_on_start'):fail(f'verified scheduler binding did not resolve automatic execution truth: {subject_row}')

        status=run([sys.executable,str(ROOT/'scripts/monitoring_status.py'),BID,'--at','2026-08-29T00:00:00Z'],env).stdout
        for phrase in ['Example Creator','active_automatic','pricing changes','hiring/layoffs','material_changes_only','sched_example_creator']:
            if phrase not in status:fail(f'human/operator monitoring status missing {phrase}')

        human=generate(BID);tracked=Path(human['tracked_subjects_view']).read_text()
        if tracked.count('## Example Creator\n')!=1:fail('human knowledge layer did not group related SourceProfiles into one subject view')
        for phrase in ['Tracked sources/surfaces:** `2`','Automatic execution:** `active automatic`','weekly','monthly','pricing changes','hiring/layoffs','Notification mode','sched_example_creator','quiet by default']:
            if phrase not in tracked:fail(f'human tracked-subject view missing {phrase}')

        enter=(ROOT/'scripts/enter.py').read_text()
        for phrase in ['monitoring_continuity','due_unbound_subjects','Never describe planned cadence as an active schedule','human_ux_rule']:
            if phrase not in enter:fail(f'AURA front door missing continuity behavior: {phrase}')

        guide=(ROOT/'OPERATOR-GUIDE.md').read_text()
        for phrase in ['manage_local_capabilities.py','list_due_monitoring.py','register_scheduler_binding.py','ffmpeg-full']:
            if phrase not in guide:fail(f'operator guide missing continuity/tool path: {phrase}')

        print('AURA capability + continuity regressions passed: scheduler truth/fallback, quiet-by-default notifications, per-source/per-signal cadence, grouped human monitoring visibility, trusted local packs, safe system-change authorization, and binding-preserving host refresh')
    finally:
        if prior_ws is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior_ws
        if prior_path is not None:os.environ['PATH']=prior_path
        shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__':main()
