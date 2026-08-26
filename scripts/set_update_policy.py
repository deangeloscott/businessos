#!/usr/bin/env python3
from pathlib import Path
import argparse, json

ROOT=Path(__file__).resolve().parents[1]
POLICY=ROOT/'deployment/update-policy.json'

def main():
    ap=argparse.ArgumentParser(description='Opt in or out of metadata-only ViralTrac AURA stable-release checks.')
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--enable',action='store_true')
    g.add_argument('--disable',action='store_true')
    a=ap.parse_args()
    d=json.loads(POLICY.read_text())
    d['enabled']=bool(a.enable)
    POLICY.write_text(json.dumps(d,indent=2)+'\n')
    print('Update checks enabled.' if a.enable else 'Update checks disabled.')
    print('No auto-download or auto-install is enabled.')

if __name__=='__main__': main()
