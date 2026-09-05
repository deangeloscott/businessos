#!/usr/bin/env python3
from _common import *
from pathlib import Path
import json, os, subprocess, sys, tempfile, zipfile
from package_edition import build_distribution


def base_env():
    env=dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE']='1'
    env['PYTHONUTF8']='1'
    return env


def run(root, rel, *args, env=None):
    subprocess.run(
        [sys.executable, str(Path(root)/rel), *map(str,args)],
        cwd=root,
        env=env or base_env(),
        check=True,
    )


# Validate the committed source checkout before building the user artifact.
run(ROOT,'scripts/generate_registry.py')
run(ROOT,'scripts/validate_workspace.py')
run(ROOT,'scripts/validate_public_distribution.py')
run(ROOT,'tests/run_all.py')
run(ROOT,'qualification/self_test.py')

# The full edition is the canonical public release artifact. package_edition.py
# deliberately strips maintainer qualification, developer tests, local workspace
# state, runtime state, and other non-user material before archiving it.
result=build_distribution(
    edition_id='full',
    output_dir=ROOT.parent/'distributions',
    keep_folder=True,
)
zip_path=Path(result['zip']).resolve()

# Validate what a user actually receives from a fresh unzip, not only the source
# checkout or pre-archive staging folder.
with tempfile.TemporaryDirectory(prefix='aura-release-artifact-') as td:
    unpack_root=Path(td)
    with zipfile.ZipFile(zip_path) as zf:
        bad=zf.testzip()
        if bad:
            raise SystemExit(f'ZIP integrity failed at {bad}')
        zf.extractall(unpack_root)

    product_root=unpack_root/zip_path.stem
    if not product_root.is_dir():
        raise SystemExit(f'Fresh ZIP did not contain expected product root: {product_root.name}')
    if (product_root/'qualification').exists():
        raise SystemExit('Release artifact contains maintainer-only qualification tooling')
    packaged_tests=sorted(
        p.relative_to(product_root).as_posix()
        for p in (product_root/'tests').rglob('*')
        if p.is_file()
    )
    if packaged_tests!=['tests/run_distribution.py']:
        raise SystemExit(f'Release artifact contains unexpected developer tests: {packaged_tests}')

    # Run the minimal packaged-product gate from the fresh unzip.
    run(product_root,'tests/run_distribution.py')

    # Smoke-test the normal consumer path with a separate organization workspace.
    workspace=unpack_root/'organization-workspace'
    clean=base_env()
    clean.pop('BUSINESSOS_WORKSPACE',None)
    clean.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
    run(product_root,'scripts/configure_workspace.py',workspace,'--profile','power_user','--json',env=clean)
    consumer=base_env()
    consumer['BUSINESSOS_WORKSPACE']=str(workspace)
    consumer.pop('BUSINESSOS_WORKSPACE_CONFIG',None)
    run(product_root,'scripts/init_business.py','release-smoke','--name','Release Smoke Test',env=consumer)
    run(product_root,'scripts/validate_business.py','release-smoke',env=consumer)

print(json.dumps(result,indent=2))
print('fresh release artifact validation passed')
print('consumer external-workspace smoke test passed')
