#!/usr/bin/env python3
"""Regressions for governed specialist execution and external-workspace media paths."""
from pathlib import Path
import json, os, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
BID='specialist-workspace-regression'


def require(cond,msg):
    if not cond: raise AssertionError(msg)


def run(*args,env=None,check=True):
    merged=os.environ.copy()
    if env: merged.update(env)
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,env=merged,check=check)


def main():
    adapter=(ROOT/'AGENTS.md').read_text()
    normalized=' '.join(adapter.lower().split())
    require('root `context.md`' in normalized,'AGENTS compatibility shim must defer to the authoritative AURA entry contract')
    require('executors' in normalized and 'aura contract/run lifecycle' in normalized,'host specialist skills must remain executors inside the governed AURA lifecycle')
    require('not alternate operating systems' in normalized,'host specialist skills must not become alternate operating systems around AURA')

    with tempfile.TemporaryDirectory(prefix='aura-specialist-workspace-') as tmp:
        ws=Path(tmp)/'workspace'
        (ws/'instances'/BID).mkdir(parents=True)
        env={'BUSINESSOS_WORKSPACE':str(ws)}

        created=run(SCRIPTS/'create_run.py',BID,'content.production.presentation','specialist workspace regression',env=env)
        rid=created.stdout.strip()
        require(rid.startswith('run_'),f'create_run should return a run id, got {created.stdout!r}')
        rdir=ws/'runtime/runs'/BID/rid
        require((rdir/'work').is_dir(),'create_run must create a Run-scoped work directory in the active workspace')
        require(not (ROOT/'runtime/runs'/BID/rid).exists(),'external-workspace Run state must not fall back into the product root')

        asset=ws/'instances'/BID/'assets'/'briefing.pptx'
        asset.parent.mkdir(parents=True,exist_ok=True)
        asset.write_bytes(b'opaque presentation fixture')
        surface=ws/'instances'/BID/'assets'/'briefing.claim-surface.json'
        surface.write_text(json.dumps({
            'format_version':'1.0',
            'artifact_ref':f'instances/{BID}/assets/briefing.pptx',
            'visible_text':['Specialist workspace regression claim'],
            'spoken_text':[],
            'material_visual_claims':['Illustrative presentation visual']
        },indent=2)+'\n')

        scanned=run(
            SCRIPTS/'build_claim_manifest.py',BID,str(asset),
            '--claim-surface',str(surface),env=env
        )
        payload=json.loads(scanned.stdout)
        require(payload['asset_file']==f'instances/{BID}/assets/briefing.pptx',f'claim manifest should emit a portable workspace ref, got {payload}')
        require('Specialist workspace regression claim' in payload['candidates'],f'opaque external-workspace claim surface should be scanned, got {payload}')

    print('specialist workspace execution regressions passed')


if __name__=='__main__':
    main()
