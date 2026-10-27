#!/usr/bin/env python3
"""Packaging boundary checks; native archive/first-use proof runs on each OS."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from package_runtime import build, download, native_platform, unpack_wheel

manifest = json.loads((ROOT/'distribution/bundled-runtimes.json').read_text())
assert set(manifest['platforms']) == {'windows-x64','windows-arm64','macos-x64','macos-arm64','linux-x64','linux-arm64'}
for target,spec in manifest['platforms'].items():
    assert len(spec['sha256'])==64 and len(spec['wheels'])==len(manifest['packages'])
    assert {w['name']:w['version'] for w in spec['wheels']}==manifest['packages']
    assert all(len(w['sha256'])==64 for w in spec['wheels'])
with tempfile.TemporaryDirectory(prefix='aura-bundle-boundary-') as directory:
    base = Path(directory)
    raw = b'verified fixture bytes'
    expected = hashlib.sha256(raw).hexdigest()
    cached = base/(expected[:16]+'-fixture.tar.gz')
    cached.write_bytes(raw)
    spec = {'url':'https://github.com/astral-sh/python-build-standalone/releases/download/fixture/fixture.tar.gz','sha256':expected}
    assert download(spec,base)==cached
    cached.write_bytes(b'changed bytes')
    try:download(spec,base);raise AssertionError('Changed cached bytes must fail before execution')
    except ValueError:pass
    wheel = base/'unsafe.whl'
    with zipfile.ZipFile(wheel,'w') as archive:archive.writestr('../outside.txt','not allowed')
    try:unpack_wheel(wheel,base/'site');raise AssertionError('Wheel traversal must be rejected')
    except ValueError:pass
    assert not (base/'outside.txt').exists()
    try:build(native_platform(),ROOT/'bundle-output',base/'cache');raise AssertionError('Build state must stay outside product source')
    except ValueError:pass
print('Bundled runtime manifests, checksum reuse, wheel traversal and source/output isolation passed.')
