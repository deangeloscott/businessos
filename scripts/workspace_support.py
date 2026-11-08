"""Bounded local diagnostics and explicit support preparation. No delivery."""
import ctypes
import json
import os
import platform
import shutil
import sys
import threading
import time
import re
import traceback
from collections import deque
from pathlib import Path

_draft_lock=threading.Lock()

UNEXPECTED_ERROR='AURA couldn’t complete this action. Try again. If it keeps happening, report it from Settings.'


def human_error(error):
    """Keep actionable validation messages; translate implementation failures."""
    if isinstance(error,FileNotFoundError):return 'The selected file or folder is no longer available. Check its location and try again.'
    if isinstance(error,PermissionError) and error.errno is not None:return 'AURA couldn’t access this item. Check the file or folder permissions and try again.'
    if isinstance(error,FileExistsError):return 'An item already exists at that location. Choose another name or location.'
    if isinstance(error,UnicodeError):return 'AURA couldn’t read this text file. Ask your AI to check its text encoding; keep the original file.'
    if isinstance(error,json.JSONDecodeError):return 'AURA couldn’t read some saved information. Keep the original and ask your AI to check the file.'
    if isinstance(error,OSError) and not isinstance(error,PermissionError):
        if error.errno==28:return 'There isn’t enough free disk space to save this change. Free some space and try again.'
        return 'AURA couldn’t read or save this item. Check that its folder is available and try again.'
    message=str(error).strip()
    if re.search(r'(?:unresolved ref|cross-business ref|canonical state still refers)',message,re.I):
        return 'Some saved information has a missing or conflicting link. Ask your AI to check those links before trying again.'
    if re.search(r'(?:post-(?:persistence|removal) validation failed|schema|is not of type|is a required property)',message,re.I):
        return 'Some saved information needs correction before this change can be saved. Ask your AI to check the affected record.'
    technical=re.search(r'(?:Traceback|\b(?:TypeError|AttributeError|KeyError|SyntaxError)\b|innerHTML|undefined|\bnull\b|[{}<>]|\b(?:ENOENT|EACCES)\b|\bat .+?:\d+:\d+)',message)
    if isinstance(error,(ValueError,PermissionError)) and message and len(message)<=350 and not technical:return message
    return UNEXPECTED_ERROR


class ErrorDetails:
    """Small in-memory error tail, included only in reviewed technical reports."""
    def __init__(self):self.lock=threading.Lock();self.rows=deque(maxlen=24)

    def record(self,error,operation,redactor=lambda value:value):
        import secrets
        from _process_errors import redact
        message=redactor(redact(str(error)+('\n'+str(error.diagnostic) if getattr(error,'diagnostic',None) else '')))
        # Full local paths and URL query strings are not needed to identify code failures.
        message=re.sub(r'(?:[A-Za-z]:[\\/]|/(?:Users|home)/)[^\s\"\'<>]+','[local path]',message)
        message=re.sub(r'(https?://[^\s?]+)\?[^\s]+',r'\1?[details hidden]',message)
        row={'id':secrets.token_hex(6),'at':time.time(),'operation':operation,
             'type':type(error).__name__,'message':message[:2000],
             'frames':[{'file':Path(f.filename).name,'line':f.lineno,'function':f.name}
                       for f in traceback.extract_tb(error.__traceback__)[-8:]]}
        with self.lock:self.rows.append(row)
        return row['id']

    def snapshot(self):
        with self.lock:return list(self.rows)

ROUTES=set("state files file media library library/item chats chats/open chats/detail chat chat/stop conversation notifications updates usage usage/settings profile diagnostics support/environment support/test support/prepare chats/native chats/import chats/changes".split())

class Performance:
    def __init__(self):
        self.started=time.monotonic();self.lock=threading.Lock();self.rows={};self.recent=deque(maxlen=128)

    def record(self,method,path,status,elapsed,size):
        name=path.removeprefix('/api/')
        if name not in ROUTES:name='other'
        key=method+' /api/'+name
        with self.lock:
            row=self.rows.setdefault(key,{'requests':0,'errors':0,'total_ms':0,'max_ms':0,'response_bytes':0})
            row['requests']+=1;row['errors']+=status>=400;row['total_ms']+=elapsed;row['max_ms']=max(row['max_ms'],elapsed);row['response_bytes']+=size
            self.recent.append({'operation':key,'status':status,'ms':round(elapsed,2),'bytes':size})

    def snapshot(self):
        with self.lock:
            rows={k:{**v,'mean_ms':round(v['total_ms']/v['requests'],2),'total_ms':round(v['total_ms'],2),'max_ms':round(v['max_ms'],2)} for k,v in self.rows.items()}
            return {'uptime_seconds':round(time.monotonic()-self.started),'operations':rows,'recent':list(self.recent),'scope':'This AURA process only; no prompts, URLs, paths or error text.'}


def machine(root):
    result={'os':platform.system(),'os_release':platform.release(),'architecture':platform.machine(),
            'logical_cpus':os.cpu_count(),'python':platform.python_version(),'aura_cpu_seconds':round(time.process_time(),2)}
    try:
        if os.name=='nt':
            class Memory(ctypes.Structure):
                _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong),*[(k,ctypes.c_ulonglong) for k in ('physical','available','page','available_page','virtual','available_virtual','extended')]]
            memory=Memory();memory.length=ctypes.sizeof(memory)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
                result.update(ram_gib=round(memory.physical/2**30,1),available_ram_gib=round(memory.available/2**30,1))
            class ProcessMemory(ctypes.Structure):
                _fields_=[('size',ctypes.c_ulong),('faults',ctypes.c_ulong),*[(k,ctypes.c_size_t) for k in ('peak_working','working','peak_paged','paged','peak_nonpaged','nonpaged','pagefile','peak_pagefile')]]
            usage=ProcessMemory();usage.size=ctypes.sizeof(usage)
            handle=ctypes.windll.kernel32.GetCurrentProcess;handle.restype=ctypes.c_void_p
            get=ctypes.windll.psapi.GetProcessMemoryInfo;get.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_ulong]
            if get(handle(),ctypes.byref(usage),usage.size):result['aura_memory_mib']=round(usage.working/2**20,1)
        elif sys.platform.startswith('linux'):
            values={line.split(':')[0]:int(line.split()[1])*1024 for line in Path('/proc/meminfo').read_text(encoding='utf-8').splitlines() if line.startswith(('MemTotal:','MemAvailable:'))}
            result.update(ram_gib=round(values['MemTotal']/2**30,1),available_ram_gib=round(values['MemAvailable']/2**30,1))
        disk=shutil.disk_usage(root);result['workspace_disk_free_gib']=round(disk.free/2**30,1)
    except (OSError,ValueError,AttributeError):pass
    if os.name=='nt':
        import subprocess
        command="$ErrorActionPreference='Stop'; @{cpu=@(Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name); gpu=@(Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion)} | ConvertTo-Json -Compress -Depth 3"
        try:
            done=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',command],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=5,creationflags=subprocess.CREATE_NO_WINDOW)
            details=json.loads(done.stdout) if done.returncode==0 else {}
            if isinstance(details.get('cpu'),list):result['cpu_models']=[str(v)[:160] for v in details['cpu'][:8]]
            if isinstance(details.get('gpu'),list):result['graphics']=[{'model':str(v.get('Name',''))[:160],'driver':str(v.get('DriverVersion',''))[:80]} for v in details['gpu'][:8] if isinstance(v,dict)]
        except (OSError,ValueError,subprocess.SubprocessError):pass
    return result


def prepare(data,environment,folder,persist=True):
    kind=data.get('kind')
    if not isinstance(kind,str) or kind not in {'troubleshooting','feature'}:raise ValueError('Choose troubleshooting or a feature request.')
    title=data.get('title');description=data.get('description')
    if not isinstance(title,str) or not 1<=len(title.strip())<=160:raise ValueError('Add a short title.')
    if not isinstance(description,str) or not 1<=len(description.strip())<=12000:raise ValueError('Describe your request in up to 12,000 characters.')
    # The browser provides only explicitly selected text/image attachments. No local paths are accepted.
    attachments=data.get('attachments',[])
    if not isinstance(attachments,list) or len(attachments)>4:raise ValueError('Choose up to four attachments.')
    import base64
    for attachment in attachments:
        if not isinstance(attachment,dict) or set(attachment)!={'name','type','data'}:raise ValueError('Choose a supported attachment.')
        if not isinstance(attachment['type'],str) or attachment['type'] not in {'image/png','image/jpeg','image/webp','text/plain'}:raise ValueError('Use PNG, JPEG, WebP or plain text attachments.')
        if not isinstance(attachment['name'],str) or len(attachment['name'])>160 or '/' in attachment['name'] or '\\' in attachment['name']:raise ValueError('Use an attachment filename without a path.')
        try:raw=base64.b64decode(attachment['data'],validate=True)
        except (ValueError,TypeError):raise ValueError('This attachment could not be read.') from None
        if len(raw)>1024*1024:raise ValueError('Each attachment must be 1 MB or smaller.')
    report={'format':'aura-support-v1','kind':kind,'title':title.strip(),'description':description.strip(),
            'created_at':time.time(),'delivery':'test_only_not_sent','environment':environment if data.get('include_environment') is True else None,
            'browser_performance':browser_metrics(data.get('browser_performance',{})) if data.get('include_environment') is True else {},'attachments':attachments}
    if data.get('include_environment') is True and environment is not None:
        report['environment']={**environment,'browser_errors':browser_errors(data.get('browser_errors'))}
    if not persist:
        report.pop('delivery',None)
        return {'report':report}
    with _draft_lock:
        folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
        import secrets
        ident=secrets.token_hex(12)
        target=folder/(ident+'.json');temporary=target.with_suffix('.tmp')
        temporary.write_text(json.dumps(report,ensure_ascii=False),encoding='utf-8');temporary.replace(target)
        existing=[]
        for path in folder.glob('*.json'):
            try:existing.append((path.stat().st_mtime_ns,path))
            except FileNotFoundError:pass
        for _,old in sorted(existing,reverse=True)[10:]:
            try:old.unlink()
            except FileNotFoundError:pass
    return {'id':ident,'sent':False,'status':'test_prepared','message':'Test report prepared on this computer. Email delivery is not connected; nothing was sent.'}


def browser_metrics(raw):
    if not isinstance(raw,dict):return {}
    # Never accept a raw browser log or arbitrary performance entry names/URLs.
    result={}
    for name in ('requests','errors','total_ms','max_ms','message_formats','message_format_ms','long_tasks','long_task_ms','max_long_task_ms','viewport_width','viewport_height','device_pixel_ratio','browser_heap_mib'):
        value=raw.get(name)
        if isinstance(value,(int,float)) and not isinstance(value,bool) and 0<=value<10**12:result[name]=round(value,2)
    for name in ('browser','platform'):
        value=raw.get(name)
        if isinstance(value,str) and value in {'Chrome','Edge','Firefox','Safari','Other','Windows','macOS','Linux','Android','iOS'}:result[name]=value
    return result


def browser_errors(raw):
    """Explicitly reviewed browser diagnostics, never arbitrary files or event payloads."""
    from _process_errors import redact
    if not isinstance(raw,list):return []
    result=[]
    for row in raw[-12:]:
        if not isinstance(row,dict):continue
        clean={key:redact(str(row.get(key,'')))[:limit] for key,limit in
               (('type',80),('message',1000),('stack',2000))}
        clean['at']=row.get('at') if isinstance(row.get('at'),(int,float)) else None
        result.append(clean)
    return result
