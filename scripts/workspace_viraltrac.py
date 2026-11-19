"""Business-scoped ViralTrac access, shared by CLI and the optional interface.

No operational data mirror, model routing or shared credentials. The remote
manifest and MCP tools remain authoritative; existing AURA records hold meaning.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

from _common import object_index, workspace_root, workspace_scope, PRODUCT_ROOT
from _native_secrets import NativeSecrets
from workspace_connections import Connections
from workspace_startup import state_dir

API = 'https://api.viraltrac.com'
DASHBOARD = 'https://app.viraltrac.com'


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # Never forward an authorization header to another origin.


def origin(value):
    parsed = urlsplit(value)
    if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('', '/'):
        raise ValueError('Use a service origin without a path, credentials or query.')
    if parsed.scheme != 'https' and not (parsed.scheme == 'http' and parsed.hostname in ('127.0.0.1', 'localhost')):
        raise ValueError('ViralTrac requires HTTPS (or loopback for local development).')
    if not parsed.hostname:
        raise ValueError('Choose a valid ViralTrac service.')
    return value.rstrip('/')


def business(bid):
    return next((obj for obj, _ in object_index(bid).values() if obj['object_type'] == 'Business'), None) or _missing()


def _missing():
    raise ValueError('Choose an existing AURA business.')


def association(bid):
    return business(bid).get('extensions', {}).get('viraltrac', {})


def store(bid):
    business(bid)
    ident = hashlib.sha256((str(Path(workspace_root()).resolve()) + '\0' + bid).encode()).hexdigest()
    vault = Connections(state_dir() / 'viraltrac' / ident)
    vault.native = NativeSecrets('com.viraltrac.aura.viraltrac.' + ident)
    return vault


def request(api, token, path, body=None):
    api = origin(api)
    if not path.startswith('/') or path.startswith('//'):
        raise ValueError('Use a relative ViralTrac API path.')
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json, text/event-stream',
               'Content-Type': 'application/json', 'MCP-Protocol-Version': '2025-11-25'}
    try:
        with build_opener(NoRedirect()).open(Request(api + path, data=None if body is None else json.dumps(body).encode(), headers=headers), timeout=45) as response:
            raw = response.read(8 * 1024 * 1024 + 1)
            if len(raw) > 8 * 1024 * 1024:
                raise ValueError('The result is too large. Request a smaller reporting period or page.')
            return json.loads(raw) if raw else {}
    except HTTPError as error:
        if error.code in (401, 403):
            raise ValueError('ViralTrac access is unavailable or not permitted. Reconnect or check your role and data permissions.') from None
        raise ValueError('ViralTrac returned HTTP ' + str(error.code) + '. Retry or check its status.') from None
    except (URLError, TimeoutError):
        raise ValueError('ViralTrac could not be reached. Saved AURA knowledge is still available; retry later.') from None


def connect(bid, token, api=API, expected_org=None, persist=True):
    if not isinstance(token, str) or not token or len(token) > 8192 or any(c.isspace() for c in token):
        raise ValueError('Provide a complete token through stdin or the pairing window.')
    api = origin(api)
    manifest = request(api, token, '/v1/external-harness/manifest')
    target = manifest.get('org_id')
    if not isinstance(target, str) or not target:
        raise ValueError('ViralTrac did not confirm the authenticated business.')
    current = association(bid)
    if expected_org and target != expected_org:
        raise ValueError('The authorized ViralTrac business does not match the business you selected.')
    if current and (current.get('organization_id') != target or current.get('api_origin') != api):
        raise ValueError('This AURA business is linked elsewhere. Unlink it explicitly before choosing a different business.')
    vault = store(bid)
    if persist and not vault.persistent:
        raise ValueError('Unlock or enable your OS keyring before pairing. No credential was saved.')
    details = manifest.get('connection') or {}
    link = {'api_origin': api, 'organization_id': target,
            'name': (details.get('organization') or {}).get('name', target)}
    from remember import remember
    previous = vault.stored() if persist else None
    if persist: vault.write({'connection': {'key': token, 'api_origin': api, 'organization_id': target}})
    try:
        remember(bid, {'objects': [{'object_ref': business(bid)['id'], 'content': {'extensions': {'viraltrac': link}}}]})
    except Exception:
        if persist: vault.write(previous)
        raise
    return {'status': 'connected' if persist else 'linked', **link, 'actor': details.get('actor', {}), 'note': 'Identity verified. Source coverage and permissions are checked when you request data.' if persist else 'Business linked without saving a secret. Supply business-scoped credentials through your process environment for headless use.'}


def credentials(bid):
    link = association(bid)
    env_token = os.environ.get('AURA_VIRALTRAC_TOKEN')
    if env_token:
        expected = {'api_origin': origin(os.environ.get('AURA_VIRALTRAC_API_ORIGIN', API)), 'organization_id': os.environ.get('AURA_VIRALTRAC_ORG_ID')}
        if not link or any(link.get(k) != expected[k] for k in expected):
            raise ValueError('The process credential is not scoped to this business. Set matching AURA_VIRALTRAC_ORG_ID and service origin, or remove the process credential.')
        actual = request(expected['api_origin'], env_token, '/v1/external-harness/manifest')
        if actual.get('org_id') != expected['organization_id']:
            raise ValueError('The process credential authorizes a different ViralTrac business.')
        return link, env_token
    saved = store(bid).stored().get('connection') or {}
    if not link or not saved or any(link.get(k) != saved.get(k) for k in ('api_origin', 'organization_id')):
        raise ValueError('Sign in to ViralTrac for this AURA business on this computer.')
    return link, saved['key']


def status(bid, live=False):
    link = association(bid)
    if not link:
        return {'status': 'not_linked'}
    try:
        link, token = credentials(bid)
        if live:
            actual = request(link['api_origin'], token, '/v1/external-harness/manifest')
            if actual.get('org_id') != link['organization_id']:
                raise ValueError('The connection now refers to a different business. Reconnect.')
        return {'status': 'verified' if live else 'saved', **link}
    except ValueError as error:
        return {'status': 'reconnect', **link, 'message': str(error)}


def disconnect(bid, unlink=False):
    vault = store(bid)
    if vault.persistent: vault.write({})
    if unlink:
        from remember import remember
        obj = business(bid)
        extensions = dict(obj.get('extensions') or {})
        extensions.pop('viraltrac', None)
        remember(bid, {'objects': [{'object_ref': obj['id'], 'replace_extensions': True, 'content': {'extensions': extensions}}]})
    return {'status': 'disconnected', 'note': 'Local credential removed. Any process-environment credential must be removed at its source. Revoke the connection in ViralTrac to invalidate it everywhere. Saved findings remain.'}


def call(bid, method, params=None):
    link, token = credentials(bid)
    return request(link['api_origin'], token, '/mcp', {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params or {}})


def mcp_configuration(bid):
    business(bid)
    return {'command': sys.executable, 'args': [str(PRODUCT_ROOT / 'scripts/workspace_viraltrac.py'),
            '--workspace', str(workspace_root()), '--business-id', bid, 'mcp']}


def session_servers(bid):
    """ACP v1 stdio configuration; no host-global settings or secrets are copied."""
    if not association(bid): return []
    config = mcp_configuration(bid)
    return [{'name': 'aura_viraltrac', **config, 'env': []}]


def guidance(bid):
    link = association(bid)
    if not link:
        return ''
    command = [sys.executable, str(PRODUCT_ROOT / 'scripts/workspace_viraltrac.py'), '--workspace', str(workspace_root()), '--business-id', bid]
    return '\nViralTrac business association: ' + json.dumps(link) + '. Optional authenticated CLI (argument array): ' + json.dumps(command) + '. Use discover for current capabilities, call --tool NAME --input FILE for a tool, or status --live to check access. No secrets are required in prompts. Native connected ViralTrac tools are also valid when they target this same business. Preserve source references, reporting windows, coverage and uncertainty using existing AURA records; update existing findings when appropriate.\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace')
    parser.add_argument('--business-id', required=True)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('connect'); p.add_argument('--api-origin', default=API); p.add_argument('--token-stdin', action='store_true'); p.add_argument('--expected-org'); p.add_argument('--no-store', action='store_true')
    p = sub.add_parser('pair'); p.add_argument('--api-origin', default=API); p.add_argument('--dashboard-origin', default=DASHBOARD); p.add_argument('--no-browser', action='store_true')
    p = sub.add_parser('status'); p.add_argument('--live', action='store_true')
    p = sub.add_parser('disconnect'); p.add_argument('--unlink', action='store_true')
    p = sub.add_parser('discover'); p.add_argument('--group')
    p = sub.add_parser('call'); p.add_argument('--tool', required=True); p.add_argument('--input', default='-')
    sub.add_parser('mcp')
    sub.add_parser('mcp-config')
    args = parser.parse_args()
    with workspace_scope(args.workspace or workspace_root()):
        if args.action == 'connect':
            if not args.token_stdin: parser.error('Use --token-stdin; credentials must not be command-line arguments.')
            result = connect(args.business_id, sys.stdin.read().strip(), args.api_origin, args.expected_org, not args.no_store)
        elif args.action == 'pair':
            from workspace_viraltrac_pair import pair
            result = pair(args.business_id, args.api_origin, args.dashboard_origin, not args.no_browser)
        elif args.action == 'status': result = status(args.business_id, args.live)
        elif args.action == 'disconnect': result = disconnect(args.business_id, args.unlink)
        elif args.action == 'discover': result = call(args.business_id, 'tools/list', {'tool_group': args.group} if args.group else {})
        elif args.action == 'mcp-config': result = {'mcpServers': {'viraltrac': mcp_configuration(args.business_id)}, 'note': 'Add through your host\'s supported MCP settings. This contains no credential; access is scoped to this workspace and business.'}
        elif args.action == 'call':
            payload = json.loads(sys.stdin.read() if args.input == '-' else Path(args.input).read_text(encoding='utf-8'))
            result = call(args.business_id, 'tools/call', {'name': args.tool, 'arguments': payload})
            result['aura_source'] = {**association(args.business_id), 'retrieved_at': datetime.now(timezone.utc).isoformat(),
                'tool': args.tool, 'rule': 'Reporting period, platform/account lineage, coverage and evidence handles come from the tool result. Do not infer missing values. Use existing AURA sources/measurements and update existing findings.'}
        else:
            # Thin stdio transport: the remote server remains the tool authority.
            for line in sys.stdin:
                packet = None
                try:
                    packet = json.loads(line)
                    if 'id' not in packet: continue
                    result = call(args.business_id, packet.get('method', ''), packet.get('params'))
                    result['id'] = packet['id']
                except Exception:
                    result = {'jsonrpc': '2.0', 'id': packet.get('id') if isinstance(packet, dict) else None, 'error': {'code': -32000, 'message': 'ViralTrac request failed. Check the connection with status --live.'}}
                print(json.dumps(result), flush=True)
            return
        print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    try: main()
    except (ValueError, OSError) as error:
        print(json.dumps({'status': 'error', 'message': str(error)}), file=sys.stderr)
        sys.exit(1)
