"""The connected services a conversation called, read from its AI app's own session record.

The apps already write every tool call to a record on this computer. AURA reads the name of each call and counts
calls to services the person connected: ones set up in an app's settings, claude.ai connectors and installed plugins'
services. The apps' built-in tools are not services the person connected, so they are left out. Nothing is asked of
the AI and nothing is sent anywhere. Settings can turn this reading off.

Each record is read once, and after that only what was added to it. Counts are kept in AURA's state folder. Claude
Code (including its delegated agents), Codex, Pi and OMP keep session logs; Hermes keeps its sessions in a local
database, read without changing it. Google Antigravity's records are in a private format and are not read. Each app's
format is its own and can change: a line or record that cannot be read adds nothing.
"""
import json
import os
import re
import sqlite3
import time
from pathlib import Path

from workspace_startup import state_dir
import workspace_library

CALL = re.compile(r'mcp__([A-Za-z0-9_.-]+?)__[A-Za-z0-9_]')
CODE_CALL = re.compile(r'tools\.(mcp__[A-Za-z0-9_.-]+?__[A-Za-z0-9_]+)')  # Codex calls services from code it runs
LOCAL = {'node_repl', 'cua_repl'}  # Codex's own local runtimes: listed in the Library as tools, not services
APPS = {'claude': 'claude', 'Claude Code': 'claude', 'codex': 'codex', 'Codex': 'codex', 'pi': 'pi', 'Pi': 'pi',
        'omp': 'omp', 'OMP': 'omp', 'hermes': 'hermes', 'Hermes': 'hermes'}
RETRY = 600  # seconds before looking again for a session whose record was not found
VERSION = 2


def _calls(app, row):
    """Tool names called in one log line."""
    if app == 'claude':
        if row.get('type') != 'assistant':
            return []
        return [str(part.get('name') or '') for part in (row.get('message') or {}).get('content') or []
                if isinstance(part, dict) and part.get('type') == 'tool_use']
    if app in {'pi', 'omp'}:
        message = row.get('message') or {}
        if row.get('type') != 'message' or message.get('role') != 'assistant':
            return []
        return [str(part.get('name') or '') for part in message.get('content') or [] if isinstance(part, dict) and part.get('type') == 'toolCall']
    payload = row.get('payload') or {}
    if row.get('type') != 'response_item' or payload.get('type') not in {'function_call', 'custom_tool_call'}:
        return []
    name = str(payload.get('name') or '')
    return [name] if CALL.match(name) else CODE_CALL.findall(str(payload.get('input') or payload.get('arguments') or ''))


def _service(tool, configured):
    """The connected service a tool belongs to, or None for an app's own tool. A claude.ai connector or a plugin's
    service is named without its prefix; other apps name a service's tools after the service."""
    found = CALL.match(tool)
    raw = found.group(1) if found else next((s for s in configured if tool.startswith((s + '_', 'mcp_' + s + '_'))), None)
    if not raw:
        return None
    if raw.startswith('claude_ai_'):
        return raw[10:]
    if raw.startswith('plugin_'):
        rest = raw[7:];parts = rest.split('_');half = len(parts) // 2
        return '_'.join(parts[:half]) if len(parts) % 2 == 0 and parts[:half] == parts[half:] else rest
    return raw if raw in configured else None


def _logs(app, ident, home):
    if app == 'claude':
        base = Path(os.environ.get('CLAUDE_CONFIG_DIR') or home / '.claude') / 'projects'
        main = list(base.glob(f'*/{ident}.jsonl'))
        return main + [p for m in main for p in (m.parent / ident / 'subagents').glob('*.jsonl')]
    if app in {'pi', 'omp'}:
        base = Path(os.environ.get('PI_CODING_AGENT_DIR') or home / '.pi/agent') if app == 'pi' else home / '.omp/agent'
        return list((base / 'sessions').glob(f'*/*_{ident}.jsonl'))
    if app == 'hermes':
        db = Path(os.environ.get('HERMES_HOME') or home / '.hermes') / 'state.db'
        return [db] if db.is_file() else []
    base = Path(os.environ.get('CODEX_HOME') or home / '.codex')
    return [*(base / 'sessions').glob(f'*/*/*/rollout-*{ident}.jsonl'), *(base / 'archived_sessions').glob(f'rollout-*{ident}.jsonl')]


def _read(app, path, cache, ident):
    """Tool calls in one record, reading only what was added since the last read."""
    if app == 'hermes':
        return _read_hermes(path, cache, ident)
    key = str(path);size = path.stat().st_size;hit = cache.get(key)
    if hit and hit['size'] == size:
        return hit['calls']
    offset, calls = (hit['offset'], dict(hit['calls'])) if hit and size > hit['size'] else (0, {})
    with path.open('rb') as lines:
        lines.seek(offset)
        for raw in lines:
            if not raw.endswith(b'\n'):
                break  # a line still being written is read next time
            offset += len(raw)
            if b'"tool_use"' not in raw and b'"toolCall"' not in raw and b'_call"' not in raw:
                continue
            try:
                row = json.loads(raw)
            except ValueError:
                continue
            for name in _calls(app, row):
                calls[name] = calls.get(name, 0) + 1
    cache[key] = {'size': size, 'offset': offset, 'calls': calls}
    return calls


def _read_hermes(path, cache, ident):
    key = f'hermes:{ident}';hit = cache.get(key) or {'last': 0, 'calls': {}};calls = dict(hit['calls']);last = hit['last']
    db = sqlite3.connect(f'file:{path.as_posix()}?mode=ro', uri=True, timeout=2)
    try:
        for row_id, raw in db.execute('select id, tool_calls from messages where session_id=? and id>? and tool_calls is not null order by id', (ident, last)):
            last = row_id
            try:
                listed = json.loads(raw) or []
            except ValueError:
                continue
            for call in listed if isinstance(listed, list) else []:
                name = str(((call or {}).get('function') or {}).get('name') or (call or {}).get('name') or '')
                if name:
                    calls[name] = calls.get(name, 0) + 1
    except sqlite3.Error:
        pass
    finally:
        db.close()
    cache[key] = {'size': last, 'last': last, 'calls': calls}
    return calls


def _store():
    return state_dir() / 'aura-services.json'


def known():
    """Every service each app has been seen connected to, by its own name: {app: [names]}."""
    try:
        store = json.loads(_store().read_text(encoding='utf-8'))
        return store.get('known', {}) if store.get('version') == VERSION else {}
    except (OSError, ValueError, AttributeError):
        return {}


def used(sessions, workspace, home=None):
    """{session id: {service: calls}} for {session id: app}. Only services the person connected are counted."""
    home = Path(home or Path.home())
    try:
        store = json.loads(_store().read_text(encoding='utf-8'))
        store = store if store.get('version') == VERSION else {}
    except (OSError, ValueError, AttributeError):
        store = {}
    cache, where, known = store.get('logs', {}), store.get('sessions', {}), store.get('known', {})
    # Each app's own connected services, now or at any time before: a tool is only matched against its own app's list,
    # and calls to a service that was later removed still count as what they were.
    configured, changed = {}, False
    for owner, name, _ in workspace_library.connections(workspace, workspace_library.APPS, home, every_folder=True):
        if name in LOCAL:continue
        configured.setdefault(owner, set()).add(name)
        if name not in known.get(owner, []):known.setdefault(owner, []).append(name);changed = True
    for owner, names in known.items():configured.setdefault(owner, set()).update(names)
    out, now = {}, time.time()
    for ident, app in sessions.items():
        app = APPS.get(app)
        if not app or not isinstance(ident, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', ident):
            continue
        record = where.get(ident) or {}
        paths = [Path(p) for p in record.get('paths', []) if Path(p).is_file()]
        if not paths and now - record.get('looked', 0) > RETRY or record.get('paths') and len(paths) < len(record['paths']):
            try:
                paths = _logs(app, ident, home)
            except OSError:
                paths = []
            where[ident] = {'paths': [str(p) for p in paths], 'looked': now};changed = True
        elif app == 'claude' and paths:
            # delegated agents' logs appear as the session goes on
            extra = [p for m in paths[:1] for p in (m.parent / ident / 'subagents').glob('*.jsonl') if str(p) not in record['paths']]
            if extra:
                paths += extra;where[ident] = {'paths': [str(p) for p in paths], 'looked': now};changed = True
        counts = {}
        for path in paths:
            key = f'hermes:{ident}' if app == 'hermes' else str(path)
            try:
                before = cache.get(key, {}).get('size')
                calls = _read(app, path, cache, ident);changed = changed or before != cache[key]['size']
            except OSError:
                continue
            for tool, n in calls.items():
                name = _service(tool, configured.get(app, set()))
                if name:
                    title = workspace_library.service_title(name)
                    counts[title] = counts.get(title, 0) + n
        if counts:
            out[ident] = counts
    if changed:
        try:
            path = _store();path.parent.mkdir(parents=True, exist_ok=True);tmp = path.with_suffix('.tmp')
            tmp.write_text(json.dumps({'version': VERSION, 'logs': cache, 'sessions': where, 'known': known}, ensure_ascii=False), encoding='utf-8');os.replace(tmp, path)
        except OSError:
            pass  # counts are read again next time
    return out
