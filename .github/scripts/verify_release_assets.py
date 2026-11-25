#!/usr/bin/env python3
"""Validate the complete release set and optionally publish it from its exact tag."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def collect(directory, version):
    stem = 'viraltrac-aura-v' + version
    artifacts = {}

    def add(path, checksum=None):
        sidecar = path.with_name(path.name + '.sha256')
        actual = digest(path)
        if sidecar.read_text(encoding='utf-8').split() != [actual, path.name] or (checksum and checksum != actual):
            raise ValueError('Checksum mismatch for ' + path.name)
        artifacts[path.name] = (path, actual)
        artifacts[sidecar.name] = (sidecar, digest(sidecar))

    add(directory / 'aura-plain' / (stem + '.zip'))
    targets = json.loads((ROOT / 'distribution/bundled-runtimes.json').read_text(encoding='utf-8'))['platforms']
    for platform in targets:
        folder = directory / ('aura-' + platform)
        report = json.loads((folder / ('bundle-report-' + platform + '.json')).read_text(encoding='utf-8'))
        if (report.get('platform') != platform or report.get('aura_version') != version or
                any(report.get(check) != 'passed' for check in
                    ('first_use_setup', 'local_interface', 'https_certificate_verification', 'update_integrity_and_settings'))):
            raise ValueError('Incomplete verification for ' + platform)
        suffix = '.zip' if platform.startswith('windows') else '.tar.gz'
        name = stem + '-' + platform
        add(folder / (name + suffix), report['sha256'])
        app = report['app_update']
        if not re.fullmatch(r'[a-f0-9]{64}', app['runtime']) or app['name'] != name + '-app-' + app['runtime'] + suffix:
            raise ValueError('Incorrect small update for ' + platform)
        add(folder / app['name'], app['sha256'])
        if (folder / app['name']).stat().st_size >= (folder / (name + suffix)).stat().st_size:
            raise ValueError('The app-only update must be smaller than the complete download.')
    actual_names = {p.name for p in directory.rglob('*') if p.is_file() and not p.name.startswith('bundle-report-')}
    if actual_names != artifacts.keys():
        raise ValueError('Release assets differ from the expected set.')
    return artifacts


def publish(tag, artifacts):
    if os.environ.get('GITHUB_EVENT_NAME') != 'push' or os.environ.get('GITHUB_REF') != 'refs/tags/' + tag:
        raise ValueError('Publish only when the pushed tag matches VERSION.')
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() != os.environ['GITHUB_SHA']:
        raise ValueError('The checkout differs from the tagged commit.')

    def view():
        return subprocess.run(['gh', 'release', 'view', tag, '--json', 'isDraft,isPrerelease,assets'],
                              cwd=ROOT, capture_output=True, text=True, encoding='utf-8')

    current = view()
    if current.returncode:
        changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
        block = re.search(r'^## ' + re.escape(tag[1:]) + r'\b[^\n]*\n(.*?)(?=^## |\Z)', changelog, re.M | re.S)
        if not block or not block[1].strip():
            raise ValueError('Add release notes for the tagged version to CHANGELOG.md.')
        with tempfile.TemporaryDirectory() as directory:
            notes = Path(directory) / 'release.md'
            notes.write_text(block[1].strip() + '\n', encoding='utf-8')
            subprocess.run(['gh', 'release', 'create', tag, '--verify-tag', '--draft', '--prerelease',
                            '--title', 'ViralTrac AURA ' + tag[1:] + ' Alpha', '--notes-file', str(notes)],
                           cwd=ROOT, check=True)
        current = view()
        current.check_returncode()

    def checked_assets(payload):
        if not payload['isPrerelease']:
            raise ValueError('The release must be a prerelease.')
        uploaded = {}
        for item in payload['assets']:
            name = item['name']
            if name not in artifacts:
                raise ValueError('Unexpected uploaded asset ' + name)
            path, checksum = artifacts[name]
            if item['size'] != path.stat().st_size or item['digest'] != 'sha256:' + checksum or item['state'] != 'uploaded':
                raise ValueError('Uploaded asset failed verification: ' + name)
            uploaded[name] = item
        return uploaded

    release = json.loads(current.stdout)
    uploaded = checked_assets(release)
    if not release['isDraft']:
        if uploaded.keys() != artifacts.keys():
            raise ValueError('The published release is incomplete.')
        return
    missing = [str(path) for name, (path, _) in artifacts.items() if name not in uploaded]
    if missing:
        subprocess.run(['gh', 'release', 'upload', tag, *missing], cwd=ROOT, check=True)
    complete = view()
    complete.check_returncode()
    if checked_assets(json.loads(complete.stdout)).keys() != artifacts.keys():
        raise ValueError('The draft is incomplete.')
    subprocess.run(['gh', 'release', 'edit', tag, '--draft=false', '--prerelease'], cwd=ROOT, check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        parser.error('VERSION must be X.Y.Z.')
    assets = collect(args.directory.resolve(), version)
    print(f'Verified {len(assets)} release files for {version}.', flush=True)
    if args.publish:
        publish('v' + version, assets)
