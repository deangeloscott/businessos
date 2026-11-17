"""Where a saved record or file was made, read on request from the AI apps' own local session logs.

AURA notes where work happened when it can see it at save time (workspace_projects.producer_context). For work done
directly in an AI app that gives commands no session id, this answers the question afterwards, from the record the
app already keeps on this computer:

  * only when someone asks about one record or file,
  * only in logs that were being written around the time it was saved,
  * only on an exact match: the record's id in the output of the save that created it, or the file's path in the
    app's own write of that file. Two sessions matching means no answer; nothing is guessed.

Nothing is sent anywhere. Found answers are kept in AURA's state folder so the world can draw them as links.
Each app's log format is its own and can change; a reader that cannot parse a log finds nothing rather than failing.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from workspace_startup import state_dir

WINDOW_BEFORE, WINDOW_AFTER = 300, 900  # seconds around the save that a log line may fall in


def _claude():
    base = Path(os.environ.get('CLAUDE_CONFIG_DIR') or Path.home() / '.claude') / 'projects'
    return list(base.glob('*/*.jsonl')) if base.is_dir() else []


def _codex():
    base = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
    return [*(base / 'sessions').glob('*/*/*/rollout-*.jsonl'), *(base / 'archived_sessions').glob('rollout-*.jsonl')]


APPS = (('Claude Code', _claude), ('Codex', _codex))


def _when(value):
    try:
        return datetime.fromisoformat(str(value).replace('Z', '+00:00')).timestamp()
    except ValueError:
        return None


def _session_id(app, path):
    return path.stem if app == 'Claude Code' else path.stem[-36:]


def _text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return ' '.join(c.get('text', '') for c in content if isinstance(c, dict))
    return ''


def _title(app, path):
    """The first thing the person asked in that session, short. It names the session; nothing else is read."""
    try:
        with path.open(encoding='utf-8', errors='replace') as lines:
            for n, line in enumerate(lines):
                if n > 400:
                    break
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if app == 'Claude Code' and row.get('type') == 'user':
                    text = _text((row.get('message') or {}).get('content'))
                elif app == 'Codex' and (row.get('payload') or {}).get('type') == 'message' and row['payload'].get('role') == 'user':
                    text = _text(row['payload'].get('content'))
                else:
                    continue
                text = ' '.join(text.split())
                if text and not text.startswith('<') and not text.startswith('# AGENTS'):
                    return text[:120]
    except OSError:
        pass
    return ''


def _writes(app, row):
    """File paths an app's own write tool wrote in this log line."""
    out = []
    if app == 'Claude Code':
        for part in (row.get('message') or {}).get('content') or []:
            if isinstance(part, dict) and part.get('type') == 'tool_use' and part.get('name') in {'Write', 'Edit', 'MultiEdit', 'NotebookEdit'}:
                out.append(str((part.get('input') or {}).get('file_path') or (part.get('input') or {}).get('notebook_path') or ''))
    else:
        payload = row.get('payload') or {}
        if payload.get('type') in {'custom_tool_call', 'function_call'}:
            text = str(payload.get('input') or payload.get('arguments') or '')
            for line in text.splitlines():
                for mark in ('*** Add File: ', '*** Update File: '):
                    if line.startswith(mark):
                        out.append(line[len(mark):].strip())
    return [p for p in out if p]


def _same_file(written, target):
    a, b = written.replace('\\', '/').lower().rstrip('/'), target.replace('\\', '/').lower().rstrip('/')
    return a == b or b.endswith('/' + a) or a.endswith('/' + b)


def _search(at, needle, match):
    """Sessions whose log has a line within the window around `at` that `match`es. Cheap checks first."""
    found = {}
    for app, logs in APPS:
        try:
            files = logs()
        except OSError:
            continue
        for path in files:
            try:
                if path.stat().st_mtime < at - WINDOW_BEFORE:
                    continue
                with path.open(encoding='utf-8', errors='replace') as lines:
                    for line in lines:
                        if needle not in line:
                            continue
                        try:
                            row = json.loads(line)
                        except ValueError:
                            continue
                        when = _when(row.get('timestamp'))
                        if when is None or not at - WINDOW_BEFORE <= when <= at + WINDOW_AFTER or not match(app, row, line):
                            continue
                        key = (app, _session_id(app, path))
                        if key not in found or when < found[key][0]:
                            found[key] = (when, path)
                        break
            except OSError:
                continue
    return found


def _store():
    return state_dir() / 'aura-origins.json'


def known():
    """Origins found so far, by record id, for the world's links."""
    try:
        data = json.loads(_store().read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}
    return {k[7:]: v for k, v in data.items() if k.startswith('record:') and isinstance(v, dict)}


def _remember(key, value):
    path = _store()
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        data = {}
    data[key] = value
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    os.replace(tmp, path)


def find(record_id=None, created_at=None, file_path=None, file_time=None):
    """One session, or None. A record is matched by its id in the save's output; a file by the app's own write of it."""
    if record_id:
        key, at, needle = 'record:' + record_id, _when(created_at), record_id
        match = lambda app, row, line: True  # the id itself is unique; the window ties it to its creation
    elif file_path:
        key, at, needle = 'file:' + file_path, file_time, Path(file_path.replace('\\', '/')).name
        match = lambda app, row, line: any(_same_file(w, file_path) for w in _writes(app, row))
    else:
        return None
    if at is None:
        return None
    found = _search(at, needle, match)
    if len(found) != 1:
        return None  # nothing, or more than one session: not certain, so no answer
    (app, ident), (when, path) = next(iter(found.items()))
    result = {'kind': 'session', 'app': app, 'id': ident, 'title': _title(app, path),
              'at': datetime.fromtimestamp(when, timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')}
    _remember(key, result)
    return result
