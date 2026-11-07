"""Bounded, display-only observations of native delegation. No agent runtime."""
import copy
import json
import time


def retain(items, completed_limit=50):
    """Keep active observations and their parents, plus recent finished work."""
    rows={row['id']:row for row in items}
    keep={ident for ident,row in rows.items() if row.get('status') in {'working','pending'}}
    pending=list(keep)
    while pending:
        parent=rows[pending.pop()].get('parent_id')
        if parent in rows and parent not in keep:
            keep.add(parent);pending.append(parent)
    recent=sorted((row for ident,row in rows.items() if ident not in keep),key=lambda row:row.get('updated',0))[-completed_limit:]
    keep.update(row['id'] for row in recent)
    return [row for ident,row in rows.items() if ident in keep]


class Tracker:
    def __init__(self, update):
        self.update = update
        self.items = {}
        self.at = None
        self.aliases = {}
        self.observing = False
        self.changed = False

    def publish(self):
        self.items={row['id']:row for row in retain(self.items.values())}
        self.aliases={key:value for key,value in self.aliases.items() if value in self.items}
        self.changed=False
        if self.update:self.update(subagents=copy.deepcopy(list(self.items.values())))

    def put(self, ident, **values):
        if not ident or not isinstance(ident, str) or len(ident) > 300:
            return
        if ident not in self.items:
            self.items[ident] = {'id':ident, 'name':'Subagent', 'status':'working', 'started':self.at or time.time()}
        row = self.items[ident]
        changes={k:str(v)[:4000 if k == 'result' else 1500] for k,v in values.items() if v is not None}
        for key in ('result','task'):
            if key in changes:changes[key+'_truncated']='true' if len(str(values[key]))>len(changes[key]) else 'false'
        if all(row.get(k)==v for k,v in changes.items()) and 'updated' in row:return
        row.update(changes)
        row['updated'] = self.at or time.time()
        self.changed=True
        if not self.observing:self.publish()

    def finish(self, status):
        for row in self.items.values():
            if row['status'] in {'working', 'pending'}:
                # A parent finishing does not establish a child's outcome.
                row['status'] = 'stopped' if status == 'stopped' else 'unconfirmed'
        if self.items and self.update:
            self.update(subagents=copy.deepcopy(list(self.items.values())))

    def omp_jobs(self,ident,details):
        """Observe native async task results and wait snapshots without polling."""
        statuses={'pending':'pending','running':'working','completed':'complete','failed':'error','cancelled':'stopped','aborted':'stopped'}
        progress=details.get('progress') or []
        if progress and ident:
            self.put(ident,name='Delegated work',status='working')
            for index,child in enumerate(progress):
                child_id=ident+':'+str(child.get('index',index))
                if child.get('id'):self.aliases[child['id']]=child_id
                if self.items.get(child_id,{}).get('status') in {'complete','error','stopped'} and child.get('status') in {'pending','running'}:continue
                self.put(child_id,parent_id=ident,name=child.get('agent'),task=child.get('task'),
                         model=child.get('resolvedModelIdentity'),status=statuses.get(child.get('status'),'working'))
        for job in details.get('jobs') or []:
            child_id=self.aliases.get(job.get('id'))
            if not child_id:continue
            self.put(child_id,status=statuses.get(job.get('status'),'unconfirmed'),model=job.get('resolvedModelIdentity'),result=job.get('resultText'))
        for parent in {r.get('parent_id') for r in self.items.values() if r.get('parent_id')}:
            children=[r for r in self.items.values() if r.get('parent_id')==parent]
            if children and all(r['status'] not in {'working','pending'} for r in children):
                self.put(parent,status='error' if any(r['status']=='error' for r in children) else 'complete')

    def observe(self, kind, event, at=None):
        """Return True for child-only frames so they cannot overwrite the parent reply/ID."""
        try:
            self.at=at
            self.observing=True
            return self._observe(kind, event)
        except (TypeError, AttributeError, ValueError, KeyError):
            # Optional display metadata must never break native chat execution.
            return bool(isinstance(event,dict) and event.get('parent_tool_use_id'))
        finally:
            self.observing=False
            if self.changed:self.publish()

    def _observe(self, kind, event):
        event_type = event.get('type', event.get('event', ''))
        item = event.get('item') or {}
        if kind=='codex' and item.get('type')=='subAgentActivity':
            status={'started':'working','completed':'complete','errored':'error','interrupted':'stopped'}.get(item.get('kind'))
            path=item.get('agentPath') or ''
            self.put(item.get('agentThreadId'),name=path.rstrip('/').rsplit('/',1)[-1] or None,model=item.get('model'),status=status)
            return True
        if kind=='codex' and event_type in {'collab_agent_spawn_end','collab_waiting_end','collab_close_end'}:
            def state(value):
                name=next(iter(value),'unconfirmed') if isinstance(value,dict) else value
                status={'pending_init':'pending','running':'working','completed':'complete','errored':'error',
                        'interrupted':'stopped','shutdown':'stopped','not_found':'unconfirmed'}.get(name,'unconfirmed')
                result=value.get(name) if isinstance(value,dict) else None
                return status,result
            if event_type=='collab_agent_spawn_end':
                status,result=state(event.get('status'))
                self.put(event.get('new_thread_id'), name=event.get('new_agent_nickname') or event.get('new_agent_role') or 'Subagent',
                         parent_id=event.get('sender_thread_id'),task=event.get('prompt'),model=event.get('model'),status=status,result=result)
            else:
                statuses=event.get('statuses') or {event.get('receiver_thread_id'):event.get('status')}
                for ident,value in statuses.items():
                    status,result=state(value)
                    self.put(ident,status=status,result=result)
            return True
        if kind == 'codex' and item.get('type') == 'collab_tool_call':
            tool = item.get('tool', '')
            states = item.get('agents_states') or {}
            for ident in dict.fromkeys([*(item.get('receiver_thread_ids') or []), *states]):
                child = states.get(ident) or {}
                status = {'pending_init':'pending', 'running':'working', 'completed':'complete',
                          'errored':'error', 'interrupted':'stopped', 'shutdown':'stopped', 'not_found':'unconfirmed'}.get(child.get('status'))
                self.put(ident, parent_id=item.get('sender_thread_id'),
                         task=item.get('prompt') if tool == 'spawn_agent' else None,
                         status=status, activity=tool.replace('_', ' '), result=child.get('message'))
            return True
        if kind == 'claude':
            parent_tool = event.get('parent_tool_use_id')
            if parent_tool:
                content = (event.get('message') or {}).get('content', [])
                text = '\n'.join(b.get('text', '') for b in content if isinstance(b, dict) and b.get('type') == 'text') if isinstance(content, list) else ''
                self.put(parent_tool, result=text or None, model=(event.get('message') or {}).get('model'),activity='Working')
                return True
            if event_type == 'system' and event.get('subtype') in {'task_started', 'task_progress', 'task_notification'}:
                task_id=event.get('task_id')
                if task_id and event.get('tool_use_id'):self.aliases[task_id]=event['tool_use_id']
                ident = event.get('tool_use_id') or self.aliases.get(task_id,task_id)
                status = {'completed':'complete', 'failed':'error', 'stopped':'stopped'}.get(event.get('status'), 'working')
                self.put(ident, task=event.get('description'), activity=event.get('last_tool_name'),
                         status=status, result=event.get('summary'))
                return True
            if event_type == 'assistant':
                for block in (event.get('message') or {}).get('content', []):
                    if isinstance(block, dict) and block.get('type') == 'tool_use' and block.get('name') in {'Agent', 'Task'}:
                        data = block.get('input') or {}
                        self.put(block.get('id'), name=data.get('description') or data.get('subagent_type') or 'Subagent',
                                 task=data.get('prompt'), requested_model=data.get('model'), activity='Starting',
                                 background='true' if data.get('run_in_background') else None)
            if event_type == 'user':
                for block in (event.get('message') or {}).get('content', []):
                    if isinstance(block, dict) and block.get('tool_use_id') in self.items:
                        content = block.get('content', '')
                        if isinstance(content, list):
                            content = '\n'.join(b.get('text', '') for b in content if isinstance(b, dict))
                        background=self.items[block['tool_use_id']].get('background')=='true' or (event.get('tool_use_result') or {}).get('isAsync')
                        self.put(block['tool_use_id'], status='error' if block.get('is_error') else 'working' if background else 'complete', result=content)
        if kind in {'pi', 'omp', 'hermes'}:
            tool = event.get('toolName') or event.get('name') or event.get('tool')
            ident = event.get('toolCallId') or event.get('tool_call_id') or event.get('tool_use_id') or event.get('id')
            args = event.get('args') or event.get('input') or {}
            if kind=='hermes' and event_type in {'subagent.spawn_requested','subagent.start','subagent.progress','subagent.tool','subagent.complete'}:
                p=event.get('payload') or {}
                ident=p.get('subagent_id') or p.get('child_session_id') or (str(p['delegation_id'])+':'+str(p.get('task_index',0)) if p.get('delegation_id') else None)
                status={'completed':'complete','failed':'error','error':'error','timeout':'error','interrupted':'stopped','running':'working'}.get(p.get('status'),'unconfirmed') if event_type=='subagent.complete' else 'pending' if event_type=='subagent.spawn_requested' else 'working'
                self.put(ident,parent_id=p.get('parent_id'),task=p.get('goal'),model=p.get('model'),status=status,
                         activity=p.get('tool_name'),result=p.get('summary') if event_type=='subagent.complete' else None)
                return True
            if kind=='hermes' and tool=='delegate_task':
                if event_type=='tool_use':
                    tasks=args.get('tasks') or ([{'goal':args['goal']}] if args.get('goal') else [])
                    self.put(ident,name='Delegated work',task=args.get('goal'),activity='Starting')
                    for index,task in enumerate(tasks):
                        self.put(f'{ident}:{index}',parent_id=ident,task=task.get('goal'),status='pending')
                elif event_type=='tool_result' and ident in self.items:
                    output=event.get('output','')
                    try:result=json.loads(output)
                    except (ValueError,TypeError):result={}
                    results=result.get('results') or [] if isinstance(result,dict) else []
                    status='error' if event.get('is_error') else 'complete' if results else 'unconfirmed'
                    self.put(ident,status=status,result=None if results else output)
                    for index,child in enumerate(results):
                        child_status={'completed':'complete','failed':'error','interrupted':'stopped','running':'working'}.get(child.get('status'),'unconfirmed')
                        if child.get('truncated'):child_status='partial'
                        index=child.get('task_index',index)
                        self.put(f'{ident}:{index}',parent_id=ident,model=child.get('model'),status=child_status,
                                 activity='Iteration limit reached' if child.get('truncated') else None,
                                 result=child.get('summary') or child.get('error'))
                return False
            if tool in {'subagent', 'task', 'delegate_task'} and event_type in {'tool_execution_start', 'tool_start', 'tool_use'}:
                self.put(ident, name='Delegated work', task=args.get('task') or args.get('prompt'),
                         requested_model=args.get('model'), activity='Starting')
            result = event.get('result') or event.get('partialResult') or {}
            details = result.get('details') or {} if isinstance(result, dict) else {}
            children = details.get('results') or [] if isinstance(details, dict) else []
            if kind=='omp' and isinstance(details,dict) and (details.get('progress') or details.get('jobs')):
                self.omp_jobs(ident,details)
                return False
            if ident in self.items:
                complete = event_type in {'tool_execution_end', 'tool_end', 'tool_result'}
                if not complete and self.items[ident]['status'] in {'complete','error','stopped'}:return False
                content = result.get('content', []) if isinstance(result, dict) else []
                text = '\n'.join(b.get('text', '') for b in content if isinstance(b, dict) and b.get('type') == 'text')
                self.put(ident, status=('error' if event.get('isError') else 'complete') if complete else 'working',
                         activity='Finished' if complete else 'Working', result=text or None)
                for index, child in enumerate(children):
                    if not isinstance(child, dict):
                        continue
                    failed=child.get('exitCode', 0) or child.get('stopReason') in {'error','aborted'}
                    status = ('error' if failed else 'complete') if complete else 'working'
                    messages=child.get('messages') or []
                    last=next((m for m in reversed(messages) if isinstance(m,dict) and m.get('role')=='assistant'),{})
                    text='\n'.join(b.get('text','') for b in last.get('content',[]) if isinstance(b,dict) and b.get('type')=='text')
                    self.put(f'{ident}:{index}', parent_id=ident, name=child.get('agent') or 'Subagent',
                             task=child.get('task'), model=child.get('model'), status=status,
                             result=child.get('errorMessage') or text or None)
        return False
