"""Focused regressions for lost requests, native errors, and safe workspace handoffs."""
from pathlib import Path
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import zipfile
from unittest.mock import patch, PropertyMock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def main():
    import workspace_agents, workspace_codex, workspace_storage, workspace_guidance
    from workspace_ui import Workspace
    from workspace_connections import Connections
    from _native_secrets import NativeSecrets
    from _process_errors import ErrorTail, redact
    assert 'secret-value-123' not in redact('refresh_token="secret-value-123"', {})
    with tempfile.TemporaryDirectory(prefix='aura-recovery-') as tmp, patch.dict(os.environ):
        base = Path(tmp)
        source = base / 'Original workspace'
        os.environ['BUSINESSOS_WORKSPACE'] = str(source)
        os.environ['BUSINESSOS_WORKSPACE_CONFIG'] = str(base / 'pointer.json')
        from setup import setup
        result = setup(organization='Recovery café')
        assert result['status'] == 'ready'
        bid = result['business_id']
        asset = source / 'attachments' / bid / 'offer.txt'
        asset.parent.mkdir(parents=True, exist_ok=True)
        asset.write_text('A useful offer, with café details.', encoding='utf-8')
        backups = base / 'backups'
        backups.mkdir()
        saved = workspace_storage.backup(source, backups)
        assert saved['verified'] and asset.read_text(encoding='utf-8').startswith('A useful')
        target = base / 'Restored workspace'
        restored = workspace_storage.restore(saved['path'], target)
        assert restored['verified'] and (target / asset.relative_to(source)).read_bytes() == asset.read_bytes()
        assert workspace_storage.inspect(target)['businesses'][0]['id'] == bid
        for folder in (source, target):
            try:
                workspace_storage.restore(saved['path'], folder)
                raise AssertionError('Restore overwrote an occupied workspace')
            except ValueError:
                pass
        try:
            workspace_storage.backup(source, source / 'attachments')
            raise AssertionError('Nested backups must be refused')
        except ValueError:
            pass
        tampered = base / 'tampered.zip'
        with zipfile.ZipFile(saved['path']) as original, zipfile.ZipFile(tampered, 'w') as bad:
            for item in original.infolist():
                value = original.read(item)
                bad.writestr(item, value + b'changed' if item.filename.endswith('offer.txt') else value)
        untouched = base / 'Do not create'
        try:
            workspace_storage.restore(tampered, untouched)
            raise AssertionError('Corrupt backup was restored')
        except ValueError:
            assert not untouched.exists()
        native = base / 'native'
        native.mkdir()
        instructions = native / 'CLAUDE.md'
        instructions.write_text('Keep my custom instructions.\n', encoding='utf-8')
        workspace_guidance.attach('claude', ROOT, native)
        workspace_guidance.attach('claude', ROOT, native)
        assert instructions.read_text().count('<!-- AURA workspace attachment -->') == 1
        assert instructions.read_text().startswith('Keep my custom instructions.')
        workspace_guidance.refresh(base / 'New AURA release', native)
        assert str(base / 'New AURA release') in instructions.read_text()
        assert instructions.read_text().startswith('Keep my custom instructions.')
        (native / '.hermes.md').write_text('Keep the selected Hermes rules.\n')
        workspace_guidance.attach('hermes', ROOT, native)
        assert 'AURA workspace attachment' in (native / '.hermes.md').read_text()
        assert workspace_guidance.attach('antigravity', ROOT, native)['status'] == 'request-guidance'

        # A large stderr burst must be drained while stdout waits for stdin.
        env = dict(os.environ, EXAMPLE_API_KEY='never-print-this-key-12345')
        program = "import sys,os;sys.stderr.write('x'*100000+'\\n401 invalid API key '+os.environ['EXAMPLE_API_KEY']);sys.stderr.flush();sys.stdin.read();sys.exit(1)"
        for kind in ('codex','pi','omp','claude','hermes','antigravity'):
            command = [sys.executable, '-c', program, *(['exec','-'] if kind == 'codex' else ['--print'])]
            try:
                if kind == 'codex':
                    workspace_codex.run(command, source, 'Keep this request', None, 'example', 'low', lambda **kw:None, env)
                else:
                    workspace_agents.run(command, kind, source, env, 'Keep this request', None, 'example', '', lambda **kw:None)
                raise AssertionError('Native failure was reported as success')
            except ValueError as exc:
                assert '401 invalid API key' in str(exc) and env['EXAMPLE_API_KEY'] not in str(exc), str(exc)
        app = Workspace(settings_file=base / 'preferences.json')
        app.connection_kind = 'codex'
        app.agent = {'name':'Codex', 'argv':[sys.executable,'-c',program,'exec','-']}
        app.preferences['connection'] = {'kind':'codex','model':'example','effort':'low'}
        with patch.dict(os.environ, EXAMPLE_API_KEY=env['EXAMPLE_API_KEY']):
            app.start_chat(bid, 'Keep my useful request after restart', [])
            for _ in range(150):
                if app.job['status'] != 'working':
                    break
                time.sleep(.05)
            assert app.job['status'] == 'error' and 'valid credentials' in app.job['reply']
            reopened = Workspace(settings_file=app.settings_file)
            view = reopened.conversation(bid)
            assert view['messages'][0]['text'] == 'Keep my useful request after restart'
            assert env['EXAMPLE_API_KEY'] not in json.dumps(view)

        # Native storage keeps keys out of argv and AURA files.
        memory = {}
        def load_mac(value=None):
            if value is not None:
                memory['value'] = value
            return memory.get('value', '{}')
        with patch('workspace_connections.WINDOWS',False), patch('_native_secrets.sys.platform','darwin'), patch.object(NativeSecrets,'_mac',side_effect=load_mac):
            keys = Connections(base / 'keys')
            keys.save('fal','fixture-native-secret','computer')
            assert keys.storage_name == 'macOS Keychain'
            assert Connections(base / 'keys').environment()['FAL_KEY'] == 'fixture-native-secret'
            assert not keys.path.exists()
        with patch.object(NativeSecrets,'backend',new_callable=PropertyMock,return_value='Linux keyring'), patch('shutil.which',return_value='/usr/bin/secret-tool'), patch('subprocess.run') as run:
            run.return_value = subprocess.CompletedProcess([],0,'','')
            NativeSecrets()._linux('{"key":"fixture-secret"}')
            args, kwargs = run.call_args
            assert 'fixture-secret' not in ' '.join(args[0]) and 'fixture-secret' in kwargs['input']
        with patch.object(NativeSecrets,'load',side_effect=ValueError('Keyring locked')):
            keys = Connections(base / 'locked')
            with patch('workspace_connections.WINDOWS',False):
                assert keys.rows()['storage_note'] == 'Keyring locked'
                keys.save('fal','session-secret','session')
                assert keys.environment()['FAL_KEY'] == 'session-secret'

        # Opening another workspace preserves original data and readiness.
        old_bytes = asset.read_bytes()
        info = app.open_workspace(target)
        assert info['path'] == str(target) and asset.read_bytes() == old_bytes
        assert app.recent_workspaces()[0]['path'] == str(target)
        # An older product's pointer resolves the original external workspace.
        older = base / 'old-download' / '.businessos'
        older.mkdir(parents=True)
        (older / 'workspace.json').write_text(json.dumps({'workspace_root':str(source)}))
        assert workspace_storage.inspect(older.parent)['path'] == str(source)
    print('Workspace backup/restore/handoff, six-host failure recovery, request persistence, and native storage regressions passed.')


if __name__ == '__main__':
    main()
