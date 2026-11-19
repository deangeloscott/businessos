"""Short-lived loopback pairing window; shared UI/CLI entry, no daemon or new account system."""
import html
import json
import re
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlencode
from _common import workspace_root, workspace_scope
from workspace_viraltrac import API, DASHBOARD, origin, business, connect


def start(bid, api=API, dashboard=DASHBOARD, expected_org=None, return_origin=None):
    api, dashboard = origin(api), origin(dashboard)
    if return_origin: return_origin = origin(return_origin)
    root = str(workspace_root())
    name = business(bid)['name']
    nonce = secrets.token_urlsafe(32)
    done = threading.Event()
    outcome = {}
    deadline = time.monotonic() + 600
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args): pass

        def send(self, code, value, content_type='application/json'):
            raw = value.encode() if isinstance(value, str) else json.dumps(value).encode()
            self.send_response(code)
            self.send_header('Content-Type', content_type + '; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'nonce-" + nonce + "'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def valid(self):
            return self.headers.get('Host') == host and time.monotonic() < deadline and self.path == '/' + nonce

        def do_GET(self):
            if not self.valid(): return self.send(404, {'message': 'Pairing expired. Start again from AURA or the CLI.'})
            target = dashboard + '/settings/api-access?' + urlencode({'aura_origin': local, 'aura_nonce': nonce})
            page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Connect ViralTrac</title>
<style>body{font:17px system-ui;background:#111827;color:#f3f4f6;max-width:36rem;margin:10vh auto;padding:24px;line-height:1.6}button{font:inherit;padding:12px 20px;border:0;border-radius:8px;background:#a5b4fc;color:#111827;cursor:pointer}button:disabled{opacity:.5}</style>
<h1>Connect ViralTrac</h1><p>Link <strong>NAME</strong> to the business you authorize in ViralTrac. Your sign-in stays on this computer.</p><button id="open">Continue to ViralTrac</button><p id="status" role="status">Choose the intended business in ViralTrac before approving.</p>
<script nonce="NONCE">let popup;const button=document.querySelector('#open'),status=document.querySelector('#status');button.onclick=()=>{popup=window.open(TARGET,'viraltrac-pair');if(!popup)status.textContent='Allow the sign-in window, then try again.';};
window.addEventListener('message',async event=>{if(event.origin!==REMOTE||event.source!==popup||event.data?.nonce!==NONCEJSON||event.data?.type!=='aura-viraltrac-authorized')return;button.disabled=true;status.textContent='Checking the business and saving your connection…';try{const response=await fetch(location.pathname,{method:'POST',headers:{'Content-Type':'application/json','X-Aura-Pair':NONCEJSON},body:JSON.stringify({token:event.data.token,organization_id:event.data.organization_id})});const result=await response.json();if(!response.ok)throw Error(result.message);status.textContent='Connected to '+result.name+'. You can close this window and continue in AURA or your AI app.';popup.postMessage({type:'aura-viraltrac-saved',nonce:NONCEJSON},REMOTE);}catch(error){status.textContent=error.message;button.disabled=false;}});</script></html>'''
            if return_origin:
                page = page.replace("popup.postMessage({type:'aura-viraltrac-saved'", "window.opener?.postMessage({type:'aura-viraltrac-connected'}," + json.dumps(return_origin) + ");popup.postMessage({type:'aura-viraltrac-saved'")
            values = {'NAME': html.escape(name), 'NONCEJSON': json.dumps(nonce), 'NONCE': nonce,
                      'TARGET': json.dumps(target), 'REMOTE': json.dumps(dashboard)}
            page = re.sub(r'NAME|NONCEJSON|NONCE|TARGET|REMOTE', lambda match: values[match.group()], page)
            self.send(200, page, 'text/html')

        def do_POST(self):
            if not self.valid() or self.headers.get('Origin') != local or self.headers.get('X-Aura-Pair') != nonce:
                return self.send(403, {'message': 'Start pairing from AURA again.'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 16384: raise ValueError('Invalid pairing response.')
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict): raise ValueError('Invalid pairing response. Start pairing again.')
                if expected_org and body.get('organization_id') != expected_org:
                    raise ValueError('Choose the ViralTrac business you started connecting, or start a new connection from AURA.')
                with lock:
                    if done.is_set(): raise ValueError('Pairing already completed.')
                    with workspace_scope(root):
                        result = connect(bid, body.get('token'), api, body.get('organization_id'))
                    outcome.update(result)
                    self.send(200, result)
                    done.set()
            except ValueError as error:
                self.send(400, {'message': str(error)})
            except OSError:
                self.send(400, {'message': 'Connection could not be saved. Check your local file permissions and OS keyring, then retry.'})

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    host = '127.0.0.1:' + str(server.server_address[1])
    local = 'http://' + host
    threading.Thread(target=server.serve_forever, daemon=True).start()
    def close():
        done.wait(600)
        server.shutdown()
        server.server_close()
    threading.Thread(target=close, daemon=True).start()
    return {'url': local + '/' + nonce, 'expires_in_seconds': 600}, done, outcome


def pair(bid, api=API, dashboard=DASHBOARD, browser=True):
    info, done, outcome = start(bid, api, dashboard)
    print(json.dumps(info), flush=True)
    if browser: webbrowser.open(info['url'])
    if not done.wait(600): raise ValueError('Pairing expired. Run pair again; no connection was saved.')
    return outcome
