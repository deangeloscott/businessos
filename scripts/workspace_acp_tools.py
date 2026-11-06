"""Optional ACP client filesystem/command services, using the current user account."""
import os
import secrets
import signal
import subprocess
import threading
from pathlib import Path


class ClientTools:
    def __init__(self,cwd,env):self.cwd=Path(cwd);self.env=env;self.items={};self.lock=threading.RLock();self.closed=False

    def busy(self):
        with self.lock:return any(r['process'].poll() is None for r in self.items.values())

    def kill(self,row):
        process=row['process']
        if process.poll() is not None:return
        if os.name=='nt':subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            try:os.killpg(process.pid,signal.SIGKILL)
            except ProcessLookupError:pass

    def close(self):
        with self.lock:self.closed=True;rows=list(self.items.values());self.items.clear()
        for row in rows:self.kill(row)
        for row in rows:
            try:row['process'].wait(timeout=5)
            except subprocess.TimeoutExpired:pass

    def call(self,method,p):
        with self.lock:
            if self.closed:raise ValueError('This connection has ended.')
        if method.startswith('fs/'):
            path=Path(p['path'])
            if not path.is_absolute():raise ValueError('Use an absolute file path.')
            if method=='fs/write_text_file':
                if not isinstance(p.get('content'),str):raise ValueError('Provide text file content.')
                path.parent.mkdir(parents=True,exist_ok=True);path.write_text(p['content'],encoding='utf-8');return {}
            if method=='fs/read_text_file':
                line=p.get('line',1);limit=p.get('limit')
                if not isinstance(line,int) or isinstance(line,bool) or line<1 or limit is not None and (not isinstance(limit,int) or isinstance(limit,bool) or limit<0):raise ValueError('Use a positive starting line and a non-negative line limit.')
                with path.open(encoding='utf-8') as stream:
                    import itertools
                    content=''.join(itertools.islice(stream,line-1,None if limit is None else line-1+limit))
                return {'content':content}
        if method=='terminal/create':
            cwd=Path(p.get('cwd') or self.cwd)
            if not cwd.is_absolute():raise ValueError('Use an absolute working folder.')
            command=p.get('command');args=p.get('args',[]);limit=p.get('outputByteLimit',1024*1024)
            if not isinstance(command,str) or not command or not isinstance(args,list) or not all(isinstance(v,str) for v in args):raise ValueError('Provide a command and an argument list.')
            if not isinstance(limit,int) or isinstance(limit,bool) or limit<0:raise ValueError('Use a non-negative output byte limit.')
            env={**self.env,**{v['name']:v['value'] for v in p.get('env',[])}}
            # Register under the cleanup lock: cancellation must not miss a child
            # that has started but has not yet entered the terminal collection.
            with self.lock:
                if self.closed:raise ValueError('This connection has ended.')
                process=subprocess.Popen([command,*args],cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                    **({'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {'start_new_session':True}))
                ident=secrets.token_urlsafe(18);row={'process':process,'output':b'','limit':min(limit,16*1024*1024),'truncated':False,'done':threading.Event()}
                self.items[ident]=row
            def read():
                try:
                    while data:=process.stdout.read1(8192):
                        with self.lock:
                            data=row['output']+data;row['truncated']|=len(data)>row['limit']
                            row['output']=data[-row['limit']:] if row['limit'] else b''
                    process.wait()
                finally:process.stdout.close();row['done'].set()
            threading.Thread(target=read,daemon=True).start()
            return {'terminalId':ident}
        with self.lock:row=self.items.get(p.get('terminalId'))
        if not row:raise ValueError('This terminal has ended or belongs to another conversation.')
        if method=='terminal/output':
            with self.lock:result={'output':row['output'].decode('utf-8',errors='ignore'),'truncated':row['truncated']}
            code=row['process'].poll()
            if code is not None:result['exitStatus']={'exitCode':code} if code>=0 else {'signal':str(-code)}
            return result
        if method=='terminal/wait_for_exit':
            code=row['process'].wait();row['done'].wait()
            return {'exitCode':code} if code>=0 else {'signal':str(-code)}
        if method in {'terminal/kill','terminal/release'}:
            self.kill(row)
            if method=='terminal/release':
                with self.lock:self.items.pop(p['terminalId'],None)
            return {}
        raise ValueError('This client operation is not supported.')

    def handle(self,event,send,execution,update):
        method=event.get('method','')
        if method not in {'fs/read_text_file','fs/write_text_file','terminal/create','terminal/output','terminal/wait_for_exit','terminal/kill','terminal/release'}:return False
        # Waits never block the native message reader or an approval/cancel response.
        def work():
            try:
                result=self.call(method,event.get('params') or {})
                if not execution.stopped.is_set():send({'id':event['id'],'result':result})
            except (OSError,ValueError,KeyError,TypeError) as error:
                update(native_diagnostic={'method':method,'reason':str(error)})
                try:
                    if not execution.stopped.is_set():send({'id':event['id'],'error':{'code':-32000,'message':'The client could not complete this file or command operation.'}})
                except (OSError,ValueError):pass
        threading.Thread(target=work,daemon=True).start();return True
