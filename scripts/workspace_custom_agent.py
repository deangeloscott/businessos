"""One machine-local ACP agent the user adds from the interface.

Same shape as --agent-file. Stored outside the product folder so upgrades keep it.
The agent owns its models, accounts, tools and permissions; AURA only launches it.
"""
import json
import os
import shlex
import shutil
from pathlib import Path

from workspace_startup import state_dir


def path():
    return state_dir() / 'custom-agent.json'


def load():
    try:
        agent = json.loads(path().read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    argv = agent.get('argv') if isinstance(agent, dict) else None
    if not isinstance(agent.get('name'), str) or not isinstance(argv, list) or not argv or not all(isinstance(a, str) and a for a in argv):
        return None
    return agent


def parse(command):
    """Split a launch command the way the user's platform would."""
    text = str(command or '').strip()
    if not text or len(text) > 2000 or '\0' in text:
        raise ValueError('Enter the command that starts your agent in ACP mode.')
    parts = shlex.split(text, posix=os.name != 'nt')
    return [p[1:-1] if len(p) > 1 and p[0] == p[-1] and p[0] in '"\'' else p for p in parts]


def save(name, command):
    name = str(name or '').strip()
    if not name or len(name) > 80:
        raise ValueError('Name your agent in up to 80 characters.')
    argv = parse(command)
    executable = shutil.which(argv[0]) or (argv[0] if Path(argv[0]).is_file() else None)
    if not executable:
        raise ValueError(f'Could not find {argv[0]!r}. Install the agent or use its full path.')
    agent = {'name': name, 'argv': [executable, *argv[1:]], 'native_protocol': 'acp'}
    target = path()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(agent, indent=2), encoding='utf-8')
    temporary.replace(target)
    return agent


def remove():
    try:
        path().unlink()
    except FileNotFoundError:
        pass
