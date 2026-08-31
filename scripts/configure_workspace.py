#!/usr/bin/env python3
"""Configure the active ViralTrac AURA organization workspace without changing product source."""
from _common import *
import argparse,json
from jsonschema import Draft202012Validator


def _profile_id(value):
    value=str(value).strip().lower().replace('-','_')
    if value not in {'simple','power_user','organization'}:raise ValueError('profile must be simple, power_user/power-user, or organization')
    return value


def _profiles():
    data=json.loads((PRODUCT_ROOT/'distribution/deployment-profiles.json').read_text())
    return {x['id']:x for x in data.get('profiles',[])}


def _business_ids(root):
    ir=Path(root)/'instances'
    if not ir.exists():return []
    return sorted(p.name for p in ir.iterdir() if p.is_dir() and p.name!='_template')


def _workspace_gitignore():
    return """# ViralTrac AURA organization-workspace safety defaults\n# Canonical state may be versioned; secrets and ephemeral logs should not be.\n.env\n.env.*\nsecrets/\ncredentials/\n*.pem\n*.key\n*.p12\n*.pfx\n*.jks\n.DS_Store\nThumbs.db\nruntime/runs/**/logs/\nruntime/tmp/\nattachments/private/\n"""


def _workspace_readme(profile):
    return f"""# ViralTrac AURA Organization Workspace\n\nAURA = Agentic Understanding and Reinforcement Architecture.\n\nWorkspace profile: **{profile['name']}** (`{profile['id']}`).\n\nThis directory is organization/user-owned AURA state, not a copy of the AURA product source.\n\n- `instances/` — canonical durable organization state.\n- `runtime/` — bounded work-receipt/recovery state.\n- `knowledge/` — human-facing generated Markdown plus clearly noncanonical notes.\n- `attachments/` — optional workspace-owned files.\n\nGit/version control is optional. If used, choose a private repository appropriate to the organization and never commit credentials or secrets.\n\nOpen `knowledge/` directly in Obsidian, VS Code, or another Markdown tool if desired; AURA does not require any of them.\n"""


def configure(root_value,profile_value='simple',knowledge_enabled=True,write_link=True,force=False,allow_state_switch=False):
    profile_id=_profile_id(profile_value);profiles=_profiles();profile=profiles[profile_id]
    current=workspace_root().resolve();root=Path(os.path.expanduser(os.path.expandvars(str(root_value or PRODUCT_ROOT))))
    root=root.resolve() if root.is_absolute() else (Path.cwd()/root).resolve()
    if root!=current and not allow_state_switch:
        missing=[x for x in _business_ids(current) if x not in _business_ids(root)]
        if missing:raise ValueError('Current workspace contains business state not present at the target ('+', '.join(missing)+'). Use scripts/migrate_workspace.py to copy/verify state first, or --allow-state-switch only when intentionally selecting a different workspace.')
    root.mkdir(parents=True,exist_ok=True)
    for rel in ['.businessos','instances','runtime/runs','attachments']:(root/rel).mkdir(parents=True,exist_ok=True)
    if knowledge_enabled:(root/'knowledge').mkdir(parents=True,exist_ok=True)
    profile_path=root/'.businessos/workspace.json';prior={}
    if profile_path.exists():
        try:prior=json.loads(profile_path.read_text())
        except Exception:
            if not force:raise ValueError(f'Existing workspace profile is invalid; use --force after inspection: {profile_path}')
    ts=now();data={'format_version':'1.0','profile':profile_id,'created_at':prior.get('created_at',ts),'updated_at':ts,'product_version':os_version(),'external_state':root!=PRODUCT_ROOT.resolve(),'knowledge_enabled':bool(knowledge_enabled),'knowledge_root':'knowledge','git_strategy':profile['git_strategy'],'collaboration':profile['collaboration'],'notes':['Canonical AURA organizational truth remains under instances/.','Human notes under knowledge/<business-id>/notes are noncanonical until deliberately incorporated with provenance.']}
    schema=json.loads((PRODUCT_ROOT/'core/schemas/config/workspace-profile.schema.json').read_text())
    errs=list(Draft202012Validator(schema).iter_errors(data))
    if errs:raise ValueError('Invalid workspace profile: '+'; '.join(e.message for e in errs))
    profile_path.write_text(json.dumps(data,indent=2)+'\n')
    if root!=PRODUCT_ROOT.resolve():
        gi=root/'.gitignore';wr=root/'WORKSPACE.md'
        if not gi.exists():gi.write_text(_workspace_gitignore())
        if not wr.exists():wr.write_text(_workspace_readme(profile))
    if knowledge_enabled:
        readme=root/'knowledge/README.md'
        if not readme.exists():readme.write_text('# ViralTrac AURA Human Knowledge Layer\n\nOpen this folder in Obsidian, VS Code, or any Markdown tool. Generated pages are derived from canonical AURA objects; human notes remain source material until explicitly incorporated with provenance.\n')
    link_path=workspace_config_path();link_written=False
    if write_link and root!=PRODUCT_ROOT.resolve():
        link_path.parent.mkdir(parents=True,exist_ok=True);link={'format_version':'1.0','workspace_root':str(root),'profile':profile_id,'knowledge_enabled':bool(knowledge_enabled)};link_path.write_text(json.dumps(link,indent=2)+'\n');link_written=True
    return {'workspace_root':str(root),'profile':profile_id,'external_state':data['external_state'],'knowledge_enabled':bool(knowledge_enabled),'workspace_profile':str(profile_path),'local_link':str(link_path) if link_written else None,'git_strategy':profile['git_strategy'],'collaboration':profile['collaboration']}


def main():
    p=argparse.ArgumentParser(description='Configure a ViralTrac AURA workspace. No external workspace is required.')
    p.add_argument('workspace_root',nargs='?',default=str(PRODUCT_ROOT));p.add_argument('--profile',default='simple',help='simple | power_user | organization');p.add_argument('--no-knowledge',action='store_true');p.add_argument('--no-link',action='store_true');p.add_argument('--allow-state-switch',action='store_true');p.add_argument('--force',action='store_true');p.add_argument('--json',action='store_true');a=p.parse_args()
    try:r=configure(a.workspace_root,a.profile,not a.no_knowledge,not a.no_link,a.force,a.allow_state_switch)
    except ValueError as e:raise SystemExit(str(e))
    if a.json:print(json.dumps(r,indent=2))
    else:
        print(f"workspace={r['workspace_root']}");print(f"profile={r['profile']} external_state={str(r['external_state']).lower()} knowledge={str(r['knowledge_enabled']).lower()}");print(f"git_strategy={r['git_strategy']} collaboration={r['collaboration']}")
        if r['local_link']:print(f"local_pointer={r['local_link']}")
        print('NEXT: initialize or use an organization normally; AURA stateful helpers resolve the configured workspace automatically.')

if __name__=='__main__':main()
