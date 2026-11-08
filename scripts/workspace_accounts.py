"""Several accounts for one AI app, using each app's own sign-in.

Claude Code: a long-lived token from its own `claude setup-token`, supplied per request.
Codex: its saved sign-in file. Switching swaps that file, exactly as signing out and in does,
so the same conversations stay available. OMP, Hermes and Pi manage their own accounts.

Secrets stay in OS-protected storage on this computer: never in business files, exports or logs.
What happens when a plan limit is reached is the user's choice; "Ask" is the default.
"""
import base64
import json
import os
import re
import secrets
import shutil
import subprocess
import time
from pathlib import Path

from workspace_startup import state_dir

MODES = ('ask', 'auto', 'off')
RESUME = ('off', 'open', 'closed')
POLICY = {'mode': 'ask', 'chats': '', 'goals': '', 'backup_app': '', 'resume': 'off'}
SWITCHABLE = {'claude', 'codex'}
NATIVE = {'omp': 'OMP balances work across every account you sign in to (`omp login` once per account).',
          'hermes': 'Hermes rotates to the next account in its credential pool when one hits a limit, and can then use a fallback provider.',
          'pi': 'Pi switches accounts automatically with the pi-multi-account extension (third-party).',
          'antigravity': 'Not available yet: Antigravity offers no supported way to use another account.'}
PI_PACKAGE = 'npm:pi-multi-account'


def _store():
    return state_dir() / 'accounts.json'


def load():
    try:
        data = json.loads(_store().read_text(encoding='utf-8'))
    except (OSError, ValueError):
        data = {}
    accounts = [a for a in data.get('accounts', []) if isinstance(a, dict) and a.get('app') in SWITCHABLE and a.get('id')]
    policy = {**POLICY, **{k: v for k, v in (data.get('policy') or {}).items() if k in POLICY}}
    return {'accounts': accounts, 'policy': policy}


def _save(data):
    target = _store()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2), encoding='utf-8')
    temporary.replace(target)


class Vault:
    """The same OS-protected storage AURA uses for API keys, in a separate entry."""

    def __init__(self):
        self.path = state_dir() / 'app-accounts.bin'

    def read(self):
        if os.name == 'nt':
            from workspace_connections import protect
            if not self.path.exists():
                return {}
            try:
                return json.loads(protect(self.path.read_bytes(), decrypt=True))
            except (OSError, ValueError):
                raise ValueError('Saved app accounts could not be opened on this computer.') from None
        from _native_secrets import NativeSecrets
        store = NativeSecrets(service='com.viraltrac.aura.app-accounts')
        if not store.backend:
            raise ValueError('Secure storage is unavailable here, so extra accounts cannot be saved.')
        return store.load()

    def write(self, rows):
        if os.name == 'nt':
            from workspace_connections import protect
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_suffix('.tmp')
            temporary.write_bytes(protect(json.dumps(rows).encode()))
            temporary.replace(self.path)
            return
        from _native_secrets import NativeSecrets
        store = NativeSecrets(service='com.viraltrac.aura.app-accounts')
        if not store.backend:
            raise ValueError('Secure storage is unavailable here, so extra accounts cannot be saved.')
        store.save(rows)


def _nickname(value, fallback):
    text = ' '.join(str(value or '').split())[:40]
    return text or fallback


def public(app=None):
    """Account list without secrets."""
    data = load()
    rows = [{k: a.get(k) for k in ('id', 'app', 'nickname', 'email', 'plan', 'active', 'added_at')}
            for a in data['accounts'] if app in (None, a['app'])]
    return {'accounts': rows, 'policy': data['policy'], 'native': NATIVE}


def set_policy(changes):
    data = load()
    for key, value in (changes or {}).items():
        if key not in POLICY:
            raise ValueError('Choose a supported setting.')
        if key in {'mode'} and value not in MODES or key in {'chats', 'goals'} and value not in ('', *MODES) or \
                key == 'resume' and value not in RESUME or key == 'backup_app' and not isinstance(value, str):
            raise ValueError('Choose one of the offered options.')
        data['policy'][key] = value
    _save(data)
    return data['policy']


def mode_for(context):
    """chats or goals: its own override, otherwise the AURA-wide choice."""
    policy = load()['policy']
    return policy.get(context) or policy['mode']


def rename(account_id, nickname):
    data = load()
    account = next((a for a in data['accounts'] if a['id'] == account_id), None)
    if not account:
        raise ValueError('That account is no longer saved.')
    account['nickname'] = _nickname(nickname, account.get('nickname') or 'Account')
    _save(data)
    return public(account['app'])


def remove(account_id):
    data = load()
    account = next((a for a in data['accounts'] if a['id'] == account_id), None)
    if not account:
        return public()
    if account['app'] == 'codex' and account.get('active'):
        raise ValueError('Switch Codex to another account before removing the one it is using.')
    data['accounts'] = [a for a in data['accounts'] if a['id'] != account_id]
    _save(data)
    vault = Vault()
    rows = vault.read()
    if rows.pop(account_id, None) is not None:
        vault.write(rows)
    return public(account['app'])


# --- Claude Code ------------------------------------------------------------

def add_claude(command, token, nickname=''):
    """Save a token made by `claude setup-token` and confirm Claude Code accepts it."""
    token = ''.join(str(token or '').split())  # terminals wrap long tokens; real tokens have no spaces
    if not re.fullmatch(r'[A-Za-z0-9_\-.]{20,4096}', token):
        raise ValueError('Paste the complete token that `claude setup-token` printed.')
    env = {**os.environ, 'CLAUDE_CODE_OAUTH_TOKEN': token}
    env.pop('ANTHROPIC_API_KEY', None)
    # `auth status` only reports that a token is present; one tiny request is the real check.
    # It costs nothing when the token is wrong and a single short reply when it is right.
    try:
        result = subprocess.run([*command, '-p', 'Reply with OK', '--model', 'haiku', '--output-format', 'json'], capture_output=True,
                                text=True, encoding='utf-8', errors='replace', timeout=120, env=env, stdin=subprocess.DEVNULL,
                                cwd=str(state_dir()), creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        checked = json.loads(result.stdout or '{}')
    except (OSError, ValueError, subprocess.SubprocessError):
        raise ValueError('Claude Code could not check this token. Try again in a moment.') from None
    if (result.returncode != 0 or not isinstance(checked, dict) or checked.get('type') != 'result'
            or checked.get('subtype') != 'success' or checked.get('is_error') is not False
            or not isinstance(checked.get('result'), str) or not checked['result'].strip()):
        raise ValueError('Claude Code did not accept this token. Run `claude setup-token` again and paste the new token.')
    status = {}
    data = load()
    ident = 'claude-' + secrets.token_hex(6)
    data['accounts'].append({'id': ident, 'app': 'claude', 'nickname': _nickname(nickname, f'Claude account {sum(a["app"] == "claude" for a in data["accounts"]) + 2}'),
                             'email': status.get('email') or '', 'plan': status.get('subscriptionType') or '', 'added_at': time.time()})
    vault = Vault()
    rows = vault.read()
    rows[ident] = {'app': 'claude', 'token': token}
    vault.write(rows)
    _save(data)
    return public('claude')


def claude_env(account_id):
    """Environment that makes one Claude Code request use this account; empty means its own sign-in."""
    if not account_id:
        return {}
    record = Vault().read().get(account_id) or {}
    if record.get('app') != 'claude' or not record.get('token'):
        raise ValueError('That Claude account is no longer saved. Choose another account.')
    return {'CLAUDE_CODE_OAUTH_TOKEN': record['token']}


# --- Codex ------------------------------------------------------------------

def codex_home():
    return Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')


def _codex_identity(raw):
    tokens = raw.get('tokens') or {}
    claims = {}
    try:
        part = str(tokens.get('id_token', '')).split('.')[1]
        claims = json.loads(base64.urlsafe_b64decode(part + '=' * (-len(part) % 4)))
    except (IndexError, ValueError):
        pass
    plan = (claims.get('https://api.openai.com/auth') or {}).get('chatgpt_plan_type', '')
    return {'account': tokens.get('account_id') or '', 'email': claims.get('email', ''), 'plan': plan}


def codex_supported():
    config = codex_home() / 'config.toml'
    try:
        text = config.read_text(encoding='utf-8')
    except OSError:
        text = ''
    if re.search(r'(?m)^\s*cli_auth_credentials_store\s*=\s*"(keyring|auto)"', text):
        return False, 'Codex keeps its sign-in in your system keyring, so AURA cannot switch it. Switch accounts in Codex instead.'
    auth = codex_home() / 'auth.json'
    try:
        raw = json.loads(auth.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return False, 'Sign in to Codex first.'
    if not (raw.get('tokens') or {}).get('account_id'):
        return False, 'Codex is signed in with an API key, not a ChatGPT account.'
    return True, ''


def codex_capture(nickname=''):
    """Remember the account Codex is signed in to now (updating its saved sign-in if already known)."""
    ok, reason = codex_supported()
    if not ok:
        raise ValueError(reason)
    text = (codex_home() / 'auth.json').read_text(encoding='utf-8')
    identity = _codex_identity(json.loads(text))
    data = load()
    account = next((a for a in data['accounts'] if a['app'] == 'codex' and a.get('account') == identity['account']), None)
    if not account:
        account = {'id': 'codex-' + secrets.token_hex(6), 'app': 'codex', 'account': identity['account'], 'added_at': time.time(),
                   'nickname': _nickname(nickname, f'Codex account {sum(a["app"] == "codex" for a in data["accounts"]) + 1}')}
        data['accounts'].append(account)
    elif nickname:
        account['nickname'] = _nickname(nickname, account['nickname'])
    account.update(email=identity['email'], plan=identity['plan'])
    for other in data['accounts']:
        if other['app'] == 'codex':
            other['active'] = other is account
    vault = Vault()
    rows = vault.read()
    rows[account['id']] = {'app': 'codex', 'auth': text}
    vault.write(rows)
    _save(data)
    return account


def codex_switch(account_id):
    """Swap Codex's saved sign-in, saving the current one first so its refreshed sign-in is kept."""
    data = load()
    target = next((a for a in data['accounts'] if a['id'] == account_id and a['app'] == 'codex'), None)
    if not target:
        raise ValueError('That Codex account is no longer saved.')
    if (codex_home() / 'auth.lock').exists() and time.time() - (codex_home() / 'auth.lock').stat().st_mtime < 30:
        raise ValueError('Codex is updating its sign-in right now. Try again in a moment.')
    codex_capture()
    record = Vault().read().get(account_id) or {}
    if not record.get('auth'):
        raise ValueError('That Codex account needs to be signed in again.')
    auth = codex_home() / 'auth.json'
    temporary = auth.with_suffix('.aura-tmp')
    temporary.write_text(record['auth'], encoding='utf-8')
    temporary.replace(auth)
    data = load()
    for account in data['accounts']:
        if account['app'] == 'codex':
            account['active'] = account['id'] == account_id
    _save(data)
    return public('codex')


def codex_login(command):
    """Start Codex's own browser sign-in for another account; the current account is saved first."""
    codex_capture()
    return subprocess.Popen([*command, 'login'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))


def usage_identity(account):
    """The usage-account identity AURA's usage records use for this saved account."""
    return account.get('account') or account.get('email') or account['id']
