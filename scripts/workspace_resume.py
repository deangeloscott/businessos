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
import math
import threading
from datetime import datetime
from pathlib import Path

from workspace_startup import state_dir
from workspace_sharing import destination_lock

TASK = 'ViralTrac AURA continue'
LOCK = threading.RLock()


def _path():
    return state_dir() / 'resumes.json'


def pending():
    try:
        rows = json.loads(_path().read_text(encoding='utf-8'))
    except FileNotFoundError:
        return []
    except (OSError,ValueError):
        raise ValueError('Saved continuations could not be read. The original file was kept; restore it before scheduling more work.') from None
    if not isinstance(rows,list) or any(not isinstance(r,dict) or not all(isinstance(r.get(k),str) for k in ('id','workspace','business','chat_id'))
            or not (r.get('chat_id') or r.get('app')) or type(r.get('at')) not in {int,float} or not math.isfinite(r['at']) for r in rows):
        raise ValueError('Saved continuations need attention. The original file was kept.')
    return rows


def _write(rows):
    target = _path()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(rows, indent=2), encoding='utf-8')
    temporary.replace(target)


def add(business, workspace, chat_id, at, text='Continue where you left off.', app='', basis=None, **context):
    """chat_id continues that chat; with no chat, app starts a new chat (a limited scheduled task)."""
    if type(at) not in {int,float} or not math.isfinite(at):raise ValueError('Choose a valid reset time.')
    workspace=str(Path(workspace).resolve())
    with LOCK,destination_lock(_path()):
        rows = [r for r in pending() if not (r['workspace']==workspace and r['business']==business and
            (chat_id and r['chat_id']==chat_id or not chat_id and context.get('task_id') and r.get('task_id')==context['task_id']))]
        rows.append({'id': secrets.token_hex(6), 'business': business, 'workspace': workspace, 'chat_id': chat_id or '',
                     'app': app, 'at': float(at) + 60, 'text': text, 'created': time.time(), 'status':'pending','basis':basis,
                     **{k:v for k,v in context.items() if k in {'task_id','task_basis','goal_id','project','limit_recovery'}}})
        _write(rows)
        return rows[-1]


def cancel(chat_id, workspace=None, business=None):
    with LOCK,destination_lock(_path()):
        _write([r for r in pending() if not (chat_id and r['chat_id']==chat_id and
            (workspace is None or Path(r['workspace']).resolve()==Path(workspace).resolve()) and (business is None or r['business']==business))])


def settle(ident, reason='', retry=False):
    """Consume only a confirmed start; retain uncertain work for review, or defer a busy chat."""
    with LOCK,destination_lock(_path()):
        rows=pending()
        for row in rows:
            if row['id']==ident:
                row.update(status='pending' if retry else 'needs_review',reason=reason)
                if retry:row['next_attempt_at']=time.time()+30
        _write([r for r in rows if r['id']!=ident or reason])


def take_due(workspace, now=None):
    """Claim due work durably. A crash during launch requires review rather than a duplicate action."""
    now = time.time() if now is None else now
    with LOCK,destination_lock(_path()):
        rows = pending()
        due = [r for r in rows if r.get('status','pending')=='pending' and max(r['at'],r.get('next_attempt_at',0))<=now
               and Path(r['workspace']).resolve()==Path(workspace).resolve()]
        for row in due:row.update(status='needs_review',reason='A continuation was interrupted. Review the chat before continuing.')
        if due:_write(rows)
        return due


def for_chat(chat_id, workspace=None, business=None):
    return next((r for r in pending() if chat_id and r['chat_id']==chat_id and
        (workspace is None or Path(r['workspace']).resolve()==Path(workspace).resolve()) and (business is None or r['business']==business)),None)


# --- Even when closed: one system wake-up for the earliest pending continue ----------------

def _launch_argv(product, workspace):
    interpreter = Path(sys.executable).resolve()
    if sys.platform == 'win32' and interpreter.with_name('pythonw.exe').is_file():
        interpreter = interpreter.with_name('pythonw.exe')
    return [str(interpreter), '-X', 'utf8', '-E', '-s', '-B', str(Path(product) / 'scripts/open_aura.py'),
            '--no-open', '--workspace', str(workspace), '--local-state', str(state_dir().resolve())]


def schedule_wake(product):
    """Point the single AURA wake-up at the earliest pending continue, or remove it when none remain."""
    rows = sorted((r for r in pending() if r.get('status','pending')=='pending'), key=lambda r:max(r['at'],r.get('next_attempt_at',0)))
    if not rows:
        return clear_wake()
    at, argv = max(time.time()+60,rows[0]['at'],rows[0].get('next_attempt_at',0)), _launch_argv(product, rows[0]['workspace'])
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
