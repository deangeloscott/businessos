#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re, sys, urllib.request, urllib.error

ROOT=Path(__file__).resolve().parents[1]
POLICY=ROOT/'deployment/update-policy.json'
VERSION=ROOT/'VERSION'
INSTALL=ROOT/'INSTALLATION.json'


def load_json(path):
    return json.loads(path.read_text())


def version_tuple(value):
    value=value.strip().lstrip('vV')
    m=re.match(r'^(\d+)\.(\d+)\.(\d+)', value)
    return tuple(map(int,m.groups())) if m else None


def main():
    ap=argparse.ArgumentParser(description='Check the official ViralTrac AURA GitHub Releases channel for a newer stable release. No business/workspace data is uploaded and no update is installed.')
    ap.add_argument('--force',action='store_true',help='Perform one check even when recurring update checks are disabled.')
    ap.add_argument('--json',action='store_true',help='Print machine-readable JSON.')
    ap.add_argument('--timeout',type=int,default=10,help='Network timeout in seconds (default: 10).')
    a=ap.parse_args()

    policy=load_json(POLICY)
    current=VERSION.read_text().strip()
    result={
        'format_version':'1.0',
        'product':'ViralTrac AURA',
        'current_version':current,
        'enabled':bool(policy.get('enabled',False)),
        'source':policy.get('source'),
        'repository':policy.get('repository'),
        'checked':False,
        'update_available':None,
        'latest_version':None,
        'release_url':None,
        'asset_names':[],
        'privacy':{
            'business_data_transmitted':False,
            'auto_download':False,
            'auto_install':False,
            'note':'Only GitHub release metadata is requested. GitHub still receives ordinary HTTPS connection metadata.'
        }
    }
    if not policy.get('enabled',False) and not a.force:
        result['status']='disabled'
        result['message']='Update checks are disabled. Use --force for a one-time check or scripts/set_update_policy.py --enable to opt in.'
        print(json.dumps(result,indent=2) if a.json else result['message'])
        return 0

    url=policy.get('latest_release_api')
    if not url:
        result['status']='not_configured'; result['message']='No official update source is configured.'
        print(json.dumps(result,indent=2) if a.json else result['message'])
        return 2
    req=urllib.request.Request(url,headers={
        'Accept':'application/vnd.github+json',
        'User-Agent':'ViralTrac-AURA-Update-Checker',
        'X-GitHub-Api-Version':'2022-11-28',
    })
    try:
        with urllib.request.urlopen(req,timeout=max(1,a.timeout)) as r:
            payload=json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        result['status']='unavailable'; result['message']=f'Official GitHub release metadata is unavailable (HTTP {e.code}).'
        print(json.dumps(result,indent=2) if a.json else result['message'])
        return 3
    except Exception as e:
        result['status']='unavailable'; result['message']=f'Update check could not complete: {type(e).__name__}.'
        print(json.dumps(result,indent=2) if a.json else result['message'])
        return 3

    tag=str(payload.get('tag_name') or payload.get('name') or '').strip()
    latest=tag.lstrip('vV')
    cur_t=version_tuple(current); latest_t=version_tuple(latest)
    if not latest_t:
        result['status']='invalid_release_metadata'; result['message']='The latest release tag is not a recognized semantic version.'
        print(json.dumps(result,indent=2) if a.json else result['message'])
        return 4
    available=(latest_t>cur_t) if cur_t else (latest!=current)
    result.update({
        'checked':True,
        'status':'update_available' if available else 'current',
        'update_available':available,
        'latest_version':latest,
        'release_url':payload.get('html_url'),
        'published_at':payload.get('published_at'),
        'asset_names':[x.get('name') for x in payload.get('assets',[]) if isinstance(x,dict) and x.get('name')],
    })
    if available:
        result['message']=f'ViralTrac AURA {latest} is available; this copy is {current}. Review the release before updating. No files were downloaded or installed.'
    else:
        result['message']=f'ViralTrac AURA {current} is current on the configured stable release channel.'
    print(json.dumps(result,indent=2) if a.json else result['message'] + (f"\n{result['release_url']}" if available and result.get('release_url') else ''))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
