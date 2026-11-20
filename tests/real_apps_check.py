"""Real AI apps, real models: the journeys that only break with real apps. Run it when you choose (before a release),
not as part of run_all. It uses its own throwaway workspace and settings, the AI apps installed on this computer, and
each app's own default model unless you name one. Nothing it does touches your workspaces or AURA settings.

  python tests/real_apps_check.py                              every connectable app, each on its own default model
  python tests/real_apps_check.py --apps claude,codex          only these apps (the first saves, the rest recall)
  python tests/real_apps_check.py --model claude=haiku --model codex=gpt-5.6-luna --effort high   AURA's model floor

Two kinds of result:
  plumbing   connect, reply, stop, continue, recover after AURA is killed mid-reply: AURA's part. These should pass with any model.
  model      the fact was saved, and another app found it: depends on the model; read what it did when one fails.
"""
import argparse,json,os,subprocess,sys,tempfile,threading,time
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

FACT='Please remember this for our business: our delivery minimum is 12 people. Save it, then reply with just: saved.'
RECALL='What is our delivery minimum? Answer from what AURA has saved, with the number only.'
LONG='Write a detailed 2,000-word guide to running office catering orders.'


def restart_check(kind,use,timeout,note):
    """A separate AURA killed in the middle of a reply, as a crash or a closed laptop would, then started again: the
    chat should say it was interrupted and continue. Its own throwaway workspace, so nothing shares state."""
    import re,signal,socket
    with tempfile.TemporaryDirectory(prefix='aura-real-restart-') as t:
        base=Path(t);env={**os.environ,'BUSINESSOS_WORKSPACE':str(base/'workspace'),'BUSINESSOS_WORKSPACE_CONFIG':str(base/'pointer.json'),'AURA_STATE_DIR':str(base/'state'),'PYTHONUTF8':'1'}
        subprocess.run([sys.executable,str(ROOT/'scripts/setup.py'),'--organization','Restart check','--json'],env=env,capture_output=True,check=True,timeout=300)
        bid='restart-check';group={'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP} if os.name=='nt' else {'start_new_session':True}
        def start():
            with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
            proc=subprocess.Popen([sys.executable,str(ROOT/'scripts/workspace_ui.py'),'--workspace',str(base/'workspace'),'--port',str(port),'--no-open'],env=env,
                                  stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,**group)
            for _ in range(120):
                try:
                    with urlopen(f'http://127.0.0.1:{port}/',timeout=2) as r:page=r.read().decode('utf-8')
                    return proc,port,re.search(r'name="aura-token" content="([^"]+)"',page).group(1)
                except OSError:time.sleep(.5)
            raise RuntimeError('AURA did not start')
        def kill(proc):
            if os.name=='nt':subprocess.run(['taskkill','/T','/F','/PID',str(proc.pid)],capture_output=True)
            else:os.killpg(proc.pid,signal.SIGKILL)
        def request(port,token,path,data=None):
            req=Request(f'http://127.0.0.1:{port}{path}',data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json','X-Aura-Token':token})
            try:
                with urlopen(req,timeout=120) as response:return json.load(response)
            except Exception as error:  # say AURA's own reason, not just the status code
                body=getattr(error,'read',lambda:b'')().decode('utf-8','replace');raise RuntimeError(path.split('?')[0]+': '+(json.loads(body).get('error') if body.startswith('{') else str(error))) from None
        started=time.monotonic();proc,port,token=start()
        try:
            request(port,token,'/api/connect',{'kind':kind,'model':use['model'],'effort':use['effort'],'workspace_write':True})
            full={'claude':'bypassPermissions','codex':'full','omp':'yolo','hermes':'yolo','antigravity':'full'}.get(kind)
            if full:request(port,token,'/api/permissions',{'business':bid,'kind':kind,'mode':full})  # no one here to answer approvals
            job=request(port,token,'/api/chat',{'business':bid,'text':LONG,'history':[],'connection':use});time.sleep(8)
        finally:kill(proc)
        proc,port,token=start()
        try:
            # As the page does when a chat is opened after a restart: check where it stands, then offer Continue chat.
            seen=request(port,token,f"/api/chats/recovery?business={bid}&id={job['chat_id']}").get('recovery') or {}
            note(kind,'plumbing: restart noticed',seen.get('can_continue') and seen.get('state') in {'interrupted','uncertain'},seen.get('message') or seen.get('state',''),started)
            # As Continue chat does: AURA prepares the careful resume message, then it is sent.
            ready=request(port,token,'/api/chats/recovery',{'business':bid,'id':job['chat_id'],'action':'prepare','revision':seen.get('revision'),'reviewed':seen.get('state')=='uncertain'})
            started=time.monotonic();after=request(port,token,'/api/chat',{'business':bid,'text':ready.get('draft') or 'Continue.','history':[],'connection':use,'chat_id':job['chat_id']})
            end=time.monotonic()+timeout
            while time.monotonic()<end and after.get('status')=='working':
                time.sleep(2);after=request(port,token,f"/api/chat?business={bid}&id={after['id']}")
            note(kind,'plumbing: restart continues',after.get('status')=='complete',after.get('error_detail') or f"{after.get('status','')}: {after.get('progress','')} {[a.get('text') for a in (after.get('activity') or [])[-4:]]}",started)
        finally:kill(proc)


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
            print(f'{kind:<12} {check:<22} {"pass" if ok else "FAIL":<5} {detail[:600]}',flush=True)
        try:
            for kind in chosen:
                if kind not in installed:note(kind,'installed',False,'not installed or has no command on this computer');continue
                started=time.monotonic()
                try:
                    try:connection=call('/api/connect',{'kind':kind,'model':models.get(kind,''),'effort':a.effort,'workspace_write':True})
                    except RuntimeError as error:  # this model takes no separate effort level (its own default applies)
                        if 'effort' not in str(error):raise
                        connection=call('/api/connect',{'kind':kind,'model':models.get(kind,''),'effort':'','workspace_write':True})
                    preset=connection['presets'].get(kind,{});note(kind,'plumbing: connect',True,f"model {preset.get('model') or 'app default'}",started)
                except RuntimeError as error:note(kind,'plumbing: connect',False,str(error),started);continue
                use={'kind':kind,'model':preset.get('model',''),'effort':preset.get('effort','')}
                # No one is here to answer approval boxes, so each app runs with full access inside this throwaway workspace,
                # as an unattended scheduled run does. (AURA answering for its own helpers is covered by the normal tests.)
                full={'claude':'bypassPermissions','codex':'full','omp':'yolo','hermes':'yolo','antigravity':'full'}.get(kind)
                if full:app.preferences.setdefault('harness_permissions',{})[kind]=full;app.save_preferences()
                started=time.monotonic();text=FACT if saved_by is None else RECALL
                job=wait(call('/api/chat',{'business':bid,'text':text,'history':[],'connection':use}),a.timeout)
                pending=[r for r in job.get('requests') or [] if r.get('status','pending')=='pending']
                waiting='; '.join(str(r.get('title') or 'a question')+(' '+' '.join(str(r.get('detail')).split())[:400] if r.get('detail') else '') for r in pending)
                note(kind,'plumbing: reply',job['status']=='complete',job.get('error_detail') or (f'waiting for the person: {waiting}' if waiting else job['status']),started,job)
                if job['status']!='complete':continue
                if saved_by is None:
                    from _common import object_index
                    said=lambda o:' '.join(str(o.get(k) or '') for k in ('statement','name','description','decision','title'))  # the fact itself, not a quote of the message
                    facts=[o for o,_ in object_index(bid).values() if '12' in said(o) and o.get('object_type')!='SourceRecord']
                    note(kind,'model: saved the fact',bool(facts),', '.join(sorted({o['object_type'] for o in facts})) or 'nothing saved with the number',started,job)
                    if facts:saved_by=kind
                    started=time.monotonic();long=call('/api/chat',{'business':bid,'text':LONG,'history':[],'connection':use});time.sleep(4)
                    call('/api/chat/stop',{'business':bid,'id':long['id']});stopped=wait(long,60)
                    note(kind,'plumbing: stop',stopped['status'] in {'stopped','complete'},stopped['status'],started,stopped)
                    started=time.monotonic();after=wait(call('/api/chat',{'business':bid,'text':'Reply with: ok','history':[],'connection':use,'chat_id':long['chat_id']}),a.timeout)
                    note(kind,'plumbing: continue',after['status']=='complete',after.get('error_detail') or after['status'],started,after)
                    try:restart_check(kind,use,a.timeout,note)
                    except Exception as error:note(kind,'plumbing: restart',False,str(error))
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
