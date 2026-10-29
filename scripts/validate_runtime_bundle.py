#!/usr/bin/env python3
"""Prove a relocated bundle can set up and serve AURA without system Python."""
import argparse
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import sys
import tarfile
import tempfile
import threading
from urllib.request import Request, urlopen
import zipfile

from workspace_execution import Execution


def validate(archive):
    archive = Path(archive).resolve()
    with tempfile.TemporaryDirectory(prefix='AURA relocated bundle ') as directory:
        base = Path(directory)
        if zipfile.is_zipfile(archive):
            with zipfile.ZipFile(archive) as bundle:
                if bundle.testzip():
                    raise ValueError('The bundle ZIP is damaged.')
                bundle.extractall(base)
        else:
            with tarfile.open(archive,'r:gz') as bundle:
                bundle.extractall(base, filter='data')
        roots = [p for p in base.iterdir() if p.is_dir()]
        if len(roots) != 1:
            raise ValueError('The bundle must contain one product folder.')
        root = roots[0]
        metadata = json.loads((root/'BUNDLED-RUNTIME.json').read_text(encoding='utf-8'))
        from workspace_updates import modified, schema_hash
        assert metadata['update_protocol'] == 1 and metadata['workspace_schema_sha256'] == schema_hash(root)
        assert not modified(root), 'The final bundled files must match their update integrity manifest'
        interpreter = root/metadata['interpreter']
        env = dict(os.environ)
        env.pop('SSL_CERT_FILE', None)
        env.update(PATH='', PYTHONHOME=str(base/'not-installed'), PYTHONPATH=str(base/'not-installed'),
                   PYTHONUSERBASE=str(base/'not-installed'), PYTHONDONTWRITEBYTECODE='1',
                   LOCALAPPDATA=str(base/'local'), XDG_STATE_HOME=str(base/'local'),
                   BUSINESSOS_WORKSPACE=str(base/'organization'),
                   BUSINESSOS_WORKSPACE_CONFIG=str(base/'workspace-pointer.json'))
        (base/'organization').mkdir()
        # -I deliberately ignores any caller Python environment. Verify native
        # dependencies and Tcl resources without creating a desktop window.
        probe = '''import json,sys,tkinter,yaml,jsonschema,attrs,rpds,certifi,urllib.request
from pathlib import Path
assert all(Path(m.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()) for m in (yaml,jsonschema,attrs,rpds,certifi))
with urllib.request.urlopen('https://pypi.org/pypi/jsonschema/json',timeout=25) as response: assert response.status==200
print(json.dumps({'python':sys.version.split()[0], 'tcl':tkinter.Tcl().eval('info patchlevel')}))'''
        native = json.loads(subprocess.check_output([str(interpreter),'-I','-B','-c',probe],
                                                   env=env,text=True,encoding='utf-8'))
        if native['python'] != metadata['python_version']:
            raise ValueError('The bundled interpreter does not match its manifest.')
        secret_storage = 'session-only fallback available'
        if sys.platform == 'darwin' and os.environ.get('GITHUB_ACTIONS') == 'true':
            # An isolated CI keychain proves the actual ctypes/native API with
            # bundled Python, without touching a person's login keychain.
            keychain = base / 'verification.keychain-db'
            import secrets
            password = secrets.token_urlsafe(24)
            subprocess.run(['/usr/bin/security','create-keychain','-p',password,str(keychain)],check=True,capture_output=True)
            try:
                subprocess.run(['/usr/bin/security','unlock-keychain','-p',password,str(keychain)],check=True,capture_output=True)
                check = ('import sys;sys.path.insert(0,sys.argv[1]);from _native_secrets import NativeSecrets;'
                         's=NativeSecrets("aura.bundle.verification",sys.argv[2]);'
                         'assert s.load()=={};s.save({"test":{"key":"temporary-fixture"}});'
                         'assert s.load()["test"]["key"]=="temporary-fixture";s.save({});assert s.load()=={}')
                subprocess.run([str(interpreter),'-I','-B','-c',check,str(root/'scripts'),str(keychain)],
                               env=env,check=True,capture_output=True,text=True,timeout=40)
                secret_storage = 'macOS Keychain native round-trip passed'
            finally:
                subprocess.run(['/usr/bin/security','delete-keychain',str(keychain)],check=True,capture_output=True)
        launcher = root/metadata['launcher']
        options = ['--no-open','--port','0','--workspace',str(base/'organization')]
        if os.name == 'nt':
            # cmd /s /c needs an outer quote pair around a quoted batch path
            # plus arguments; Popen's ordinary argv quoting is not that grammar.
            command = subprocess.list2cmdline([str(launcher),*options])
            argv = subprocess.list2cmdline([os.environ.get('COMSPEC',r'C:\Windows\System32\cmd.exe')])+' /d /s /c "'+command+'"'
        else:
            argv = ['/bin/sh',str(launcher),*options]
        control = Execution()
        lines = queue.Queue()
        with control.popen(argv,cwd=root,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace') as process:
            def read():
                for line in process.stdout:
                    lines.put(line)
                lines.put(None)
            threading.Thread(target=read,daemon=True).start()
            transcript = []
            try:
                while True:
                    line = lines.get(timeout=45)
                    if line is None:
                        raise ValueError('The bundled launcher could not start: '+''.join(transcript))
                    transcript.append(line)
                    match = re.search(r'http://127\.0\.0\.1:\d+/',line)
                    if match:
                        address = match.group(0)
                        break
                with urlopen(address,timeout=15) as response:
                    page = response.read().decode('utf-8')
                token = re.search(r'name="aura-token" content="([^"]+)"',page).group(1)
                def api(path,data=None):
                    request = Request(address.rstrip('/')+path,
                                      data=json.dumps(data).encode() if data is not None else None,
                                      headers={'X-Aura-Token':token,'Content-Type':'application/json'})
                    with urlopen(request,timeout=90) as response:
                        return json.load(response)
                initial = api('/api/state')
                update = api('/api/updates', {'action':'policy', 'policy':'manual'})
                assert update['current'] == metadata['aura_version'] and update['policy'] == 'manual'
                assert not initial['businesses'] and not initial['connection']['connected']
                setup = api('/api/setup',{'name':'Runtime bundle smoke café'})
                state = api('/api/state?business='+setup['business_id'])
                assert state['version']==metadata['aura_version'] and not state['diagnostics']
                assert state['business_id']==setup['business_id'] and not state['connection']['connected']
                assert Path(state['workspace']).resolve()==(base/'organization').resolve()
                assert any(r['type']=='Business' and r['title']=='Runtime bundle smoke café' for r in state['records'])
                assert (base/'organization'/'instances'/setup['business_id']).is_dir()
            finally:
                control.stop()
                process.wait(timeout=10)
        updater_test = Path(__file__).resolve().parents[1] / 'tests/run_workspace_updates.py'
        if updater_test.is_file():
            proof = subprocess.run([str(interpreter), '-I', '-B', str(updater_test)], cwd=updater_test.parents[1],
                                   env=env, capture_output=True, text=True, encoding='utf-8', timeout=120)
            if proof.returncode:
                raise ValueError('Native updater checks failed:\n' + (proof.stdout + proof.stderr)[-8000:])
        return {'platform':metadata['platform'],'aura_version':metadata['aura_version'],
                'python_version':native['python'],'tcl_version':native['tcl'],
                'relocated_path_with_spaces':True,'system_python_removed_from_path':True,
                'isolated_libraries':True,'first_use_setup':'passed','local_interface':'passed',
                'https_certificate_verification':'passed',
                'update_integrity_and_settings':'passed',
                'native_updater_boundaries':'passed' if updater_test.is_file() else 'not included',
                'native_secret_storage':secret_storage,
                'ai_requests_sent':0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    args = parser.parse_args()
    print(json.dumps(validate(args.archive)))
