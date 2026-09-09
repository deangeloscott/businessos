#!/usr/bin/env python3
"""Idempotently prepare AURA's own workspace and organization state.

This is a thin composition layer over existing AURA primitives. It does not install
third-party software, configure credentials, or guess a host's Skill mechanism.
"""
from pathlib import Path
import argparse,json,os,re

from _common import PRODUCT_ROOT,business_directory,business_ids,resolve_business,slug,workspace_profile,workspace_root
from configure_workspace import configure
from init_business import init_business
from doctor import doctor


def _ensure_generated():
    required=[PRODUCT_ROOT/'generated/workflow-registry.json',PRODUCT_ROOT/'generated/schema-registry.json']
    if all(path.exists() for path in required):return False
    import generate_registry
    generate_registry.main()
    missing=[str(path.relative_to(PRODUCT_ROOT)) for path in required if not path.exists()]
    if missing:raise ValueError('AURA generated indexes are still missing after regeneration: '+', '.join(missing))
    return True


def _target_path(value):
    if value is None:return workspace_root().resolve()
    p=Path(os.path.expanduser(os.path.expandvars(str(value))))
    return p.resolve() if p.is_absolute() else (Path.cwd()/p).resolve()


def _profile_for(root,requested):
    if requested:return requested
    profile_path=root/'.businessos/workspace.json'
    if profile_path.exists():
        try:
            data=json.loads(profile_path.read_text())
            if isinstance(data,dict) and data.get('profile'):return data['profile']
        except Exception:pass
    if root==workspace_root().resolve():return workspace_profile().get('profile','simple')
    return 'power_user' if root!=PRODUCT_ROOT.resolve() else 'simple'


def _stable_business_id(name):
    value=slug(name)[:64].strip('-')
    if not value or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',value):
        raise ValueError('Could not derive a stable organization ID; supply --business-id explicitly.')
    return value


def _resolve_or_initialize(organization=None,business_id=None):
    directory=business_directory();ids=set(business_ids())
    if organization:
        name=str(organization).strip()
        if not name:raise ValueError('organization name must not be empty')
        matches=[row for row in directory if str(row.get('name') or '').strip().casefold()==name.casefold()]
        if business_id:
            if business_id in ids:
                current=next((row for row in directory if row['id']==business_id),None)
                if current and str(current.get('name') or '').strip().casefold()!=name.casefold():
                    raise ValueError(f'Organization ID {business_id!r} already exists as {current.get("name")!r}; refusing to overwrite it.')
                return business_id,False
            init_business(business_id,name);return business_id,True
        if len(matches)==1:return matches[0]['id'],False
        if len(matches)>1:raise ValueError('More than one initialized organization has that name; supply --business-id.')
        derived=_stable_business_id(name)
        if derived in ids:
            current=next((row for row in directory if row['id']==derived),None)
            raise ValueError(f'Derived organization ID {derived!r} already exists as {current.get("name") if current else derived!r}; supply --business-id.')
        init_business(derived,name);return derived,True
    resolved=resolve_business(business_id)
    if resolved.get('status')=='resolved':return resolved['business_id'],False
    return None,False


def setup(workspace=None,profile=None,organization=None,business_id=None,knowledge_enabled=True,write_link=True,run_doctor=True):
    changes=[]
    if _ensure_generated():changes.append({'action':'generated_indexes_refreshed'})
    target=_target_path(workspace);current=workspace_root().resolve();target_profile=_profile_for(target,profile)
    profile_path=target/'.businessos/workspace.json'
    needs_config=(workspace is not None and target!=current) or not profile_path.exists()
    if target==current and profile_path.exists():
        try:needs_config=bool(profile and workspace_profile().get('profile')!=target_profile)
        except Exception:needs_config=bool(profile)
    if needs_config:
        configured=configure(target,target_profile,knowledge_enabled,write_link,False,False)
        changes.append({'action':'workspace_configured','workspace_root':configured['workspace_root'],'profile':configured['profile']})
    if workspace is not None and target!=workspace_root().resolve():
        # Ensure this setup invocation uses the selected target even when --no-link was requested.
        os.environ['BUSINESSOS_WORKSPACE']=str(target)
    bid,created=_resolve_or_initialize(organization,business_id)
    if created:changes.append({'action':'organization_initialized','business_id':bid})
    skill=PRODUCT_ROOT/'skills/viraltrac-aura'
    result={
        'format_version':'1.0','status':'needs_input' if not bid else 'prepared',
        'product_root':str(PRODUCT_ROOT),'workspace_root':str(workspace_root()),
        'business_id':bid,'changes':changes,
        'attachment':{
            'skill_source':str(skill),
            'status':'available' if skill.exists() else 'missing',
            'rule':'The active host owns native Skill/persistent-instruction attachment. AURA setup does not modify unknown host configuration.'
        }
    }
    if not bid:
        resolved=resolve_business(business_id)
        result['missing']=resolved.get('missing') or ['active_business']
        result['reason']=resolved.get('reason') or 'Provide --organization or --business-id.'
        result['available_businesses']=resolved.get('available_businesses',business_directory())
        return result
    if run_doctor:
        readiness=doctor(bid)
        result['readiness']=readiness
        result['status']='ready' if readiness.get('status')=='ready' else 'not_ready'
    return result


def main():
    p=argparse.ArgumentParser(description='Prepare AURA workspace/organization state idempotently, then prove readiness. Host-native Skill attachment remains the host\'s responsibility.')
    p.add_argument('--workspace',help='Optional organization workspace. Omit to reuse the active workspace.')
    p.add_argument('--profile',choices=['simple','power_user','organization'])
    p.add_argument('--organization',help='Organization name. Existing exact-name matches are reused.')
    p.add_argument('--business-id',help='Stable organization ID. Optional when --organization can be safely slugged.')
    p.add_argument('--no-knowledge',action='store_true')
    p.add_argument('--no-link',action='store_true',help='Do not persist the local workspace pointer.')
    p.add_argument('--no-doctor',action='store_true',help='Prepare state without running the readiness proof.')
    p.add_argument('--json',action='store_true')
    a=p.parse_args()
    try:r=setup(a.workspace,a.profile,a.organization,a.business_id,not a.no_knowledge,not a.no_link,not a.no_doctor)
    except (ValueError,FileExistsError,OSError,json.JSONDecodeError) as exc:raise SystemExit(str(exc))
    if a.json:print(json.dumps(r,indent=2,ensure_ascii=False))
    else:
        print(f"AURA setup: {r['status']}")
        print(f"workspace={r['workspace_root']}")
        print(f"organization={r.get('business_id') or '(not selected)'}")
        if r.get('readiness'):
            print(f"readiness={r['readiness']['status']}")
        if r.get('reason'):print(r['reason'])
        print(f"skill_source={r['attachment']['skill_source']}")
    raise SystemExit(0 if r['status'] in {'ready','prepared'} else 2)

if __name__=='__main__':main()
