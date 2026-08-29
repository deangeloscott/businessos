#!/usr/bin/env python3
"""Summarize durable monitoring cadence versus actual scheduler execution state."""
from _common import *
import argparse,json
from datetime import datetime,timezone


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


def summarize(business_id,environment=None,at=None):
    if not instance_dir(business_id).exists():raise ValueError(f'Unknown business: {business_id}')
    environment=environment or installation().get('default_environment') or 'local'
    if not environment_exists(environment):raise ValueError(f'Unknown environment: {environment}')
    current=_dt(at) if at else datetime.now(timezone.utc)
    if current is None:raise ValueError('--at must be an ISO date-time')
    groups={}
    for obj,path in _profiles(business_id):
        if obj.get('watch_status') not in {'active','candidate'}:continue
        key=obj.get('subject_key') or obj.get('id')
        g=groups.setdefault(key,{'subject_key':obj.get('subject_key'),'subject_name':obj.get('subject_name') or obj.get('display_name') or key,'profiles':[]})
        g['profiles'].append((obj,path))
    bindings=_bindings(environment);rows=[]
    for key,g in sorted(groups.items(),key=lambda kv:str(kv[1].get('subject_name') or kv[0]).lower()):
        profs=g['profiles'];next_values=[(_dt(p.get('next_check_at')),p.get('next_check_at')) for p,_ in profs if _dt(p.get('next_check_at'))]
        earliest=min(next_values,key=lambda x:x[0]) if next_values else (None,None)
        due=bool(earliest[0] and earliest[0]<=current)
        cadences=[]
        for p,_ in profs:
            c=p.get('monitoring_cadence')
            if c and c not in cadences:cadences.append(c)
        matched=_matching_bindings(g,business_id,bindings)
        active=[b for b in matched if b.get('status')=='active' and b.get('last_verified_at')]
        reminder=[b for b in active if b.get('executor_kind')=='reminder_only']
        automatic=[b for b in active if b.get('executor_kind')!='reminder_only']
        if automatic:execution='active_automatic'
        elif reminder:execution='reminder_only'
        elif any(b.get('status')=='paused' for b in matched):execution='paused'
        elif cadences or earliest[1]:execution='planned_unbound'
        else:execution='manual'
        rows.append({
            'subject_key':g.get('subject_key'),
            'subject_name':g.get('subject_name'),
            'source_profile_count':len(profs),
            'cadences':cadences,
            'next_check_at':earliest[1],
            'due':due,
            'execution_status':execution,
            'active_scheduler_binding_ids':[b.get('id') for b in active],
            'needs_on_start_attention':bool(due and execution not in {'active_automatic'}),
            'profile_refs':[storage_ref(path) for _,path in profs]
        })
    due_unbound=[r for r in rows if r['needs_on_start_attention']]
    return {
        'business_id':business_id,'environment':environment,'checked_at':current.isoformat().replace('+00:00','Z'),
        'tracked_subject_count':len(rows),'due_unbound_count':len(due_unbound),
        'due_unbound_subjects':[{'subject_key':r['subject_key'],'subject_name':r['subject_name'],'next_check_at':r['next_check_at'],'execution_status':r['execution_status']} for r in due_unbound],
        'subjects':rows,
        'rule':'Cadence/next_check_at is monitoring intent. Only a verified active scheduler binding is active automatic execution; otherwise overdue monitoring falls back to the next AURA start/manual refresh.'
    }


def main():
    p=argparse.ArgumentParser(description='List tracked subjects whose semantic monitoring is due and distinguish actual scheduler bindings from planned cadence.')
    p.add_argument('business_id');p.add_argument('--environment');p.add_argument('--at');p.add_argument('--due-only',action='store_true')
    a=p.parse_args()
    try:r=summarize(a.business_id,a.environment,a.at)
    except ValueError as e:raise SystemExit(str(e))
    if a.due_only:r={**r,'subjects':[x for x in r['subjects'] if x['due']]}
    print(json.dumps(r,indent=2))

if __name__=='__main__':main()
