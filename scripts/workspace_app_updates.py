"""Keeping up with the AI apps as they update themselves.

AURA never updates an app on its own: each keeps its own way of updating, and you can still hold off. AURA reads each
app's version (no AI request), notices when it changed, checks that what AURA relies on still works, says what is new
from the lists the app reports, and, where the app can tell, says when an update is available and offers the app's own
update command. Every note is one short line; nothing is fetched from the apps' websites by AURA itself.
"""
import re
import subprocess

# How each app reports its version and updates itself. `check` reports an update without installing it, where the app
# offers that; the others install straight away, so AURA only offers their button and never claims one is available.
APPS = {
    'claude': {'name': 'Claude Code', 'update': ['update']},
    'codex': {'name': 'Codex', 'update': ['update']},
    'omp': {'name': 'OMP', 'update': ['update'], 'check': ['update', '--check'], 'latest': r'New version available:\s*v?([0-9][\w.+-]*)'},
    'pi': {'name': 'Pi', 'update': ['update', '--self']},
    'hermes': {'name': 'Hermes', 'update': ['update'], 'check': ['update', '--check'], 'latest': r'release available:\s*\S+\s+v?([0-9][\w.+-]*)'},
    'antigravity': {'name': 'Google Antigravity', 'update': ['update']},
}
VERSION = re.compile(r'(\d+\.\d+(?:\.\d+)?(?:[-+.][\w.]+)?)')
# The names the schedule reader gives each app when it cannot read something.
SCHEDULE_NAMES = {'codex': 'Codex', 'hermes': 'Hermes', 'pi': 'Pi', 'antigravity': 'Google Antigravity'}


def _run(argv, args, env, timeout):
    try:
        done = subprocess.run([*argv, *args], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout, env=env,
                              stdin=subprocess.DEVNULL, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    except (OSError, subprocess.SubprocessError):
        return ''
    return re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', (done.stdout or '') + '\n' + (done.stderr or ''))


def version(argv, env=None):
    """The app's own version string, or None when it does not answer."""
    match = VERSION.search(_run(argv, ['--version'], env, 25))
    return match.group(1) if match else None


def latest(kind, argv, env=None):
    """A newer version the app itself reports as available, or None (up to date, unknown, or no way to ask)."""
    spec = APPS.get(kind) or {}
    if not spec.get('check'):
        return None
    match = re.search(spec['latest'], _run(argv, spec['check'], env, 90))
    return match.group(1) if match else None


def added(before, now):
    """What appeared since the last look, in a stable order."""
    seen = set(before or [])
    return [x for x in dict.fromkeys(now or []) if x not in seen]


def news(name, version_now, found):
    """One short line: "New in Codex 0.164.0: 2 commands (/review, /plan), 1 model"."""
    parts = []
    for label, items in found.items():
        if not items:
            continue
        shown = ', '.join(items[:3]) + (', …' if len(items) > 3 else '')
        parts.append(f"{len(items)} {label if len(items) > 1 else label.rstrip('s')} ({shown})")
    return f"New in {name} {version_now}: " + '; '.join(parts) if parts else ''
