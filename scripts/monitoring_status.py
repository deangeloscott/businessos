#!/usr/bin/env python3
"""Human view of AURA monitoring intent and semantic due state."""
from list_due_monitoring import summarize
import argparse,json


def _fmt_signal(row):
    bits=[row.get('signal') or '(unnamed signal)',row.get('expression') or row.get('mode') or 'manual']
    if row.get('watch_status'):bits.append(f"watch {row['watch_status']}")
    if row.get('next_check_at'):bits.append(f"next {row['next_check_at']}")
    if row.get('notification_mode'):bits.append(f"notify {row['notification_mode']}")
    return ' · '.join(bits)


def main():
    p=argparse.ArgumentParser(description='Show what AURA intends to monitor. Runtime scheduling/execution is external.')
    p.add_argument('business_id');p.add_argument('--at');p.add_argument('--due-only',action='store_true');p.add_argument('--json',action='store_true')
    a=p.parse_args()
    try:data=summarize(a.business_id,a.at)
    except ValueError as e:raise SystemExit(str(e))
    rows=[x for x in data['subjects'] if (x.get('due') if a.due_only else True)]
    if a.json:print(json.dumps({**data,'subjects':rows},indent=2));return
    print(f"AURA monitoring intent — {a.business_id}")
    print(f"Tracked subjects: {data['tracked_subject_count']} | Due for another useful check: {data['due_count']}")
    print('Runtime scheduling is external to AURA; this view does not claim any background task is active.')
    if not rows:print('No matching monitoring plans.');return
    for row in rows:
        due=' DUE' if row.get('due') else ''
        print(f"\n{row.get('subject_name') or row.get('subject_key')}{due}")
        if row.get('watch_statuses'):print(f"  watch: {', '.join(row['watch_statuses'])}")
        if row.get('cadences'):print(f"  cadence intent: {', '.join(row['cadences'])}")
        print(f"  notification intent: {', '.join(row.get('notification_modes') or [data.get('default_notification_mode','material_changes_only')])}")
        if row.get('next_check_at'):print(f"  next useful check: {row['next_check_at']}" + (f" ({row.get('next_check_signal')})" if row.get('next_check_signal') else ''))
        for signal in row.get('signal_cadences') or []:print(f"  signal: {_fmt_signal(signal)}")

if __name__=='__main__':main()
