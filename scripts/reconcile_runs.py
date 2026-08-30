#!/usr/bin/env python3
"""Inspect or safely reconcile Run lifecycle state after one completed Run."""
import argparse,json
from run_lifecycle import reconcile_run_lifecycle


def main():
    ap=argparse.ArgumentParser(description='Classify related AURA Runs and optionally apply only mechanically exact empty-Run supersession.')
    ap.add_argument('business_id');ap.add_argument('completed_run_id')
    ap.add_argument('--apply-safe-supersession',action='store_true')
    args=ap.parse_args();result=reconcile_run_lifecycle(args.business_id,args.completed_run_id,args.apply_safe_supersession)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    raise SystemExit(0 if result.get('status') in {'clean','reconciled','safe_supersession_available','remaining_work','needs_judgment'} else 2)


if __name__=='__main__':main()
