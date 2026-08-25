#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parents[1]

REQUIRED=['LICENSE.md','TRADEMARKS.md','SECURITY.md','PUBLIC-DISTRIBUTION.md','PUBLISHER.json','DEPLOYMENT.md','distribution/deployment-profiles.json','core/policies/workspace-and-human-knowledge.md','core/schemas/runtime/workspace-profile.schema.json','scripts/configure_workspace.py','scripts/workspace_status.py','scripts/generate_knowledge_layer.py','deployment/update-policy.json']
FORBIDDEN_PATH_PARTS=[
    'apps/api/src','packages/contracts','infra/d1','DIRECTIVES_STATUS.md',
]
FORBIDDEN_TEXT=[
    (re.compile(r'\bDirective\s+\d+(?:\.\d+)?\b',re.I),'internal engineering directive numbering'),
    (re.compile(r'\bGAP-\d+\b',re.I),'internal roadmap gap id'),
    (re.compile(r'apps/api/src|packages/contracts|infra/d1|DIRECTIVES_STATUS\.md',re.I),'private ViralTrac repository path'),
    (re.compile(r'\bVT_MASTER_KEY\w*\b|\bCH_PASSWORD\b|\bCF_ACCESS_CLIENT_SECRET\b',re.I),'private infrastructure secret/config name'),
    (re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),'private key material'),
    (re.compile(r'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}\b'),'GitHub credential material'),
]
TEXT_SUFFIXES={'.md','.json','.py','.txt','.yaml','.yml','.toml','.ini','.cfg','.csv'}


def validate_public_distribution():
    errors=[]
    for rel in REQUIRED:
        if not (ROOT/rel).exists(): errors.append(f'missing required public-distribution file: {rel}')
    # The product-local workspace pointer/profile is operator-specific runtime configuration,
    # not distributable source. It may contain an absolute private workspace path.
    local_workspace=ROOT/'.businessos/workspace.json'
    if local_workspace.exists(): errors.append('contains local .businessos/workspace.json; never distribute an operator workspace pointer/profile')
    for p in ROOT.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(ROOT).as_posix()
        if rel == 'scripts/validate_public_distribution.py':
            continue
        if any(x.lower() in rel.lower() for x in FORBIDDEN_PATH_PARTS): errors.append(f'forbidden internal path included: {rel}')
        if p.name.startswith('.env') or p.suffix.lower() in {'.pem','.key','.p12','.pfx'}:
            errors.append(f'sensitive credential/config file included: {rel}')
        if p.suffix.lower() not in TEXT_SUFFIXES and p.name not in {'VERSION'}: continue
        try: text=p.read_text(errors='strict')
        except (UnicodeDecodeError,OSError): continue
        for rx,label in FORBIDDEN_TEXT:
            if rx.search(text): errors.append(f'{rel}: contains {label}')
    # No packaged business state.
    inst=ROOT/'instances'
    if inst.exists():
        unexpected=[p.name for p in inst.iterdir() if p.is_dir() and p.name!='_template']
        if unexpected: errors.append(f'contains business instances: {unexpected}')
    # No reusable operator identity.
    op=ROOT/'deployment/operator-profile.json'
    if op.exists():
        d=json.loads(op.read_text())
        if any(v not in (None,'') for v in (d.get('identity') or {}).values()) or d.get('reuse_across_businesses'):
            errors.append('contains populated reusable operator identity')
    # Public update policy must be safe-by-default and notification-only.
    up=ROOT/'deployment/update-policy.json'
    if up.exists():
        d=json.loads(up.read_text())
        if d.get('enabled') is not False: errors.append('update checks must be disabled by default')
        if d.get('auto_download') is not False: errors.append('auto_download must be false')
        if d.get('auto_install') is not False: errors.append('auto_install must be false')
        if d.get('transmit_business_data') is not False: errors.append('transmit_business_data must be false')
    pub=ROOT/'PUBLISHER.json'
    if pub.exists():
        d=json.loads(pub.read_text())
        if not (d.get('publisher') or {}).get('canonical_project_url'): errors.append('canonical public project URL missing')
        if (d.get('updates') or {}).get('auto_install') is not False: errors.append('publisher update metadata must prohibit auto-install')
        if (d.get('updates') or {}).get('business_data_transmitted') is not False: errors.append('publisher update metadata must declare no BusinessOS business-data transmission')
    inst_meta=ROOT/'INSTALLATION.json'
    if inst_meta.exists():
        d=json.loads(inst_meta.read_text())
        if d.get('configurable_workspace_root') is not True: errors.append('INSTALLATION.json must declare configurable_workspace_root=true')
        if d.get('human_knowledge_layer') is not True: errors.append('INSTALLATION.json must declare human_knowledge_layer=true')
        if d.get('deployment_profiles')!='distribution/deployment-profiles.json': errors.append('INSTALLATION.json deployment_profiles path is missing/incorrect')
    if errors:
        print(f'Public distribution validation errors: {len(errors)}')
        for e in errors: print('ERROR',e)
        raise SystemExit(1)
    print('public distribution validation passed')
    return True

if __name__=='__main__': validate_public_distribution()
