"""Real local HTTP + isolated workspace: pairing, tenancy, credentials and CLI access."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from _common import workspace_scope
from setup import setup
import workspace_viraltrac as vt
from workspace_viraltrac_pair import start


def main():
    active = {'revoked': False, 'revenue': 100, 'coverage': 'full', 'calls': []}
    class Remote(BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def respond(self, body, code=200):
            self.send_response(code); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps(body).encode())
        def do_GET(self):
            if active['revoked']: return self.respond({}, 401)
            target = 'org-b' if self.headers.get('Authorization') == 'Bearer fixture-b' else 'org-a'
            self.respond({'org_id': target, 'connection': {'organization': {'id': target, 'name': target}, 'actor': {'user_id': 'fixture-user'}}})
        def do_POST(self):
            if active['revoked']: return self.respond({}, 401)
            packet = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            result = {'tools': [{'name': 'performance_summary', 'inputSchema': {'type': 'object'}}]} if packet['method'] == 'tools/list' else {'content': [{'type': 'text', 'text': 'fixture result'}]}
            if packet['method'] == 'initialize':
                result = {'protocolVersion': '2025-11-25', 'capabilities': {'tools': {}}, 'serverInfo': {'name': 'Synthetic ViralTrac', 'version': '1.0'}}
            if packet['method'] == 'tools/call':
                args = packet['params']['arguments']; tool = packet['params']['name']
                active['calls'].append((tool, args))
                envelope = {'ok': True, 'tool': tool, 'auth_context': {'org_id': 'org-a'},
                    'coverage': active['coverage'], 'reason_codes': [], 'window_applied': args,
                    'request_id': str(len(active['calls'])),
                    'data': {'summary': {'stats': {'revenue': active['revenue']}}, 'source_scope': {'source_platform': 'stripe', 'source_ids': ['account-fixture']}} if tool == 'performance_summary' else {'summary': {'total_connections': 1}, 'readiness': [{'connection_id': 'connection-fixture', 'platform': 'stripe', 'status': 'active', 'reauth_required': False, 'last_checked_at': str(len(active['calls']))}]}}
                result = {'structuredContent': {'ok': True, 'tool_name': tool, 'auth_context': {'org_id': 'org-a', 'user_id': 'fixture-user'}, 'envelope': envelope}}
            self.respond({'jsonrpc': '2.0', 'id': packet['id'], 'result': result})
    remote = ThreadingHTTPServer(('127.0.0.1', 0), Remote)
    threading.Thread(target=remote.serve_forever, daemon=True).start()
    api = 'http://127.0.0.1:' + str(remote.server_address[1])
    try:
        with tempfile.TemporaryDirectory(prefix='aura-viraltrac-') as folder, patch.dict(os.environ):
            os.environ['AURA_STATE_DIR'] = str(Path(folder) / 'state')
            os.environ['BUSINESSOS_WORKSPACE_CONFIG'] = str(Path(folder) / 'pointer.json')
            root = Path(folder) / 'workspace'
            with workspace_scope(root):
                bid = setup(organization='Pairing fixture NAME NONCE TARGET REMOTE')['business_id']
                # Secure storage is real on supported platforms; test portable logic with
                # a temporary in-memory keyring where an OS keyring is unavailable.
                vaults = {}
                class Vault:
                    persistent = True
                    def stored(self): return vaults.get(bid, {})
                    def write(self, rows): vaults[bid] = rows
                actual_store = vt.store
                use_native = actual_store(bid).persistent
                with patch.object(vt, 'store', actual_store if use_native else lambda _: Vault()):
                    assert vt.status(bid)['status'] == 'not_linked'
                    info, done, outcome = start(bid, api, api)
                    page = urlopen(info['url']).read().decode()
                    assert 'Pairing fixture NAME NONCE TARGET REMOTE' in page and 'fixture-a' not in page
                    nonce = info['url'].rsplit('/', 1)[1]
                    local = info['url'].rsplit('/', 1)[0]
                    body = json.dumps({'token': 'fixture-a', 'organization_id': 'org-a'}).encode()
                    try:
                        urlopen(Request(info['url'], data=body, headers={'Origin': 'https://attacker.invalid', 'X-Aura-Pair': nonce}))
                        raise AssertionError('wrong origin accepted')
                    except HTTPError as error: assert error.code == 403
                    result = json.load(urlopen(Request(info['url'], data=body, headers={'Origin': local, 'X-Aura-Pair': nonce})))
                    assert result['status'] == 'connected' and done.wait(2)
                    assert vt.status(bid, True)['status'] == 'verified'
                    assert vt.call(bid, 'tools/list')['result']['tools'][0]['name'] == 'performance_summary'
                    from workspace_viraltrac_report import comparable, report, reports, saved_report
                    for values in ({'start': []}, {'end': 12}, {'source': {}}, {'start': ''}, {'end': 'not-a-date'}):
                        try: report(bid, **values)
                        except ValueError: pass
                        else: raise AssertionError('invalid report input accepted: ' + repr(values))
                    assert saved_report({'object_type': 'SourceRecord', 'extensions': {'viraltrac_report': {'arguments': {}}}}) is None
                    readings = {'readiness': {'data': {'readiness': [
                        {'connection_id': 'b', 'last_checked_at': 'today'},
                        {'connection_id': 'a', 'last_checked_at': 'today'}]}}}
                    reordered = {'readiness': {'data': {'readiness': [
                        {'connection_id': 'a', 'last_checked_at': 'later'},
                        {'connection_id': 'b', 'last_checked_at': 'later'}]}}}
                    assert comparable(readings) == comparable(reordered)
                    first = report(bid, '2026-10-01', '2026-10-31', save=True)
                    source = first['source_id']
                    assert first['saved'] and first['report']['performance']['authorized_actor']['user_id'] == 'fixture-user'
                    assert report(bid, '2026-10-01', '2026-10-31', save=True)['source_id'] == source
                    assert report(bid, source=source)['status'] == 'unchanged'
                    active['revenue'] = 110
                    changed = report(bid, source=source)
                    assert changed['status'] == 'changed' and changed['source_id'] == source
                    assert changed['comparison']['before']['performance']['data']['summary']['stats']['revenue'] == 100
                    assert len(reports(bid)) == 1
                    assert active['calls'][-2] == ('performance_summary', {'start_date': '2026-10-01', 'end_date': '2026-10-31'})
                    active['coverage'] = 'degraded'
                    assert report(bid, source=source)['status'] == 'unavailable'
                    active['coverage'] = 'full'
                    assert report(bid, source=source)['status'] == 'unchanged'
                    # Existing source/measurement records preserve the reporting period,
                    # and corrections update their identity rather than duplicating them.
                    from remember import remember
                    from _common import object_index
                    remember(bid, {'objects': [
                        {'key': 'source', 'object_type': 'SourceRecord', 'content': {'source_type': 'viraltrac', 'source_reference': api + '/mcp#fixture-query', 'retrieved_at': '2026-11-19T00:00:00Z', 'access_scope': 'authorized organization', 'extensions': {'viraltrac': {'organization_id': 'org-a', 'platforms': ['website', 'stripe'], 'request_id': 'fixture-query', 'coverage': 'partial'}}}},
                        {'key': 'metric', 'object_type': 'MetricDefinition', 'content': {'name': 'Revenue', 'unit': 'USD', 'direction': 'informational'}},
                        {'object_type': 'MetricObservation', 'content': {'metric_ref': '@metric', 'source_ref': '@source', 'window_start': '2026-10-01T00:00:00Z', 'window_end': '2026-11-01T00:00:00Z', 'value': 100}},
                    ]})
                    observation = next(obj for obj, _ in object_index(bid).values() if obj['object_type'] == 'MetricObservation')
                    remember(bid, {'objects': [{'object_ref': observation['id'], 'correction_summary': 'Provider restated the same reporting period.', 'content': {'value': 110}}]})
                    updated = [obj for obj, _ in object_index(bid).values() if obj['object_type'] == 'MetricObservation']
                    assert len(updated) == 1 and updated[0]['id'] == observation['id'] and updated[0]['value'] == 110
                    assert updated[0]['window_end'] == '2026-11-01T00:00:00Z'
                    try: vt.connect(bid, 'fixture-b', api)
                    except ValueError as error: assert 'linked elsewhere' in str(error)
                    else: raise AssertionError('cross-business credential accepted')
                    assert vt.credentials(bid)[1] == 'fixture-a'
                    other = setup(organization='Separate client')['business_id']
                    assert vt.status(other)['status'] == 'not_linked'
                    try: report(other, source=source)
                    except ValueError: pass
                    else: raise AssertionError('a second business accessed the first business report')
                    serialized = ''.join(p.read_text(errors='replace') for p in root.rglob('*.json'))
                    assert 'fixture-a' not in serialized and 'fixture-b' not in serialized
                    config = vt.mcp_configuration(bid)
                    assert 'fixture-a' not in json.dumps(config)
                    if use_native:
                        command = [config['command'], *config['args']]
                        packets = '\n'.join(json.dumps(p) for p in [
                            {'jsonrpc': '2.0', 'id': 9, 'method': 'initialize'},
                            {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
                            {'jsonrpc': '2.0', 'id': 10, 'method': 'tools/list'},
                            {'jsonrpc': '2.0', 'id': 11, 'method': 'tools/call', 'params': {'name': 'performance_summary', 'arguments': {'start_date': '2026-10-01', 'end_date': '2026-10-31'}}},
                        ]) + '\n'
                        output = subprocess.run(command, input=packets, text=True, capture_output=True, check=True)
                        messages = [json.loads(line) for line in output.stdout.splitlines()]
                        assert [m['id'] for m in messages] == [9, 10, 11]
                        assert messages[-1]['result']['structuredContent']['envelope']['data']['summary']['stats']['revenue'] == 110
                        cli = subprocess.run([sys.executable, str(ROOT / 'scripts/workspace_viraltrac.py'),
                            '--workspace', str(root), '--business-id', bid, 'report',
                            '--start', '2026-10-01', '--end', '2026-10-31', '--save'],
                            text=True, capture_output=True, check=True)
                        assert json.loads(cli.stdout)['source_id'] == source
                    active['revoked'] = True
                    assert vt.status(bid, True)['status'] == 'reconnect'
                    try: report(bid, source=source)
                    except ValueError: pass
                    else: raise AssertionError('revoked credential refreshed a report')
                    assert len(reports(bid)) == 1
                    active['revoked'] = False
                    vt.disconnect(bid)
                    assert vt.status(bid)['status'] == 'reconnect' and vt.association(bid)['organization_id'] == 'org-a'
                    with patch.dict(os.environ, {'AURA_VIRALTRAC_TOKEN': 'fixture-a', 'AURA_VIRALTRAC_ORG_ID': 'org-a', 'AURA_VIRALTRAC_API_ORIGIN': api}):
                        assert vt.status(bid, True)['status'] == 'verified'
                        os.environ['AURA_VIRALTRAC_TOKEN'] = 'fixture-b'
                        assert vt.status(bid, True)['status'] == 'reconnect'
                    vt.disconnect(bid, True)
                    assert vt.status(bid)['status'] == 'not_linked'
                    assert vt.guidance(bid) == ''
    finally:
        remote.shutdown(); remote.server_close()
    print('ViralTrac connection passed: loopback pairing, origin checks, tenant isolation, private credentials, MCP forwarding and revocation.')


if __name__ == '__main__': main()
