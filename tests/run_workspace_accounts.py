"""Accounts and continuing at reset: the parts where a mistake would cost a working sign-in or repeat work."""
import base64
import json
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def sign_in(account, email, refresh):
    claims = base64.urlsafe_b64encode(json.dumps({'email': email, 'https://api.openai.com/auth': {'chatgpt_plan_type': 'plus'}}).encode()).decode().rstrip('=')
    return json.dumps({'auth_mode': 'chatgpt', 'tokens': {'id_token': 'x.' + claims + '.y', 'access_token': 'a', 'refresh_token': refresh, 'account_id': account}})


def main():
    with tempfile.TemporaryDirectory() as td:
        os.environ['AURA_STATE_DIR'] = str(Path(td) / 'state')
        os.environ['CODEX_HOME'] = str(Path(td) / 'codex')
        home = Path(os.environ['CODEX_HOME']); home.mkdir()
        import workspace_accounts as accounts
        if os.name != 'nt':  # The OS keyring is not available in every CI; exercise the logic with a memory vault.
            store = {}
            accounts.Vault.read = lambda self: dict(store)
            accounts.Vault.write = lambda self, rows: (store.clear(), store.update(rows))
        auth = home / 'auth.json'

        auth.write_text(sign_in('acct-1', 'one@example.com', 'r1'), encoding='utf-8')
        first = accounts.codex_capture('Personal')
        assert first['email'] == 'one@example.com' and first['plan'] == 'plus'
        auth.write_text(sign_in('acct-2', 'two@example.com', 'r2'), encoding='utf-8')
        second = accounts.codex_capture('Work')
        assert {a['nickname'] for a in accounts.public('codex')['accounts']} == {'Personal', 'Work'}

        # Codex refreshes its sign-in in place; switching away must keep that newer sign-in.
        auth.write_text(sign_in('acct-2', 'two@example.com', 'r2-refreshed'), encoding='utf-8')
        accounts.codex_switch(first['id'])
        assert json.loads(auth.read_text(encoding='utf-8'))['tokens']['account_id'] == 'acct-1'
        accounts.codex_switch(second['id'])
        assert json.loads(auth.read_text(encoding='utf-8'))['tokens']['refresh_token'] == 'r2-refreshed', 'refreshed sign-in was lost'
        assert [a['nickname'] for a in accounts.public('codex')['accounts'] if a['active']] == ['Work']
        try:
            accounts.remove(second['id']); raise AssertionError('removed the account Codex is using')
        except ValueError:
            pass

        (home / 'config.toml').write_text('cli_auth_credentials_store = "keyring"\n', encoding='utf-8')
        assert accounts.codex_supported()[0] is False
        (home / 'config.toml').unlink()

        for bad in ({'mode': 'sometimes'}, {'resume': 'always'}, {'unknown': 'x'}):
            try:
                accounts.set_policy(bad); raise AssertionError(f'accepted {bad}')
            except ValueError:
                pass
        accounts.set_policy({'mode': 'auto', 'goals': 'ask'})
        assert accounts.mode_for('chats') == 'auto' and accounts.mode_for('goals') == 'ask'

        import workspace_resume as resume
        resume.add('biz', td, 'chat-1', time.time() - 120)
        resume.add('biz', td, 'chat-2', time.time() + 3600)
        assert [r['chat_id'] for r in resume.take_due(td)] == ['chat-1']
        assert resume.take_due(td) == [], 'a continue ran twice'
        assert resume.for_chat('chat-2') and not resume.for_chat('chat-1')
    print('Accounts passed: Codex sign-in swap keeps refreshed sign-ins, keyring refusal, settings validation, and continue-at-reset runs once.')


if __name__ == '__main__':
    main()
