"""Optional real-browser regression for AURA pairing, first report and refresh.

Uses a temporary workspace and synthetic HTTP provider/approval page. Install
Playwright separately, or set AURA_PLAYWRIGHT_MODULE to its module directory.
Run: python tests/workspace_viraltrac_browser.py
The ViralTrac dashboard's own approval UI is covered in its component tests.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def main():
    with tempfile.TemporaryDirectory(prefix='aura-viraltrac-browser-') as folder, patch.dict(os.environ):
        base = Path(folder)
        os.environ.update(AURA_STATE_DIR=str(base / 'state'), BUSINESSOS_WORKSPACE=str(base / 'workspace'),
                          BUSINESSOS_WORKSPACE_CONFIG=str(base / 'pointer.json'))
        for key in ('AURA_VIRALTRAC_TOKEN', 'AURA_VIRALTRAC_ORG_ID', 'AURA_VIRALTRAC_API_ORIGIN', 'AURA_PRODUCER'):
            os.environ.pop(key, None)
        class Remote(BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def send(self, body, kind='application/json'):
                self.send_response(200); self.send_header('Content-Type', kind); self.end_headers()
                self.wfile.write((body if isinstance(body, str) else json.dumps(body)).encode())
            def do_GET(self):
                if self.path.startswith('/settings/api-access?'):
                    query = parse_qs(urlsplit(self.path).query)
                    packet = {'type': 'aura-viraltrac-authorized', 'nonce': query['aura_nonce'][0],
                              'organization_id': 'org-fixture', 'token': 'synthetic-token'}
                    self.send('<button id="approve">Approve synthetic business</button><script>'
                              'document.querySelector("#approve").onclick=()=>window.opener.postMessage('
                              + json.dumps(packet) + ',' + json.dumps(query['aura_origin'][0]) + ')</script>', 'text/html')
                else:
                    self.send({'org_id': 'org-fixture', 'connection': {'organization': {'name': 'Synthetic Studio'}}})
            def do_POST(self):
                packet = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                tool, args = packet['params']['name'], packet['params']['arguments']
                data = {'summary': {'stats': {'revenue': 1400, 'conversions': 42}}} if tool == 'performance_summary' else {
                    'readiness': [{'connection_id': 'synthetic-stripe', 'platform': 'stripe', 'status': 'active'}]}
                envelope = {'ok': True, 'tool': tool, 'auth_context': {'org_id': 'org-fixture'},
                            'coverage': 'partial', 'reason_codes': ['youtube_not_connected'], 'window_applied': args, 'data': data}
                self.send({'jsonrpc': '2.0', 'id': packet['id'], 'result': {'structuredContent': {
                    'ok': True, 'tool_name': tool, 'auth_context': {'org_id': 'org-fixture'}, 'envelope': envelope}}})

        remote = ThreadingHTTPServer(('127.0.0.1', 0), Remote)
        threading.Thread(target=remote.serve_forever, daemon=True).start()
        from setup import setup
        import workspace_viraltrac as vt
        import workspace_viraltrac_pair as pairing
        from workspace_ui import Workspace, handler_for
        bid = setup(organization='Synthetic Studio')['business_id']
        class Vault:
            persistent = True
            rows = {}
            def stored(self): return self.rows
            def write(self, rows): self.rows = rows
        vault = Vault()
        start = pairing.start
        origin = 'http://127.0.0.1:' + str(remote.server_port)
        with patch.object(vt, 'store', lambda _: vault), patch.object(pairing, 'start', lambda bid, **kw: start(bid, api=origin, dashboard=origin, **kw)):
            server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(Workspace(settings_file=base / 'preferences.json')))
            threading.Thread(target=server.serve_forever, daemon=True).start()
            try:
                url = 'http://127.0.0.1:' + str(server.server_port) + '/?connect=viraltrac&viraltrac_org=org-fixture'
                subprocess.run(['node', str(ROOT / 'tests/workspace_viraltrac_browser.cjs'), url, bid], check=True, timeout=120)
            finally:
                server.shutdown(); server.server_close()
                remote.shutdown(); remote.server_close()


if __name__ == '__main__': main()
