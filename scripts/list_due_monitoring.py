#!/usr/bin/env python3
"""Summarize organization-owned monitoring intent and semantic due state."""
from _common import *
import argparse,json
from datetime import datetime,timezone

DEFAULT_NOTIFICATION='material_changes_only'
VISIBLE_WATCH_STATUSES={'active','candidate','paused','blocked'}
DUE_WATCH_STATUSES={'active','candidate'}


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
        if obj.get('object_type')=='SourceProfile' and obj.get('business_id')==business_id:rows.append((obj,path))
    return rows


def _cadence_label(c):
    if not c:return None
    bits=[c.get('expression') or c.get('mode')]
    if c.get('source'):bits.append(c['source'])
    if c.get('timezone'):bits.append(c['timezone'])
    return ' · '.join(str(x) for x in bits if x)


def _notification(profile):
    return (profile.get('monitoring_notification') or {}).get('mode') or DEFAULT_NOTIFICATION


def summarize(business_id,at=None):
    if not instance_dir(business_id).exists():raise ValueError(f'Unknown business: {business_id}')
    current=_dt(at) if at else datetime.now(timezone.utc)
    if current is None:raise ValueError('--at must be an ISO date-time')
    groups={}
    for obj,path in _profiles(business_id):
        if obj.get('watch_status') not in VISIBLE_WATCH_STATUSES:continue
        key=obj.get('subject_key') or obj.get('id')
        g=groups.setdefault(key,{'subject_key':obj.get('subject_key'),'subject_name':obj.get('subject_name') or obj.get('display_name') or key,'profiles':[]})
        g['profiles'].append((obj,path))
    rows=[]
    for key,g in sorted(groups.items(),key=lambda kv:str(kv[1].get('subject_name') or kv[0]).lower()):
        due_points=[];cadences=[];signals=[];notification_modes=[];watch_statuses=[]
        for p,_ in g['profiles']:
            status=p.get('watch_status');watch_statuses.append(status);base_notice=_notification(p);notification_modes.append(base_notice)
            label=_cadence_label(p.get('monitoring_cadence'))
            if label and label not in cadences:cadences.append(label)
            base_next=_dt(p.get('next_check_at'))
            if status in DUE_WATCH_STATUSES and base_next:due_points.append({'at':base_next,'value':p.get('next_check_at'),'kind':'source','signal':None,'profile_id':p.get('id'),'notification_mode':base_notice})
            for s in p.get('monitoring_signal_cadences') or []:
                row={'signal':s.get('signal'),'mode':s.get('mode'),'expression':s.get('expression'),'timezone':s.get('timezone'),'source':s.get('source'),'next_check_at':s.get('next_check_at'),'notification_mode':s.get('notification_mode') or base_notice,'profile_id':p.get('id'),'watch_status':status}
                if row not in signals:signals.append(row)
                notification_modes.append(row['notification_mode'])
                sat=_dt(s.get('next_check_at'))
                if status in DUE_WATCH_STATUSES and sat:due_points.append({'at':sat,'value':s.get('next_check_at'),'kind':'signal','signal':s.get('signal'),'profile_id':p.get('id'),'notification_mode':row['notification_mode']})
        earliest=min(due_points,key=lambda x:x['at']) if due_points else None
        due_items=[x for x in due_points if x['at']<=current]
        rows.append({'subject_key':g.get('subject_key'),'subject_name':g.get('subject_name'),'source_profile_count':len(g['profiles']),'watch_statuses':sorted(set(watch_statuses)),'cadences':cadences,'signal_cadences':sorted(signals,key=lambda x:(str(x.get('signal') or '').lower(),str(x.get('profile_id') or ''))),'notification_modes':sorted(set(notification_modes or [DEFAULT_NOTIFICATION])),'next_check_at':earliest['value'] if earliest else None,'next_check_kind':earliest['kind'] if earliest else None,'next_check_signal':earliest['signal'] if earliest else None,'due':bool(due_items),'due_items':[{'at':x['value'],'kind':x['kind'],'signal':x['signal'],'profile_id':x['profile_id'],'notification_mode':x['notification_mode']} for x in sorted(due_items,key=lambda x:x['at'])],'profile_refs':[storage_ref(path) for _,path in g['profiles']]})
    due=[r for r in rows if r['due']]
    return {'business_id':business_id,'checked_at':current.isoformat().replace('+00:00','Z'),'tracked_subject_count':len(rows),'due_count':len(due),'due_subjects':[{'subject_key':r['subject_key'],'subject_name':r['subject_name'],'next_check_at':r['next_check_at']} for r in due],'subjects':rows,'default_notification_mode':DEFAULT_NOTIFICATION,'rule':'This is organization-owned monitoring intent and semantic due state only. Scheduling/execution truth belongs to the current runtime/harness and is not inferred by AURA.'}


def main():
    p=argparse.ArgumentParser(description='List monitoring intent and semantic due state. This does not inspect external scheduler state.')
    p.add_argument('business_id');p.add_argument('--at');p.add_argument('--due-only',action='store_true')
    a=p.parse_args()
    try:r=summarize(a.business_id,a.at)
    except ValueError as e:raise SystemExit(str(e))
    if a.due_only:r={**r,'subjects':[x for x in r['subjects'] if x['due']]}
    print(json.dumps(r,indent=2))

if __name__=='__main__':main()
