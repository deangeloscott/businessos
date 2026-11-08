"""Continue a chat in the same conversation once its plan limit resets.

AURA runs due continues while it is open. "Even when closed" asks the system's own scheduler
(Task Scheduler, launchd or systemd) to start AURA quietly at that time, the same way the
startup option does. Nothing here keeps a separate background service running.
"""
import base64
import json
import os
import plistlib
import secrets
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from workspace_startup import state_dir

TASK = 'ViralTrac AURA continue'


def _path():
    return state_dir() / 'resumes.json'


def pending():
    try:
        rows = json.loads(_path().read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return []
    return [r for r in rows if isinstance(r, dict) and (r.get('chat_id') or r.get('app')) and isinstance(r.get('at'), (int, float))]


def _write(rows):
    target = _path()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(rows, indent=2), encoding='utf-8')
    temporary.replace(target)


def add(business, workspace, chat_id, at, text='Continue where you left off.', app=''):
    """chat_id continues that chat; with no chat, app starts a new chat (a limited scheduled task)."""
    rows = [r for r in pending() if not chat_id or r['chat_id'] != chat_id]
    rows.append({'id': secrets.token_hex(6), 'business': business, 'workspace': str(workspace), 'chat_id': chat_id or '',
                 'app': app, 'at': float(at) + 60, 'text': text, 'created': time.time()})
    _write(rows)
    return rows[-1]


def cancel(chat_id):
    _write([r for r in pending() if r['chat_id'] != chat_id])


def take_due(workspace, now=None):
    """Continues that are due for this workspace; they are removed before running so they run once."""
    now = now or time.time()
    rows = pending()
    due = [r for r in rows if r['at'] <= now and Path(r['workspace']).resolve() == Path(workspace).resolve()]
    if due:
        _write([r for r in rows if r not in due])
    return due


def for_chat(chat_id):
    return next((r for r in pending() if chat_id and r['chat_id'] == chat_id), None)


# --- Even when closed: one system wake-up for the earliest pending continue ----------------

def _launch_argv(product, workspace):
    interpreter = Path(sys.executable).resolve()
    if sys.platform == 'win32' and interpreter.with_name('pythonw.exe').is_file():
        interpreter = interpreter.with_name('pythonw.exe')
    return [str(interpreter), '-X', 'utf8', '-E', '-s', '-B', str(Path(product) / 'scripts/open_aura.py'),
            '--no-open', '--workspace', str(workspace), '--local-state', str(state_dir().resolve())]


def schedule_wake(product):
    """Point the single AURA wake-up at the earliest pending continue, or remove it when none remain."""
    rows = sorted(pending(), key=lambda r: r['at'])
    if not rows:
        return clear_wake()
    at, argv = rows[0]['at'], _launch_argv(product, rows[0]['workspace'])
    if sys.platform == 'win32':
        quoted = lambda value: "'" + str(value).replace("'", "''") + "'"
        when = datetime.fromtimestamp(at).strftime('%Y-%m-%dT%H:%M:%S')
        command = (f"$a=New-ScheduledTaskAction -Execute {quoted(argv[0])} -Argument {quoted(subprocess.list2cmdline(argv[1:]))} -WorkingDirectory {quoted(product)};"
                   f"$t=New-ScheduledTaskTrigger -Once -At ([datetime]::Parse({quoted(when)}));"
                   "$s=New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries;"
                   f"Register-ScheduledTask -TaskName {quoted(TASK)} -Action $a -Trigger $t -Settings $s -Force | Out-Null")
        _powershell(command)
    elif sys.platform == 'darwin':
        moment = datetime.fromtimestamp(at)
        target = Path.home() / 'Library/LaunchAgents/com.viraltrac.aura.continue.plist'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(plistlib.dumps({'Label': 'com.viraltrac.aura.continue', 'ProgramArguments': argv, 'WorkingDirectory': str(product),
                                          'StartCalendarInterval': {'Month': moment.month, 'Day': moment.day, 'Hour': moment.hour, 'Minute': moment.minute}}))
        subprocess.run(['launchctl', 'unload', str(target)], capture_output=True)
        subprocess.run(['launchctl', 'load', str(target)], capture_output=True, check=True)
    elif shutil.which('systemd-run'):
        clear_wake()
        subprocess.run(['systemd-run', '--user', '--unit=viraltrac-aura-continue', '--on-calendar=' + datetime.fromtimestamp(at).strftime('%Y-%m-%d %H:%M:%S'), *argv],
                       capture_output=True, check=True)
    else:
        raise ValueError('This system has no supported scheduler, so AURA can only continue while it is open.')
    return {'scheduled': True, 'at': at}


def clear_wake():
    if sys.platform == 'win32':
        _powershell(f"Unregister-ScheduledTask -TaskName '{TASK}' -Confirm:$false -ErrorAction SilentlyContinue")
    elif sys.platform == 'darwin':
        target = Path.home() / 'Library/LaunchAgents/com.viraltrac.aura.continue.plist'
        if target.exists():
            subprocess.run(['launchctl', 'unload', str(target)], capture_output=True)
            target.unlink()
    elif shutil.which('systemctl'):
        subprocess.run(['systemctl', '--user', 'stop', 'viraltrac-aura-continue.timer'], capture_output=True)
    return {'scheduled': False}


def wake_status():
    if sys.platform != 'win32':
        return None
    result = _powershell(f"(Get-ScheduledTask -TaskName '{TASK}' -ErrorAction SilentlyContinue | Get-ScheduledTaskInfo).NextRunTime", check=False)
    return result.stdout.strip() or None


def _powershell(command, check=True):
    encoded = base64.b64encode(command.encode('utf-16-le')).decode('ascii')
    powershell = Path(os.environ.get('SystemRoot', r'C:\Windows')) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
    return subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-EncodedCommand', encoded], capture_output=True, text=True,
                          timeout=30, check=check, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
