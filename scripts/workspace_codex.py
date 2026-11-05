"""Native Codex connection for the optional view; no separate chat store or model loop."""
from pathlib import Path
import json
import os
import queue
import re
import subprocess
import threading
import time
from _process_errors import ErrorTail
import workspace_usage
import workspace_chats


def base_command(command):
    return command[:command.index('exec')]


def rpc(command, calls, cwd, env=None, experimental=False):
    """Read host metadata without inference or changing its shared settings."""
    events = queue.Queue()
    with subprocess.Popen([*base_command(command), 'app-server'], cwd=cwd, env=env,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0) as process:
        errors = ErrorTail(process, env)
        def read():
            for line in process.stdout:
                try:
                    events.put(json.loads(line))
                except ValueError:
                    pass
            events.put(None)
        threading.Thread(target=read, daemon=True).start()

        def send(value):
            errors.send(process, json.dumps(value) + '\n')

        def response(number):
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                try:
                    event = events.get(timeout=max(.01, deadline-time.monotonic()))
                except queue.Empty:
                    break
                if event is None:
                    raise ValueError(errors.message('Codex metadata connection closed. Open Codex to check its setup.'))
                if event.get('id') == number:
                    if 'error' in event:
                        raise ValueError(event['error'].get('message', 'Codex could not read its settings.'))
                    return event.get('result', {})
            raise ValueError(errors.message('Codex did not return its settings in time. Open Codex and try again.'))

        try:
            send({'id': 0, 'method': 'initialize', 'params': {'clientInfo': {'name': 'aura_workspace', 'version': '1.0'},**({'capabilities':{'experimentalApi':True}} if experimental else {})}})
            response(0)
            send({'method': 'initialized', 'params': {}})
            number=0
            def call(method,params):
                nonlocal number
                number+=1
                send({'id': number, 'method': method, 'params': params})
                return response(number)
            # Adaptive discovery pages stay on the same native connection.
            if callable(calls):return calls(call)
            results = []
            for method,params in calls:
                results.append(call(method,params))
            return results
        finally:
            ErrorTail.close_input(process)
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.terminate()
                process.wait(timeout=5)


def options(command, cwd, env=None):
    models, settings = rpc(command, [('model/list', {'limit': 100}), ('config/read', {'includeLayers': False})], cwd, env)
    config = settings.get('config', {})
    try:
        # Retain only the access type, never account identifiers or credentials.
        account = rpc(command, [('account/read', {'refreshToken': False})], cwd, env)[0].get('account') or {}
        access = {'chatgpt': 'signin', 'chatgptAuthTokens': 'signin', 'apiKey': 'api'}.get(account.get('type'), 'codex')
    except (ValueError, OSError, subprocess.SubprocessError):
        access = 'codex'
    if (config.get('model_provider') or 'openai') != 'openai':
        access = 'codex'
    rows = [{'id': row['model'], 'name': row.get('displayName', row['model']), 'provider': config.get('model_provider') or 'openai',
             'efforts': [v['reasoningEffort'] for v in row.get('supportedReasoningEfforts', [])],
             'default_effort': row.get('defaultReasoningEffort', ''), 'access': access}
            for row in models.get('data', []) if not row.get('hidden')]
    default = config.get('model') or next((m['model'] for m in models.get('data', []) if m.get('isDefault')), '')
    return {'models': rows, 'model': default,
            'effort': config.get('model_reasoning_effort') or next((m['default_effort'] for m in rows if m['id'] == default), ''),
            'sessions': True}


def attach(product, workspace):
    """One project-local pointer, using native instructions and Skill discovery."""
    product, workspace = Path(product).resolve(), Path(workspace).resolve()
    if workspace == product:
        return {'instructions': str(product / 'AGENTS.md'), 'skill': str(product / 'skills/viraltrac-aura/SKILL.md')}
    instructions = workspace / 'AGENTS.md'
    if instructions.is_symlink():
        raise ValueError('Workspace instructions are linked elsewhere. Ask your AI to attach AURA without replacing them.')
    block = (f'<!-- AURA workspace attachment -->\nFor organizational work, read `{product / "AGENTS.md"}` '
             f'and `{product / "skills/viraltrac-aura/SKILL.md"}`.\n'
             f'Organization workspace: `{workspace}`. Use AURA helpers with BUSINESSOS_WORKSPACE set to this folder. '
             'Resolve the intended business; do not guess across businesses.\n'
             'The user owns this workspace. Customize its optional visual interface in an organization-owned copy, '
             f'using `{product / "docs/visual-workspace.md"}`.\n<!-- /AURA workspace attachment -->')
    current = instructions.read_text(encoding='utf-8') if instructions.exists() else ''
    pattern = r'<!-- AURA workspace attachment -->[\s\S]*?<!-- /AURA workspace attachment -->'
    updated = re.sub(pattern, lambda _: block, current) if re.search(pattern, current) else current.rstrip()+'\n\n'+block+'\n'
    folder = workspace / '.agents' / 'skills' / 'viraltrac-aura'
    if not folder.resolve().is_relative_to(workspace) or any(p.is_symlink() for p in (workspace / '.agents', workspace / '.agents/skills', folder)):
        raise ValueError('The workspace Skill folder is linked elsewhere. Ask your AI to finish native attachment.')
    skill = folder / 'SKILL.md'
    marker = '<!-- AURA native Skill pointer -->'
    if skill.is_symlink() or not skill.resolve().is_relative_to(workspace):
        raise ValueError('The AURA Skill points outside this workspace. Ask your AI to check it.')
    header = '---\nname: viraltrac-aura\ndescription: Reuse saved AURA business context and operating knowledge for organizational work.\n---\n'
    pointer = marker + f'\nRead the current full guidance at `{product / "skills/viraltrac-aura/SKILL.md"}`.\n' + f'AURA product: `{product}`. Organization workspace: `{workspace}`.\n'
    ending = '<!-- /AURA native Skill pointer -->'
    skill_text = header + pointer + ending + '\n'
    if skill.exists():
        existing = skill.read_text(encoding='utf-8')
        if marker in existing and ending in existing:
            skill_text = re.sub(re.escape(marker)+r'[\s\S]*?'+re.escape(ending), lambda _:pointer+ending, existing)
        elif existing != header + pointer:
            raise ValueError('An existing or customized AURA Skill is already here. Ask your AI to check it; it was not overwritten.')
    if updated != current:
        instructions.write_text(updated.lstrip('\n'), encoding='utf-8')
    folder.mkdir(parents=True, exist_ok=True)
    skill.write_text(skill_text, encoding='utf-8')
    return {'instructions': str(instructions), 'skill': str(skill)}


def verify_attachment(command, cwd, attachment):
    result = rpc(command, [('skills/list', {'cwds': [str(cwd)], 'forceReload': True})], cwd)[0]
    expected = Path(attachment['skill']).resolve()
    found = any(s.get('name') == 'viraltrac-aura' and s.get('enabled') is not False and
                Path(s.get('path', '')).resolve() == expected
                for row in result.get('data', []) for s in row.get('skills', []))
    return dict(attachment, discovered=found)


def run(command, cwd, prompt, native_id, model, effort, update, env=None, execution=None, child_model=''):
    if execution and execution.interactive:
        from workspace_native_io import codex_run
        return codex_run(command,cwd,prompt,native_id,model,effort,update,env,execution,child_model)
    from workspace_delegation import Tracker
    delegation = Tracker(update)
    argv = [*base_command(command), '-C', str(cwd), 'exec']
    if '--sandbox' in command:
        index = command.index('--sandbox')
        argv += command[index:index+2]
    if native_id:
        argv += ['resume']
    argv += ['--json', '--model', model, '-c', 'model_reasoning_effort=' + json.dumps(effort), '--skip-git-repo-check']
    if child_model:
        argv += ['-c', 'agents.default_subagent_model=' + json.dumps(child_model)]
    argv += [native_id, '-'] if native_id else ['-']
    env = env or dict(os.environ, BUSINESSOS_WORKSPACE=str(cwd), PYTHONUTF8='1')
    final, usage, error, thread = '', {}, '', native_id
    with (execution.popen if execution else subprocess.Popen)(argv, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0) as process:
        errors = ErrorTail(process, env)
        errors.send(process, prompt)
        ErrorTail.close_input(process)
        for line in process.stdout:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            kind = event.get('type')
            if delegation.observe('codex', event):continue
            if kind == 'thread.started':
                if native_id and event['thread_id']!=native_id:
                    error='Codex returned a different chat ID. Check the native app before continuing.'
                else:
                    thread = event['thread_id']
                    update(native_id=thread)
            elif kind in {'item.started', 'item.updated', 'item.completed'}:
                item = event.get('item', {})
                if item.get('type') == 'agent_message':
                    final = item.get('text', final)
                    update(reply=final, progress='Preparing a reply')
                else:
                    label = {'command_execution': 'Running a command', 'file_change': 'Updating files',
                             'web_search': 'Searching the web', 'mcp_tool_call': 'Using a connected tool'}.get(item.get('type'))
                    if label:
                        update(progress=label)
            elif kind == 'turn.completed':
                usage = workspace_usage.measure(event.get('usage', {}), 'codex', time.time())
                update(usage=usage)
            elif kind in {'turn.failed', 'error'}:
                detail = event.get('error', event)
                error = str(detail.get('message', detail) if isinstance(detail, dict) else detail)
        code = process.wait()
    if execution:execution.check()
    if code or error:
        raise ValueError(error or errors.message(f'Codex exited with code {code}. Open Codex to check sign-in or permissions. The request was not resubmitted.'))
    if not final.strip():
        raise ValueError('Codex ended without a reply. Open the saved native chat before retrying.')
    return {'reply': final, 'native_id': thread, 'usage': usage}


def history_turns(thread, native_id):
    """Public native turns when the app owns a transcript Aura cannot open."""
    from workspace_context import message_ref
    messages=[];brief=None;observation={'request_id':'','state':'unknown'}
    for turn in thread.get('turns',[]):
        for item in turn.get('items',[]):
            if item.get('type')=='userMessage':
                role='user';text='\n'.join(p.get('text','') for p in item.get('content',[]) if p.get('type')=='text').replace('\r\n','\n')
                at=turn.get('startedAt')
                if text.lstrip().startswith('<environment_context>') or (text.startswith('# AGENTS.md instructions for ') and '<environment_context>' in text):continue
                reference=message_ref(text);observation={'request_id':reference,'state':'unfinished'}
                if '\nUser request:\n' in text:text=text.split('\nUser request:\n',1)[1]
                if text.startswith('Welcome me to my AURA workspace'):text='Set up my AURA workspace and suggest a useful next step.'
            elif item.get('type')=='agentMessage' and item.get('phase') in {None,'final_answer'}:
                role='assistant';text=item.get('text','');at=turn.get('completedAt');reference=''
                if observation['request_id'] and turn.get('status')=='completed':observation['state']='complete'
            else:continue
            candidate=workspace_chats.brief(text) if role=='assistant' else None
            text=workspace_chats.clean(re.sub(r'(?m)^\s*AURA_SETUP[^\n]*','',text)).strip()
            if text:messages.append({'role':role,'text':text,'at':workspace_usage.timestamp(at),'agent':'Codex',**({'request_id':reference} if reference else {})})
            if candidate:brief=dict(candidate,through=len(messages),at=workspace_usage.timestamp(at))
    if not messages:
        raise ValueError('Codex could not return any messages for this chat. Open the original chat in Codex or restore its transcript from a backup.')
    return {'messages':messages,'model':'','effort':'','usage':{},'native_id':native_id,'native_observation':observation,'chat_brief':brief,
            'title':thread.get('name'),'summary':thread.get('summary'),'summary_updated':thread.get('summaryUpdatedAt'),
            'status':thread.get('status'),'native_workspace':thread.get('cwd',''),'resume':f'codex resume {native_id}'}


def history(command, cwd, native_id, env=None):
    from workspace_delegation import Tracker
    delegation=Tracker(None)
    def read(call):
        thread=call('thread/read',{'threadId':native_id,'includeTurns':False})['thread']
        if not Path(thread.get('path') or '').is_file():
            thread=call('thread/read',{'threadId':native_id,'includeTurns':True})['thread']
        return thread
    thread = rpc(command, read, cwd, env)
    if thread.get('id',native_id)!=native_id:raise ValueError('Codex returned a different chat. Your saved messages have been kept.')
    path = Path(thread.get('path') or '')
    if not path.is_file():
        return history_turns(thread,native_id)
    messages, model, effort, usage, cache_hit, brief = [], '', '', {}, None, None
    observation={'request_id':'','state':'unknown'}
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            try:
                row = json.loads(line)
            except ValueError:
                continue
            payload = row.get('payload', {})
            if row.get('type')=='event_msg' and observation['request_id']:
                if payload.get('type')=='task_complete':observation['state']='complete'
                elif payload.get('type') in {'turn_aborted','task_started'}:observation['state']='unfinished'
            if row.get('type')=='event_msg':delegation.observe('codex',payload,workspace_usage.timestamp(row.get('timestamp')))
            if row.get('type') == 'event_msg' and payload.get('type') == 'token_count':
                info = payload.get('info') or {}
                if info.get('total_token_usage'):
                    usage = workspace_usage.measure(info['total_token_usage'], 'codex', row.get('timestamp'))
                    usage['last'] = workspace_usage.measure(info.get('last_token_usage'), 'codex', row.get('timestamp'))
                    if usage['last'].get('cached_input_tokens',0)>0:
                        cache_hit={'at':usage['last'].get('at'),'tokens':usage['last']['cached_input_tokens']}
                    if cache_hit:usage['cache_hit']=cache_hit
                    window = workspace_usage.number(info.get('model_context_window'))
                    if window and usage['last']:
                        usage['context'] = {'tokens':sum(usage['last'].get(k,0) for k in ('input_tokens','output_tokens')),
                                            'window':window,'est':True}
            if row.get('type') == 'turn_context':
                model, effort = payload.get('model', model), payload.get('effort', effort)
            if row.get('type') != 'response_item' or payload.get('type') != 'message':
                continue
            role = payload.get('role')
            if role not in {'user', 'assistant'} or payload.get('channel') == 'analysis':
                continue
            if role == 'assistant' and payload.get('phase') not in {None, 'final_answer'}:
                continue
            text = '\n'.join(p.get('text', '') for p in payload.get('content', []) if p.get('type') in {'input_text', 'output_text'}).replace('\r\n', '\n')
            if role == 'user' and (text.lstrip().startswith('<environment_context>') or
                                   (text.startswith('# AGENTS.md instructions for ') and '<environment_context>' in text)):
                continue
            from workspace_context import message_ref
            aura_ref=message_ref(text) if role=='user' else ''
            if role=='user':observation={'request_id':aura_ref,'state':'unfinished'}
            elif role=='assistant' and observation['request_id'] and payload.get('phase')=='final_answer':observation['state']='complete'
            if role == 'user' and '\nUser request:\n' in text:
                text = text.split('\nUser request:\n', 1)[1]
                if text.startswith('Welcome me to my AURA workspace'):
                    text = 'Set up my AURA workspace and suggest a useful next step.'
            candidate=workspace_chats.brief(text) if role=='assistant' else None
            text = workspace_chats.clean(re.sub(r'(?m)^\s*AURA_SETUP[^\n]*', '', text)).strip()
            if text:
                messages.append({'role': role, 'text': text, 'at': row.get('timestamp'),**({'request_id':aura_ref} if aura_ref else {}), 'agent': 'Codex', 'model': model, 'effort': effort})
            if candidate:brief=dict(candidate,through=len(messages),at=workspace_usage.timestamp(row.get('timestamp')))
    return {**({'subagents':list(delegation.items.values())} if delegation.items else {}),
            'messages': messages, 'model': model, 'effort': effort, 'usage': usage, 'native_id': native_id,'native_observation':observation,
            'chat_brief':brief,'title':thread.get('name'),'summary':thread.get('summary'),'summary_updated':thread.get('summaryUpdatedAt'),
            'status': thread.get('status'), 'source_file':str(path),'native_workspace':thread.get('cwd',''),'resume': f'codex resume {native_id}'}
