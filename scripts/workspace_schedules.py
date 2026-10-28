"""Read native schedule inventories; leave execution and edits with their owner."""
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess

try:
    import tomllib
except ImportError:
    tomllib = None


def roots():
    return (Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')),
            Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes')))


def inventory(codex_home=None, hermes_home=None, workspaces=(), antigravity_home=None):
    defaults = roots()
    codex_home, hermes_home = Path(codex_home or defaults[0]), Path(hermes_home or defaults[1])
    items, notes = [], []
    def append(owner, profile, native_id, **values):
        key = hashlib.sha256(f'{owner}:{profile}:{native_id}'.encode()).hexdigest()[:24]
        items.append({'id':key, 'owner':owner, 'profile':profile, 'native_id':str(native_id), **values})
    for path in sorted((codex_home / 'automations').glob('*/automation.toml'))[:200]:
        try:
            if not tomllib:
                raise ValueError('Reading Codex schedules needs Python 3.11 or newer.')
            data = tomllib.loads(path.read_text(encoding='utf-8'))
            append('codex', 'default', data.get('id', path.parent.name),
                   app='Codex', name=data.get('name') or path.parent.name,
                   schedule=data.get('rrule', ''), model=data.get('model', ''),
                   effort=data.get('reasoning_effort', data.get('reasoningEffort', '')),
                   status=str(data.get('status', 'unknown')).lower(),
                   next_run=data.get('next_run_at', ''), editable=False,
                   runtime='Requires the Codex desktop app',
                   workspace=data.get('cwds', []))
        except (OSError, ValueError, TypeError) as exc:
            notes.append(f'Codex: {exc}')
    profiles = [('default', hermes_home)]
    profiles += [(p.name, p) for p in sorted((hermes_home / 'profiles').glob('*')) if p.is_dir()]
    for profile, home in profiles[:50]:
        path = home / 'cron' / 'jobs.json'
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            jobs = data.get('jobs', [])
            if not isinstance(jobs, list):
                raise ValueError('The native schedule list has an unsupported format.')
            for job in jobs[:200]:
                schedule = job.get('schedule') or {}
                raw = schedule.get('expr') or schedule.get('value') or (f"every {schedule['minutes']}m" if schedule.get('minutes') else '')
                append('hermes', profile, job['id'], app='Hermes' + (f' · {profile}' if profile != 'default' else ''),
                       name=job.get('name') or 'Scheduled task',
                       schedule=job.get('schedule_display') or raw, schedule_raw=raw,
                       model=job.get('model') or '', effort=job.get('reasoning_effort') or '',
                       provider=job.get('model_provider') or '',
                       status=job.get('state') or ('active' if job.get('enabled', True) else 'paused'),
                       next_run=job.get('next_run_at') or '', workspace=job.get('workdir') or '', editable=True,
                       runtime='Requires the Hermes gateway')
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            notes.append(f'Hermes ({profile}): could not read schedules. {exc}')
    # pi-schedule-prompt documents project-local storage. Read only workspaces
    # the user opened; do not crawl the computer or rewrite a live scheduler.
    seen = set()
    for folder in list(workspaces)[:13]:
        root = Path(folder).expanduser().resolve()
        if root in seen:
            continue
        seen.add(root)
        path = root / '.pi/schedule-prompts.json'
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            if data.get('version') != 1 or not isinstance(data.get('jobs'), list):
                raise ValueError('Unsupported Pi schedule format')
            for job in data['jobs'][:200]:
                append('pi', str(root), job['id'], app='Pi', name=job.get('name') or 'Scheduled prompt',
                       schedule=job.get('schedule', ''), model=job.get('model', ''), effort='', provider='',
                       status='enabled' if job.get('enabled') else 'paused', next_run=job.get('nextRun', ''),
                       editable=False, workspace=str(root), session=job.get('session', ''), source_path=str(path),
                       runtime='Requires the original Pi session' if job.get('session') else 'Requires Pi open in this workspace')
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            notes.append('Pi: a saved schedule list could not be read. Check it in Pi.')
    # Antigravity's documented persistent schedule sidecars, not conversation
    # timers or a guess at its private desktop database.
    home = Path(antigravity_home or Path.home() / '.gemini/config')
    paths = sorted((home / 'sidecars').glob('*/sidecar.json'))
    paths += sorted((home / 'plugins').glob('*/sidecars/*/sidecar.json'))
    try:
        config = json.loads((home / 'config.json').read_text(encoding='utf-8')) if (home / 'config.json').exists() else {}
        enabled = config.get('sidecars', {})
        if not isinstance(enabled, dict):
            raise ValueError('Unsupported sidecar configuration')
        for path in paths[:200]:
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
                if data.get('builtin') != 'schedule':
                    continue
                args = data.get('args', [])
                if not isinstance(args, list) or not args or not all(isinstance(a, str) for a in args):
                    raise ValueError('Unsupported sidecar schedule')
                ident = path.parent.name
                if path.is_relative_to(home / 'plugins'):
                    ident = path.relative_to(home / 'plugins').parts[0] + '/' + ident
                settings = enabled.get(ident, {})
                append('antigravity', 'sidecars', ident, app='Google Antigravity',
                       name=data.get('display_name') or data.get('description') or ident,
                       schedule=args[0], model='', effort='', provider='',
                       status='enabled' if settings.get('enabled') is True else 'paused', next_run='',
                       editable=False, workspace='', source_path=str(path),
                       runtime='Requires the Antigravity app')
            except (OSError, ValueError, KeyError, TypeError, AttributeError):
                notes.append('Google Antigravity: a schedule could not be read. Check it in the app.')
    except (OSError, ValueError, TypeError, AttributeError):
        notes.append('Google Antigravity: schedule settings could not be read. Check them in the app.')
    return {'items':items, 'notes':notes,
            'support':'Shows local Codex and Hermes schedules, Pi schedule-prompt jobs in opened workspaces, and Google Antigravity schedule sidecars. Live-chat timers, Claude schedules and cloud-only jobs are not automatically listed. Enabled means configured; the owning app must still be running.'}


def update(ident, data, hermes_command, env):
    # Resolve the opaque ID again instead of accepting a client-supplied command,
    # profile path, or native task ID. Never move a job by rewriting its store.
    task = next((t for t in inventory()['items'] if t['id'] == ident), None)
    if not task:
        raise ValueError('This task is no longer available. Refresh the task list.')
    if not task['editable'] or task['owner'] != 'hermes' or not hermes_command:
        raise ValueError('This app does not expose direct schedule controls. Adjust it in its native app.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:-]{0,199}', task['native_id']):
        raise ValueError('This native task ID is unsupported. Manage it in Hermes.')
    action = data.get('action', 'edit')
    if action not in {'edit', 'pause', 'resume'}:
        raise ValueError('Choose Edit, Pause, or Resume.')
    argv = [*hermes_command, 'cron', action, task['native_id']]
    changes = []
    if action == 'edit':
        for field, flag in [('name','--name'), ('schedule','--schedule'), ('model','--model'), ('provider','--provider'), ('effort','--reasoning-effort')]:
            if field not in data:
                continue
            value = str(data[field]).strip()
            if len(value) > 500 or '\n' in value or '\r' in value or (field in {'name','schedule'} and not value):
                raise ValueError('Enter a short name and a valid schedule.')
            if field == 'effort' and value not in {'','none','minimal','low','medium','high','xhigh','max','ultra'}:
                raise ValueError('Choose a supported effort level.')
            argv += [flag, value]
            changes.append(field)
        if not changes:
            return task
    native_env = dict(env)
    home = roots()[1]
    native_env['HERMES_HOME'] = str(home if task['profile'] == 'default' else home / 'profiles' / task['profile'])
    flags = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
    result = subprocess.run(argv, env=native_env, stdin=subprocess.DEVNULL, capture_output=True,
                            text=True, encoding='utf-8', errors='replace', timeout=30, **flags)
    if result.returncode:
        raise ValueError((result.stderr or result.stdout).strip()[-1500:] or 'The scheduler could not save this change.')
    refreshed = next((t for t in inventory()['items'] if t['id'] == ident), None)
    if not refreshed:
        raise ValueError('The scheduler replied, but the task could not be read back. Check Hermes before retrying.')
    if action in {'pause','resume'} and (refreshed['status'] == 'paused') != (action == 'pause'):
        raise ValueError('The requested status could not be confirmed. Refresh or check Hermes.')
    for field in changes:
        if field != 'schedule' and refreshed[field] != str(data[field]).strip():
            raise ValueError('The requested change could not be confirmed. Refresh or check Hermes.')
    return refreshed
