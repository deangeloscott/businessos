"""The aura in a real browser, on a few months of made-up work: layout and camera behaviour no unit test can see.

Builds the medium sample workspace with one conversation tied to a collection, runs AURA on it, and drives an
installed Chrome or Edge (tests/workspace_world_browser.mjs). Skips, saying so, when no browser or Node is installed.
"""
import json,os,shutil,socket,subprocess,sys,tempfile,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BROWSERS={'win32':['C:/Program Files/Google/Chrome/Application/chrome.exe','C:/Program Files (x86)/Google/Chrome/Application/chrome.exe','C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','C:/Program Files/Microsoft/Edge/Application/msedge.exe'],
          'darwin':['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge']}
SEED=r'''
import json,sys
from pathlib import Path
sys.path[:0]=[sys.argv[1],sys.argv[2]]
import world_levels
built=world_levels.build(sys.argv[3],'medium')
import os;os.environ['BUSINESSOS_WORKSPACE']=built['path']
import workspace_ui,workspace_world,workspace_collections
app=workspace_ui.Workspace();bid=built['business_id']
land=next(l for l in workspace_world.world(bid)['lands'] if l['kind']=='collection')
app.preferences['chats'].append({'id':'browser-chat','business_id':bid,'workspace':built['path'],'title':'Review of '+land['name'],'agent':'Sample app','status':'complete','created':1,'updated':2})
display=Path(app.chat_display_path('browser-chat'));display.parent.mkdir(parents=True,exist_ok=True)
display.write_text(json.dumps([{'role':'user','text':'Review it.','references':[{'kind':'collection','id':land['id'],'label':land['name']}]}]),encoding='utf-8')
workspace_collections.projects.bind(bid,'chat','browser-chat',collection=land['id'])
app.preferences['connection']={'kind':'handoff'};app.preferences['seen']=list(set(app.preferences['seen']+[bid]));app.save_preferences()
print(json.dumps(built))
'''


def main():
    browser=next((b for b in BROWSERS.get(sys.platform,['/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser']) if Path(b).exists()),None)
    if not browser or not shutil.which('node'):
        print('world browser: skipped (no Chrome, Edge or Node here)');return
    with tempfile.TemporaryDirectory(prefix='aura-world-browser-') as t:
        base=Path(t);env={**os.environ,'BUSINESSOS_WORKSPACE_CONFIG':str(base/'pointer.json'),'AURA_STATE_DIR':str(base/'state')};env.pop('BUSINESSOS_WORKSPACE',None);env.pop('AURA_PRODUCER',None)
        built=json.loads(subprocess.run([sys.executable,'-c',SEED,str(ROOT/'scripts'),str(ROOT/'tests'),str(base/'w')],check=True,capture_output=True,text=True,encoding='utf-8',env=env).stdout.strip().splitlines()[-1])
        with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
        server=subprocess.Popen([sys.executable,str(ROOT/'scripts/workspace_ui.py'),'--workspace',built['path'],'--business-id',built['business_id'],'--port',str(port),'--no-open'],
                                env={**env,'BUSINESSOS_WORKSPACE':built['path']},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(150):
                try:urllib.request.urlopen(f'http://127.0.0.1:{port}/',timeout=1);break
                except OSError:time.sleep(.2)
            subprocess.run(['node',str(ROOT/'tests/workspace_world_browser.mjs'),browser,f"http://127.0.0.1:{port}/?business={built['business_id']}&view=aura"],check=True,timeout=240)
        finally:
            server.terminate()
            try:server.wait(10)
            except subprocess.TimeoutExpired:server.kill()


if __name__=='__main__':main()
