#!/usr/bin/env python3
"""Summarize durable monitoring cadence versus actual scheduler execution state."""
from _common import *
import argparse,json
from datetime import datetime,timezone

DEFAULT_NOTIFICATION='material_changes_only'
VISIBLE_WATCH_STATUSES={'active','candidate','paused','blocked'}
EXECUTING_WATCH_STATUSES={'active','candidate'}


def _dt(value):
    if not value:return None
    try:
        parsed=datetime.fromisoformat(str(value).replace('Z','+00:00'))
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)
    except ValueError:return None


def _read(path,default):
    try:return json.loads(path.read_text())
    except (FileNotFoundError,json.JSONDecodeError):return default


def _profiles(business_id):
    root=instance_dir(business_id)/'intelligence'/'source-profiles'
    rows=[]
    if not root.exists():return rows
    for path in sorted(root.glob('*.json')):
        obj=_read(path,{})
        if obj.get('object_type')=='SourceProfile' and obj.get('business_id')==business_id:
            rows.append((obj,path))
    return rows


def _bindings(environment):
    path=environment_file(environment,'scheduler-bindings.json')
    return _read(path,{'bindings':[]}).get('bindings',[])


def _matching_bindings(group,business_id,bindings):
    profile_ids={p.get('id') for p,_ in group['profiles']}
    subject_key=group.get('subject_key')
    out=[]
    for b in bindings:
        if b.get('business_id')!=business_id:continue
        if b.get('target_kind')=='subject' and subject_key and b.get('subject_key')==subject_key:out.append(b)
        elif b.get('target_kind')=='source_profile' and b.get('source_profile_id') in profile_ids:out.append(b)
        elif b.get('target_kind')=='business_monitoring':out.append(b)
    return out


def _cadence_label(c):
    if not c:return None
    bits=[c.get('expression') or c.get('mode')]
    if c.get('source'):bits.append(c['source'])
    if c.get('timezone'):bits.append(c['timezone'])
    return ' · '.join(str(x) for x in bits if x)


def _profile_notification(profile):
    n=profile.get('monitoring_notification') or {}
    return n.get('mode') or DEFAULT_NOTIFICATION


def summarize(business_id,environment=None,at=None):
    if not instance_dir(business_id).exists():raise ValueError(f'Unknown business: {business_id}')
    environment=environment or installation().get('default_environment') or 'local'
    if not environment_exists(environment):raise ValueError(f'Unknown environment: {environment}')
    current=_dt(at) if at else datetime.now(timezone.utc)
    if current is None:raise ValueError('--at must be an ISO date-time')
    groups={}
    for obj,path in _profiles(business_id):
        if obj.get('watch_status') not in VISIBLE_WATCH_STATUSES:continue
        key=obj.get('subject_key') or obj.get('id')
        g=groups.setdefault(key,{'subject_key':obj.get('subject_key'),'subject_name':obj.get('subject_name') or obj.get('display_name') or key,'profiles':[]})
        g['profiles'].append((obj,path))
    bindings=_bindings(environment);rows=[]
    for key,g in sorted(groups.items(),key=lambda kv:str(kv[1].get('subject_name') or kv[0]).lower()):
        profs=g['profiles'];due_points=[];cadences=[];signal_rows=[];notification_modes=[];watch_statuses=[]
        for p,_ in profs:
            status=p.get('watch_status');watch_statuses.append(status);executing=status in EXECUTING_WATCH_STATUSES
            base_notification=_profile_notification(p);notification_modes.append(base_notification)
            base_next=_dt(p.get('next_check_at'))
            if executing and base_next:
                due_points.append({'at':base_next,'value':p.get('next_check_at'),'kind':'source','signal':None,'profile_id':p.get('id'),'notification_mode':base_notification})
            label=_cadence_label(p.get('monitoring_cadence'))
            if label and label not in cadences:cadences.append(label)
            for s in p.get('monitoring_signal_cadences') or []:
                row={
                    'signal':s.get('signal'),'mode':s.get('mode'),'expression':s.get('expression'),'timezone':s.get('timezone'),
                    'source':s.get('source'),'next_check_at':s.get('next_check_at'),'notification_mode':s.get('notification_mode') or base_notification,
                    'profile_id':p.get('id'),'watch_status':status
                }
                if row not in signal_rows:signal_rows.append(row)
                notification_modes.append(row['notification_mode'])
                sat=_dt(s.get('next_check_at'))
                if executing and sat:
                    due_points.append({'at':sat,'value':s.get('next_check_at'),'kind':'signal','signal':s.get('signal'),'profile_id':p.get('id'),'notification_mode':row['notification_mode']})
        earliest=min(due_points,key=lambda x:x['at']) if due_points else None
        due_items=[x for x in due_points if x['at']<=current]
        due=bool(due_items);has_executing=any(x in EXECUTING_WATCH_STATUSES for x in watch_statuses)
        matched=_matching_bindings(g,business_id,bindings)
        active=[b for b in matched if b.get('status')=='active' and b.get('last_verified_at')]
        reminder=[b for b in active if b.get('executor_kind')=='reminder_only']
        automatic=[b for b in active if b.get('executor_kind')!='reminder_only']
        mismatch=False
        if not has_executing and automatic:
            execution='configuration_mismatch_active_scheduler';mismatch=True
        elif not has_executing and reminder:
            execution='configuration_mismatch_active_reminder';mismatch=True
        elif not has_executing and 'blocked' in watch_statuses:
            execution='blocked'
        elif not has_executing and 'paused' in watch_statuses:
            execution='paused'
        elif automatic:execution='active_automatic'
        elif reminder:execution='reminder_only'
        elif any(b.get('status')=='paused' for b in matched):execution='paused_scheduler_with_active_watch'
        elif cadences or signal_rows or earliest:execution='planned_unbound'
        else:execution='manual'
        due_notice_allowed=any(x.get('notification_mode') in {'due_and_material_changes','all_checks'} for x in due_items)
        rows.append({
            'subject_key':g.get('subject_key'),
            'subject_name':g.get('subject_name'),
            'source_profile_count':len(profs),
            'watch_statuses':sorted(set(watch_statuses)),
            'cadences':cadences,
            'signal_cadences':sorted(signal_rows,key=lambda x:(str(x.get('signal') or '').lower(),str(x.get('profile_id') or ''))),
            'notification_modes':sorted(set(notification_modes or [DEFAULT_NOTIFICATION])),
            'next_check_at':earliest['value'] if earliest else None,
            'next_check_kind':earliest['kind'] if earliest else None,
            'next_check_signal':earliest['signal'] if earliest else None,
            'due':due,
            'due_items':[{'at':x['value'],'kind':x['kind'],'signal':x['signal'],'profile_id':x['profile_id'],'notification_mode':x['notification_mode']} for x in sorted(due_items,key=lambda x:x['at'])],
            'execution_status':execution,
            'configuration_mismatch':mismatch,
            'active_scheduler_binding_ids':[b.get('id') for b in active],
            'needs_refresh_on_start':bool(due and has_executing and execution not in {'active_automatic'}),
            'proactive_due_notice_allowed':bool(due and due_notice_allowed),
            'profile_refs':[storage_ref(path) for _,path in profs]
        })
    due_unbound=[r for r in rows if r['needs_refresh_on_start']]
    due_notice=[r for r in due_unbound if r['proactive_due_notice_allowed']]
    mismatches=[r for r in rows if r['configuration_mismatch']]
    return {
        'business_id':business_id,'environment':environment,'checked_at':current.isoformat().replace('+00:00','Z'),
        'tracked_subject_count':len(rows),'due_unbound_count':len(due_unbound),'proactive_due_notice_count':len(due_notice),'configuration_mismatch_count':len(mismatches),
        'due_unbound_subjects':[{'subject_key':r['subject_key'],'subject_name':r['subject_name'],'next_check_at':r['next_check_at'],'execution_status':r['execution_status'],'proactive_due_notice_allowed':r['proactive_due_notice_allowed']} for r in due_unbound],
        'subjects':rows,
        'default_notification_mode':DEFAULT_NOTIFICATION,
        'rule':'Cadence/next_check_at is monitoring intent. Only a verified active scheduler binding is active automatic execution. Unchanged checks are quiet by default. Paused/blocked semantic watches are not due; if their host scheduler is still active, AURA reports a configuration mismatch instead of pretending the watch is stopped.'
    }


def main():
    p=argparse.ArgumentParser(description='List tracked monitoring state and distinguish semantic cadence, due work, notification intent, pause state, and actual scheduler bindings.')
    p.add_argument('business_id');p.add_argument('--environment');p.add_argument('--at');p.add_argument('--due-only',action='store_true')
    a=p.parse_args()
    try:r=summarize(a.business_id,a.environment,a.at)
    except ValueError as e:raise SystemExit(str(e))
    if a.due_only:r={**r,'subjects':[x for x in r['subjects'] if x['due']]}
    print(json.dumps(r,indent=2))

if __name__=='__main__':main()
