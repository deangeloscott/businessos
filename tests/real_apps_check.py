"""Real AI apps, real models: the journeys that only break with real apps. Run it when you choose (before a release),
not as part of run_all. It uses its own throwaway workspace and settings, the AI apps installed on this computer, and
each app's own default model unless you name one. Nothing it does touches your workspaces or AURA settings.

  python tests/real_apps_check.py                              every connectable app, each on its own default model
  python tests/real_apps_check.py --apps claude,codex          only these apps (the first saves, the rest recall)
  python tests/real_apps_check.py --model claude=haiku --model codex=gpt-5.6-luna --effort high   AURA's model floor

Two kinds of result:
  plumbing   connect, reply, stop, continue: AURA's part. These should pass with any model.
  model      the fact was saved, and another app found it: depends on the model; read what it did when one fails.
"""
import argparse,json,os,sys,tempfile,threading,time
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

FACT='Please remember this for our business: our delivery minimum is 12 people. Save it, then reply with just: saved.'
RECALL='What is our delivery minimum? Answer from what AURA has saved, with the number only.'
LONG='Write a detailed 2,000-word guide to running office catering orders.'


def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--apps',default='',help='comma-separated app ids, in order; the first saves the fact')
    ap.add_argument('--model',action='append',default=[],help='app=model, e.g. claude=haiku')
    ap.add_argument('--effort',default='',help='effort or reasoning level for every app, where the app supports it')
    ap.add_argument('--timeout',type=int,default=900,help='seconds to wait for one reply (local models can be slow)')
    a=ap.parse_args();models=dict(m.split('=',1) for m in a.model)
    with tempfile.TemporaryDirectory(prefix='aura-real-apps-') as t:
        base=Path(t)
        os.environ.update(BUSINESSOS_WORKSPACE=str(base/'workspace'),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        from setup import setup
        import workspace_ui
        bid=setup(organization='Real apps check')['business_id']
        app=workspace_ui.Workspace();app.remember_workspace()
        server=ThreadingHTTPServer(('127.0.0.1',0),workspace_ui.handler_for(app));threading.Thread(target=server.serve_forever,daemon=True).start()
        def call(path,data):
            req=Request(f'http://127.0.0.1:{server.server_port}{path}',data=json.dumps(data).encode(),headers={'Content-Type':'application/json','X-Aura-Token':app.token})
            try:
                with urlopen(req,timeout=120) as response:return json.load(response)
            except Exception as error:
                body=getattr(error,'read',lambda:b'')().decode('utf-8','replace');raise RuntimeError(json.loads(body).get('error') if body.startswith('{') else str(error)) from None
        def wait(job,seconds):
            end=time.monotonic()+seconds
            while time.monotonic()<end and app.jobs[job['id']]['status']=='working':time.sleep(.5)
            with app.lock:return dict(app.jobs[job['id']])
        installed=[x['id'] for x in workspace_ui.installed_agents() if x.get('argv')]
        chosen=[k for k in (a.apps.split(',') if a.apps else installed) if k]
        rows=[];saved_by=None
        def note(kind,check,ok,detail='',started=None,job=None):
            usage=(job or {}).get('usage') or {};tokens=(usage.get('input_tokens') or 0)+(usage.get('output_tokens') or 0)
            rows.append((kind,check,'pass' if ok else 'FAIL',f'{time.monotonic()-started:.0f}s' if started else '',f'{tokens:,} tokens' if tokens else '',detail[:160]))
            print(f'{kind:<12} {check:<22} {"pass" if ok else "FAIL":<5} {detail[:120]}',flush=True)
        try:
            for kind in chosen:
                if kind not in installed:note(kind,'installed',False,'not installed or has no command on this computer');continue
                started=time.monotonic()
                try:
                    connection=call('/api/connect',{'kind':kind,'model':models.get(kind,''),'effort':a.effort,'workspace_write':True})
                    preset=connection['presets'].get(kind,{});note(kind,'plumbing: connect',True,f"model {preset.get('model') or 'app default'}",started)
                except RuntimeError as error:note(kind,'plumbing: connect',False,str(error),started);continue
                use={'kind':kind,'model':preset.get('model',''),'effort':preset.get('effort','')}
                started=time.monotonic();text=FACT if saved_by is None else RECALL
                job=wait(call('/api/chat',{'business':bid,'text':text,'history':[],'connection':use}),a.timeout)
                note(kind,'plumbing: reply',job['status']=='complete',job.get('error_detail') or job['status'],started,job)
                if job['status']!='complete':continue
                if saved_by is None:
                    from _common import object_index
                    facts=[o for o,_ in object_index(bid).values() if '12' in json.dumps(o) and o.get('object_type')!='SourceRecord']
                    note(kind,'model: saved the fact',bool(facts),', '.join(sorted({o['object_type'] for o in facts})) or 'nothing saved with the number',started,job)
                    if facts:saved_by=kind
                    started=time.monotonic();long=call('/api/chat',{'business':bid,'text':LONG,'history':[],'connection':use});time.sleep(4)
                    call('/api/chat/stop',{'business':bid,'id':long['id']});stopped=wait(long,60)
                    note(kind,'plumbing: stop',stopped['status'] in {'stopped','complete'},stopped['status'],started,stopped)
                    started=time.monotonic();after=wait(call('/api/chat',{'business':bid,'text':'Reply with: ok','history':[],'connection':use,'chat_id':long['chat_id']}),a.timeout)
                    note(kind,'plumbing: continue',after['status']=='complete',after.get('error_detail') or after['status'],started,after)
                else:
                    reply=str(job.get('reply') or '')
                    note(kind,'model: found the fact','12' in reply,reply.strip().replace('\n',' ')[:120],started,job)
        finally:
            for running in app.running_jobs():app.stop_chat(bid,running['id'])
            app.native_sessions.close();server.shutdown();server.server_close()
        failed=[r for r in rows if r[2]=='FAIL']
        print(f"\n{len(rows)-len(failed)} passed, {len(failed)} failed"+(f" ({sum(r[1].startswith('plumbing') for r in failed)} plumbing)" if failed else ''))
        size=(ROOT/'CONTEXT.md').stat().st_size;print(f'CONTEXT.md is {size:,} bytes; every AI reads it, so keep it lean.')
        raise SystemExit(1 if any(r[1].startswith('plumbing') for r in failed) else 0)


if __name__=='__main__':main()
