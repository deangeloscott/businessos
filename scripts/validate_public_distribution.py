#!/usr/bin/env python3
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_NAME='ViralTrac AURA';EXPECTED_EXPANSION='Agentic Understanding and Reinforcement Architecture'
REQUIRED=['LICENSE.md','TRADEMARKS.md','SECURITY.md','PUBLIC-DISTRIBUTION.md','PUBLISHER.json','BRANDING.md','DEPLOYMENT.md','distribution/deployment-profiles.json','core/policies/workspace-and-human-knowledge.md','core/schemas/config/workspace-profile.schema.json','scripts/configure_workspace.py','scripts/migrate_workspace.py','scripts/workspace_status.py','scripts/generate_knowledge_layer.py','scripts/register_human_note.py','deployment/update-policy.json']
LEGACY_PUBLIC_NAMES=["ViralTrac's BusinessOS",'ViralTrac BusinessOS'];LEGACY_BRAND_ALLOW={'CHANGELOG.md','BRANDING.md','PUBLISHER.json','scripts/validate_public_distribution.py'};FORBIDDEN_PATH_PARTS=['apps/api/src','packages/contracts','infra/d1','DIRECTIVES_STATUS.md']
FORBIDDEN_TEXT=[(re.compile(r'\bDirective\s+\d+(?:\.\d+)?\b',re.I),'internal engineering directive numbering'),(re.compile(r'\bGAP-\d+\b',re.I),'internal roadmap gap id'),(re.compile(r'apps/api/src|packages/contracts|infra/d1|DIRECTIVES_STATUS\.md',re.I),'private ViralTrac repository path'),(re.compile(r'\bVT_MASTER_KEY\w*\b|\bCH_PASSWORD\b|\bCF_ACCESS_CLIENT_SECRET\b',re.I),'private infrastructure secret/config name'),(re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),'private key material'),(re.compile(r'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}\b'),'GitHub credential material')]
TEXT_SUFFIXES={'.md','.json','.py','.txt','.yaml','.yml','.toml','.ini','.cfg','.csv'}


def validate_public_distribution():
    errors=[]
    for rel in REQUIRED:
        if not (ROOT/rel).exists():errors.append(f'missing required public-distribution file: {rel}')
    local_workspace=ROOT/'.businessos/workspace.json'
    if local_workspace.exists():errors.append('contains local .businessos/workspace.json; never distribute an organization workspace pointer/profile')
    for p in ROOT.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(ROOT).as_posix()
        if any(x.lower() in rel.lower() for x in FORBIDDEN_PATH_PARTS):errors.append(f'forbidden internal path included: {rel}')
        if p.name.startswith('.env') or p.suffix.lower() in {'.pem','.key','.p12','.pfx'}:errors.append(f'sensitive credential/config file included: {rel}')
        if p.suffix.lower() not in TEXT_SUFFIXES and p.name!='VERSION':continue
        try:text=p.read_text(errors='strict')
        except (UnicodeDecodeError,OSError):continue
        if rel not in LEGACY_BRAND_ALLOW:
            for legacy in LEGACY_PUBLIC_NAMES:
                if legacy in text:errors.append(f'{rel}: legacy public name {legacy!r} is historical-only; use ViralTrac AURA')
        if rel!='scripts/validate_public_distribution.py':
            for rx,label in FORBIDDEN_TEXT:
                if rx.search(text):errors.append(f'{rel}: contains {label}')
    inst=ROOT/'instances'
    if inst.exists():
        unexpected=[p.name for p in inst.iterdir() if p.is_dir() and p.name!='_template']
        if unexpected:errors.append(f'contains business instances: {unexpected}')
    up=ROOT/'deployment/update-policy.json'
    if up.exists():
        d=json.loads(up.read_text())
        if d.get('enabled') is not False:errors.append('update checks must be disabled by default')
        if d.get('auto_download') is not False:errors.append('auto_download must be false')
        if d.get('auto_install') is not False:errors.append('auto_install must be false')
        if d.get('transmit_business_data') is not False:errors.append('transmit_business_data must be false')
    pub=ROOT/'PUBLISHER.json'
    if pub.exists():
        d=json.loads(pub.read_text());publisher=d.get('publisher') or {}
        if not publisher.get('canonical_project_url'):errors.append('canonical public project URL missing')
        if publisher.get('product_name')!=EXPECTED_NAME:errors.append(f'publisher product_name must be {EXPECTED_NAME!r}')
        if publisher.get('product_acronym')!='AURA':errors.append('publisher product_acronym must be AURA')
        if publisher.get('product_name_expansion')!=EXPECTED_EXPANSION:errors.append('publisher AURA expansion is missing/incorrect')
        if publisher.get('product_descriptor')!='AI-native BusinessOS':errors.append('publisher descriptor must remain AI-native BusinessOS')
        if (d.get('updates') or {}).get('auto_install') is not False:errors.append('publisher update metadata must prohibit auto-install')
        if (d.get('updates') or {}).get('business_data_transmitted') is not False:errors.append('publisher update metadata must declare no AURA/BusinessOS business-data transmission')
    meta=ROOT/'INSTALLATION.json'
    if meta.exists():
        d=json.loads(meta.read_text());edition=d.get('edition');display=str(d.get('display_name',''));public=str(d.get('public_name',''))
        if edition=='full':
            if display!=EXPECTED_NAME or public!=EXPECTED_NAME:errors.append('full INSTALLATION.json must expose ViralTrac AURA as exact display/public name')
        elif not display.startswith(EXPECTED_NAME) or public!=display:errors.append('component/custom INSTALLATION.json must expose a ViralTrac AURA family display/public name')
        if d.get('name_expansion')!=EXPECTED_EXPANSION:errors.append('INSTALLATION.json AURA expansion is missing/incorrect')
        if d.get('descriptor')!='AI-native BusinessOS':errors.append('INSTALLATION.json descriptor must remain AI-native BusinessOS')
        if d.get('configurable_workspace_root') is not True:errors.append('INSTALLATION.json must declare configurable_workspace_root=true')
        if d.get('human_knowledge_layer') is not True:errors.append('INSTALLATION.json must declare human_knowledge_layer=true')
        if d.get('deployment_profiles')!='distribution/deployment-profiles.json':errors.append('INSTALLATION.json deployment_profiles path is missing/incorrect')
        if 'host_capability_discovery' in d:errors.append('INSTALLATION.json must not claim AURA-owned host capability discovery')
    editions=ROOT/'distribution/editions.json'
    if editions.exists():
        ed=json.loads(editions.read_text()).get('editions',[]);full=next((x for x in ed if x.get('id')=='full'),None)
        if not full or full.get('display_name')!=EXPECTED_NAME:errors.append('full edition must be named ViralTrac AURA')
        for item in ed:
            if not str(item.get('display_name','')).startswith(EXPECTED_NAME):errors.append(f"edition {item.get('id')} is outside the ViralTrac AURA naming family")
    if errors:
        print(f'Public distribution validation errors: {len(errors)}')
        for e in errors:print('ERROR',e)
        raise SystemExit(1)
    print('public distribution validation passed');return True

if __name__=='__main__':validate_public_distribution()
