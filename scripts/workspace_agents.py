"""Read installed harness catalogues; execution and provider routing stay host-owned."""
import json
import queue
import subprocess
import threading
import time
import os
from pathlib import Path
import re


def base_command(command):
    # Built-in adapters put their print flag after the complete launcher prefix.
    for flag in ('--print', '-p'):
        if flag in command:
            return command[:command.index(flag)]
    if 'chat' in command:
        return command[:command.index('chat')]
    raise ValueError('This connection needs a supported print command.')


class Metadata:
    def __init__(self, command, kind, cwd, env, model='', native_id=''):
        args = ['--mode', 'rpc', '--no-session'] if kind in {'pi', 'omp'} else ['-p', '--input-format', 'stream-json', '--output-format', 'stream-json', '--verbose', '--no-session-persistence']
        if kind == 'hermes':
            args = ['acp']
        if native_id:
            args = ['--mode', 'rpc', '--session' if kind == 'pi' else '--resume', native_id]
        if model:
            args += ['--model', model]
        self.kind, self.number, self.events = kind, 0, queue.Queue()
        self.process = subprocess.Popen([*base_command(command), *args], cwd=cwd, env=env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                                        encoding='utf-8', errors='replace')
        def read():
            for line in self.process.stdout:
                try:
                    self.events.put(json.loads(line))
                except ValueError:
                    pass
            self.events.put(None)
        threading.Thread(target=read, daemon=True).start()

    def call(self, kind, **params):
        self.number += 1
        ident = str(self.number)
        value = {'id': ident, 'type': kind, **params} if self.kind != 'claude' else {'type': 'control_request', 'request_id': ident, 'request': {'subtype': kind, **params}}
        if self.kind == 'hermes':
            value = {'jsonrpc':'2.0', 'id':ident, 'method':kind, 'params':params}
        self.process.stdin.write(json.dumps(value) + '\n')
        self.process.stdin.flush()
        deadline = time.monotonic() + 40
        while time.monotonic() < deadline:
            try:
                event = self.events.get(timeout=max(.01, deadline-time.monotonic()))
            except queue.Empty:
                break
            if event is None:
                break
            response = event.get('response', {}) if self.kind == 'claude' else event
            if response.get('request_id' if self.kind == 'claude' else 'id') != ident:
                continue
            if response.get('success') is False or response.get('subtype') == 'error' or 'error' in response:
                detail=response.get('error') or response.get('message') or 'This app version could not return that setting. Update it or use its own settings.'
                raise ValueError(str(detail.get('message',detail) if isinstance(detail,dict) else detail))
            return response.get('result', {}) if self.kind == 'hermes' else response.get('response', {}) if self.kind == 'claude' else response.get('data', {})
        raise ValueError('The AI app did not return its catalogue. Open it to check sign-in or update it, then refresh the choices.')

    def close(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            # Only this metadata subprocess and its launcher children; no prompt was sent.
            if __import__('os').name == 'nt':
                subprocess.run(['taskkill', '/PID', str(self.process.pid), '/T', '/F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                self.process.terminate()
            self.process.wait(timeout=5)


def options(command, kind, cwd, env):
    if kind == 'antigravity':
        result = subprocess.run([*base_command(command), 'models'], cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, text=True, encoding='utf-8', timeout=40)
        rows = []
        for line in result.stdout.splitlines():
            if '\t' not in line:
                continue
            ident, name = line.split('\t', 1)
            provider = 'anthropic' if ident.startswith('claude-') else 'openai' if ident.startswith(('gpt-', 'o1', 'o3')) else 'google'
            rows.append({'id':ident, 'name':name.strip(), 'provider':provider, 'efforts':[], 'default_effort':''})
        if result.returncode or not rows:
            raise ValueError('Antigravity did not return its models. Sign in through agy, then refresh the choices.')
        return {'models':rows, 'model':'', 'effort':'', 'sessions':True,
                'note':'Models come from agy. Effort is included in some model names; separate supported tiers are not reported.'}
    if kind == 'hermes':
        return hermes_options(command, cwd, env)
    host = Metadata(command, kind, cwd, env)
    try:
        if kind == 'claude':
            result = host.call('initialize')
            rows = [{'id': m['value'], 'name': m.get('displayName', m['value']), 'provider': 'anthropic',
                     'efforts': m.get('supportedEffortLevels', []), 'default_effort': ''}
                    for m in result.get('models', [])]
            return {'models': rows, 'model': '', 'effort': '', 'sessions': True,
                    'note': 'Choices come from Claude Code. Effort stays at app default when this version does not report supported levels.'}
        result, state = host.call('get_available_models'), host.call('get_state')
        current = state.get('model') or {}
        rows = [{'id': m['provider'] + '/' + m['id'], 'name': m.get('name', m['id']) + ' · ' + m['provider'], 'provider': m['provider'],
                 'efforts': [], 'default_effort': '', 'discover_efforts': True} for m in result.get('models', [])]
        return {'models': rows, 'model': current.get('provider', '') + '/' + current.get('id', ''),
                'effort': state.get('thinkingLevel', ''), 'sessions': True,
                'note': 'Models and supported thinking levels come from your AI app. Your app owns permissions and saved conversations.'}
    finally:
        host.close()


def efforts(command, kind, cwd, env, model):
    host = Metadata(command, kind, cwd, env, model)
    try:
        result = host.call('get_available_thinking_levels')
        state = host.call('get_state')
        return {'efforts': result.get('levels', []), 'default_effort': state.get('thinkingLevel', '')}
    finally:
        host.close()


def check_signin(command, kind, model, cwd, env):
    """Use a native credential check where one is exposed; never send a prompt."""
    if kind != 'pi':
        return
    provider = model.split('/', 1)[0]
    if provider.lower() in {'ollama','lmstudio','llama.cpp','llamacpp'} or re.fullmatch(r'\d*local',provider,re.I):
        return
    flags = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
    # Older Pi versions may interpret positional words as a user prompt.
    # Only call this subcommand when its non-inference help advertises it.
    help_result = subprocess.run([*base_command(command), '--help'], cwd=cwd, env=env,
                                stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=40, **flags)
    if help_result.returncode or not re.search(r'\bauth\s+check\b',help_result.stdout,re.I):
        return
    result = subprocess.run([*base_command(command), 'auth', 'check', '--provider', provider, '--json'],
                            cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True,
                            text=True, encoding='utf-8', errors='replace', timeout=40, **flags)
    try:
        status = json.loads(result.stdout).get('status')
    except ValueError:
        status = None
    if result.returncode or status != 'ready':
        raise ValueError('Your AI app needs you to sign in. Open it, sign in, and try again.')


def check_transport(command, kind, cwd, env):
    # ACP initialize is a handshake only. Avoid session/new (and empty chats)
    # merely to repeat a connection check.
    host = Metadata(command, kind, cwd, env)
    try:
        host.call('initialize', protocolVersion=1, clientCapabilities={}, clientInfo={'name':'aura-workspace','version':'1'})
    finally:
        host.close()


def execution_command(command, kind, model, effort):
    argv = list(command)
    if kind in {'pi', 'omp', 'claude'} and model:
        argv += ['--model', model]
        if effort:
            argv += ['--effort' if kind == 'claude' else '--thinking', effort]
    return argv


def hermes_options(command, cwd, env):
    host = Metadata(command, 'hermes', cwd, env)
    try:
        host.call('initialize', protocolVersion=1, clientCapabilities={}, clientInfo={'name':'aura-workspace','version':'1'})
        state = host.call('session/new', cwd=str(cwd), mcpServers=[])
        catalog = state.get('models') or {}
        rows = [{'id':m['modelId'], 'name':m['name'], 'provider':m['modelId'].split(':',1)[0],
                 'efforts':[], 'default_effort':''} for m in catalog.get('availableModels', [])]
        return {'models':rows, 'model':catalog.get('currentModelId',''), 'effort':'', 'sessions':True,
                'note':'Models come from Hermes through ACP. Supported effort tiers are not exposed by this interface; Hermes keeps its own reasoning setting.'}
    finally:
        host.close()


def message_text(value):
    if isinstance(value, list):
        value = '\n'.join(p.get('text','') for p in value if isinstance(p,dict) and p.get('type') in {'text','input_text','output_text'})
    if not isinstance(value, str):
        return ''
    return value.replace('\r\n','\n')


def display_text(value):
    value=message_text(value)
    if '\nUser request:\n' in value:
        value=value.split('\nUser request:\n',1)[1]
    if value.startswith('Welcome me to my AURA workspace'):
        value='Set up my AURA workspace and suggest a useful next step.'
    return re.sub(r'(?m)^\s*AURA_SETUP[^\n]*','',value).strip()


def resume_command(kind, native_id):
    return {'pi':['pi','--session',native_id], 'omp':['omp','--resume',native_id],
            'claude':['claude','--resume',native_id], 'hermes':['hermes','--resume',native_id],
            'antigravity':['agy','--conversation',native_id]}[kind]


def history(command, kind, cwd, env, native_id):
    model, effort = '', ''
    if kind in {'pi','omp'}:
        host=Metadata(command,kind,cwd,env,native_id=native_id)
        try:
            state=host.call('get_state')
            if state.get('sessionId')!=native_id:
                raise ValueError('The AI app did not reopen the exact saved chat. No request was sent.')
            messages=host.call('get_messages').get('messages',[])
            current=state.get('model') or {}
            model=(current.get('provider','')+'/'+current.get('id','')).strip('/')
            effort=state.get('thinkingLevel','')
        finally:host.close()
    elif kind=='hermes':
        result=subprocess.run([*base_command(command),'sessions','export','--session-id',native_id,'--format','jsonl','--redact','-'],
                              cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,encoding='utf-8',timeout=40)
        sessions=[json.loads(line) for line in result.stdout.splitlines() if line.strip().startswith('{')]
        session=next((s for s in sessions if s.get('id',s.get('session_id'))==native_id),None)
        if result.returncode or not session:
            raise ValueError('Hermes did not return this saved chat. Open its native session before retrying.')
        messages=session.get('messages',[])
    elif kind=='claude':
        root=Path(env.get('CLAUDE_CONFIG_DIR') or Path.home()/'.claude')/'projects'
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,100}',native_id):
            raise ValueError('The saved Claude chat ID is invalid.')
        matches=list(root.glob('*/'+native_id+'.jsonl'))
        if len(matches)!=1:
            raise ValueError('Claude Code has not exposed this native transcript locally.')
        messages=[]
        for line in matches[0].read_text(encoding='utf-8').splitlines():
            row=json.loads(line)
            if row.get('type') in {'user','assistant'} and isinstance(row.get('message'),dict):
                messages.append({**row['message'],'timestamp':row.get('timestamp')})
    else:
        raise ValueError('Showing the saved display. Antigravity keeps the full native chat; edits made in its app may not appear here.')
    out=[]
    for message in messages:
        if message.get('role') not in {'user','assistant'}:continue
        text=display_text(message.get('content',''))
        at=message.get('timestamp') or message.get('created_at')
        if isinstance(at,(int,float)) and at>1e11:at/=1000
        if text:out.append({'role':message['role'],'text':text,'at':at,
                           'agent':{'pi':'Pi','omp':'OMP','claude':'Claude Code','hermes':'Hermes'}[kind]})
    return {'messages':out,'model':model,'effort':effort,'usage':{},'native_id':native_id,
            'resume':subprocess.list2cmdline(resume_command(kind,native_id))}


def tool_activity(name):
    name = str(name or '').lower()
    if any(word in name for word in ('search', 'browse', 'fetch', 'web')):
        return 'Researching with a connected tool'
    if any(word in name for word in ('edit', 'write', 'patch')):
        return 'Updating a file'
    if any(word in name for word in ('read', 'list', 'find', 'glob', 'grep')):
        return 'Reading files and context'
    if any(word in name for word in ('bash', 'shell', 'exec', 'terminal')):
        return 'Running a command'
    return 'Using a connected tool'


def run(command, kind, cwd, env, prompt, native_id, model, effort, update, execution=None):
    argv=base_command(command)
    if kind in {'pi','omp'}:
        argv += ['--print','--mode','json']
        if native_id:argv += ['--session' if kind=='pi' else '--resume',native_id]
        argv=execution_command(argv,kind,model,effort)
    elif kind=='claude':
        argv += ['-p','--output-format','stream-json','--verbose']
        if native_id:argv += ['--resume',native_id]
        argv=execution_command(argv,kind,model,effort)
    elif kind=='hermes':
        argv += ['chat','--query-file','-','--format','stream-json']
        if native_id:argv += ['--resume',native_id]
        argv += ['--model',model]
        if effort:argv += ['--reasoning',effort]
    else:
        argv += ['--input-format','stream-json','--output-format','stream-json','--model',model]
        if native_id:argv += ['--conversation',native_id]
        if effort:argv += ['--effort',effort]
        prompt=json.dumps({'event':'user','message':{'content':prompt}})+'\n'
    final, ident, error='',native_id,''
    with (execution.popen if execution else subprocess.Popen)(argv,cwd=cwd,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                          text=True,encoding='utf-8',errors='replace') as process:
        process.stdin.write(prompt);process.stdin.close()
        for line in process.stdout:
            try:event=json.loads(line)
            except ValueError:continue
            event_type=event.get('type',event.get('event'))
            new_id=event.get('session_id') or (event.get('id') if event_type=='session' else None) or event.get('conversation_id')
            if new_id:
                if native_id and new_id!=native_id:
                    error='The app returned a different chat ID. Check the native app before continuing.'
                else:
                    ident=new_id;update(native_id=ident)
            if event_type=='message_end':
                message=event.get('message',{})
                if message.get('role')=='assistant':
                    if message.get('stopReason') in {'error','aborted'}:error=message.get('errorMessage') or 'The AI request did not complete.'
                    text=message_text(message.get('content',[]))
                    if text:final=text;update(reply=final,progress='Preparing a reply')
            elif event_type=='message_start' and event.get('message',{}).get('role')=='assistant':
                final=''
                update(reply='',progress='Preparing a reply')
            elif event_type=='message_update':
                delta=event.get('assistantMessageEvent') or {}
                if delta.get('type')=='text_delta':
                    final+=str(delta.get('delta',''))
                    update(reply=final)
            elif event_type=='text' and kind=='hermes':
                final+=str(event.get('text',''))
                update(reply=final,progress='Preparing a reply')
            elif event_type in {'error','turn.failed'}:
                detail=event.get('error',event.get('message','The AI request failed.'))
                error=str(detail.get('message',detail) if isinstance(detail,dict) else detail)
            elif event_type=='assistant':
                content=(event.get('message') or {}).get('content',[])
                text=message_text(content)
                if text:final=text;update(reply=final,progress='Preparing a reply')
                for block in content if isinstance(content,list) else []:
                    if block.get('type')=='tool_use':update(progress=tool_activity(block.get('name')))
            elif event_type=='result':
                result=event.get('result') if isinstance(event.get('result'),dict) else event
                result_id=result.get('conversation_id') or result.get('session_id') or ident
                if native_id and result_id!=native_id:
                    error='The app returned a different chat ID. Check the native app before continuing.'
                elif result_id:
                    ident=result_id;update(native_id=ident)
                final=result.get('response') or result.get('text') or (event.get('result') if isinstance(event.get('result'),str) else '') or final
                if result.get('is_error') or result.get('exit_code') or (result.get('status') and result['status']!='SUCCESS'):
                    error=str(result.get('error') or final or 'The host did not complete this request. Check its native chat.')
            elif event_type in {'tool_execution_start','tool_use','step_update','tool_start'}:
                update(progress=tool_activity(event.get('toolName') or event.get('name') or event.get('tool')))
            elif event_type in {'tool_execution_end','tool_end','tool_result'}:
                update(progress='Tool finished. Continuing the request')
        code=process.wait()
    if execution:execution.check()
    if code or error or not ident or not final.strip():
        raise ValueError(error or 'The AI app did not complete a saved reply. Open its native chat to check authentication or approvals; no automatic retry was made.')
    return {'reply':final,'native_id':ident,'usage':{}}
