"""The example business: invented, labelled, built through the normal validated helpers, and kept apart from real workspaces."""
import json,os,re,subprocess,sys,tempfile,threading,urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
SEED=ROOT/'examples/harbor-pine-bakery'


def main():
    # The seed itself keeps the truth rules: no web links, no fixed dates, and every file says it is made up.
    raw=(SEED/'example.json').read_text(encoding='utf-8');seed=json.loads(raw)
    assert '(example)' in seed['name'] and 'made-up' in seed['description'].lower().replace('made up','made-up')
    assert not re.search(r'https?://',raw),'example evidence is local files, never web links'
    assert not re.search(r'\b20\d\d-\d\d-\d\d',raw),'dates in the seed are relative to the day it is built'
    files=[p for p in (SEED/'files').rglob('*') if p.is_file()]
    assert len(files)>=12,'the example needs its source files and sample results'
    for path in files:
        text=path.read_text(encoding='utf-8')
        assert re.search(r'made[- ]up|invented|fictional',text[:1500],re.I) and re.search(r'example',text[:1500],re.I),f'{path.name} must say it is part of the made-up example'
        assert not re.search(r'https?://',text),f'{path.name} must not link to the web'
        if path.suffix=='.html':assert not re.search(r'<script|<link|src=|@import|url\(',text,re.I),f'{path.name} must be self-contained'
    assert (SEED/'README.md').is_file()

    with tempfile.TemporaryDirectory(prefix='aura-example-') as t,patch.dict(os.environ):
        base=Path(t);home=base/'home';home.mkdir()
        env=dict(os.environ,AURA_STATE_DIR=str(base/'state'),PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
        for key in ('BUSINESSOS_WORKSPACE','BUSINESSOS_WORKSPACE_CONFIG','BUSINESSOS_BUSINESS_ID'):env.pop(key,None)
        build=lambda target:subprocess.run([sys.executable,str(ROOT/'scripts/workspace_example.py'),'build','--destination',str(target)],env=env,capture_output=True,text=True)

        # It builds cleanly through the same helpers real work uses, and validates like any other business.
        import workspace_example as example
        target=example.free_folder(home);assert target.name=='Example - Harbor Pine Bakery'
        done=build(target);assert done.returncode==0,done.stderr[-2000:]
        built=json.loads(done.stdout);bid=built['business_id'];assert built['records']>=150,built
        marker=json.loads((target/example.MARKER).read_text(encoding='utf-8'));assert marker['business_id']==bid and marker['example']=='harbor-pine-bakery'
        check=subprocess.run([sys.executable,str(ROOT/'scripts/validate_business.py'),bid,'--require-context'],env=dict(env,BUSINESSOS_WORKSPACE=str(target),BUSINESSOS_WORKSPACE_CONFIG=str(target/'.businessos/workspace.json')),capture_output=True,text=True)
        assert check.returncode==0 and 'Errors: 0' in check.stdout,check.stdout[-1500:]

        # The summary reads like a business in mid-week, and says it is an example.
        out=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_summary.py'),'--workspace',str(target),'--business-id',bid],env=env,capture_output=True,text=True,check=True)
        s=json.loads(out.stdout);k=s['knowledge']
        assert s['business']['example'] is True and not s['empty']
        assert 36<=k['findings']<=46 and k['by_status']['challenged']==2 and k['by_status']['needs_review']>=2 and k['by_status']['unverified']>=5,k['by_status']
        assert sum(1 for a in k['by_area'] if a['findings'])>=8,'findings should cover every operating area'
        assert k['reviewed']['with_date']>=25 and k['reviewed']['recent']>=15,k['reviewed']
        assert s['totals']['watches']==4 and s['totals']['goals']==3 and s['totals']['agents']==4 and s['totals']['attention']==3 and s['totals']['results']>=6,s['totals']
        assert all(isinstance(g.get('latest'),(int,float)) for g in s['goals']),'every example goal shows a recorded number'
        assert any(c['kind']=='challenged' for c in s['changes']) and any(c.get('collection')=='Local competitors' for c in s['changes']),s['changes']
        assert s['deadlines'] and 0<=s['deadlines'][0]['days']<=7
        words=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_summary.py'),'--workspace',str(target),'--business-id',bid,'--text'],env=env,capture_output=True,text=True,check=True).stdout
        assert "This is AURA's example business. Everything in it is made up." in words

        # Its sample results exist as saved files, and its competitors can be drawn on a map.
        work=target/'attachments'/bid/'work'
        for name in ('landing-page.html','newsletter.md','competitor-brief.md','grant-application-draft.md','proof-page.html','social-carousel.md'):assert (work/'outputs'/name).is_file(),name
        rows=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_views.py'),'rows','--workspace',str(target),'--business-id',bid,'--id',next(w['id'] for w in s['watches'] if w['name']=='Local competitors')],env=env,capture_output=True,text=True,check=True)
        placed=[r for r in json.loads(rows.stdout)['items'] if 'lat' in r];assert len(placed)==5 and sum(bool(r['fields'].get('yours')) for r in placed)==1

        # It never builds into a folder that has something in it, and a failed build leaves nothing behind.
        again=build(target);assert again.returncode!=0 and 'already has something in it' in again.stderr
        assert build(ROOT/'instances'/'x').returncode!=0
        assert [e['path'] for e in example.existing(home)]==[str(target)] and example.free_folder(home).name=='Example - Harbor Pine Bakery (2)'

        # From the interface it opens in its own workspace, is reused the next time, and asks no setup questions.
        os.environ.update(BUSINESSOS_WORKSPACE=str(base/'mine'),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'),AURA_WORKSPACES_HOME=str(home))
        from setup import setup
        setup(organization='My real shop')
        from workspace_ui import Workspace,handler_for
        app=Workspace();server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));port=server.server_port
        threading.Thread(target=server.serve_forever,daemon=True).start()
        def call(route,data=None):
            request=urllib.request.Request(f'http://127.0.0.1:{port}{route}',data=None if data is None else json.dumps(data).encode(),
                                           headers={'X-Aura-Token':app.token,'Content-Type':'application/json'})
            with urllib.request.urlopen(request,timeout=120) as response:return json.loads(response.read())
        try:
            opened=call('/api/example',{})
            assert opened['built'] is False,'an example that already exists is reused, not rebuilt'
            state=call('/api/state')
            assert Path(state['workspace']).resolve()==target.resolve() and state['business_id']==bid and state['onboarding']['seen'] is True
            assert call(f'/api/summary?business={bid}')['business']['example'] is True
            assert not (base/'mine'/'instances'/bid).exists(),'the example never lands inside a real workspace'
        finally:server.shutdown();server.server_close()
    print('workspace example: ok')


if __name__=='__main__':main()
