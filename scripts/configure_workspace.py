#!/usr/bin/env python3
"""Configure the active ViralTrac AURA organization workspace without changing product source."""
from _common import *
import argparse,json
from jsonschema import Draft202012Validator


def _profile_id(value):
    value=str(value).strip().lower().replace('-','_')
    if value not in {'simple','power_user','organization'}:
        raise ValueError('profile must be simple, power_user/power-user, or organization')
    return value


def _profiles():
    p=PRODUCT_ROOT/'distribution/deployment-profiles.json'
    data=json.loads(p.read_text())
    return {x['id']:x for x in data.get('profiles',[])}


def _business_ids(root):
    ir=Path(root)/'instances'
    if not ir.exists(): return []
    return sorted(p.name for p in ir.iterdir() if p.is_dir() and p.name!='_template')


def _workspace_gitignore():
    return """# ViralTrac AURA organization-workspace safety defaults\n# Canonical state is intentionally versionable; secrets and ephemeral logs are not.\n.env\n.env.*\nsecrets/\ncredentials/\n*.pem\n*.key\n*.p12\n*.pfx\n*.jks\n.DS_Store\nThumbs.db\nruntime/runs/**/logs/\nruntime/tmp/\nattachments/private/\n"""


def _workspace_readme(profile):
    return f"""# ViralTrac AURA Organization Workspace\n\nAURA = Agentic Understanding and Reinforcement Architecture.\n\nDeployment profile: **{profile['name']}** (`{profile['id']}`).\n\nThis directory is organization/user-owned AURA state, not a copy of the AURA product source.\n\n- `instances/` — canonical durable BusinessOS state.\n- `runtime/` — bounded run/recovery state.\n- `knowledge/` — human-facing generated Markdown plus clearly noncanonical notes.\n- `attachments/` — optional workspace-owned files; keep large/sensitive authoritative data in the governing external system when appropriate.\n\nGit/version control is optional. If this workspace is stored in Git, use a private repository appropriate to the organization and never commit credentials or secrets.\n\nOpen `knowledge/` directly in Obsidian or another Markdown tool if desired; AURA does not require Obsidian.\n"""


def configure(root_value,profile_value='simple',knowledge_enabled=True,write_link=True,force=False,allow_state_switch=False):
    profile_id=_profile_id(profile_value); profiles=_profiles(); profile=profiles[profile_id]
    current=workspace_root().resolve()
    root=Path(os.path.expanduser(os.path.expandvars(str(root_value or PRODUCT_ROOT))))
    root=root.resolve() if root.is_absolute() else (Path.cwd()/root).resolve()
    if root!=current and not allow_state_switch:
        current_businesses=_business_ids(current);target_businesses=_business_ids(root)
        missing=[x for x in current_businesses if x not in target_businesses]
        if missing:
            raise ValueError('Current workspace contains business state not present at the target ('+', '.join(missing)+'). Use scripts/migrate_workspace.py to copy/verify state first, or --allow-state-switch only when intentionally selecting a different workspace.')
    root.mkdir(parents=True,exist_ok=True)
    for rel in ['.businessos','instances','runtime/runs','attachments']:
        (root/rel).mkdir(parents=True,exist_ok=True)
    if knowledge_enabled:
        (root/'knowledge').mkdir(parents=True,exist_ok=True)
    profile_path=root/'.businessos/workspace.json'
    prior={}
    if profile_path.exists():
        try: prior=json.loads(profile_path.read_text())
        except Exception:
            if not force: raise ValueError(f'Existing workspace profile is invalid; use --force after inspection: {profile_path}')
    ts=now()
    data={
        'format_version':'1.0','profile':profile_id,'created_at':prior.get('created_at',ts),'updated_at':ts,
        'product_version':os_version(),'external_state':root!=PRODUCT_ROOT.resolve(),'knowledge_enabled':bool(knowledge_enabled),
        'knowledge_root':'knowledge','git_strategy':profile['git_strategy'],'collaboration':profile['collaboration'],
        'notes':['Canonical BusinessOS truth remains under instances/.','Human notes under knowledge/<business-id>/notes are noncanonical until governed incorporation.']
    }
    schema=json.loads((PRODUCT_ROOT/'core/schemas/runtime/workspace-profile.schema.json').read_text())
    errs=list(Draft202012Validator(schema).iter_errors(data))
    if errs: raise ValueError('Invalid workspace profile: '+'; '.join(e.message for e in errs))
    profile_path.write_text(json.dumps(data,indent=2)+'\n')
    if root!=PRODUCT_ROOT.resolve():
        gi=root/'.gitignore'
        if not gi.exists(): gi.write_text(_workspace_gitignore())
        wr=root/'WORKSPACE.md'
        if not wr.exists(): wr.write_text(_workspace_readme(profile))
    if knowledge_enabled:
        kr=root/'knowledge'; readme=kr/'README.md'
        if not readme.exists():
            readme.write_text('# ViralTrac AURA Human Knowledge Layer\n\nOpen this folder in Obsidian, VS Code, or any Markdown tool. Generated pages are derived from canonical BusinessOS objects; human notes are noncanonical until explicitly incorporated through normal AURA evidence/truth governance.\n')
    link_path=workspace_config_path(); link_written=False
    # When the product root itself is the workspace, profile_path and link_path are the
    # same local file. The profile already implies product-local/default selection, so do
    # not overwrite it with a pointer object. For external workspaces, write the local
    # untracked product pointer unless the host will select via BUSINESSOS_WORKSPACE.
    if write_link and root!=PRODUCT_ROOT.resolve():
        link_path.parent.mkdir(parents=True,exist_ok=True)
        link={'format_version':'1.0','workspace_root':str(root),'profile':profile_id,'knowledge_enabled':bool(knowledge_enabled)}
        link_path.write_text(json.dumps(link,indent=2)+'\n');link_written=True
    return {'workspace_root':str(root),'profile':profile_id,'external_state':data['external_state'],'knowledge_enabled':bool(knowledge_enabled),'workspace_profile':str(profile_path),'local_link':str(link_path) if link_written else None,'git_strategy':profile['git_strategy'],'collaboration':profile['collaboration']}


def main():
    p=argparse.ArgumentParser(description='Configure a ViralTrac AURA workspace. No external workspace is required; omit the path to keep state with the product folder.')
    p.add_argument('workspace_root',nargs='?',default=str(PRODUCT_ROOT))
    p.add_argument('--profile',default='simple',help='simple | power_user | organization')
    p.add_argument('--no-knowledge',action='store_true')
    p.add_argument('--no-link',action='store_true',help='Create the workspace but do not write the local untracked product pointer; use BUSINESSOS_WORKSPACE instead.')
    p.add_argument('--allow-state-switch',action='store_true',help='Select a different workspace even when current businesses are not present there. Use migrate_workspace.py instead when moving existing state.')
    p.add_argument('--force',action='store_true')
    p.add_argument('--json',action='store_true')
    a=p.parse_args()
    try:r=configure(a.workspace_root,a.profile,not a.no_knowledge,not a.no_link,a.force,a.allow_state_switch)
    except ValueError as e: raise SystemExit(str(e))
    if a.json: print(json.dumps(r,indent=2))
    else:
        print(f"workspace={r['workspace_root']}")
        print(f"profile={r['profile']} external_state={str(r['external_state']).lower()} knowledge={str(r['knowledge_enabled']).lower()}")
        print(f"git_strategy={r['git_strategy']} collaboration={r['collaboration']}")
        if r['local_link']: print(f"local_pointer={r['local_link']}")
        print('NEXT: initialize or use a business normally; stateful AURA/BusinessOS helpers now resolve the configured workspace automatically.')

if __name__=='__main__': main()
