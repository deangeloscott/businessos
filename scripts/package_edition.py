#!/usr/bin/env python3
from _common import *
import argparse,json,os,shutil,subprocess,sys,hashlib,zipfile


def editions():
    p=ROOT/'distribution/editions.json'
    if not p.exists():return {}
    return {e['id']:e for e in json.loads(p.read_text()).get('editions',[])}
def resolve_modules(requested):
    cat=module_catalog();unknown=[m for m in requested if m not in cat]
    if unknown:raise ValueError('Unknown module(s): '+', '.join(unknown))
    resolved=set(requested)|{'core'};changed=True
    while changed:
        changed=False
        for mid in list(resolved):
            for dep in cat[mid].get('required_modules',[]):
                if dep not in resolved:resolved.add(dep);changed=True
    return resolved
def dependency_manifest(modules):
    cat=module_catalog();out=[]
    for mid in sorted(modules):
        m=cat[mid];out.append({'module':mid,'required_modules':m.get('required_modules',[]),'optional_installed':[x for x in m.get('optional_modules',[]) if x in modules],'optional_not_installed':[x for x in m.get('optional_modules',[]) if x not in modules],'standalone':m.get('standalone',False)})
    return {'format_version':'1.0','modules':out}
def _copy_clean(dest):
    def ignore(path,names):
        ignored={'__pycache__','.git','.DS_Store','.businessos'}&set(names);rel=Path(path).resolve().relative_to(ROOT.resolve()) if Path(path).resolve()!=ROOT.resolve() else Path('.')
        if rel==Path('.'):ignored|={'generated','dist','.businessos','runtime','knowledge','attachments','qualification'}&set(names)
        if rel==Path('instances'):ignored|={n for n in names if n!='_template'}
        if rel==Path('tests'):ignored|=set(names)
        return ignored
    shutil.copytree(ROOT,dest,ignore=ignore)
    if (dest/'qualification').exists():raise RuntimeError('Packaged distribution contains maintainer-only qualification infrastructure')
    (dest/'generated').mkdir(exist_ok=True);(dest/'tests').mkdir(exist_ok=True)
def _prune_modules(dest,modules):
    sdir=dest/'systems'
    for p in list(sdir.iterdir()):
        if p.is_dir() and p.name not in modules:shutil.rmtree(p)
def _copy_interface_schemas(dest):
    present_titles={}
    for sp in dest.rglob('*.schema.json'):
        try:present_titles[json.loads(sp.read_text()).get('title')]=sp
        except Exception:pass
    source_by_title={}
    for sp in ROOT.rglob('*.schema.json'):
        try:source_by_title[json.loads(sp.read_text()).get('title')]=sp
        except Exception:pass
    needed=set()
    for cp in dest.rglob('CONTEXT.md'):
        if '/contracts/' not in cp.as_posix():continue
        meta,_=read_frontmatter(cp)
        for sel in meta.get('reads',[]):needed.add(selector_type(sel))
        for typ in meta.get('writes',[]):needed.add(selector_type(typ))
    for typ in sorted(needed):
        if typ in present_titles or typ not in source_by_title:continue
        src=source_by_title[typ];parts=src.relative_to(ROOT).parts;owner=parts[1] if len(parts)>2 and parts[0]=='systems' else 'external';out=dest/'core/interfaces'/owner/src.name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,out)
def _prune_capabilities(dest):
    """Keep only provider-neutral capability vocabulary used by the packaged SOPs."""
    used=set()
    for p in dest.rglob('CONTEXT.md'):
        if '/contracts/' not in p.as_posix():continue
        meta,_=read_frontmatter(p)
        for c in meta.get('capabilities',{}).get('required',[])+meta.get('capabilities',{}).get('optional',[]):
            if c!='none':used.add(c)
    cp=dest/'core/capabilities/catalog.json';d=json.loads(cp.read_text());d['capabilities']=[x for x in d.get('capabilities',[]) if x.get('id') in used];cp.write_text(json.dumps(d,indent=2)+'\n')
def _write_instance_template(dest,modules):
    p=dest/'instances/_template/instance.json';d=json.loads(p.read_text());d['enabled_systems']=sorted(modules-{'core'});p.write_text(json.dumps(d,indent=2)+'\n')
def _write_navigation(dest,edition_id,display_name,modules):
    cat=module_catalog();version=os_version();domains=sorted(modules-{'core'});expansion='Agentic Understanding and Reinforcement Architecture';names=', '.join(cat[m]['display_name'] for m in domains) if domains else 'Core only'
    inst={'format_version':'1.0','source_version':version,'maturity':'alpha','edition':edition_id,'display_name':display_name,'public_name':display_name,'name_expansion':expansion,'descriptor':'AI-native BusinessOS','installed_modules':['core']+domains,'standalone_distribution':edition_id!='full','portable_first':True,'default_environment':'local','configurable_workspace_root':True,'human_knowledge_layer':True,'deployment_profiles':'distribution/deployment-profiles.json','brand':'ViralTrac','startup_message':'BEGINNERS-GUIDE.md'}
    (dest/'INSTALLATION.json').write_text(json.dumps(inst,indent=2)+'\n');(dest/'distribution/ACTIVE-DEPENDENCIES.json').write_text(json.dumps(dependency_manifest(modules),indent=2)+'\n')
    readme=f'''# {display_name}\n\n**Alpha · v{version}**  \n**AURA = {expansion}.**\n\n{display_name} gives AI organization-owned memory, reusable operating knowledge, and lightweight continuity so useful work can build on what the organization already knows.\n\n> Alpha means the architecture is usable and integrity-tested while real-work quality, playbooks, retrieval, Learning, and usability are still being improved before 1.0.\n\nInstalled domain modules: **{names}**. Core is always included.\n\n## Start in three steps\n\n1. Download and unzip this AURA edition.\n2. Give an AI tool access to the folder.\n3. Tell it about the business and what you want.\n\nYou do not need to choose a playbook, contract, schema, provider, or operating mode first. See `BEGINNERS-GUIDE.md` for the main human guide and `PLAYBOOKS.md` for installed capabilities.\n\nAURA is local-first, organization-owned, and model/provider/harness neutral. The active harness owns tools, models, credentials, orchestration, scheduling, and other execution mechanics; AURA owns durable organizational memory, reusable operating knowledge, and the integrity of what it persists.\n\n- `BEGINNERS-GUIDE.md` — main human guide, including first use, memory, upgrades, optional tools, and troubleshooting\n- `PLAYBOOKS.md` — plain-language capabilities\n- `OPERATOR-GUIDE.md` — practical commands and advanced use\n- `DEPLOYMENT.md` — storage, deployment, multi-device, and team details\n- `CONTEXT.md` — AI/agent operating context\n- `LICENSE.md` — source-available license\n\nThis distribution is **source-available, not open source**. See `LICENSE.md`.\n''';(dest/'README.md').write_text(readme)
    lines=['# Task Navigator','',f'Installed edition: **{display_name}**.','']
    for mid in domains:
        mp=dest/'systems'/mid/'process-map.json';lines += [f"## {cat[mid]['display_name']}",'',cat[mid]['description'],'','| Activity | Result | Entry contract |','|---|---|---|']
        if mp.exists():
            d=json.loads(mp.read_text())
            for a in d.get('activities',[]):lines.append(f"| `{a['id']}` | {a.get('result','')} | `{a['entry_contract']}` |")
        lines.append('')
    lines += ['## Core','','Core supplies organization-owned context, evidence/provenance, decisions, optional continuity objects, measurement, Learning, reusable SOP knowledge, workspace integrity, and provider-neutral capability vocabulary.','']
    cp=dest/'core/process-map.json'
    if cp.exists():
        lines += ['| Activity | Result | Entry contract |','|---|---|---|'];d=json.loads(cp.read_text())
        for a in d.get('activities',[]):lines.append(f"| `{a['id']}` | {a.get('result','')} | `{a['entry_contract']}` |")
        lines.append('')
    (dest/'TASK-NAVIGATOR.md').write_text('\n'.join(lines))
def _write_distribution_test(dest):
    (dest/'tests/run_distribution.py').write_text('#!/usr/bin/env python3\nfrom pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1]\nsys.path.insert(0,str(ROOT/"scripts"))\nfrom validate_distribution import validate_distribution\nvalidate_distribution()\n')
def _run(dest,rel):
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';subprocess.run([sys.executable,str(dest/rel)],cwd=dest,env=env,check=True)
def build_distribution(edition_id=None,requested_modules=None,output_dir=None,keep_folder=True):
    eds=editions()
    if edition_id:
        if edition_id not in eds:raise ValueError(f'Unknown edition {edition_id}')
        ed=eds[edition_id];requested=ed['modules'];display=ed['display_name'];eid=edition_id
    else:
        requested=requested_modules or []
        if not requested:raise ValueError('Choose --edition or --modules')
        eid='custom-'+'-'.join(sorted(requested));display='ViralTrac AURA — Custom'
    modules=resolve_modules(requested);available={'core'}|{p.name for p in (ROOT/'systems').iterdir() if p.is_dir()};missing=modules-available
    if missing:raise ValueError('Source workspace does not contain required module(s): '+', '.join(sorted(missing)))
    outbase=Path(output_dir) if output_dir else ROOT.parent/'distributions';outbase.mkdir(parents=True,exist_ok=True);pkgname=f"{slug(display)}-v{os_version()}";dest=outbase/pkgname
    if dest.exists():shutil.rmtree(dest)
    _copy_clean(dest);_prune_modules(dest,modules);_copy_interface_schemas(dest);_write_navigation(dest,eid,display,modules);_write_instance_template(dest,modules);_prune_capabilities(dest);_write_distribution_test(dest)
    (dest/'VERSION').write_text(os_version()+'\n');_run(dest,'scripts/generate_registry.py');_run(dest,'scripts/validate_workspace.py');_run(dest,'tests/run_distribution.py');_run(dest,'scripts/generate_registry.py');_run(dest,'scripts/validate_workspace.py')
    zpath=outbase/(pkgname+'.zip')
    if zpath.exists():zpath.unlink()
    shutil.make_archive(str(zpath.with_suffix('')),'zip',outbase,pkgname)
    with zipfile.ZipFile(zpath) as zf:
        bad=zf.testzip()
        if bad:raise RuntimeError(f'ZIP integrity failed at {bad}')
    digest=hashlib.sha256(zpath.read_bytes()).hexdigest();sha=zpath.with_suffix('.zip.sha256');sha.write_text(f'{digest}  {zpath.name}\n')
    if not keep_folder:shutil.rmtree(dest)
    return {'edition':eid,'display_name':display,'modules':sorted(modules),'folder':str(dest),'zip':str(zpath),'sha256_file':str(sha),'sha256':digest}
def main():
    ap=argparse.ArgumentParser(description='Build dependency-aware ViralTrac AURA distributions.');ap.add_argument('--edition');ap.add_argument('--modules',nargs='+');ap.add_argument('--output-dir');ap.add_argument('--list',action='store_true');ap.add_argument('--no-folder',action='store_true');a=ap.parse_args()
    if a.list:
        for e in editions().values():print(f"{e['id']}: {e['display_name']} — {e['description']}")
        return
    try:r=build_distribution(a.edition,a.modules,a.output_dir,not a.no_folder)
    except (ValueError,RuntimeError) as e:raise SystemExit(str(e))
    print(json.dumps(r,indent=2))
if __name__=='__main__':main()
