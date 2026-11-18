"""The connected services a conversation called, read from its AI app's own session log.

The apps already write every tool call to a log on this computer. AURA reads the service name of each call and counts
calls to services the person connected: ones set up in an app's settings, claude.ai connectors and installed plugins'
services. The apps' built-in tools are not services the person connected, so they are left out. Nothing is asked of the
AI and nothing is sent anywhere.

Each log is read once, and after that only what was added to it. Counts are kept in AURA's state folder. Claude Code
(including its delegated agents) and Codex logs are read today. Each app's log format is its own and can change: a
line or log that cannot be read adds nothing.
"""
import json
import os
import re
import time
from pathlib import Path

from workspace_startup import state_dir
import workspace_library

CALL = re.compile(r'mcp__([A-Za-z0-9_.-]+?)__[A-Za-z0-9_]')
CODE_CALL = re.compile(r'tools\.mcp__([A-Za-z0-9_.-]+?)__[A-Za-z0-9_]')  # Codex calls services from code it runs
LOCAL = {'node_repl', 'cua_repl'}  # Codex's own local runtimes: listed in the Library as tools, not services
APPS = {'claude': 'claude', 'Claude Code': 'claude', 'codex': 'codex', 'Codex': 'codex'}
RETRY = 600  # seconds before looking again for a session whose log was not found


def _calls(app, row):
    """Raw service names called in one log line."""
    if app == 'claude':
        if row.get('type') != 'assistant':
            return []
        return [m.group(1) for part in (row.get('message') or {}).get('content') or []
                if isinstance(part, dict) and part.get('type') == 'tool_use' and (m := CALL.match(str(part.get('name') or '')))]
    payload = row.get('payload') or {}
    if row.get('type') != 'response_item' or payload.get('type') not in {'function_call', 'custom_tool_call'}:
        return []
    named = CALL.match(str(payload.get('name') or ''))
    return [named.group(1)] if named else CODE_CALL.findall(str(payload.get('input') or payload.get('arguments') or ''))


def _server(raw):
    """The service's own name: a claude.ai connector or a plugin's service is named without its prefix."""
    if raw.startswith('claude_ai_'):
        return raw[10:], True
    if raw.startswith('plugin_'):
        rest = raw[7:];parts = rest.split('_');half = len(parts) // 2
        return ('_'.join(parts[:half]) if len(parts) % 2 == 0 and parts[:half] == parts[half:] else rest), True
    return raw, False


def _logs(app, ident, home):
    if app == 'claude':
        base = Path(os.environ.get('CLAUDE_CONFIG_DIR') or home / '.claude') / 'projects'
        main = list(base.glob(f'*/{ident}.jsonl'))
        return main + [p for m in main for p in (m.parent / ident / 'subagents').glob('*.jsonl')]
    base = Path(os.environ.get('CODEX_HOME') or home / '.codex')
    return [*(base / 'sessions').glob(f'*/*/*/rollout-*{ident}.jsonl'), *(base / 'archived_sessions').glob(f'rollout-*{ident}.jsonl')]


def _read(app, path, cache):
    """Raw service calls in one log, reading only what was added since the last read."""
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
            if b'mcp__' not in raw:
                continue
            try:
                row = json.loads(raw)
            except ValueError:
                continue
            for name in _calls(app, row):
                calls[name] = calls.get(name, 0) + 1
    cache[key] = {'size': size, 'offset': offset, 'calls': calls}
    return calls


def _store():
    return state_dir() / 'aura-services.json'


def used(sessions, workspace, home=None):
    """{session id: {service: calls}} for {session id: app}. Only services the person connected are counted."""
    home = Path(home or Path.home())
    try:
        store = json.loads(_store().read_text(encoding='utf-8'))
    except (OSError, ValueError):
        store = {}
    cache, where = store.get('logs', {}), store.get('sessions', {})
    configured = {name for _, name, _ in workspace_library.connections(workspace, workspace_library.APPS, home)} - LOCAL
    out, now, changed = {}, time.time(), False
    for ident, app in sessions.items():
        app = APPS.get(app)
        if not app or not isinstance(ident, str) or not re.fullmatch(r'[A-Za-z0-9-]{1,80}', ident):
            continue
        known = where.get(ident) or {}
        paths = [Path(p) for p in known.get('paths', []) if Path(p).is_file()]
        if not paths and now - known.get('looked', 0) > RETRY or known.get('paths') and len(paths) < len(known['paths']):
            try:
                paths = _logs(app, ident, home)
            except OSError:
                paths = []
            where[ident] = {'paths': [str(p) for p in paths], 'looked': now};changed = True
        elif app == 'claude' and paths:
            # delegated agents' logs appear as the session goes on
            extra = [p for m in paths[:1] for p in (m.parent / ident / 'subagents').glob('*.jsonl') if str(p) not in known['paths']]
            if extra:
                paths += extra;where[ident] = {'paths': [str(p) for p in paths], 'looked': now};changed = True
        counts = {}
        for path in paths:
            try:
                before = cache.get(str(path), {}).get('size')
                calls = _read(app, path, cache);changed = changed or before != cache[str(path)]['size']
            except OSError:
                continue
            for raw, n in calls.items():
                name, connector = _server(raw)
                if connector or raw in configured:
                    title = workspace_library.service_title(name)
                    counts[title] = counts.get(title, 0) + n
        if counts:
            out[ident] = counts
    if changed:
        try:
            path = _store();path.parent.mkdir(parents=True, exist_ok=True);tmp = path.with_suffix('.tmp')
            tmp.write_text(json.dumps({'logs': cache, 'sessions': where}, ensure_ascii=False), encoding='utf-8');os.replace(tmp, path)
        except OSError:
            pass  # counts are read again next time
    return out
