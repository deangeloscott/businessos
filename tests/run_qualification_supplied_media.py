#!/usr/bin/env python3
"""Regressions for maintainer-selected qualification fixtures with candidate-visible supplied media."""
from pathlib import Path
import json, os, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
PNG_MAGIC=b'\x89PNG\r\n\x1a\n'


def require(cond,msg):
    if not cond:raise AssertionError(msg)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-media-evaluator-') as td, tempfile.TemporaryDirectory(prefix='aura-workspaces-media-') as cd:
        request='Create a short product video for Northline Coffee using the supplied product reference.'
        cmd=[
            sys.executable,str(ROOT/'qualification/prepare_run.py'),
            '--profile','atomic',
            '--contract','content.production.short-video',
            '--fixture','northline-commerce',
            '--request',request,
            '--run-root',td,
            '--candidate-root',cd,
            '--run-id','media-fixture-smoke'
        ]
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env)
        require(p.returncode==0,f'prepare_run fixture/media smoke failed:\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}')
        prep=json.loads(p.stdout); rd=Path(td)/'media-fixture-smoke'; workspace=Path(prep['workspace']); product=Path(prep['product_root'])
        queue=json.loads((rd/'evaluator/queue.json').read_text())
        events=queue.get('events') or []
        require(len(events)==1,'fixture override smoke should prepare exactly one event')
        event=events[0]
        require(event.get('fixture')=='northline-commerce' and event.get('business_id')=='northline-coffee',f'fixture override did not rebind event: {event}')
        require((workspace/'instances/northline-coffee').is_dir(),'Northline business was not initialized')
        require(not (workspace/'instances/atlasops').exists(),'default AtlasOps fixture leaked into overridden run')

        supplied=workspace/'attachments/supplied'
        media=supplied/'northline-discovery-box-source.png'
        require(media.is_file() and media.stat().st_size>0,'supplied product reference image was not staged')
        require(media.read_bytes()[:8]==PNG_MAGIC,'candidate-visible supplied product reference is not a real PNG')
        require(not (supplied/'northline-discovery-box-source.png.b64').exists(),'encoded fixture representation leaked into candidate workspace')
        require(not (product/'qualification').exists(),'qualification tooling leaked into candidate product')

        business_material=json.loads((supplied/'northline-commerce.json').read_text())
        media_rows=business_material.get('supplied_media') or []
        require(len(media_rows)==1 and media_rows[0].get('filename')=='northline-discovery-box-source.png',f'candidate-visible supplied media metadata missing: {media_rows}')
        require('source' not in media_rows[0],'candidate-visible fixture metadata leaked evaluator-side source path')
        require('encoding' not in media_rows[0],'candidate-visible fixture metadata leaked maintainer storage encoding')
        require('qualification' not in json.dumps(media_rows).lower(),'candidate-visible supplied media metadata leaked qualification language')

        start=subprocess.run([sys.executable,str(ROOT/'qualification/task_controller.py'),'start',str(rd)],cwd=ROOT,capture_output=True,text=True,env=env)
        require(start.returncode==0,f'task controller start failed:\n{start.stdout}\n{start.stderr}')
        started=json.loads(start.stdout)
        require(started.get('business_id')=='northline-coffee','controller did not preserve overridden business')
        require(started.get('candidate_message')==request,'controller did not preserve ordinary candidate request')

    print('qualification supplied-media regressions passed')


if __name__=='__main__':main()
