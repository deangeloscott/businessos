#!/usr/bin/env python3
"""List organizations managed by the active AURA workspace.

This helper exposes identity only. The active model/harness resolves natural-language
references to an organization; AURA verifies the chosen business_id and preserves
business isolation.
"""
from _common import business_directory
import argparse,json


def main():
    ap=argparse.ArgumentParser(description='List AURA-managed organizations in the active workspace.')
    ap.add_argument('--json',action='store_true',help='Return the directory as JSON.')
    a=ap.parse_args();rows=business_directory()
    if a.json:
        print(json.dumps({'organizations':rows},indent=2,ensure_ascii=False));return
    if not rows:
        print('(none)');return
    for row in rows:
        print(f"{row['name']}\t{row['id']}")


if __name__=='__main__':main()
