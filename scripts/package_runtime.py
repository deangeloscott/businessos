#!/usr/bin/env python3
"""Build one native, relocatable AURA download. No runtime binaries enter Git."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def native_platform():
    system = {'Windows':'windows', 'Darwin':'macos', 'Linux':'linux'}.get(platform.system())
    machine = platform.machine().lower()
    arch = 'arm64' if machine in {'arm64','aarch64'} else 'x64' if machine in {'amd64','x86_64'} else ''
    if not system or not arch:
        raise ValueError('This platform does not have a bundled runtime yet.')
    return system+'-'+arch


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def download(record, cache):
    """Only use pinned upstream bytes, including when reusing the build cache."""
    url, expected = record['url'], record['sha256']
    if urlsplit(url).scheme != 'https' or urlsplit(url).hostname not in {'github.com','raw.githubusercontent.com','files.pythonhosted.org'}:
        raise ValueError('Runtime downloads must use the pinned official upstream hosts.')
    cache.mkdir(parents=True, exist_ok=True)
    name = Path(unquote(urlsplit(url).path)).name
    target = cache/(expected[:16]+'-'+name)
    if target.exists():
        if digest(target) != expected:
            raise ValueError('A cached runtime download has changed. Remove this cache file and retry: '+str(target))
        return target
    print('Downloading '+name, flush=True)
    with tempfile.NamedTemporaryFile(dir=cache, suffix='.partial', delete=False) as stream:
        temporary = Path(stream.name)
        try:
            with urlopen(Request(url, headers={'User-Agent':'AURA-runtime-builder'}), timeout=120) as response:
                shutil.copyfileobj(response, stream)
        except BaseException:
            stream.close()
            temporary.unlink(missing_ok=True)
            raise
    if digest(temporary) != expected:
        temporary.unlink()
        raise ValueError('The runtime download did not match its pinned SHA-256: '+name)
    temporary.replace(target)
    return target


def unpack_wheel(archive, destination):
    with zipfile.ZipFile(archive) as wheel:
        for member in wheel.infolist():
            path = Path(member.filename)
            if path.is_absolute() or '..' in path.parts or any(p.endswith('.data') for p in path.parts):
                raise ValueError('The pinned wheel needs an unsupported installation layout: '+member.filename)
        wheel.extractall(destination)


def clean_environment():
    env = dict(os.environ)
    for name in ('PYTHONHOME','PYTHONPATH','PYTHONUSERBASE','PYTHONSTARTUP',
                 'BUSINESSOS_WORKSPACE','BUSINESSOS_WORKSPACE_CONFIG'):
        env.pop(name, None)
    env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1')
    return env


def write_launcher(root, target):
    if target.startswith('windows'):
        name = 'Open AURA.cmd'
        text = '@echo off\r\nsetlocal DisableDelayedExpansion\r\n"%~dp0.aura-runtime\\python.exe" -X utf8 -E -s -B "%~dp0scripts\\open_aura.py" %*\r\nif errorlevel 1 (\r\n echo AURA could not open. Check the message above.\r\n pause\r\n exit /b 1\r\n)\r\n'
    else:
        name = 'Open AURA.command' if target.startswith('macos') else 'Open AURA.sh'
        text = '#!/bin/sh\nHERE=${0%/*}\n[ "$HERE" != "$0" ] || HERE=.\nCDPATH= cd -- "$HERE" || exit 1\nexec "$PWD/.aura-runtime/bin/python3" -X utf8 -E -s -B "$PWD/scripts/open_aura.py" "$@"\n'
    launcher = root/name
    launcher.write_bytes(text.encode('utf-8'))
    launcher.chmod(0o755)
    return name


def build(target, output, cache):
    manifest = json.loads((ROOT/'distribution/bundled-runtimes.json').read_text(encoding='utf-8'))
    if target not in manifest['platforms'] or target != native_platform():
        raise ValueError('Build and verify this target on its native OS and architecture: '+target)
    spec = manifest['platforms'][target]
    output, cache = Path(output).resolve(), Path(cache).resolve()
    if output.is_relative_to(ROOT) or cache.is_relative_to(ROOT):
        raise ValueError('Keep bundle outputs and runtime caches outside the product source folder.')
    output.mkdir(parents=True, exist_ok=True)
    version = (ROOT/'VERSION').read_text().strip()
    name = 'viraltrac-aura-v'+version+'-'+target
    suffix = '.zip' if target.startswith('windows') else '.tar.gz'
    archive = output/(name+suffix)
    if archive.exists():
        raise ValueError('This bundle already exists; use a new output directory: '+str(archive))
    upstream = download(spec, cache)
    with tempfile.TemporaryDirectory(prefix='aura-bundle-build-', dir=output) as directory:
        temporary = Path(directory)
        with tarfile.open(upstream, 'r:gz') as runtime:
            runtime.extractall(temporary, filter='data')
        python_root = temporary/'python'
        interpreter = python_root/spec['interpreter']
        env = clean_environment()
        purelib = subprocess.check_output([str(interpreter),'-I','-B','-c',
                   'import sysconfig; print(sysconfig.get_path("purelib"))'],env=env,text=True).strip()
        libraries = Path(purelib).resolve()
        if not libraries.is_relative_to(python_root.resolve()):
            raise ValueError('The Python runtime did not resolve its own library directory.')
        libraries.mkdir(parents=True, exist_ok=True)
        for wheel in spec['wheels']:
            unpack_wheel(download(wheel, cache), libraries)
        # Supply portable HTTPS roots (not an OS-wide certificate change).
        # An explicitly configured certificate bundle keeps precedence.
        (libraries/'sitecustomize.py').write_text(
            'import os\nimport certifi\nos.environ.setdefault("SSL_CERT_FILE", certifi.where())\n',encoding='utf-8')
        # Build through the bundled interpreter: the build does not need host
        # PyYAML/jsonschema either. This retains the existing clean packaging gate.
        subprocess.run([str(interpreter),'-X','utf8','-E','-s','-B',str(ROOT/'scripts/package_edition.py'),
                        '--edition','full','--output-dir',str(temporary/'base')],env=env,cwd=ROOT,check=True)
        root = temporary/name
        (temporary/'base'/('viraltrac-aura-v'+version)).rename(root)
        python_root.rename(root/'.aura-runtime')
        shutil.copy2(download(manifest['license_notices'], cache),root/'.aura-runtime/THIRD-PARTY-LICENSES.rst')
        if target.startswith('windows') and not (root/'.aura-runtime/python3.exe').exists():
            shutil.copy2(root/'.aura-runtime/python.exe',root/'.aura-runtime/python3.exe')
        launcher = write_launcher(root, target)
        metadata = {'format_version':'1.0','aura_version':version,'platform':target,
                    'python_version':manifest['python_version'],'upstream':manifest['upstream'],
                    'runtime_sha256':spec['sha256'],'packages':manifest['packages'],
                    'launcher':launcher,'interpreter':'.aura-runtime/'+spec['interpreter']}
        (root/'BUNDLED-RUNTIME.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
        notices = ('# Bundled runtime notices\n\nPython is provided by Astral python-build-standalone.\n'
                   +spec['url']+'\n\nPinned upstream SHA-256: '+spec['sha256']+'\n\n'
                   'The upstream aggregate license text is included in .aura-runtime/THIRD-PARTY-LICENSES.rst. '
                   'It may describe optional upstream components as well as those in this build. '
                   'Original Python, standard-library, native-library, pip, and package license notices '
                   'are retained inside .aura-runtime, including package .dist-info license directories. '
                   'Those components retain their respective licenses; AURA’s license does not replace them.\n\n'
                   +'Included application libraries: '+', '.join(k+' '+v for k,v in manifest['packages'].items())+'.\n')
        (root/'THIRD-PARTY-RUNTIME.md').write_text(notices,encoding='utf-8')
        readme = root/'README.md'
        readme.write_text('# Open AURA\n\nThis download includes Python and AURA’s required libraries. '
                          'Keep the folder together; no separate Python installation is needed.\n\n'
                          '**Open `'+launcher+'` to start.** On Linux, choose Run as Program, or run `./"'+launcher+'"`. '
                          'The launcher opens your browser. Keep its terminal open while using the workspace; '
                          'close it to stop the local view.\n\nConnect an existing AI app, or use the short setup guide to download one and sign in. '
                          'AI accounts, local models, and optional tools such as FFmpeg are not included.\n\n'
                          'macOS may require approving the downloaded launcher in Privacy & Security. '
                          'This release is not notarized; AURA does not disable OS protections.\n\n'
                          'Your business files remain editable and usable in other apps. New UI workspaces use Documents/AURA Workspaces by default. '
                          'A newer AURA download reuses your selected workspace. Add or open a workspace can find older saved work and preview it first. '
                          'Back up or restore includes a file preview and an option to include linked files. '
                          'Keep your existing business data when upgrading; application files and account sign-ins remain separate.\n\n---\n\n'
                          +readme.read_text(encoding='utf-8'),encoding='utf-8')
        from workspace_updates import schema_hash, write_integrity
        metadata.update(update_protocol=1, workspace_schema_sha256=schema_hash(root))
        (root/'BUNDLED-RUNTIME.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
        write_integrity(root)
        if suffix == '.zip':
            shutil.make_archive(str(archive.with_suffix('')), 'zip', temporary, name)
        else:
            with tarfile.open(archive,'w:gz') as bundle:
                bundle.add(root,arcname=name)
    checksum = digest(archive)
    archive.with_name(archive.name+'.sha256').write_text(checksum+'  '+archive.name+'\n',encoding='utf-8')
    # Verify the final archive after extracting to another path with spaces,
    # not the build tree. The check deliberately removes Python from PATH.
    report = subprocess.check_output([sys.executable,str(ROOT/'scripts/validate_runtime_bundle.py'),str(archive)],text=True)
    verification = json.loads(report)
    verification['sha256'] = checksum
    (output/('bundle-report-'+target+'.json')).write_text(json.dumps(verification,indent=2)+'\n',encoding='utf-8')
    return {'archive':str(archive),'sha256':checksum,'verification':verification}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform',default=native_platform())
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--cache-dir',required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.platform,args.output_dir,args.cache_dir),indent=2))
