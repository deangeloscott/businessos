#!/usr/bin/env python3
"""Human/operator view of AURA monitoring intent, due work, notifications, and scheduler truth."""
from _common import *
from list_due_monitoring import summarize
import argparse,json


def _fmt_signal(row):
    bits=[row.get('signal') or '(unnamed signal)',row.get('expression') or row.get('mode') or 'manual']
    if row.get('next_check_at'):bits.append(f"next {row['next_check_at']}")
    if row.get('notification_mode'):bits.append(f"notify {row['notification_mode']}")
    return ' · '.join(bits)


def main():
    p=argparse.ArgumentParser(description='Show what AURA is monitoring, how often, notification intent, what is due, and whether automation is actually active.')
    p.add_argument('business_id');p.add_argument('--environment');p.add_argument('--at');p.add_argument('--due-only',action='store_true');p.add_argument('--json',action='store_true')
    a=p.parse_args()
    try:data=summarize(a.business_id,a.environment,a.at)
    except ValueError as e:raise SystemExit(str(e))
    rows=[x for x in data['subjects'] if (x.get('due') if a.due_only else True)]
    if a.json:
        print(json.dumps({**data,'subjects':rows},indent=2));return
    print(f"AURA monitoring — {a.business_id} ({data['environment']})")
    print(f"Tracked subjects: {data['tracked_subject_count']} | Due/unbound: {data['due_unbound_count']} | Due notices allowed: {data.get('proactive_due_notice_count',0)}")
    if not rows:
        print('No matching monitoring plans.');return
    for row in rows:
        due=' DUE' if row.get('due') else ''
        print(f"\n{row.get('subject_name') or row.get('subject_key')}{due}")
        print(f"  execution: {row.get('execution_status')}")
        if row.get('cadences'):print(f"  default cadence: {', '.join(row['cadences'])}")
        print(f"  notification: {', '.join(row.get('notification_modes') or [data.get('default_notification_mode','material_changes_only')])}")
        if row.get('next_check_at'):print(f"  next check: {row['next_check_at']}" + (f" ({row.get('next_check_signal')})" if row.get('next_check_signal') else ''))
        for signal in row.get('signal_cadences') or []:print(f"  signal: {_fmt_signal(signal)}")
        if row.get('active_scheduler_binding_ids'):print(f"  scheduler binding: {', '.join(row['active_scheduler_binding_ids'])}")
    print('\nChange these through AURA in natural language (for example: “make pricing monthly but hiring weekly,” “only notify me on material changes,” or “pause this watch”). Operators can inspect the same state with --json.')

if __name__=='__main__':main()
