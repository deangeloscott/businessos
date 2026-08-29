#!/usr/bin/env python3
"""Discover, safely acquire, update, repair, and bind trusted optional local tools.

Pack definitions are product-owned/reviewable. This helper never searches for arbitrary
installers, never uses shell=True, and only mutates system software after --approve.
"""
from _common import *
from jsonschema import Draft202012Validator
import argparse,json,re,shutil,subprocess,sys

PACK_ROOT=ROOT/'core/capability-packs'


def _platform():
    if sys.platform=='darwin':return 'darwin'
    if sys.platform.startswith('win'):return 'windows'
    return 'linux'


def _load(path,default=None):
    if not path.exists():return default
    return json.loads(path.read_text())


def _schema():return _load(ROOT/'core/schemas/runtime/capability-pack.schema.json',{})


def _pack_paths():return sorted(PACK_ROOT.glob('*.json')) if PACK_ROOT.exists() else []


def packs():
    out={};caps={x['id'] for x in _load(ROOT/'core/capabilities/catalog.json',{'capabilities':[]}).get('capabilities',[])}
    validator=Draft202012Validator(_schema())
    for path in _pack_paths():
        data=_load(path,{})
        errors=sorted(validator.iter_errors(data),key=lambda e:list(e.path))
        if errors:raise ValueError(f"{path.relative_to(ROOT)} invalid: "+'; '.join(f'{list(e.path)} {e.message}' for e in errors))
        unknown=sorted({cap for t in data.get('tools',[]) for cap in t.get('capabilities',[]) if cap not in caps})
        if unknown:raise ValueError(f"{path.relative_to(ROOT)} references unknown capabilities: {', '.join(unknown)}")
        if data['id'] in out:raise ValueError(f"duplicate capability pack id: {data['id']}")
        out[data['id']]=data
    return out


def _brew_prefix(formula):
    brew=shutil.which('brew')
    if not brew:return None
    p=subprocess.run([brew,'--prefix',formula],capture_output=True,text=True,timeout=15)
    if p.returncode!=0:return None
    value=p.stdout.strip()
    return value or None


def _candidate_paths(tool):
    vals=[];direct=shutil.which(tool['executable'])
    if direct:vals.append(('path',direct,None))
    suffix=tool.get('brew_path_suffix')
    if suffix:
        for formula in tool.get('brew_formula_candidates',[]) or []:
            prefix=_brew_prefix(formula)
            if not prefix:continue
            candidate=str(Path(prefix)/suffix)
            if Path(candidate).is_file():vals.append(('brew',candidate,formula))
    seen=set();out=[]
    for row in vals:
        if row[1] in seen:continue
        seen.add(row[1]);out.append(row)
    return out


def _version(tool,path):
    args=tool.get('version_args') or []
    if not args:return {'ok':True,'raw':None,'parsed':None}
    try:p=subprocess.run([path,*args],capture_output=True,text=True,timeout=15)
    except Exception as e:return {'ok':False,'raw':str(e),'parsed':None}
    text=(p.stdout or p.stderr or '').strip()
    if p.returncode!=0:return {'ok':False,'raw':text or f'exit {p.returncode}','parsed':None}
    first=(text.splitlines() or [''])[0].strip()
    if tool.get('id')=='yt-dlp':
        m=re.search(r'(\d{4}[.\-]\d{1,2}[.\-]\d{1,2})',first);parsed=m.group(1).replace('-','.') if m else first
    else:
        m=re.search(r'\bversion\s+([0-9]+(?:\.[0-9]+)*)',first,re.I);parsed=m.group(1) if m else first
    return {'ok':True,'raw':first,'parsed':parsed}


def _compatible(tool,version):
    if not version.get('ok'):return False,'health_check_failed'
    parsed=str(version.get('parsed') or '')
    minimum=tool.get('minimum_version')
    if minimum:
        def parts(v):
            try:return tuple(int(x) for x in re.split(r'[.\-]',v)[:3])
            except Exception:return ()
        if parts(parsed) and parts(minimum) and parts(parsed)<parts(minimum):return False,f'below_minimum_{minimum}'
    major=tool.get('minimum_major')
    if major is not None:
        m=re.match(r'(\d+)',parsed)
        if not m:return False,'version_unparsed'
        if int(m.group(1))<int(major):return False,f'below_minimum_major_{major}'
    return True,None


def inspect_pack(pack):
    platform=_platform();rows=[]
    for tool in pack.get('tools',[]):
        if platform not in tool.get('platforms',[]):continue
        candidates=_candidate_paths(tool)
        if not candidates:
            rows.append({'id':tool['id'],'display_name':tool['display_name'],'status':'missing','path':None,'version':None,'capabilities':tool['capabilities'],'limitations':tool.get('limitations',[])})
            continue
        best=None
        for source,path,formula in candidates:
            ver=_version(tool,path);ok,reason=_compatible(tool,ver)
            row={'id':tool['id'],'display_name':tool['display_name'],'status':'healthy' if ok else ('broken' if not ver.get('ok') else 'incompatible'),'reason':reason,'path':path,'source':source,'brew_formula':formula,'version':ver.get('parsed') or ver.get('raw'),'version_raw':ver.get('raw'),'capabilities':tool['capabilities'],'limitations':tool.get('limitations',[])}
            if best is None or row['status']=='healthy':best=row
            if row['status']=='healthy':break
        rows.append(best)
    required_caps=sorted({cap for t in pack.get('tools',[]) if platform in t.get('platforms',[]) for cap in t.get('capabilities',[])})
    healthy_caps={cap for r in rows if r.get('status')=='healthy' for cap in r.get('capabilities',[])}
    return {'pack_id':pack['id'],'display_name':pack['display_name'],'platform':platform,'responsibility_note':pack['responsibility_note'],'capabilities':required_caps,'available_capabilities':sorted(healthy_caps),'ready':set(required_caps).issubset(healthy_caps),'tools':rows}


def _merge_binding_state(environment,pack,status):
    env=environment_overlay_dir(environment,create=True)
    inv_path=env/'tool-inventory.json';bind_path=env/'capability-bindings.json'
    inv=_load(inv_path,{'tools':[]}) or {'tools':[]};bindings=_load(bind_path,{'bindings':[]}) or {'bindings':[]}
    inv.setdefault('tools',[]);bindings.setdefault('bindings',[])
    prefix=f"local-pack:{pack['id']}:"
    healthy={r['id']:r for r in status['tools'] if r.get('status')=='healthy'}
    inv['tools']=[x for x in inv['tools'] if not str(x.get('id','')).startswith(prefix)]
    bindings['bindings']=[x for x in bindings['bindings'] if not str(x.get('connection_ref','')).startswith(prefix)]
    for tool in pack.get('tools',[]):
        row=healthy.get(tool['id'])
        if not row:continue
        tid=prefix+tool['id'];inv['tools'].append({'id':tid,'description':tool['display_name'],'enabled':True,'provider_id':None,'capabilities':tool['capabilities'],'source':'local_capability_pack','path':row['path'],'version':row.get('version'),'pack_id':pack['id']})
        for cap in tool['capabilities']:
            bindings['bindings'].append({'capability':cap,'provider_id':None,'provider_action':row['path'],'connection_ref':tid,'permissions':['local_process'],'limitations':tool.get('limitations',[]),'coverage':'local_machine','reliability':1.0,'freshness':row.get('version'),'enabled':True})
    inv_path.write_text(json.dumps(inv,indent=2)+'\n');bind_path.write_text(json.dumps(bindings,indent=2)+'\n')
    return {'tool_inventory_ref':storage_ref(inv_path),'capability_bindings_ref':storage_ref(bind_path),'bound_tools':sorted(healthy),'bound_capabilities':status['available_capabilities']}


def _installer(pack):
    platform=_platform()
    for row in pack.get('installers',[]):
        if platform in row.get('platforms',[]) and shutil.which(row.get('manager_executable','')):return row
    return None


def _brew_installed(manager,formula):
    p=subprocess.run([manager,'list','--formula',formula],capture_output=True,text=True,timeout=30)
    return p.returncode==0


def _system_action(pack,action,approve,status=None):
    if action not in {'install','upgrade','repair'}:raise ValueError(f'unsupported system action: {action}')
    if not approve:raise ValueError(f'{action} changes system software and requires explicit --approve')
    installer=_installer(pack)
    if not installer:
        raise ValueError(f"No trusted automatic installer configured for {pack['display_name']} on this environment. Use the tool project's/package manager's normal installation path, then run status/bind again.")
    if installer.get('manager')!='brew':raise ValueError(f"Unsupported trusted installer manager: {installer.get('manager')}")
    manager=shutil.which(installer['manager_executable'])
    status=status or inspect_pack(pack)
    unhealthy={r.get('id'):r for r in status.get('tools',[]) if r.get('status')!='healthy'}
    if not unhealthy:
        return {'installer_id':installer['id'],'manager':installer['manager'],'changed':False,'commands':[],'message':'All pack capabilities already meet the configured AURA health/version floor; no system change was needed.'}

    allowed=set((installer.get('install_args') or [])[1:])
    tool_by_id={t.get('id'):t for t in pack.get('tools',[])}
    formulas=[]
    for tid,row in unhealthy.items():
        tool=tool_by_id.get(tid) or {}
        candidate=row.get('brew_formula') if row.get('brew_formula') in allowed else None
        if not candidate:
            candidate=next((f for f in tool.get('brew_formula_candidates',[]) if f in allowed),None)
        if candidate and candidate not in formulas:formulas.append(candidate)
    if not formulas:
        raise ValueError(f"No reviewed formula in the trusted {installer['id']} recipe can repair the unhealthy tools: {', '.join(sorted(unhealthy))}")

    commands=[];outputs=[]
    for formula in formulas:
        installed=_brew_installed(manager,formula)
        if action=='repair':verb='reinstall' if installed else 'install'
        elif action=='upgrade':verb='upgrade' if installed else 'install'
        else:verb='upgrade' if installed else 'install'
        cmd=[manager,verb,formula]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=1800)
        if p.returncode!=0:raise ValueError(f"{action} failed via trusted {installer['manager']} recipe for {formula}: {(p.stderr or p.stdout or '').strip()}")
        commands.append(cmd);outputs.append({'formula':formula,'operation':verb,'stdout':(p.stdout or '').strip()[-3000:]})
    return {'installer_id':installer['id'],'manager':installer['manager'],'changed':True,'commands':commands,'results':outputs}


def recommendation(pack,status):
    unhealthy=[r for r in status['tools'] if r.get('status')!='healthy']
    if status['ready']:
        message=f"{pack['display_name']} is healthy and can be bound to AURA on this machine."
        action='bind'
    elif any(r.get('status') in {'incompatible','broken'} for r in unhealthy):
        message=f"{pack['display_name']} is partially installed but one or more tools are too old or unhealthy for the configured AURA capability floor."
        action='upgrade_or_repair'
    else:
        message=f"{pack['display_name']} can raise AURA's local execution ceiling for: {', '.join(status['capabilities'])}."
        action='offer_install'
    return {'message':message,'next_action':action,'responsibility_note':pack['responsibility_note'],'status_command':f"python3 scripts/manage_local_capabilities.py status --pack {pack['id']}",'bind_command':f"python3 scripts/manage_local_capabilities.py bind --pack {pack['id']}",'install_command':f"python3 scripts/manage_local_capabilities.py install --pack {pack['id']} --approve" if pack.get('installers') else None,'upgrade_command':f"python3 scripts/manage_local_capabilities.py upgrade --pack {pack['id']} --approve" if pack.get('installers') else None,'repair_command':f"python3 scripts/manage_local_capabilities.py repair --pack {pack['id']} --approve" if pack.get('installers') else None}


def main():
    p=argparse.ArgumentParser(description='Manage trusted optional local capability packs. System install/update/repair never occurs without --approve.')
    p.add_argument('action',choices=['status','recommend','bind','install','upgrade','repair'])
    p.add_argument('--pack',help='Pack ID; omit with status/recommend to inspect all packs')
    p.add_argument('--environment',default='local')
    p.add_argument('--approve',action='store_true',help='Explicitly authorize the selected system install/update/repair action')
    a=p.parse_args()
    try:
        allpacks=packs()
        if a.pack and a.pack not in allpacks:raise ValueError(f'Unknown capability pack: {a.pack}')
        selected=[allpacks[a.pack]] if a.pack else list(allpacks.values())
        if a.action in {'bind','install','upgrade','repair'} and len(selected)!=1:raise ValueError(f'{a.action} requires --pack <id>')
        if not environment_exists(a.environment):raise ValueError(f'Unknown environment: {a.environment}')
        out=[]
        for pack in selected:
            before=inspect_pack(pack);row={'status':before}
            if a.action=='recommend':row['recommendation']=recommendation(pack,before)
            elif a.action=='bind':row['binding']=_merge_binding_state(a.environment,pack,before);row['recommendation']=recommendation(pack,before)
            elif a.action in {'install','upgrade','repair'}:
                row['system_action']=_system_action(pack,a.action,a.approve,before)
                after=inspect_pack(pack);row['status']=after;row['binding']=_merge_binding_state(a.environment,pack,after);row['recommendation']=recommendation(pack,after)
            out.append(row)
    except (ValueError,json.JSONDecodeError,subprocess.TimeoutExpired) as e:raise SystemExit(str(e))
    print(json.dumps({'environment':a.environment,'action':a.action,'packs':out,'rule':'Trusted pack definitions only; no arbitrary installer search. System software changes require explicit approval.'},indent=2))

if __name__=='__main__':main()
