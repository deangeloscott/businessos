"""AURA tasks on the computer's own scheduler: Task Scheduler on Windows, launchd on macOS, cron on Linux.

For AI apps without a scheduler AURA can reach, a task is an entry in the operating system's scheduler that runs one
request through that app, in the business's workspace, with the permission chosen when it was set up. The operating
system decides when it runs; AURA keeps the request (name, instructions, app, model) and the last few results on this
computer, and can list, pause, resume, change and remove each task with the system's own commands. Everything AURA
adds is named for AURA: the "AURA" folder in Task Scheduler, com.viraltrac.aura.task.* launch agents, and cron lines
marked "aura-task". Tasks run while the computer is on and keep running if the AURA folder is deleted, until removed.

  workspace_os_schedules.py create --business-id <id> --app claude --name "Weekly check" --when "weekly mon 09:00"
                                    --prompt-file <file> [--model <id>] [--effort <level>] [--permission <mode>]
  workspace_os_schedules.py list | pause <id> | resume <id> | remove <id> | edit <id> [--when ...] [--prompt-file ...]
  workspace_os_schedules.py run <id>        (what the scheduler calls)
  workspace_os_schedules.py remove-all      (before deleting AURA: removes every AURA task from this computer's scheduler)

When: "hourly", "daily HH:MM", "weekly mon HH:MM" (mon..sun) or "monthly D HH:MM" (D 1-28), local time.
"""
import argparse,json,os,plistlib,re,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _common import PRODUCT_ROOT,new_id,workspace_root
from workspace_startup import state_dir

APPS = ('claude','codex','omp','pi')  # apps whose own scheduler AURA cannot reach from their command line
# Each app's own name for running without asking; Pi has no permission modes.
FULL = {'claude':'bypassPermissions','codex':'full','omp':'yolo','pi':'native'}
DAYS = ('mon','tue','wed','thu','fri','sat','sun')
FLAGS = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {}


def store():return state_dir()/'os-tasks'
def definition_path(ident):
    if not re.fullmatch(r'[A-Za-z0-9_-]{6,40}',str(ident)):raise ValueError('Choose an AURA task on this computer.')
    return store()/f'{ident}.json'
def load(ident):
    try:return json.loads(definition_path(ident).read_text(encoding='utf-8'))
    except FileNotFoundError:raise ValueError('This task is no longer on this computer. Refresh the task list.') from None
def save(task):
    path=definition_path(task['id']);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(task,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path)
def definitions():
    rows=[]
    for path in sorted(store().glob('*.json')) if store().is_dir() else []:
        if path.name.endswith('.runs.json'):continue
        try:rows.append(json.loads(path.read_text(encoding='utf-8')))
        except (OSError,ValueError):continue
    return rows


def parse_when(text):
    """The small timing format this helper accepts; the AI that set the task up turns the person's words into it."""
    words=str(text or '').strip().lower().split()
    clock=lambda v:re.fullmatch(r'([01]?\d|2[0-3]):([0-5]\d)',v or '')
    if words==['hourly']:return {'every':'hourly'}
    if len(words)==2 and words[0]=='daily' and clock(words[1]):return {'every':'daily','time':words[1].zfill(5)}
    if len(words)==3 and words[0]=='weekly' and words[1][:3] in DAYS and clock(words[2]):return {'every':'weekly','day':words[1][:3],'time':words[2].zfill(5)}
    if len(words)==3 and words[0]=='monthly' and words[1].isdigit() and 1<=int(words[1])<=28 and clock(words[2]):return {'every':'monthly','day':int(words[1]),'time':words[2].zfill(5)}
    raise ValueError('Use "hourly", "daily 09:00", "weekly mon 09:00" or "monthly 15 09:00" (local time).')
def when_text(when):
    """The same timing in the format parse_when reads, for editing."""
    return ' '.join(str(v) for v in (when['every'],when.get('day'),when.get('time')) if v is not None)
def rrule(when):
    """The timing as a calendar rule, the form AURA's task list already reads for grouping and next-run display."""
    if when['every']=='hourly':return 'FREQ=HOURLY'
    hour,minute=(int(v) for v in when['time'].split(':'));base=f'FREQ={when["every"].upper()};BYHOUR={hour};BYMINUTE={minute}'
    if when['every']=='weekly':base+=';BYDAY='+when['day'][:2].upper()
    if when['every']=='monthly':base+=f';BYMONTHDAY={when["day"]}'
    return base
def describe_when(when):
    if when['every']=='hourly':return 'Every hour'
    at=when['time']
    if when['every']=='daily':return f'Every day at {at}'
    if when['every']=='weekly':return f"Every {['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][DAYS.index(when['day'])]} at {at}"
    return f"Monthly on day {when['day']} at {at}"


def _runner(ident):
    python=Path(sys.executable)
    quiet=python.with_name('pythonw.exe')  # no console window flashing up on Windows
    # The scheduler starts without AURA's environment, so a separate settings folder (as previews use) is passed along.
    return [str(quiet if os.name=='nt' and quiet.is_file() else python),str(PRODUCT_ROOT/'scripts/workspace_os_schedules.py'),'run',ident,
            *(['--state',os.environ['AURA_STATE_DIR']] if os.environ.get('AURA_STATE_DIR') else [])]
def _call(argv,data=None):
    done=subprocess.run(argv,input=data,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60,**FLAGS)
    if done.returncode:raise ValueError((done.stderr or done.stdout).strip()[-400:] or 'The computer\'s scheduler did not accept this change.')
    return done.stdout


# Windows: the AURA folder in Task Scheduler.
def _win_create(task):
    """schtasks sets the timing (it covers hourly to monthly); PowerShell sets the action, which has no 261-character
    limit on the command the way schtasks /TR does."""
    when=task['when'];name='\\AURA\\'+task['id']
    argv=['schtasks','/Create','/F','/TN',name,'/TR','cmd.exe']
    every=when['every']
    if every=='hourly':argv+=['/SC','HOURLY']
    else:argv+=['/SC',every.upper(),*(['/D',str(when['day']).upper()] if every!='daily' else []),'/ST',when['time']]
    _call(argv)
    program,*rest=_runner(task['id']);quote=lambda v:"'"+str(v).replace("'","''")+"'"
    arguments=' '.join(f'"{a}"' for a in rest)
    _call(['powershell','-NoProfile','-NonInteractive','-Command',
           f"$a=New-ScheduledTaskAction -Execute {quote(program)} -Argument {quote(arguments)} -WorkingDirectory {quote(task['workspace'])}; "
           "Set-ScheduledTask -TaskPath '\\AURA\\' -TaskName "+quote(task['id'])+" -Action $a | Out-Null"])
    if task.get('paused'):_call(['schtasks','/Change','/TN',name,'/DISABLE'])


_STATUS={'at':0,'rows':None}
def _win_status():
    if time.time()-_STATUS['at']<15:return _STATUS['rows']  # the list refreshes often; asking Windows each time starts PowerShell
    _STATUS.update(at=time.time(),rows=_win_status_now());return _STATUS['rows']
def _win_status_now():
    script=("Get-ScheduledTask -TaskPath '\\AURA\\' -ErrorAction SilentlyContinue | ForEach-Object { $i=$_|Get-ScheduledTaskInfo; "
            "[pscustomobject]@{id=$_.TaskName;state=[string]$_.State;next=if($i.NextRunTime){$i.NextRunTime.ToString('s')}else{''}} } | ConvertTo-Json -Compress")
    try:out=_call(['powershell','-NoProfile','-NonInteractive','-Command',script]).strip()
    except (ValueError,OSError,subprocess.SubprocessError):return None
    rows=json.loads(out) if out else []
    return {r['id']:r for r in ([rows] if isinstance(rows,dict) else rows)}


# macOS: one launch agent per task.
def _mac_label(ident):return f'com.viraltrac.aura.task.{ident}'
def _mac_plist(ident):return Path.home()/'Library/LaunchAgents'/f'{_mac_label(ident)}.plist'
def _mac_create(task):
    when=task['when'];plist={'Label':_mac_label(task['id']),'ProgramArguments':_runner(task['id']),'WorkingDirectory':task['workspace']}
    if when['every']=='hourly':plist['StartInterval']=3600
    else:
        hour,minute=(int(v) for v in when['time'].split(':'));slot={'Hour':hour,'Minute':minute}
        if when['every']=='weekly':slot['Weekday']=(DAYS.index(when['day'])+1)%7
        if when['every']=='monthly':slot['Day']=when['day']
        plist['StartCalendarInterval']=slot
    path=_mac_plist(task['id']);path.parent.mkdir(parents=True,exist_ok=True)
    _mac_unload(task['id']);path.write_bytes(plistlib.dumps(plist))
    if not task.get('paused'):_call(['launchctl','bootstrap',f'gui/{os.getuid()}',str(path)])
def _mac_unload(ident):
    try:subprocess.run(['launchctl','bootout',f'gui/{os.getuid()}/{_mac_label(ident)}'],capture_output=True,timeout=30)
    except (OSError,subprocess.SubprocessError):pass


# Linux: lines in the person's own crontab, marked for AURA.
def _cron_lines():
    done=subprocess.run(['crontab','-l'],capture_output=True,text=True,timeout=30)
    return done.stdout.splitlines() if done.returncode==0 else []
def _cron_write(lines):_call(['crontab','-'],'\n'.join(lines)+'\n')
def _cron_create(task):
    when=task['when'];mark=f"# aura-task:{task['id']}"
    hour,minute=(when.get('time') or '0:0').split(':')
    every=when['every']
    if every=='hourly':spec='0 * * * *'
    elif every=='daily':spec=f'{int(minute)} {int(hour)} * * *'
    elif every=='weekly':spec=f'{int(minute)} {int(hour)} * * {(DAYS.index(when["day"])+1)%7}'
    else:spec=f'{int(minute)} {int(hour)} {when["day"]} * *'
    command=' '.join("'"+a.replace("'","'\\''")+"'" for a in _runner(task['id']))
    line=('#AURA-PAUSED ' if task.get('paused') else '')+f"{spec} cd '{task['workspace']}' && {command} {mark}"
    _cron_write([l for l in _cron_lines() if not l.endswith(mark)]+[line])


def _place(task):
    if os.name=='nt':_win_create(task)
    elif sys.platform=='darwin':_mac_create(task)
    else:_cron_create(task)


def create(bid,app,name,when,prompt,model='',effort='',permission='',workspace=None):
    """Add a task to the computer's scheduler. Permission is chosen once here, so unattended runs don't stop to ask."""
    import workspace_permissions
    if app not in APPS:raise ValueError('This app keeps its own scheduler; set the task up there.')
    name=str(name or '').strip()[:120];prompt=str(prompt or '').strip()
    if not name or not prompt or len(prompt)>20000:raise ValueError('Give the task a name and instructions of up to 20,000 characters.')
    permission=FULL[app] if permission in {'','full'} else permission  # runs on its own, so by default it doesn't stop to ask
    if app!='pi':workspace_permissions.validate(app,permission)
    root=Path(workspace or workspace_root()).resolve()
    if not (root/'instances'/bid).is_dir():raise ValueError('Choose a business in this workspace.')
    task={'id':new_id(9).replace('-','x'),'business_id':bid,'app':app,'name':name,'prompt':prompt,'when':parse_when(when),'model':model,'effort':effort,
          'permission':permission,'workspace':str(root),'created':time.time(),'paused':False}
    save(task)
    try:_place(task)
    except Exception:definition_path(task['id']).unlink(missing_ok=True);raise
    return task


def change(ident,action,values=None):
    task=load(ident)
    if action in {'pause','resume'}:task['paused']=action=='pause'
    elif action=='edit':
        values=dict(values or {})
        if 'when' in values:task['when']=parse_when(values['when'])
        for key in ('name','prompt','model','effort'):
            if key in values and str(values[key]).strip():task[key]=str(values[key]).strip()
    elif action=='remove':
        _STATUS['at']=0
        if os.name=='nt':
            try:_call(['schtasks','/Delete','/F','/TN',f'\\AURA\\{ident}'])
            except ValueError:pass  # already gone from Task Scheduler
        elif sys.platform=='darwin':_mac_unload(ident);_mac_plist(ident).unlink(missing_ok=True)
        else:_cron_write([l for l in _cron_lines() if not l.endswith(f'# aura-task:{ident}')])
        definition_path(ident).unlink(missing_ok=True);definition_path(ident).with_suffix('.runs.json').unlink(missing_ok=True)
        return {**task,'status':'removed'}
    else:raise ValueError('Choose pause, resume, edit or remove.')
    save(task);_STATUS['at']=0
    if os.name=='nt' and action in {'pause','resume'}:_call(['schtasks','/Change','/TN',f'\\AURA\\{ident}','/DISABLE' if task['paused'] else '/ENABLE'])
    else:_place(task)
    return task


def runs(ident):
    try:return json.loads(definition_path(ident).with_suffix('.runs.json').read_text(encoding='utf-8'))
    except (OSError,ValueError):return []


def listed():
    """Each AURA task with what the scheduler reports (Windows) or knows (macOS, Linux)."""
    status=_win_status() if os.name=='nt' else None
    rows=[]
    for task in definitions():
        seen=(status or {}).get(task['id']);last=(runs(task['id']) or [{}])[-1]
        gone=status is not None and not seen
        rows.append({**task,'schedule':describe_when(task['when']),'status':'missing' if gone else 'paused' if task.get('paused') or (seen or {}).get('state')=='Disabled' else 'active',
                     'next_run':(seen or {}).get('next',''),'last_run':last.get('at',''),'last_status':last.get('status',''),'last_error':last.get('error','')})
    return rows


def run(ident):
    """What the scheduler calls: one request through the task's app, in its workspace, with its chosen permission."""
    import workspace_agents,workspace_codex
    from workspace_execution import Execution
    from workspace_connections import Connections
    task=load(ident);started=time.strftime('%Y-%m-%dT%H:%M:%S');record={'at':started,'status':'error'}
    try:
        if task.get('paused'):record.update(status='skipped',error='Paused');return
        import workspace_ui
        choice=next((a for a in workspace_ui.installed_agents() if a['id']==task['app'] and a.get('argv')),None)
        if not choice:raise ValueError(f"{task['app']} is not installed on this computer anymore.")
        command=list(choice['argv'])
        env={**os.environ,**Connections(state_dir()).environment(),'BUSINESSOS_WORKSPACE':task['workspace'],'PYTHONUTF8':'1'}
        execution=Execution();execution.permission=task.get('permission','native')
        prompt=(f"This is an unattended scheduled run of “{task['name']}” for AURA business {task['business_id']}, with no one watching. "
                "Check what is already done before acting, and don't repeat anything that already happened.\n\n"+task['prompt'])
        if task['app']=='codex':
            command[-1:-1]=['--sandbox',{'full':'danger-full-access','read-only':'read-only'}.get(execution.permission,'workspace-write')]
            result=workspace_codex.run(command,Path(task['workspace']),prompt,None,task.get('model',''),task.get('effort',''),lambda **v:None,env,execution)
        else:
            result=workspace_agents.run(command,task['app'],Path(task['workspace']),env,prompt,None,task.get('model',''),task.get('effort',''),lambda **v:None,execution)
        record.update(status='complete',reply=str(result.get('reply') or '')[:4000])
    except Exception as error:  # the run's own record says what happened; nothing else is waiting on it
        record['error']=str(error)[:600]
    finally:
        history=(runs(ident)+[record])[-20:]
        try:definition_path(ident).with_suffix('.runs.json').write_text(json.dumps(history,ensure_ascii=False,indent=2),encoding='utf-8')
        except OSError:pass


def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('action',choices=['create','list','pause','resume','remove','remove-all','edit','run'])
    ap.add_argument('id',nargs='?');ap.add_argument('--business-id');ap.add_argument('--app');ap.add_argument('--name');ap.add_argument('--when')
    ap.add_argument('--prompt-file');ap.add_argument('--model',default='');ap.add_argument('--effort',default='');ap.add_argument('--permission',default='');ap.add_argument('--state')
    a=ap.parse_args()
    if a.state:os.environ['AURA_STATE_DIR']=a.state
    prompt=Path(a.prompt_file).read_text(encoding='utf-8') if a.prompt_file else None
    if a.action=='run':run(a.id);return
    if a.action=='list':result=listed()
    elif a.action=='remove-all':result=[change(t['id'],'remove')['name'] for t in definitions()]
    elif a.action=='create':result=create(a.business_id,a.app,a.name,a.when,prompt,a.model,a.effort,a.permission)
    elif a.action=='edit':result=change(a.id,'edit',{k:v for k,v in {'when':a.when,'prompt':prompt,'name':a.name,'model':a.model,'effort':a.effort}.items() if v})
    else:result=change(a.id,a.action)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    try:main()
    except ValueError as error:raise SystemExit(str(error))
