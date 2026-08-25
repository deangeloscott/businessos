#!/usr/bin/env python3
from _common import *
import argparse, json, os, shutil, subprocess, sys, hashlib, zipfile, tempfile


def editions():
    p=ROOT/'distribution/editions.json'
    if not p.exists(): return {}
    return {e['id']:e for e in json.loads(p.read_text()).get('editions',[])}


def resolve_modules(requested):
    cat=module_catalog()
    unknown=[m for m in requested if m not in cat]
    if unknown: raise ValueError('Unknown module(s): '+', '.join(unknown))
    resolved=set(requested)|{'core'}
    changed=True
    while changed:
        changed=False
        for mid in list(resolved):
            for dep in cat[mid].get('required_modules',[]):
                if dep not in resolved: resolved.add(dep);changed=True
    return resolved


def dependency_manifest(modules):
    cat=module_catalog(); out=[]
    for mid in sorted(modules):
        m=cat[mid]
        out.append({
            'module':mid,
            'required_modules':m.get('required_modules',[]),
            'optional_installed':[x for x in m.get('optional_modules',[]) if x in modules],
            'optional_not_installed':[x for x in m.get('optional_modules',[]) if x not in modules],
            'standalone':m.get('standalone',False)
        })
    return {'format_version':'1.0','modules':out}


def _copy_clean(dest):
    def ignore(path,names):
        ignored={'__pycache__','.git','.DS_Store','.businessos'} & set(names)
        # Generated indexes are rebuilt for the edition; full-suite tests do not belong in subset distributions.
        rel=Path(path).resolve().relative_to(ROOT.resolve()) if Path(path).resolve()!=ROOT.resolve() else Path('.')
        if rel==Path('.'):
            ignored |= {'generated','dist'} & set(names)
        if rel==Path('instances'):
            ignored |= {n for n in names if n!='_template'}
        if rel==Path('tests'):
            ignored |= set(names)
        return ignored
    shutil.copytree(ROOT,dest,ignore=ignore)
    (dest/'generated').mkdir(exist_ok=True)
    (dest/'tests').mkdir(exist_ok=True)


def _reset_operator_profile(dest):
    # Never distribute a publisher/operator's populated shared identity.
    p=dest/'deployment/operator-profile.json'
    if not p.exists(): return
    d=json.loads(p.read_text())
    for k in list((d.get('identity') or {}).keys()): d['identity'][k]=None
    d['reuse_across_businesses']=[]
    d['notes']=None
    p.write_text(json.dumps(d,indent=2)+'\n')


def _prune_modules(dest,modules):
    sdir=dest/'systems'
    for p in list(sdir.iterdir()):
        if p.is_dir() and p.name not in modules: shutil.rmtree(p)



def _copy_interface_schemas(dest):
    # A standalone module may consume a canonical object owned by an omitted module.
    # Copy only that object's schema as an interface contract; do not install the owner module's SOPs.
    present_titles={}
    for sp in dest.rglob('*.schema.json'):
        try: present_titles[json.loads(sp.read_text()).get('title')]=sp
        except Exception: pass
    source_by_title={}
    for sp in ROOT.rglob('*.schema.json'):
        try: source_by_title[json.loads(sp.read_text()).get('title')]=sp
        except Exception: pass
    needed=set()
    for cp in dest.rglob('CONTEXT.md'):
        if '/contracts/' not in cp.as_posix(): continue
        meta,_=read_frontmatter(cp)
        for sel in meta.get('reads',[]): needed.add(selector_type(sel))
        for typ in meta.get('writes',[]): needed.add(selector_type(typ))
    for typ in sorted(needed):
        if typ in present_titles or typ not in source_by_title: continue
        src=source_by_title[typ]
        parts=src.relative_to(ROOT).parts
        owner=parts[1] if len(parts)>2 and parts[0]=='systems' else 'external'
        out=dest/'core/interfaces'/owner/src.name
        out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,out)

def _prune_capabilities(dest):
    used=set()
    for p in dest.rglob('CONTEXT.md'):
        if '/contracts/' not in p.as_posix(): continue
        meta,_=read_frontmatter(p)
        for c in meta.get('capabilities',{}).get('required',[])+meta.get('capabilities',{}).get('optional',[]):
            if c!='none': used.add(c)
    cp=dest/'core/capabilities/catalog.json'; d=json.loads(cp.read_text())
    d['version']=os_version();d['capabilities']=[x for x in d.get('capabilities',[]) if x.get('id') in used]
    cp.write_text(json.dumps(d,indent=2)+'\n')
    companion=dest/'core/providers/viraltrac/companion-profile.json'
    if companion.exists():
        cd=json.loads(companion.read_text())
        cd['capability_mappings']=[x for x in cd.get('capability_mappings',[]) if x.get('businessos_capability') in used]
        companion.write_text(json.dumps(cd,indent=2)+'\n')

    # Keep provider metadata aligned with the edition's actual capability surface.
    rp=dest/'core/providers/registry.json'
    if rp.exists():
        r=json.loads(rp.read_text()); kept=[]
        for provider in r.get('providers',[]):
            caps=[c for c in provider.get('capabilities',[]) if c in used]
            if caps:
                provider=dict(provider);provider['capabilities']=caps;kept.append(provider)
        r['providers']=kept;rp.write_text(json.dumps(r,indent=2)+'\n')
    pref_paths=[dest/'distribution/provider-defaults.json']
    envroot=dest/'deployment/environments'
    if envroot.exists(): pref_paths += sorted(envroot.glob('*/provider-preferences.json'))
    instroot=dest/'instances'
    if instroot.exists(): pref_paths += sorted(instroot.glob('*/config/provider-preferences.json'))
    for pp in pref_paths:
        if not pp.exists(): continue
        pd=json.loads(pp.read_text());pd['preferences']=[x for x in pd.get('preferences',[]) if x.get('capability') in used]
        pp.write_text(json.dumps(pd,indent=2)+'\n')



def _prune_event_consumer_profile(dest,modules):
    p=dest/'core/monitoring/event-consumer-profile.json'
    if not p.exists(): return
    d=json.loads(p.read_text())
    present_ids=set()
    for cp in dest.rglob('CONTEXT.md'):
        if '/contracts/' not in cp.as_posix(): continue
        try: meta,_=read_frontmatter(cp)
        except Exception: continue
        if meta.get('id'): present_ids.add(meta['id'])
    kept=[]
    for fam in d.get('event_families',[]):
        owner=fam.get('owner_system')
        if owner not in modules: continue
        fam=dict(fam)
        fam['preferred_contracts']=[x for x in fam.get('preferred_contracts',[]) if x in present_ids]
        if fam['preferred_contracts']: kept.append(fam)
    d['event_families']=kept
    p.write_text(json.dumps(d,indent=2)+'\n')

def _prune_provider_recommendations(dest):
    path=dest/'distribution/provider-recommendations.json'
    reg=dest/'core/providers/registry.json'
    if not path.exists() or not reg.exists(): return
    providers={p['id'] for p in json.loads(reg.read_text()).get('providers',[])}
    data=json.loads(path.read_text())
    data['recommendations']=[r for r in data.get('recommendations',[]) if r.get('provider_id') in providers]
    path.write_text(json.dumps(data,indent=2)+'\n')

def _write_instance_template(dest,modules):
    p=dest/'instances/_template/instance.json';d=json.loads(p.read_text())
    d['enabled_systems']=sorted(modules-{'core'});p.write_text(json.dumps(d,indent=2)+'\n')


def _write_navigation(dest,edition_id,display_name,modules):
    cat=module_catalog(); version=os_version(); domains=sorted(modules-{'core'})
    inst={
        'format_version':'1.0','source_version':version,'edition':edition_id,'display_name':display_name,
        'installed_modules':['core']+domains,'standalone_distribution':edition_id!='full','portable_first':True,'default_environment':'local',
        'configurable_workspace_root':True,'human_knowledge_layer':True,'deployment_profiles':'distribution/deployment-profiles.json',
        'brand':'ViralTrac','startup_message':'WELCOME.md','host_capability_discovery':True
    }
    (dest/'INSTALLATION.json').write_text(json.dumps(inst,indent=2)+'\n')
    (dest/'distribution/ACTIVE-DEPENDENCIES.json').write_text(json.dumps(dependency_manifest(modules),indent=2)+'\n')
    names=', '.join(cat[m]['display_name'] for m in domains) if domains else 'Core only'
    readme=f'''# {display_name} v{version}

**A portable, AI-native business operating system that gives AI agents structured processes to research, operate, optimize, and grow a business.**

Installed domain modules: **{names}**. Core is always included.

This distribution is **source-available, not open source**. Internal/commercial business use, customization, and agency/consulting use for clients are permitted under `LICENSE.md`; white-label resale or repackaging it as someone else's standalone BusinessOS product is not.

Business logic remains model/provider/vendor agnostic. The default is still download/unzip-and-use from one local folder. Users may optionally separate organization-owned state into a private workspace, version that workspace with Git, and browse its generated Markdown knowledge layer in Obsidian or another editor. No proprietary BusinessOS server/database/UI, Git provider, second-brain app, ViralTrac account, or cloud runtime is required for local operation.

## Start

**AI/agent:** read root `CONTEXT.md` and `core/policies/agent-execution.md` before the first business write. Contract IDs are not executable paths; durable Business Context must use validated canonical objects.
- Automatic first-run message: `WELCOME.md`
- Human: `START-HERE.md`
- Deployment/storage/versioning/Obsidian: `DEPLOYMENT.md`
- Browse what BusinessOS can do: `PLAYBOOKS.md`
- AI/agent: `CONTEXT.md`
- License: `LICENSE.md`
- Public distribution/security boundary: `PUBLIC-DISTRIBUTION.md`, `SECURITY.md`
- Installed modules/dependencies: `INSTALLATION.json` and `distribution/ACTIVE-DEPENDENCIES.json`
- Tasks: `TASK-NAVIGATOR.md`
- Publisher/origin: `PUBLISHER.json`
- Provider defaults: `distribution/provider-defaults.json`

Optional modules are enrichments, not hidden hard dependencies. When one is absent, use `core/policies/module-independence.md`.

## Deployment profiles
The same edition supports `simple`, `power_user`, and `organization` deployment profiles. Configure an optional external workspace with `python3 scripts/configure_workspace.py <path> --profile power_user|organization`, inspect it with `python3 scripts/workspace_status.py`, and refresh the human knowledge view with `python3 scripts/generate_knowledge_layer.py <business-id>`. See `DEPLOYMENT.md`.

## ViralTrac native companion
When ViralTrac is connected, BusinessOS can dynamically discover its current machine-facing capabilities and use its governed semantic data, measurement, tracking, supported action/receipt surfaces, and event/reactive plane without making ViralTrac a required runtime. The public BusinessOS package contains only integration-facing metadata needed by authorized clients; it does not include ViralTrac's proprietary hosted-application source code or private infrastructure. See `core/policies/viraltrac-native-companion.md`.

## Updates
Update checks use official GitHub Releases, are disabled by default, metadata-only, and never auto-install. For a one-time check: `python scripts/check_for_updates.py --force`.
'''
    (dest/'README.md').write_text(readme)
    start=f'''# Start Here — {display_name}

This copy contains Core plus: **{names}**.

## Human use
You can browse the plain-language capability catalog in `PLAYBOOKS.md`, but you do not need to choose a playbook before asking BusinessOS for help. For storage/versioning/team/Obsidian options, see `DEPLOYMENT.md`; these are optional and use the same BusinessOS contracts.

1. Give the workspace to a compatible LLM/agent harness or operate it directly. On first activation the agent should present `WELCOME.md`.
2. Optional deployment: keep the default product-local workspace, or run `python3 scripts/configure_workspace.py <workspace-path> --profile power_user|organization` to separate organization-owned state. Inspect the active resolution with `python3 scripts/workspace_status.py`.
3. Discover/map the tools already visible in the host using `core/policies/host-capability-discovery.md` and `scripts/bootstrap_environment.py`.
4. Create a brand/business with `python scripts/init_business.py <business-id> --name "Business Name"`.
5. `core.context.bootstrap-business` is a contract ID, not a command/path. Resolve it with `python scripts/resolve_contract.py core.context.bootstrap-business`, read its `CONTEXT.md`, and perform it through the active agent. Persist explicit user-supplied setup facts first with `scripts/bootstrap_explicit_context.py`; repeat `--source-file` for multiple original supplied sources instead of manually merging them. A grounded `brand` object and `--preference-profile-file` inputs can be included so organization Brand and reusable preferences exist before residual work. If the original request contains work beyond setup, pass the remaining natural-language outcome with `--residual-request`, or use `--initialization-only` only for true setup-only requests. Explicit reusable promises/claims or claim constraints should use the helper's `approved_claims` / `claim_constraints` support so they become grounded `BusinessClaim` objects. Optional discovery fills only evidence-supported gaps.
6. Canonical Business Context is schema-valid JSON under logical `instances/<business-id>/`; free-form Markdown does not satisfy canonical object writes. Unknowns remain unknown, and plausible prices/margins/KPIs/geography/audiences/offers/performance/targets must never be fabricated. Agent-created Brand/Audience/Offer strategy remains derived/candidate rather than being relabeled `explicit_user`; explicit organization Brand instructions are grounded only through the supported deterministic bootstrap. Customer-facing Content/Marketing Assets must follow `core/policies/context-provenance-and-claims.md`; an unpublished outward draft remains customer-facing, must use the appropriate customer-facing production root, and referenced production Runs must record required-subcontract/QA completion before being reported complete.
7. Ask the desired business task in plain language. `scripts/route_task.py` routes only to installed modules. If setup is a prerequisite and the original request contains a broader goal/next-work question, preserve that residual intent through the bootstrap/routing handoff and continue it automatically rather than asking the user to pick a module.
8. Composite jobs expand through `scripts/process_plan.py`; each executable job gets minimal context through `scripts/context_plan.py`.
9. Before each atomic job, run `scripts/preflight_capabilities.py` (default `local` environment) so missing tools/provider decisions/manual fallbacks are known before execution.
10. Preserve durable state under logical `instances/<business-id>/` and resumable working state under logical `runtime/runs/<business-id>/<run-id>/`; do not blindly restart or delete prior state without explicit authorization. If the human knowledge layer is enabled, refresh it with `python3 scripts/generate_knowledge_layer.py <business-id>`; generated Markdown is not a second source of truth.
11. Connect real tools through provider-neutral capabilities under `deployment/`. Existing tools are used first; scoped provider preferences may propose a compatible provider when a capability is missing. New signup/connection still requires authorization.
12. If ViralTrac is already connected, discover its current machine-facing capabilities instead of assuming them. Follow `core/policies/viraltrac-native-companion.md`; when the host can retrieve a non-secret capability/descriptor response, synchronize it with `python scripts/sync_viraltrac_capabilities.py local --manifest <file>`. For continuous/reactive use, run `core.monitoring.configure-reactive-monitoring`; live ViralTrac event/reactive activation requires current runtime-mode evidence plus a real host delivery path and may be persisted with `scripts/activate_viraltrac_event_plane.py`.
13. Configure business-specific provider preferences in logical `instances/<business-id>/config/provider-preferences.json` when the organization has preferred or prohibited software.
14. This copy is source-available under `LICENSE.md`. Do not remove publisher provenance or redistribute/white-label the BusinessOS outside the license. `SECURITY.md` describes the boundary between this public workspace and proprietary ViralTrac software.
15. Update checks are disabled by default. Use `python scripts/check_for_updates.py --force` for a one-time official GitHub release check, or opt in with `python scripts/set_update_policy.py --enable`. Checks are metadata-only and never auto-install.

## ViralTrac recommendation
ViralTrac is the recommended first-party companion for this distribution. Existing compatible tools may continue executing work, while ViralTrac may still be recommended when relevant. Never switch/connect without authorization, and respect an explicit refusal. When connected, use ViralTrac's discovered governed business-data, measurement, tracking, and supported action surfaces where they are the best available authority; do not hardcode or assume unavailable capabilities.

## AI/agent use
Before the first business write, read root `CONTEXT.md`, `INSTALLATION.json`, and `core/policies/agent-execution.md`. Contract IDs are not executable paths. Never assume an omitted module ran.

## Validate active business state
Run `python scripts/validate_business.py <business-id>`; after bootstrap use `--require-context`.

## Validate a clean release/package
`python tests/run_distribution.py` is only for a clean distributable copy with no business instances.
'''
    (dest/'START-HERE.md').write_text(start)
    # Generate an edition-aware first-run message from the actual installed module set.
    subprocess.run([sys.executable,str(dest/'scripts/generate_welcome.py')],cwd=dest,check=True)
    lines=['# Task Navigator','',f'Installed edition: **{display_name}**.','']
    for mid in domains:
        mp=dest/'systems'/mid/'process-map.json'
        lines += [f"## {cat[mid]['display_name']}",'',cat[mid]['description'],'','| Activity | Result | Entry contract |','|---|---|---|']
        if mp.exists():
            d=json.loads(mp.read_text())
            for a in d.get('activities',[]):
                lines.append(f"| `{a['id']}` | {a.get('result','')} | `{a['entry_contract']}` |")
        lines.append('')
    lines += ['## Core','','Core supplies shared business context, evidence/provenance, Opportunities, Actions, verification, measurement, Learning, workspace/knowledge governance, capability abstraction, and module-independence rules.','']
    cp=dest/'core/process-map.json'
    if cp.exists():
        lines += ['| Activity | Result | Entry contract |','|---|---|---|']
        d=json.loads(cp.read_text())
        for a in d.get('activities',[]): lines.append(f"| `{a['id']}` | {a.get('result','')} | `{a['entry_contract']}` |")
        lines.append('')
    (dest/'TASK-NAVIGATOR.md').write_text('\n'.join(lines))


def _write_distribution_test(dest):
    (dest/'tests/run_distribution.py').write_text('''#!/usr/bin/env python3\nfrom pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1]\nsys.path.insert(0,str(ROOT/"scripts"))\nfrom validate_distribution import validate_distribution\nvalidate_distribution()\n''')


def _run(dest,rel):
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    subprocess.run([sys.executable,str(dest/rel)],cwd=dest,env=env,check=True)


def build_distribution(edition_id=None,requested_modules=None,output_dir=None,keep_folder=True):
    eds=editions();cat=module_catalog()
    if edition_id:
        if edition_id not in eds: raise ValueError(f'Unknown edition {edition_id}')
        ed=eds[edition_id];requested=ed['modules'];display=ed['display_name'];eid=edition_id
    else:
        requested=requested_modules or []
        if not requested: raise ValueError('Choose --edition or --modules')
        eid='custom-'+'-'.join(sorted(requested));display="ViralTrac's Custom BusinessOS"
    modules=resolve_modules(requested)
    available={'core'} | {p.name for p in (ROOT/'systems').iterdir() if p.is_dir()}
    missing=modules-available
    if missing: raise ValueError('Source workspace does not contain required module(s): '+', '.join(sorted(missing)))
    outbase=Path(output_dir) if output_dir else ROOT.parent/'distributions'
    outbase.mkdir(parents=True,exist_ok=True)
    pkgname=f"{slug(display)}-v{os_version()}"
    dest=outbase/pkgname
    if dest.exists(): shutil.rmtree(dest)
    _copy_clean(dest);_reset_operator_profile(dest);_prune_modules(dest,modules);_copy_interface_schemas(dest);_write_navigation(dest,eid,display,modules);_write_instance_template(dest,modules);_prune_event_consumer_profile(dest,modules);_prune_capabilities(dest);_prune_provider_recommendations(dest);_write_distribution_test(dest)
    # Update visible version labels and regenerate all indexes from the actual subset.
    (dest/'VERSION').write_text(os_version()+'\n')
    _run(dest,'scripts/generate_registry.py');_run(dest,'scripts/validate_workspace.py');_run(dest,'tests/run_distribution.py')
    # Regenerate once after smoke-test cleanup so manifests match the final package.
    _run(dest,'scripts/generate_registry.py');_run(dest,'scripts/validate_workspace.py')
    zpath=outbase/(pkgname+'.zip')
    if zpath.exists(): zpath.unlink()
    shutil.make_archive(str(zpath.with_suffix('')),'zip',outbase,pkgname)
    with zipfile.ZipFile(zpath) as zf:
        bad=zf.testzip()
        if bad: raise RuntimeError(f'ZIP integrity failed at {bad}')
    digest=hashlib.sha256(zpath.read_bytes()).hexdigest();sha=zpath.with_suffix('.zip.sha256');sha.write_text(f'{digest}  {zpath.name}\n')
    if not keep_folder: shutil.rmtree(dest)
    return {'edition':eid,'display_name':display,'modules':sorted(modules),'folder':str(dest),'zip':str(zpath),'sha256_file':str(sha),'sha256':digest}


def main():
    ap=argparse.ArgumentParser(description='Build dependency-aware Business OS distributions.')
    ap.add_argument('--edition');ap.add_argument('--modules',nargs='+');ap.add_argument('--output-dir');ap.add_argument('--list',action='store_true');ap.add_argument('--no-folder',action='store_true')
    a=ap.parse_args()
    if a.list:
        for e in editions().values(): print(f"{e['id']}: {e['display_name']} — {e['description']}")
        return
    try:r=build_distribution(a.edition,a.modules,a.output_dir,not a.no_folder)
    except (ValueError,RuntimeError) as e: raise SystemExit(str(e))
    print(json.dumps(r,indent=2))

if __name__=='__main__': main()
