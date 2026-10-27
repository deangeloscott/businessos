#!/usr/bin/env python3
"""Optional, on-demand local view of the existing AURA workspace.

No accounts, independent memory store, or scheduler. An
optional installed command receives a request on stdin and returns text on stdout.
"""
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs, quote
import argparse
import hashlib
import json
import mimetypes
import os
import re
import secrets
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from concurrent.futures import ThreadPoolExecutor

from _common import (PRODUCT_ROOT, workspace_root, business_directory, resolve_business,
                     iter_instance_objects, describe_object, load_registry, os_version)
from remember import remember
from setup import setup
import workspace_codex
import workspace_agents
import workspace_locations
import workspace_schedules
import workspace_storage
import workspace_guidance
from configure_workspace import configure
from workspace_execution import Execution, Stopped
from workspace_connections import Connections

STATIC = PRODUCT_ROOT / 'interface'
MAX_BODY = 96 * 1024
HIDDEN = {'__pycache__', 'credentials', 'secrets', 'node_modules'}
MEDIA = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.mp4', '.webm', '.mp3', '.wav', '.ogg'}
NATIVE_AGENTS = {'codex', 'claude', 'pi', 'omp', 'hermes', 'antigravity'}


def selected(value):
    result = resolve_business(value)
    if result.get('status') != 'resolved':
        raise ValueError('Choose the business you want to open.')
    return result['business_id']


def records(bid):
    # Preserve diagnostics: an unreadable record must not silently look absent.
    diagnostics = []
    rows = []
    for obj, path in iter_instance_objects(bid, diagnostics=diagnostics):
        if not path.resolve().is_relative_to(workspace_root().resolve() / 'instances' / bid):
            diagnostics.append({'path': path.name, 'reason': 'Linked record is outside this business.'})
            continue
        if 'history' in path.relative_to(workspace_root() / 'instances' / bid).parts:
            continue
        desc = describe_object(obj, path)
        title = desc.get('title') or obj['id']
        if obj.get('object_type') == 'SourceRecord' and title == obj['id']:
            reference = obj.get('source_reference') or obj.get('source_type', 'Saved source')
            title = Path(reference).name if '/' in reference and not reference.startswith('http') else reference
        rows.append({'ref': obj['id'], 'type': obj['object_type'],
                     'title': title,
                     'path': path.relative_to(workspace_root()).as_posix(), 'data': obj})
    return rows, diagnostics


def private_path(path):
    return any(part.startswith('.') or part.lower() in HIDDEN for part in path.parts) or path.suffix.lower() in {'.key', '.pem', '.pfx', '.p12'}


def file_roots(bid):
    root = workspace_root().resolve()
    return [root / 'instances' / bid, root / 'knowledge' / bid,
            root / 'attachments' / bid, root / 'runtime' / 'runs' / bid]


def local_file(bid, ref, locations=None):
    if ref.startswith('linked/'):
        return workspace_locations.resolve(ref, locations or [], private_path)
    root = workspace_root().resolve()
    relative = Path(ref)
    if relative.is_absolute() or private_path(relative):
        raise ValueError('This file is outside the selected business view.')
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError('This file is outside the workspace.')
    for other in business_directory():
        if other['id'] != bid and path.is_relative_to(root / 'attachments' / other['id']):
            raise ValueError('This attachment belongs to another business.')
    allowed = any(path.is_relative_to(base) for base in file_roots(bid))
    if not allowed:
        # Assets may reference shared workspace attachments; never cross into
        # another business's instances, notes, or receipts.
        if path.is_relative_to(root / 'attachments'):
            rows, _ = records(bid)
            allowed = any(r['type'] == 'Asset' and
                          r['data'].get('location_reference') == relative.as_posix() for r in rows)
    if not allowed or not path.is_file():
        raise ValueError('File not found in this business workspace.')
    return path


def files(bid, locations=None):
    root = workspace_root().resolve()
    out, seen = [], set()
    rows, _ = records(bid)
    candidates = [r['data'].get('location_reference') for r in rows if r['type'] == 'Asset']
    # Bounded directory walking; do not follow directory links into other stores.
    for base in file_roots(bid):
        if not base.exists() or not base.resolve().is_relative_to(base):
            continue
        for directory, dirs, names in os.walk(base, followlinks=False):
            dirs[:] = [d for d in sorted(dirs) if not private_path(Path(d)) and
                       not (Path(directory) / d).is_symlink()]
            for name in sorted(names):
                candidates.append((Path(directory) / name).relative_to(root).as_posix())
            if len(candidates) >= 1200:
                break
    for ref in candidates:
        if not isinstance(ref, str) or ref in seen:
            continue
        try:
            path = local_file(bid, ref)
        except (ValueError, OSError):
            continue
        seen.add(ref)
        out.append({'path': ref, 'name': path.name, 'bytes': path.stat().st_size,
                    'modified': path.stat().st_mtime, 'media': path.suffix.lower() in MEDIA})
        if len(out) >= 1000:
            break
    linked = workspace_locations.entries(locations or [], private_path, MEDIA)
    return {'items': out + linked['items'], 'locations': linked['locations'],
            'limited': len(out) >= 1000 or linked['limited']}


def library():
    out = []
    for row in load_registry().get('workflows', []):
        page = PRODUCT_ROOT / row['path']
        title = next((line[2:].strip() for line in page.read_text(encoding='utf-8').splitlines() if line.startswith('# ')), '')
        out.append({'title': title or row['id'].replace('.', ' ').replace('-', ' ').title(),
                    'path': row['path'], 'kind': 'Workflow', 'area': row.get('owner_system', 'core'),
                    'id': row['id']})
    for path in sorted((PRODUCT_ROOT / 'recipes').rglob('*.md')):
        if path.name in {'README.md', 'INDEX.md', 'DIALECTS.md'}:
            continue
        title = next((s.lstrip('# ').strip() for s in path.read_text(encoding='utf-8').splitlines() if s.startswith('# ')), path.stem)
        out.append({'title': title, 'path': path.relative_to(PRODUCT_ROOT).as_posix(),
                    'kind': 'Recipe', 'area': path.parent.relative_to(PRODUCT_ROOT / 'recipes').as_posix()})
    for row in out:
        area, path = row['area'], row['path']
        if row['kind'] == 'Workflow':
            category, group = {
                'competitor-intelligence': ('Research', 'Competitors'),
                'customer-intelligence': ('Research', 'Customers'),
                'industry-intelligence': ('Research', 'Market & industry'),
                'seo-aeo': ('SEO & AEO', ''),
                'marketing-synthesis': ('Marketing', ''),
                'content-synthesis': ('Content creation', ''),
                'customer-optimization': ('Sales & customers', ''),
                'core': ('Business & operations', ''),
            }.get(area, ('Business & operations', ''))
            stage = path.split('/workflows/')[-1].split('/')[0]
            group = group or {'bootstrap':'Getting started', 'intelligence':'Research',
                              'execution':'Create & improve', 'diagnosis':'Find opportunities',
                              'monitoring':'Monitoring', 'measurement':'Measure results',
                              'learning':'Learn & improve'}.get(stage, stage.replace('-', ' ').title())
        elif 'ecommerce-image-lookbooks' in area:
            category, group = 'E-commerce', 'Product images'
            section = area.split('ecommerce-image-lookbooks', 1)[1].strip('/')
            if section and section != 'notes':
                group = re.sub(r'^\d+-', '', section).replace('-', ' ').title()
        elif area.startswith('web-design'):
            category, group = 'Websites', 'Design guidance' if area.endswith('/notes') else 'Website recipes'
        else:
            category = 'Marketing' if 'copy-messaging' in area else 'Content creation'
            group = {'audio':'Audio', 'video':'Video', 'motion-graphics':'Motion graphics',
                     'information-design':'Information design', 'copy-messaging':'Copy & messaging'}.get(
                         area.split('/')[1] if '/' in area else '', 'Creative direction')
        row.update(category=category, group=group)
    return out


def codex_command():
    executable = shutil.which('codex')
    if not executable:
        return None
    path = Path(executable)
    if os.name == 'nt' and path.suffix.lower() in {'.cmd', '.bat', '.ps1'}:
        # Invoke the official npm entry point through Node, never a command shell.
        entry = path.parent / 'node_modules' / '@openai' / 'codex' / 'bin' / 'codex.js'
        node = shutil.which('node')
        if not node or not entry.is_file():
            return None
        try:
            shim = path.read_text(encoding='utf-8', errors='replace').replace('\\', '/')
        except OSError:
            return None
        if '@openai/codex/bin/codex.js' not in shim:
            return None
        return [node, str(entry), 'exec', '--skip-git-repo-check', '-']
    return [str(path), 'exec', '--skip-git-repo-check', '-']


def installed_agents():
    """Small command adapters; models, accounts and tools remain host-owned."""
    apps = [('codex', 'Codex', ['exec', '--skip-git-repo-check', '-'], '@openai/codex/bin/codex.js'),
            ('claude', 'Claude Code', ['-p', '--output-format', 'text'], '@anthropic-ai/claude-code/cli.js'),
            ('pi', 'Pi', ['--print'], '@mariozechner/pi-coding-agent/dist/cli.js'),
            ('omp', 'OMP', ['--print'], '@oh-my-pi/pi-coding-agent/dist/cli.js'),
            ('hermes', 'Hermes', ['chat', '--query-file', '-'], ''),
            ('antigravity', 'Google (Antigravity)', ['--print'], '')]
    found = []
    for key, name, options, entry in apps:
        executable = shutil.which('agy' if key == 'antigravity' else key)
        if not executable:
            found.append({'id': key, 'name': name, 'argv': None})
            continue
        path = Path(executable)
        command = None
        if key == 'codex':
            command = codex_command()
        elif os.name != 'nt' or path.suffix.lower() == '.exe':
            command = [str(path), *options]
        elif path.suffix.lower() == '.ps1':
            # Invoke the user's actual PowerShell launcher, preserving its policy.
            powershell = shutil.which('pwsh') or shutil.which('powershell')
            if powershell:
                command = [powershell, '-NoProfile', '-NonInteractive', '-File', str(path), *options]
        elif path.suffix.lower() == '.cmd':
            # Only standard npm shims. Custom wrappers must supply their own
            # command; do not bypass a user's launcher or guess its semantics.
            target = path.parent / 'node_modules' / entry
            try:
                shim = path.read_text(encoding='utf-8', errors='replace').replace('\\', '/')
            except OSError:
                shim = ''
            node = shutil.which('node')
            if node and target.is_file() and entry in shim:
                command = [node, str(target), *options]
            else:
                # Static Python forwarding wrappers can be preserved without a
                # command shell. Unknown batch programs still need configuration.
                match = re.fullmatch(r'@echo off\s+python(?:\.exe)? "([^"\r\n]+\.py)" (pi|omp) -- %\*\s+exit /b %ERRORLEVEL%\s*', shim, re.IGNORECASE)
                python = shutil.which('python')
                if match and python and Path(match[1]).is_file():
                    command = [python, match[1], match[2], '--', *options]
                elif path.with_suffix('.ps1').is_file():
                    powershell = shutil.which('pwsh') or shutil.which('powershell')
                    if powershell:
                        command = [powershell, '-NoProfile', '-NonInteractive', '-File', str(path.with_suffix('.ps1')), *options]
        found.append({'id': key, 'name': name, 'argv': command})
    return found


SETUP_ERRORS = {
    'billing': 'Your AI provider needs credits or a billing update. Check billing or choose another connection, then try again.',
    'limit': 'Your AI account has reached a usage limit. Try another model or try again later.',
    'credentials': 'Your AI connection needs valid credentials. Check its sign-in or API key, then try again.',
    'signin': 'Your AI app needs you to sign in. Open it, sign in, and try again.',
    'model_access': 'Your account cannot use this model. Choose another model or check access with your provider.',
    'service': 'The AI service is temporarily unavailable. Try again later or choose another connection.',
    'network': 'Your AI app could not connect. Check your connection and try again.',
    'model': 'The selected model is unavailable. Refresh the model choices and choose another one.',
    'files': 'Your AI could not access this folder. Allow access in your AI app and try again.',
    'permissions': 'Your AI app denied this request. Open the app to check its permissions, then try again.',
    'unknown': 'Your AI app did not finish connecting. Open the app to check what needs attention, then try again.',
    'proof': 'Your AI replied, but AURA could not confirm workspace access. Try again or check file access in your AI app.',
}


def setup_error(message):
    """Keep onboarding brief; the native AI app retains detailed diagnostics."""
    text = message.lower()
    if message in SETUP_ERRORS.values():
        return message
    if any(word in text for word in ('payment required', 'insufficient balance', 'insufficient credits', 'out of credits', 'billing')) or re.search(r'\b402\b', text):
        return SETUP_ERRORS['billing']
    if any(word in text for word in ('quota', 'rate limit', 'rate_limit', 'resource_exhausted', 'usage limit', 'too many requests', '429')):
        return SETUP_ERRORS['limit']
    if any(word in text for word in ('invalid_grant', 'oauth refresh failed', 'refresh token expired', 'refresh token revoked', 'refresh token has already been used')):
        return SETUP_ERRORS['signin']
    if any(word in text for word in ('api key', 'api_key', 'credentials', 'unauthorized', 'authentication', '401')):
        return SETUP_ERRORS['credentials']
    if any(word in text for word in ('sign-in', 'sign in', 'login expired', 'token expired', 'token has expired')):
        return SETUP_ERRORS['signin']
    if re.search(r'permission denied:\s*[\x22\x27]?(?:[a-z]:[\\/]|[/\\])|eacces|read.only file|\b(?:file|folder|directory)\b.{0,80}(permission|denied|not readable)|(?:permission|denied).{0,80}\b(file|folder|directory)\b', text):
        return SETUP_ERRORS['files']
    if re.search(r'model.{0,100}(access|permission|denied|forbidden|not allowed)|(?:access|permission|denied|forbidden|not allowed).{0,100}model', text) or re.search(r'\b403\b', text):
        return SETUP_ERRORS['model_access']
    if any(word in text for word in ('service unavailable', 'service is unavailable', 'overloaded', 'no available endpoints', 'no endpoints found')) or re.search(r'\b50[234]\b', text):
        return SETUP_ERRORS['service']
    if any(word in text for word in ('network', 'timeout', 'timed out', 'connection', 'unreachable', 'fetch failed')):
        return SETUP_ERRORS['network']
    if re.search(r'model.{0,100}(not found|not available|unavailable|unsupported|does not exist)|(?:unsupported|unknown|unavailable) model|model_not_found', text):
        return SETUP_ERRORS['model']
    if any(word in text for word in ('permission', 'denied', 'forbidden')):
        return SETUP_ERRORS['permissions']
    return SETUP_ERRORS['unknown']


class Workspace:
    def __init__(self, agent=None, interface=None, settings_file=None):
        self.token = secrets.token_urlsafe(32)
        self.agent = agent
        self.configured_agent = agent
        self.connection_kind = 'configured' if agent else ''
        self.handoff = False
        self.static = Path(interface).resolve() if interface else STATIC
        if not all((self.static / name).is_file() for name in ('index.html', 'app.js', 'style.css')):
            raise ValueError('The interface folder needs index.html, app.js, and style.css.')
        self.lock = threading.RLock()
        self.job = None
        self.execution = None
        self.catalog = library()
        self.verified_business = None
        self.option_cache = {}
        self.notification_focus_until = 0
        # UI preferences are local to this computer and workspace, never
        # canonical business memory or a portable store of credentials/commands.
        local = Path(os.environ.get('LOCALAPPDATA') or os.environ.get('XDG_STATE_HOME') or Path.home() / '.local' / 'state')
        identity = hashlib.sha256(str(workspace_root()).encode()).hexdigest()[:20]
        self.settings_file = Path(settings_file) if settings_file else local / 'ViralTrac' / 'Aura' / (identity + '.json')
        self.connections = Connections(self.settings_file.parent)
        try:
            self.preferences = json.loads(self.settings_file.read_text(encoding='utf-8'))
            if not isinstance(self.preferences, dict):
                self.preferences = {}
        except (OSError, ValueError):
            self.preferences = {}
        if not isinstance(self.preferences.get('connection'), dict):
            self.preferences['connection'] = {}
        if not isinstance(self.preferences.get('seen'), list):
            self.preferences['seen'] = []
        if not isinstance(self.preferences.get('chats'), list):
            self.preferences['chats'] = []
        if not isinstance(self.preferences.get('notification_items'), list):
            self.preferences['notification_items'] = []
        if not isinstance(self.preferences.get('active_chats'), dict):
            self.preferences['active_chats'] = {}
        if not isinstance(self.preferences.get('model_picker'), dict):
            self.preferences['model_picker'] = {}
        if not isinstance(self.preferences.get('file_locations'), dict):
            self.preferences['file_locations'] = {}
        if not isinstance(self.preferences.get('connected_apps'), dict):
            self.preferences['connected_apps'] = {}
            # Older versions retained native chat references, but only one
            # selected connection. Actual prior chats identify used apps;
            # mere installation or catalogue discovery does not.
            for chat in sorted(self.preferences['chats'], key=lambda c:c.get('updated', 0)):
                if chat.get('agent') in NATIVE_AGENTS and chat.get('native_id') and chat.get('model'):
                    self.preferences['connected_apps'][chat['agent']] = {
                        'kind':chat['agent'], 'model':chat['model'], 'effort':chat.get('effort', '')}
        if self.preferences.get('appearance') not in {'system', 'light', 'dark'}:
            self.preferences['appearance'] = 'system'
        saved = self.preferences.get('connection', {})
        if self.configured_agent:
            self.preferences['connected_apps'].setdefault('configured', {'kind':'configured','model':'','effort':''})
        if saved.get('kind') in NATIVE_AGENTS | {'configured'}:
            self.preferences['connected_apps'].setdefault(saved['kind'], dict(saved))
        if not agent and isinstance(saved, dict):
            self.handoff = saved.get('kind') == 'handoff'
            choice = next((a for a in installed_agents() if a['id'] == saved.get('kind') and a['argv']), None)
            if choice:
                self.select_agent(choice, saved.get('workspace_write') is True)
        if business_directory():
            self.remember_workspace()

    def recent_workspaces(self):
        try:
            data = json.loads((self.settings_file.parent / 'recent-workspaces.json').read_text(encoding='utf-8'))
            return [r for r in data if isinstance(r, dict) and isinstance(r.get('path'), str) and isinstance(r.get('name'), str)][:12]
        except (OSError, ValueError, TypeError):
            return []

    def remember_workspace(self):
        root = str(workspace_root().resolve())
        name = ', '.join(b['name'] for b in business_directory())[:160]
        rows = [{'path':root, 'name':name}] + [r for r in self.recent_workspaces() if r['path'] != root]
        path = self.settings_file.parent / 'recent-workspaces.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(rows[:12]), encoding='utf-8')
        temporary.replace(path)

    def open_workspace(self, path):
        info = workspace_storage.inspect(path)
        target = Path(info['path'])
        profile_file = target / '.businessos/workspace.json'
        profile = json.loads(profile_file.read_text(encoding='utf-8')) if profile_file.exists() else {}
        configure(target, profile.get('profile','power_user'), profile.get('knowledge_enabled',True), allow_state_switch=True)
        os.environ['BUSINESSOS_WORKSPACE'] = str(target)
        identity = hashlib.sha256(str(workspace_root()).encode()).hexdigest()[:20]
        fresh = Workspace(self.configured_agent, self.static, self.settings_file.parent / (identity + '.json'))
        try:
            workspace_guidance.refresh(PRODUCT_ROOT, target)
        except (OSError, ValueError):
            info['connection_note'] = 'Your workspace is open. Ask your AI to check its existing AURA instructions before using a native chat.'
        if not fresh.preferences['connection'] and self.connection_kind in NATIVE_AGENTS:
            choice = next((a for a in installed_agents() if a['id'] == self.connection_kind and a['argv']), None)
            if choice:
                fresh.select_agent(choice, self.preferences['connection'].get('workspace_write', True))
                connection = dict(self.preferences['connection'], attachment=None)
                try:
                    connection['attachment'] = (workspace_codex.attach(PRODUCT_ROOT, target) if self.connection_kind == 'codex'
                                                else workspace_guidance.attach(self.connection_kind, PRODUCT_ROOT, target))
                except (OSError, ValueError):
                    info['connection_note'] = 'Your workspace is open. Check Adjust AI settings to finish its native app guidance.'
                fresh.preferences['connection'] = connection
                fresh.preferences['connected_apps'][self.connection_kind] = dict(connection)
                fresh.preferences['model_picker'] = self.preferences['model_picker']
                fresh.preferences['appearance'] = self.preferences['appearance']
                if self.preferences['seen']:
                    fresh.preferences['seen'] = [b['id'] for b in info['businesses']]
                fresh.save_preferences()
        fresh.token, fresh.lock = self.token, self.lock
        self.__dict__.update(fresh.__dict__)
        return info

    def save_preferences(self):
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.settings_file.with_suffix('.tmp')
        temporary.write_text(json.dumps(self.preferences), encoding='utf-8')
        temporary.replace(self.settings_file)

    def check_connections(self, bid):
        checks, context_error = [], ''
        try:
            (PRODUCT_ROOT / 'skills/viraltrac-aura/SKILL.md').read_text(encoding='utf-8')
            business = next(r for r in records(bid)[0] if r['type'] == 'Business')
            (workspace_root() / business['path']).read_text(encoding='utf-8')
        except (OSError, ValueError, StopIteration):
            context_error = 'Your workspace files could not be read. Check the folder and try again.'
        choices = {a['id']:a for a in installed_agents()}
        configured = dict(self.preferences['connected_apps'])
        if self.connection_kind in NATIVE_AGENTS | {'configured'} and self.agent:
            configured[self.connection_kind] = dict(self.preferences.get('connection', {}))
        def check(entry):
            kind, settings = entry
            choice = choices.get(kind, {})
            command = (self.configured_agent or {}).get('argv') if kind == 'configured' else choice.get('argv')
            row = {'id':kind, 'name':(self.configured_agent or {}).get('name','Your AI app') if kind == 'configured' else choice.get('name',kind),
                   'status':'checking', 'checked_at':time.time()}
            try:
                if not command or not shutil.which(command[0]):
                    row.update(status='error', detail='This AI app could not be found. Open or reconnect it, then try again.')
                    return row
                if kind in NATIVE_AGENTS:
                    model = settings.get('model', '')
                    if kind == 'hermes':
                        workspace_agents.check_transport(command, kind, workspace_root(), self.agent_environment())
                    else:
                        options = self.agent_options(kind, refresh=True)
                        if not any(m['id'] == model for m in options['models']):
                            raise ValueError('The selected model is unavailable. Refresh the model choices and choose another one.')
                    workspace_agents.check_signin(command, kind, model, workspace_root(), self.agent_environment())
                    row['detail'] = 'App responded. Ready to send a request.'
                else:
                    row['detail'] = 'Command found. Its response is checked when you send a request.'
                row['status'] = 'ready'
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                row.update(status='error', detail=setup_error(str(exc)))
            return row
        with ThreadPoolExecutor(max_workers=4) as pool:
            checks = list(pool.map(check, configured.items()))
        with self.lock:
            for row in checks:
                saved = self.preferences['connected_apps'].get(row['id'])
                if saved and saved.get('model') == configured[row['id']].get('model'):
                    saved['check'] = row
            self.save_preferences()
        current = next((r for r in checks if r['id'] == self.connection_kind), None)
        ready = not context_error and (bool(current and current['status'] == 'ready') or self.handoff)
        return {'items':checks, 'ready':ready, 'files_ready':not context_error,
                'message':context_error or (current or {}).get('detail') or 'Choose an AI app to connect.',
                'checked_at':time.time()}

    def notifications(self, bid):
        items = [n for n in self.preferences['notification_items'] if n['business_id'] == bid]
        titles = {c['id']: c['title'] for c in self.preferences['chats'] if c['business_id'] == bid}
        return {'items': [{**n, 'title': titles.get(n['chat_id'], '')} for n in items], 'unread': sum(not n['read'] for n in items),
                'enabled': self.preferences.get('notifications') is True}

    def record_notification(self, job, chat):
        # One receipt per finished request; no transcript or credential content.
        if job['status'] == 'stopped' or (job.get('welcome') and job['status'] == 'complete'):
            return
        items = self.preferences['notification_items']
        if any(n['id'] == job['id'] for n in items):
            return
        items.append({'id': job['id'], 'business_id': job['business_id'],
                      'chat_id': chat['id'] if chat else None,
                      'agent': self.agent['name'], 'status': job['status'],
                      'at': job['updated'], 'read': False, 'delivered': False})
        self.preferences['notification_items'] = items[-50:]

    def select_agent(self, choice, workspace_write=True):
        command = list(choice['argv'])
        if choice['id'] == 'codex':
            command[-1:-1] = ['--sandbox', 'workspace-write' if workspace_write else 'read-only']
        self.agent = {'name': choice['name'], 'argv': command}
        self.connection_kind = choice['id']
        self.handoff = False
        self.verified_business = None

    def agent_options(self, kind, refresh=False):
        if refresh:
            self.option_cache.pop(kind, None)
        if kind not in NATIVE_AGENTS:
            return {'models': [], 'sessions': False,
                    'note': 'This command uses its app settings. Model controls and chat restoration need a native session connection.'}
        if kind not in self.option_cache:
            choice = next((a for a in installed_agents() if a['id'] == kind), None)
            command = choice and choice['argv']
            if not command:
                raise ValueError('This AI app is not installed or its command needs setup.')
            if kind == 'codex':
                self.option_cache[kind] = workspace_codex.options(command, workspace_root(), self.agent_environment())
            else:
                self.option_cache[kind] = workspace_agents.options(command, kind, workspace_root(), self.agent_environment())
        return self.option_cache[kind]

    def agent_efforts(self, kind, model):
        options = self.agent_options(kind)
        chosen = next((m for m in options['models'] if m['id'] == model), None)
        if not chosen:
            raise ValueError('Choose a model returned by this AI app.')
        if chosen.get('discover_efforts') and not chosen.get('efforts_loaded'):
            command = next(a['argv'] for a in installed_agents() if a['id'] == kind and a['argv'])
            try:
                result = workspace_agents.efforts(command, kind, workspace_root(), self.agent_environment(), model)
                chosen.update(result)
            except ValueError:
                # Older hosts lack effort metadata. Never invent supported tiers.
                chosen.update(efforts=[], default_effort='')
            chosen['efforts_loaded'] = True
        return {'efforts': chosen['efforts'], 'default_effort': chosen.get('default_effort', '')}

    def model_catalog(self, refresh=False, kind=None):
        """One view of native catalogues; execution still uses an explicit host."""
        if kind is not None and kind not in NATIVE_AGENTS:
            raise ValueError('Choose a supported AI app.')
        choices = [a for a in installed_agents() if a['argv'] and a['id'] in NATIVE_AGENTS and (kind is None or a['id'] == kind)]
        def discover(choice):
            try:
                return choice, self.agent_options(choice['id'], refresh), None
            except (ValueError, OSError, subprocess.SubprocessError) as exc:
                return choice, None, setup_error(str(exc))
        grouped, unavailable = {}, []
        with ThreadPoolExecutor(max_workers=6) as pool:
            for choice, options, error in pool.map(discover, choices):
                if error:
                    unavailable.append({'app': choice['name'], 'reason': error})
                    continue
                for model in options['models']:
                    raw = model.get('provider') or choice['id']
                    bare = model['id']
                    for separator in ('/', ':'):
                        if bare.startswith(raw + separator):
                            bare = bare[len(raw)+1:]
                            break
                    family = {'openai-codex':'openai','anthropic-oauth':'anthropic','google-gemini-cli':'google',
                              'google-vertex':'google','google-antigravity':'google','xai-oauth':'xai'}.get(raw, raw)
                    local = bool(re.fullmatch(r'\d*local', raw, re.I) or raw.lower() in {'ollama','lmstudio','llama.cpp','llamacpp'})
                    if raw == 'openrouter':
                        access = 'openrouter'
                    elif local:
                        access = 'local'
                    elif model.get('access'):
                        access = model['access']
                    elif raw.endswith(('-oauth', '-codex')):
                        access = 'signin'
                    elif choice['id'] == 'antigravity':
                        access = 'google-app'
                    else:
                        access = 'provider' if raw in {'openai','anthropic','google','xai'} else 'app-'+choice['id']
                    if raw == 'openrouter':
                        maker = bare.split('/',1)[0]
                        family = {'openai':'openai','anthropic':'anthropic','google':'google','x-ai':'xai','xai':'xai'}.get(maker, 'other')
                    if local:
                        family = 'local'
                    identity = (raw if local or access.startswith('app-') else family, access, bare)
                    ident = hashlib.sha256(json.dumps(identity).encode()).hexdigest()[:24]
                    row = grouped.setdefault(ident, {'id':ident, 'name':model.get('name',bare).removesuffix(' · '+raw),
                                                    'provider':family, 'access':access, 'routes':[]})
                    row['routes'].append({'agent':choice['id'], 'app':choice['name'], 'model':model['id'],
                                          'key':choice['id']+'/'+model['id'],
                                          'current':model['id']==options.get('model'),
                                          'efforts':model.get('efforts',[]), 'default_effort':model.get('default_effort',''),
                                          'discover_efforts':model.get('discover_efforts',False)})
        models = sorted(grouped.values(), key=lambda m:(m['provider'],m['access'],m['name'].casefold()))
        saved = self.preferences['model_picker']
        picker = saved.get('all')
        if picker is None:
            favorites, efforts = [], {}
            for model in models:
                for route in model['routes']:
                    prior = saved.get(route['agent'], {})
                    if route['model'] in prior.get('favorites',[]) and model['id'] not in favorites:
                        favorites.append(model['id'])
                    if route['model'] in prior.get('efforts',{}):
                        efforts[route['key']] = prior['efforts'][route['model']]
            picker = {'view':'all', 'favorites':favorites, 'providers':list(dict.fromkeys(m['provider'] for m in models)), 'efforts':efforts}
        return {'models':models, 'picker':picker, 'unavailable':unavailable, 'kind':kind}

    def agent_environment(self):
        return dict(os.environ, BUSINESSOS_WORKSPACE=str(workspace_root()), PYTHONUTF8='1',
                    PATH=os.pathsep.join(filter(None,[os.environ.get('PATH'),str(Path(sys.executable).parent)])), **self.connections.environment())

    def active_chat(self, bid):
        key = self.preferences['active_chats'].get(bid)
        return next((c for c in self.preferences['chats'] if c['id'] == key and c['business_id'] == bid), None)

    def conversation(self, bid):
        chat = self.active_chat(bid)
        job = dict(self.job) if self.job and self.job['business_id'] == bid and (self.job.get('chat_id') == (chat or {}).get('id')) else None
        if not chat:
            return {'messages': [], 'chat': None, 'job': job}
        if not chat.get('native_id'):
            path = self.settings_file.parent/'chat-views'/(chat['id']+'.json')
            shown = json.loads(path.read_text(encoding='utf-8')) if path.is_file() else []
            return {'messages': shown, 'chat': chat, 'job': job}
        try:
            choice = next(a for a in installed_agents() if a['id'] == chat['agent'] and a['argv'])
            result = (workspace_codex.history(choice['argv'], workspace_root(), chat['native_id']) if chat['agent']=='codex' else
                      workspace_agents.history(choice['argv'],chat['agent'],workspace_root(),self.agent_environment(),chat['native_id']))
        except (ValueError, OSError, StopIteration, subprocess.SubprocessError) as exc:
            if job and job['status'] == 'working':
                return {'messages': [], 'chat': chat, 'job': job}
            path = self.settings_file.parent/'chat-views'/(chat['id']+'.json')
            if not path.is_file():
                raise ValueError(str(exc) or 'Reconnect the app that owns this chat.') from None
            result = {'messages':json.loads(path.read_text(encoding='utf-8')), 'usage':{}, 'history_note':str(exc)}
        # Native metadata is authoritative if the chat was also used in Codex.
        chat.update({k: result[k] for k in ('model', 'effort') if result.get(k)})
        for message in result['messages']:
            message['text'] = self.connections.redact(message['text'])
        return dict(result, chat=chat, job=job)

    def save_chat_turn(self, chat, job, text, final=False):
        """A recovery display, never supplied as native model context."""
        path = self.settings_file.parent / 'chat-views' / (chat['id'] + '.json')
        shown = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
        shown = [r for r in shown if r.get('request_id') != job['id']]
        shown.append({'role':'user', 'text':self.connections.redact(workspace_agents.display_text(text)),
                      'at':job['created'], 'request_id':job['id']})
        if final:
            shown.append({'role':'assistant', 'text':job['reply'], 'at':job['updated'],
                          'agent':self.agent['name'], 'model':chat['model'], 'effort':chat['effort'],
                          'request_id':job['id'], 'error_detail':job.get('error_detail','')})
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(shown), encoding='utf-8')
        temporary.replace(path)

    def connection(self, bid=None):
        choices = ([{'id': 'configured', 'name': self.configured_agent['name'], 'available': True}] if self.configured_agent else [])
        choices += [{'id': a['id'], 'name': a['name'], 'available': bool(a['argv']),
                     'guide':workspace_guidance.GUIDES.get(a['id'], ('',''))} for a in installed_agents()]
        return {'connected': bool(self.agent), 'name': (self.agent or {}).get('name', 'Your existing chat'),
                'choices': choices, 'selected': self.connection_kind,
                'apps': [dict(self.preferences['connected_apps'][kind].get('check') or {}, id=kind,
                              name=next((c['name'] for c in choices if c['id']==kind),kind))
                         for kind in self.preferences['connected_apps']],
                'verified': bool(bid and self.verified_business == bid),
                'workspace_write': self.preferences.get('connection', {}).get('workspace_write') is True,
                'effort': self.preferences.get('connection', {}).get('effort') or '',
                'native_sessions': self.connection_kind in NATIVE_AGENTS,
                'model_controls': self.connection_kind in NATIVE_AGENTS,
                'attachment': self.preferences.get('connection', {}).get('attachment'),
                'mode': 'agent' if self.agent else ('copy' if self.handoff else 'unconnected'),
                'model': self.preferences.get('connection', {}).get('model') or (self.agent or {}).get('model') or '',
                'codex_available': codex_command() is not None,
                'scope': 'A saved native conversation.' if self.connection_kind in NATIVE_AGENTS else 'Independent command requests; native chat restoration is not available.',
                'authentication': 'Owned by the installed agent. Availability is not proof of sign-in.'}

    def state(self, bid=None):
        directory = business_directory()
        if not bid and len(directory) == 1:
            bid = directory[0]['id']
        rows, diagnostics = records(selected(bid)) if bid else ([], [])
        return {'businesses': directory, 'business_id': bid, 'records': rows,
                'diagnostics': diagnostics, 'workspace': str(workspace_root()),
                'product': str(PRODUCT_ROOT), 'version': os_version(), 'refreshed': time.time(),
                'connection': self.connection(bid),
                'appearance': self.preferences.get('appearance', 'system'),
                'notifications': self.preferences.get('notifications') is True,
                'model_picker': self.preferences['model_picker'],
                'preferred_app': self.preferences.get('preferred_app', ''),
                'onboarding': {'seen': bid in self.preferences.get('seen', [])}}

    def request_text(self, bid, text, history=None):
        if not isinstance(text, str) or not text.strip() or len(text) > 16000:
            raise ValueError('Enter a request of up to 16,000 characters.')
        # User/assistant transcript stays in memory; it is never canonical memory.
        prior = []
        for row in (history or [])[-6:]:
            if isinstance(row, dict) and row.get('role') in {'user', 'assistant'} and isinstance(row.get('text'), str):
                prior.append(f"{row['role']}: {row['text'][:4000]}")
        return (f"Work for the explicitly selected AURA business ID: {bid}.\n"
                f"AURA product: {PRODUCT_ROOT}\nOrganization workspace: {workspace_root()}\n"
                f"Read {PRODUCT_ROOT / 'AGENTS.md'} and use the existing AURA helpers and workspace.\n"
                f"For Python helpers, the running interpreter is {Path(sys.executable).as_posix()}. "
                "Quote its full path for your shell; do not assume python3 is installed. "
                "You can read workspace files directly with your normal tools. A simple conversation does not need helper calls.\n"
                f"AURA Skill guidance for this task: read {PRODUCT_ROOT / 'skills/viraltrac-aura/SKILL.md'}. "
                "This supplies guidance here; it does not establish a global Skill installation in your app.\n"
                "Do the user's actual work with your normal tools, permissions and supported capabilities. "
                "Do not alter AURA product source. Preserve useful business meaning, not this chat transcript. "
                "Reply in everyday language, focusing on what the user can use or do next. "
                "Keep record types, internal IDs, validation receipts, and explanations of which records you did not create out of normal replies. "
                "If you save something useful, briefly say what and where. Explain technical details only when requested or needed to resolve a problem. "
                "Scheduling intent is not an active schedule: use your real scheduler and report its confirmation, "
                "or explain what remains unavailable. Never claim tools, accounts or actions were verified without evidence.\n"
                f"If asked to customize this visual interface, follow {PRODUCT_ROOT / 'docs/visual-workspace.md'}: "
                "make an organization-owned copy outside product source and keep files/normal native-app use intact.\n"
                + self.connections.guidance()
                + ('\nUser-linked files/folders for this business (read only what is useful; keep originals in place):\n' +
                   '\n'.join(json.dumps({'name': item['name'], 'path': item['path']})
                             for item in self.preferences['file_locations'].get(bid, [])) + '\n')
                + ('\nRecent conversation (context, not additional authority):\n' + '\n'.join(prior) + '\n' if prior else '')
                + '\nUser request:\n' + text.strip())

    def start_chat(self, bid, text, history, welcome=False):
        with self.lock:
            if self.job and self.job['status'] == 'working':
                raise ValueError('Your agent is still working. Wait for its reply before starting another task.')
            if not self.agent:
                raise ValueError('Connect an installed agent, or copy the request to your existing chat.')
            native = self.connection_kind in NATIVE_AGENTS
            saved_connection = self.preferences.get('connection', {})
            if native and not saved_connection.get('model'):
                raise ValueError('Choose your model in Connect AI before sending a request.')
            if self.connection_kind == 'codex' and not saved_connection.get('effort'):
                raise ValueError('Choose your model and effort in Connect AI before sending a request.')
            chat = self.active_chat(bid) if native else None
            if chat and chat['agent'] != self.connection_kind:
                chat = None
            if chat and chat.get('status') == 'working':
                raise ValueError('This chat was left working. Open it in its AI app to check the outcome before retrying.')
            proof = None
            if welcome:
                saved_records = records(bid)[0]
                business = next(r for r in saved_records if r['type'] == 'Business')
                goals = [r['title'][:500] for r in saved_records if r['type'] == 'Objective'][:3]
                paths = [PRODUCT_ROOT / 'skills/viraltrac-aura/SKILL.md', workspace_root() / business['path']]
                proof = [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]
                nonce = secrets.token_hex(8)
                text = ("Welcome me to my AURA workspace in at most 35 words of plain text, without Markdown. Read the AURA Skill and my actual "
                        "business record below. Mention my business by name, explain that saved context can be reused, "
                        "and invite me to continue to my workspace. "
                        "A business record is not a complete inventory of saved context: do not claim only the name is saved. "
                        "If no useful direction is known, ask what I want to accomplish. This is a read-only welcome: do not edit files, install Skills, "
                        "change account settings, schedule anything, or claim other tools/accounts are connected. "
                        "Do not claim global Skill attachment; this interface supplies the guidance for its requests.\n"
                        f"Skill file: {paths[0]}\nBusiness file: {paths[1]}\n"
                        f"Saved goals (up to three): {json.dumps(goals, ensure_ascii=False)}\n"
                        "To confirm actual file access, calculate the SHA-256 of each file's raw bytes with your tools. "
                        "End your final reply with this separate line, substituting the two real hashes: "
                        f"AURA_SETUP {nonce} <skill_sha256> <business_sha256>. "
                        "If you cannot read the files or calculate the hashes, explain the problem; do not invent them.")
            prompt = self.request_text(bid, text, None if native else history)
            job = {'id': secrets.token_urlsafe(12), 'business_id': bid, 'status': 'working', 'reply': '', 'activity': [],
                   'created': time.time(), 'updated': time.time(), 'progress': 'Starting your AI'}
            if native:
                if not chat:
                    chat = {'id': secrets.token_urlsafe(12), 'business_id': bid, 'agent': self.connection_kind,
                            'title': 'Welcome to AURA' if welcome else text.strip()[:70],
                            'created': time.time(), 'native_id': None}
                    self.preferences['chats'].append(chat)
                    self.preferences['active_chats'][bid] = chat['id']
                chat.update(status='working', model=saved_connection['model'], effort=saved_connection['effort'], updated=time.time())
                job.update(chat_id=chat['id'], model=chat['model'], effort=chat['effort'])
                self.save_chat_turn(chat, job, text)
                self.save_preferences()
            if welcome:
                job['welcome'] = True
            self.job = job
            execution = self.execution = Execution()
            command = list(self.agent['argv'])
            kind = self.connection_kind
            env = self.agent_environment()
            def update(**values):
                with self.lock:
                    if values.get('native_id') and not job.get('native_id'):
                        values.setdefault('progress', 'Connected. Waiting for your AI')
                    if 'reply' in values:
                        values['reply'] = self.connections.redact(values['reply'][-100000:])
                    if values.get('progress') and (not job['activity'] or job['activity'][-1]['text'] != values['progress']):
                        job['activity'] = [*job['activity'], {'text':values['progress'], 'at':time.time()}][-12:]
                    job.update(values, updated=time.time())
                    if chat and values.get('native_id'):
                        chat['native_id'] = values['native_id']
                        try:
                            self.save_preferences()
                        except OSError:
                            job['preference_warning'] = 'Your AI is working, but this view could not save its chat reference. Use the native app before retrying.'
            def work():
                try:
                    if native:
                        result = (workspace_codex.run(command, workspace_root(), prompt, chat.get('native_id'), chat['model'], chat['effort'], update, env, execution)
                                  if kind=='codex' else workspace_agents.run(command,kind,workspace_root(),env,prompt,chat.get('native_id'),chat['model'],chat['effort'],update,execution))
                        output, code = result['reply'], 0
                        job['usage'] = result['usage']
                    else:
                        with execution.popen(command, cwd=workspace_root(), env=env, stdin=subprocess.PIPE,
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                              text=True, encoding='utf-8', errors='replace') as process:
                            output, stderr = process.communicate(prompt)
                        code = process.returncode
                    with self.lock:
                        execution.check()
                        job['status'] = 'complete' if code == 0 else 'error'
                        job['reply'] = self.connections.redact(output[-100000:]) if code == 0 else self.connections.redact(
                            (stderr or output)[-5000:].strip() or f'The agent exited with code {code}. Open your AI app to check the failure. Your request was not marked complete.')
                        if not job['reply']:
                            job['reply'] = 'The command finished without a text reply. Check the agent and refresh your workspace.'
                        if welcome:
                            match = re.search(r'(?m)^\s*AURA_SETUP ' + nonce + r' ([0-9a-fA-F]{64}) ([0-9a-fA-F]{64})\s*$', output)
                            confirmed = bool(code == 0 and match and [v.lower() for v in match.groups()] == proof)
                            job['reply'] = re.sub(r'(?m)^\s*AURA_SETUP[^\n]*', '', job['reply']).strip()
                            job['setup'] = {'reply_received': bool(output.strip()) and code == 0,
                                            'aura_guidance': confirmed, 'business_context': confirmed}
                            if confirmed and job['reply']:
                                self.verified_business = bid
                                seen = self.preferences.setdefault('seen', [])
                                if bid not in seen:
                                    seen.append(bid)
                                try:
                                    self.save_preferences()
                                except OSError:
                                    job['preference_warning'] = 'Connected, but setup preferences could not be saved on this computer.'
                            elif code == 0:
                                job['status'] = 'error'
                                job['reply'] = SETUP_ERRORS['proof']
                except Stopped:
                    with self.lock:
                        job.update(status='stopped', progress='Stopped', reply=job.get('reply') or '')
                except (OSError, ValueError, subprocess.SubprocessError) as exc:
                    with self.lock:
                        if execution.stopped.is_set():
                            job.update(status='stopped', progress='Stopped')
                        else:
                            detail = self.connections.redact(str(exc))
                            job.update(status='error', error_detail=detail, reply=setup_error(detail))
                finally:
                    with self.lock:
                        if welcome and job['status'] == 'error':
                            job['reply'] = setup_error(job['reply'])
                            job['setup_error'] = True
                        job['updated'] = time.time()
                        self.record_notification(job, chat)
                        if chat:
                            chat.update(status=job['status'], updated=job['updated'])
                            try:
                                self.save_chat_turn(chat, job, text, final=True)
                                self.save_preferences()
                            except OSError:
                                job['preference_warning'] = 'Reply received, but its chat reference could not be saved. Use the native app before retrying.'
                        if not chat:
                            try:
                                self.save_preferences()
                            except OSError:
                                job['preference_warning'] = 'Reply received, but its notification could not be saved.'
            threading.Thread(target=work, daemon=True).start()
            return {'id': job['id'], 'status': job['status']}

    def stop_chat(self, bid, ident):
        job = self.job
        if not job or job['business_id'] != bid or job['id'] != ident:
            raise ValueError('This request does not belong to the selected workspace.')
        if job['status'] == 'working':
            self.execution.stop()
            job.update(stopping=True, progress='Stopping this request…', updated=time.time())
        return {'id':job['id'], 'status':job['status']}


def handler_for(app):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'AURA-local'

        def log_message(self, *args):
            pass  # No request URLs, prompts or private file paths in access logs.

        def send(self, status, data, content_type='application/json; charset=utf-8', headers=None):
            body = json.dumps(data, ensure_ascii=False).encode() if content_type.startswith('application/json') else data
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' blob:; media-src 'self' blob:; connect-src 'self'; object-src 'none'; frame-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
            for key, value in (headers or {}).items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)

        def guard(self):
            expected = f'127.0.0.1:{self.server.server_port}'
            if self.headers.get('Host') != expected:
                raise PermissionError('Open the local address printed by AURA.')
            origin = self.headers.get('Origin')
            if origin and origin != 'http://' + expected:
                raise PermissionError('Requests must come from the local AURA view.')
            if self.path.startswith('/api/') and not secrets.compare_digest(self.headers.get('X-Aura-Token', ''), app.token):
                raise PermissionError('Refresh the AURA page to reconnect.')

        def do_GET(self):
            try:
                self.guard()
                parsed = urlsplit(self.path)
                query = {key: val[0] for key, val in parse_qs(parsed.query).items()}
                route = parsed.path
                if route == '/':
                    page = (app.static / 'index.html').read_text(encoding='utf-8').replace('__AURA_TOKEN__', app.token)
                    self.send(200, page.encode(), 'text/html; charset=utf-8')
                elif route in {'/app.js', '/style.css'}:
                    path = app.static / route[1:]
                    self.send(200, path.read_bytes(), 'text/javascript; charset=utf-8' if path.suffix == '.js' else 'text/css; charset=utf-8')
                elif route == '/api/state':
                    self.send(200, app.state(query.get('business')))
                elif route == '/api/notifications':
                    bid = selected(query.get('business'))
                    with app.lock:
                        if query.get('foreground') == '1':
                            app.notification_focus_until = time.time() + 12
                        self.send(200, app.notifications(bid))
                elif route == '/api/agent-options':
                    self.send(200, app.agent_options(query.get('kind'), query.get('refresh') == '1'))
                elif route == '/api/model-catalog':
                    self.send(200, app.model_catalog(query.get('refresh') == '1', query.get('kind')))
                elif route == '/api/agent-efforts':
                    self.send(200, app.agent_efforts(query.get('kind'), query.get('model')))
                elif route == '/api/connections':
                    self.send(200, app.connections.rows())
                elif route == '/api/workspaces':
                    self.send(200, {'current':str(workspace_root()), 'recent':app.recent_workspaces()})
                elif route == '/api/chats':
                    bid = selected(query.get('business'))
                    self.send(200, {'items': [c for c in app.preferences['chats'] if c['business_id'] == bid],
                                    'active': app.preferences['active_chats'].get(bid)})
                elif route == '/api/conversation':
                    self.send(200, app.conversation(selected(query.get('business'))))
                elif route == '/api/library':
                    self.send(200, app.catalog)
                elif route == '/api/schedules':
                    self.send(200, workspace_schedules.inventory())
                elif route == '/api/connection-check':
                    self.send(200, app.check_connections(selected(query.get('business'))))
                elif route == '/api/files':
                    bid = selected(query.get('business'))
                    self.send(200, files(bid, app.preferences['file_locations'].get(bid, [])))
                elif route == '/api/document':
                    path = (PRODUCT_ROOT / query.get('path', '')).resolve()
                    allowed = any(path == (PRODUCT_ROOT / entry['path']).resolve() for entry in app.catalog)
                    if not allowed or path.suffix != '.md' or not path.is_file():
                        raise ValueError('Choose an installed Workflow or recipe.')
                    self.send(200, {'text': path.read_text(encoding='utf-8')[:100000]})
                elif route == '/api/file':
                    bid = selected(query.get('business'))
                    path = local_file(bid, query.get('path', ''), app.preferences['file_locations'].get(bid, []))
                    if path.stat().st_size > 2 * 1024 * 1024:
                        raise ValueError('This file is too large for a text preview. Use its location to open the original.')
                    try:
                        text = path.read_text(encoding='utf-8')
                    except UnicodeDecodeError:
                        raise ValueError('This file has no text preview. Use its location to open the original.')
                    self.send(200, {'text': text})
                elif route == '/api/media':
                    bid = selected(query.get('business'))
                    path = local_file(bid, query.get('path', ''), app.preferences['file_locations'].get(bid, []))
                    if path.stat().st_size > 64 * 1024 * 1024:
                        raise ValueError('Open this large file from its original workspace location.')
                    mime = mimetypes.guess_type(path.name)[0] if path.suffix.lower() in MEDIA else 'application/octet-stream'
                    self.send(200, path.read_bytes(), mime or 'application/octet-stream',
                              {'Content-Disposition': "attachment; filename*=UTF-8''" + quote(path.name)})
                elif route == '/api/chat':
                    bid = selected(query.get('business'))
                    with app.lock:
                        job = app.job
                        if not job or job['business_id'] != bid or job['id'] != query.get('id'):
                            raise ValueError('Task not found for this business.')
                        self.send(200, dict(job))
                else:
                    self.send(404, {'error': 'Not found.'})
            except PermissionError as exc:
                self.send(403, {'error': str(exc)})
            except (ValueError, OSError, KeyError, subprocess.SubprocessError) as exc:
                self.send(400, {'error': app.connections.redact(str(exc))})

        def do_POST(self):
            try:
                self.guard()
                if self.headers.get_content_type() != 'application/json':
                    raise ValueError('Send JSON from the local view.')
                length = int(self.headers.get('Content-Length', '0'))
                if length <= 0 or length > MAX_BODY:
                    raise ValueError('Request is empty or too large.')
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict):
                    raise ValueError('Expected an object.')
                route = urlsplit(self.path).path
                if route == '/api/locations/browse':
                    if data.get('kind') not in {'folder', 'file'}:
                        raise ValueError('Choose a file or folder.')
                    self.send(200, {'path': workspace_locations.choose(data['kind'])})
                    return
                with app.lock:
                    if app.job and app.job['status'] == 'working' and route not in {'/api/preferences', '/api/notifications', '/api/chat/stop'}:
                        raise ValueError('Your agent is working. Wait for its reply before changing this workspace.')
                    if route == '/api/setup':
                        name = str(data.get('name', '')).strip()
                        if not name or len(name) > 160:
                            raise ValueError('Enter a business name of up to 160 characters.')
                        result = setup(organization=name)
                        if result['status'] != 'ready':
                            raise ValueError('Setup needs attention. Ask your agent to run AURA doctor.')
                        app.remember_workspace()
                        self.send(200, result)
                    elif route == '/api/workspaces/open':
                        self.send(200, app.open_workspace(str(data.get('path',''))))
                    elif route == '/api/workspaces/backup':
                        self.send(200, workspace_storage.backup(workspace_root(), str(data.get('path',''))))
                    elif route == '/api/workspaces/restore':
                        self.send(200, workspace_storage.restore(str(data.get('archive','')), str(data.get('path',''))))
                    elif route == '/api/connections/session-only':
                        app.connections.session_only = True
                        self.send(200, {'ok':True})
                    elif route == '/api/save':
                        bid = selected(data.get('business'))
                        kind = data.get('kind')
                        name = str(data.get('name', '')).strip()
                        if not name or len(name) > 2000:
                            raise ValueError('Enter a name of up to 2,000 characters.')
                        rows, _ = records(bid)
                        if kind == 'business':
                            obj = next(row for row in rows if row['type'] == 'Business')
                            item = {'object_ref': obj['ref'], 'content': {'name': name}}
                        elif kind == 'goal':
                            ref = data.get('ref')
                            if ref and not any(r['ref'] == ref and r['type'] == 'Objective' for r in rows):
                                raise ValueError('Goal not found in this business.')
                            item = {'content': {'name': name}, **({'object_ref': ref} if ref else {'object_type': 'Objective'})}
                        else:
                            raise ValueError('Unsupported edit. Use your agent for this change.')
                        self.send(200, remember(bid, {'objects': [item]}))
                    elif route == '/api/connect':
                        model, effort, attachment = '', '', None
                        if data.get('kind') in NATIVE_AGENTS:
                            options = app.agent_options(data['kind'])
                            model = data.get('model')
                            chosen = next((m for m in options['models'] if m['id'] == model), None)
                            effort = data.get('effort') or ''
                            if chosen:
                                app.agent_efforts(data['kind'], model)
                            if not chosen or (chosen['efforts'] and effort not in chosen['efforts']) or (not chosen['efforts'] and effort):
                                raise ValueError('Choose an available model and its supported effort level.')
                        if data.get('kind') == 'configured' and app.configured_agent:
                            app.agent = app.configured_agent
                            app.connection_kind = 'configured'
                            app.handoff = False
                            app.verified_business = None
                        elif data.get('kind') == 'handoff':
                            app.agent = None
                            app.connection_kind = ''
                            app.handoff = True
                            app.verified_business = None
                        else:
                            choice = next((a for a in installed_agents() if a['id'] == data.get('kind') and a['argv']), None)
                            if not choice:
                                raise ValueError('This app needs a one-time command connection. Copy the setup instructions to your AI app.')
                            app.select_agent(choice, data.get('workspace_write', True) is True)
                        if app.connection_kind == 'codex':
                            attachment = workspace_codex.attach(PRODUCT_ROOT, workspace_root())
                            attachment = workspace_codex.verify_attachment(app.agent['argv'], workspace_root(), attachment)
                        elif app.connection_kind in NATIVE_AGENTS:
                            attachment = workspace_guidance.attach(app.connection_kind, PRODUCT_ROOT, workspace_root())
                        app.preferences['connection'] = {'kind': 'handoff' if app.handoff else app.connection_kind,
                                                         'workspace_write': data.get('workspace_write', True) is True,
                                                         'model': model, 'effort': effort, 'attachment': attachment}
                        if app.connection_kind in NATIVE_AGENTS | {'configured'} and not app.handoff:
                            app.preferences['connected_apps'][app.connection_kind] = dict(app.preferences['connection'])
                        app.save_preferences()
                        self.send(200, app.connection())
                    elif route == '/api/connections/save':
                        app.connections.save(data.get('provider'), data.get('key'), data.get('storage', 'session'),
                                             str(data.get('name', '')), str(data.get('env', '')), data.get('category', 'tools'))
                        app.option_cache.clear()
                        self.send(200, app.connections.rows())
                    elif route == '/api/connections/remove':
                        app.connections.remove(data.get('provider'))
                        app.option_cache.clear()
                        self.send(200, app.connections.rows())
                    elif route == '/api/schedules/update':
                        choice = next((a for a in installed_agents() if a['id'] == 'hermes' and a['argv']), None)
                        command = workspace_agents.base_command(choice['argv']) if choice else None
                        if 'model' in data:
                            model = str(data['model'])
                            if model:
                                if not any(m['id'] == model for m in app.agent_options('hermes')['models']):
                                    raise ValueError('Choose a model reported by Hermes, or refresh its model choices.')
                                parts = model.split(':', 2 if model.startswith('custom:') else 1)
                                if len(parts) < 2:
                                    raise ValueError('Hermes did not identify the provider for this model.')
                                data['provider'], data['model'] = ':'.join(parts[:-1]), parts[-1]
                            else:
                                data['provider'] = ''
                        result = workspace_schedules.update(data.get('id'), data, command, app.agent_environment())
                        self.send(200, {'task':result})
                    elif route == '/api/locations':
                        bid = selected(data.get('business'))
                        items = app.preferences['file_locations'].setdefault(bid, [])
                        if data.get('remove'):
                            app.preferences['file_locations'][bid] = [i for i in items if i['id'] != data['remove']]
                        else:
                            path = workspace_locations.validate(str(data.get('path', '')), workspace_root(), business_directory(), bid, private_path)
                            if not any(Path(i['path']) == path for i in items):
                                if len(items) >= 20:
                                    raise ValueError('You can link up to 20 files or folders per business.')
                                items.append({'id':secrets.token_hex(8), 'path':str(path), 'name':str(data.get('name') or path.name)[:100],
                                              'kind':'folder' if path.is_dir() else 'file'})
                        app.save_preferences()
                        self.send(200, {'ok':True})
                    elif route == '/api/notifications':
                        bid = selected(data.get('business'))
                        items = [n for n in app.preferences['notification_items'] if n['business_id'] == bid]
                        action = data.get('action')
                        claimed = []
                        if action == 'read':
                            for item in items:
                                if data.get('all') is True or item['id'] == data.get('id'):
                                    item['read'] = True
                        elif action == 'claim':
                            now = time.time()
                            # Batch close arrivals, avoid replaying stale alerts, and
                            # share delivery ownership across tabs under this lock.
                            if (app.preferences.get('notifications') is True and
                                    now >= app.notification_focus_until and
                                    now - app.preferences.get('notification_sent_at', 0) >= 30):
                                claimed = [n for n in items if not n['read'] and not n['delivered'] and now - n['at'] < 120]
                                if claimed:
                                    for item in claimed:
                                        item['delivered'] = True
                                    app.preferences['notification_sent_at'] = now
                        else:
                            raise ValueError('Choose a notification action.')
                        if action == 'read' or claimed:
                            app.save_preferences()
                        self.send(200, {**app.notifications(bid), 'claimed': claimed})
                    elif route == '/api/preferences':
                        if 'preferred_app' in data:
                            if data['preferred_app'] not in NATIVE_AGENTS | {'configured'}:
                                raise ValueError('Choose a supported AI app.')
                            app.preferences['preferred_app'] = data['preferred_app']
                        if 'model_picker' in data:
                            picker = data['model_picker']
                            if not isinstance(picker, dict) or picker.get('kind') not in NATIVE_AGENTS | {'all'} or picker.get('view') not in {'favorites', 'all'}:
                                raise ValueError('Choose Favorites or All models for a supported AI app.')
                            for field, limit in (('favorites', 2000), ('providers', 200)):
                                values = picker.get(field)
                                if not isinstance(values, list) or len(values) > limit or any(not isinstance(v, str) or not v or len(v) > 300 for v in values):
                                    raise ValueError('Choose models and providers from the picker.')
                            self_picker = {field: list(dict.fromkeys(picker[field])) for field in ('favorites', 'providers')}
                            self_picker['view'] = picker['view']
                            efforts = picker.get('efforts', app.preferences['model_picker'].get(picker['kind'], {}).get('efforts', {}))
                            if (not isinstance(efforts, dict) or len(efforts) > 2000 or
                                    any(not isinstance(key, str) or not key or len(key) > 300 or
                                        not isinstance(value, str) or len(value) > 64 for key, value in efforts.items())):
                                raise ValueError('Choose an effort level for each model from its available settings.')
                            self_picker['efforts'] = efforts
                            app.preferences['model_picker'][picker['kind']] = self_picker
                        if 'notifications' in data:
                            app.preferences['notifications'] = data['notifications'] is True
                            # Enabling alerts must not announce old activity.
                            for item in app.preferences['notification_items']:
                                item['delivered'] = True
                        if 'appearance' in data:
                            if data['appearance'] not in {'system', 'light', 'dark'}:
                                raise ValueError('Choose System, Light, or Dark.')
                            app.preferences['appearance'] = data['appearance']
                        if data.get('dismiss_setup'):
                            bid = selected(data.get('business'))
                            seen = app.preferences.setdefault('seen', [])
                            if bid not in seen:
                                seen.append(bid)
                        app.save_preferences()
                        self.send(200, {'ok': True})
                    elif route == '/api/chats/new':
                        bid = selected(data.get('business'))
                        app.preferences['active_chats'][bid] = None
                        app.job = None
                        app.save_preferences()
                        self.send(200, {'ok': True})
                    elif route == '/api/chats/open':
                        bid = selected(data.get('business'))
                        chat = next((c for c in app.preferences['chats'] if c['id'] == data.get('id') and c['business_id'] == bid), None)
                        if not chat:
                            raise ValueError('This chat does not belong to the selected business.')
                        choice = next((a for a in installed_agents() if a['id'] == chat['agent'] and a['argv']), None)
                        if not choice:
                            raise ValueError('Install or reconnect the AI app that owns this chat before opening it.')
                        app.select_agent(choice, app.preferences.get('connection', {}).get('workspace_write') is True)
                        app.preferences['connection'].update(kind=chat['agent'], model=chat['model'], effort=chat['effort'])
                        if chat['agent'] != 'codex':
                            app.preferences['connection']['attachment'] = None
                        app.preferences['active_chats'][bid] = chat['id']
                        app.save_preferences()
                        self.send(200, app.conversation(bid))
                    elif route == '/api/request':
                        bid = selected(data.get('business'))
                        self.send(200, {'text': app.request_text(bid, data.get('text'), data.get('history'))})
                    elif route == '/api/chat/stop':
                        self.send(200, app.stop_chat(selected(data.get('business')), data.get('id')))
                    elif route == '/api/chat':
                        bid = selected(data.get('business'))
                        self.send(202, app.start_chat(bid, data.get('text'), data.get('history'), data.get('welcome') is True))
                    else:
                        self.send(404, {'error': 'Not found.'})
            except PermissionError as exc:
                self.send(403, {'error': str(exc)})
            except (ValueError, OSError, KeyError, StopIteration, subprocess.SubprocessError) as exc:
                self.send(400, {'error': app.connections.redact(str(exc)) or 'The selected record was not found.'})
    return Handler


def main():
    parser = argparse.ArgumentParser(description='Open an optional local view of your AURA files. No cloud account or background daemon.')
    parser.add_argument('--workspace', help='Reuse this existing organization workspace.')
    parser.add_argument('--business-id', help='Business to open; a single business is selected automatically.')
    parser.add_argument('--port', type=int, default=0, help='Local port; default chooses an available port.')
    parser.add_argument('--no-open', action='store_true', help='Print the address without opening a browser.')
    parser.add_argument('--agent-file', help='Local JSON with name and argv. Command reads prompt on stdin and returns final text on stdout.')
    parser.add_argument('--interface-dir', help='Optional organization-owned copy of the three interface assets.')
    args = parser.parse_args()
    if args.workspace:
        os.environ['BUSINESSOS_WORKSPACE'] = str(Path(args.workspace).expanduser().resolve())
    agent = None
    if args.agent_file:
        agent = json.loads(Path(args.agent_file).read_text(encoding='utf-8'))
        if not isinstance(agent, dict) or not isinstance(agent.get('name'), str) or not isinstance(agent.get('argv'), list) or not agent['argv'] or not all(isinstance(a, str) and a for a in agent['argv']):
            parser.error('Agent file requires a name and a non-empty argv list. Keep credentials in the agent, not this file.')
    app = Workspace(agent, args.interface_dir)
    if args.business_id:
        selected(args.business_id)
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(app))
    url = f'http://127.0.0.1:{server.server_port}/' + ('?business=' + quote(args.business_id) if args.business_id else '')
    print(f'AURA workspace: {url}\nLocal to this computer. Press Ctrl+C to close the view.', flush=True)
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
