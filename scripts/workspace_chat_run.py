"""One chat request after it starts: live progress from the AI app, then the recorded outcome.

Workspace (workspace_ui) prepares the chat, prompt and execution, then hands them to ChatRun.
Every value the run needs is an explicit attribute instead of a captured local.
"""
import threading

from workspace_ui import (
    SETUP_ERRORS, Stopped, json, re, setup_error, subprocess, time, workspace_activity,
    workspace_agents, workspace_chats, workspace_codex, workspace_delegation, workspace_goals,
    workspace_history, workspace_native_goals, workspace_recovery, workspace_usage,
    workspace_scope)


class ChatRun:
    FIELDS = ('assistant', 'bid', 'chat', 'command', 'effort', 'env', 'execution', 'job', 'keep_warm_id', 'kind', 'model', 'native', 'native_id', 'native_root', 'native_spec', 'nonce', 'prompt', 'proof', 'root', 'text', 'welcome')

    def __init__(self, app, **values):
        missing = set(self.FIELDS) - set(values)
        if missing:
            raise TypeError('ChatRun needs: ' + ', '.join(sorted(missing)))
        self.app = app
        for name in self.FIELDS:
            setattr(self, name, values[name])

    def start(self):
        def scoped():
            with workspace_scope(self.root):
                self.work()
        threading.Thread(target=scoped, daemon=True).start()

    def update(self, **values):
        app=self.app;bid=self.bid;chat=self.chat;execution=self.execution;job=self.job;native_spec=self.native_spec
        with app.lock:
            if 'native_maintenance' in values:
                event=values['native_maintenance'];session=execution.native_session
                if session and event.get('type') in {'cache_warming_start','cache_warming_end'}:
                    session.warming_until=time.monotonic()+60 if event['type']=='cache_warming_start' else 0
                if event.get('type')!='cache_warming_start':
                    workspace_usage.maintenance(app.preferences,bid,chat,event)
                    try:app.save_preferences()
                    except OSError:job['usage_warning']='Native maintenance ran, but its usage report could not be saved.'
                return
            if 'native_diagnostic' in values:
                app.errors.record(ValueError(json.dumps(values.pop('native_diagnostic'))),'native/interaction',app.connections.redact)
            if 'native_output' in values:
                from workspace_native_requests import save_image
                try:
                    media=save_image(values.pop('native_output'),bid)
                    values['native_media']=list({r['path']:r for r in [*job.get('native_media',[]),media]}.values())
                except (OSError,ValueError) as error:
                    values.pop('native_output',None)
                    values['native_notices']=[*job.get('native_notices',[]),{'text':str(error)}][-20:]
            if 'subagents' in values:
                observed={row['id']:{k:app.connections.redact(v) if isinstance(v,str) else v for k,v in row.items()}
                          for row in values['subagents']}
                merged={row['id']:dict(row) for row in job.get('subagents',[])}
                for ident,row in observed.items():merged[ident]={**merged.get(ident,{}),**row}
                values['subagents']=workspace_delegation.retain(merged.values())
                pending_children=any(c.get('status') in {'pending','working','unconfirmed'} for c in values['subagents'])
                if chat.get('recovery',{}).get('background_work',False)!=pending_children:
                    chat['recovery']['background_work']=pending_children
                    try:app.save_preferences()
                    except OSError:job['recovery_warning']='Work is running, but its recovery reference could not be saved.'
            if values.get('native_id') and not job.get('native_id'):
                values.setdefault('progress', 'Connected. Waiting for your AI')
            if 'native_goal' in values and native_spec:
                workspace_native_goals.observe(app,bid,chat,native_spec,values['native_goal'])
            session=execution.native_session
            if session:
                session.touch()
                if 'native_goal' in values:session.goal_active=(values['native_goal'] or {}).get('status')=='active'
                if 'background_processes' in values:session.background=bool(values['background_processes'])
            if 'reply' in values:
                values['reply'] = app.connections.redact(workspace_chats.clean(values['reply'],streaming=True))
            if values.get('native_title') and not chat.get('title_edited'):
                title=app.connections.redact(str(values['native_title'])[:100])
                if chat.get('title')!=title:chat['title']=title;app.save_preferences()
            for key in ('requests','native_notices','native_editor','native_modes','native_config','native_commands'):
                if key in values:values[key]=json.loads(app.connections.redact(json.dumps(values[key])))
            for key in ('native_config','native_commands'):
                if key in values:chat[key]=values[key]
            if 'native_modes' in values or 'native_config' in values:
                info={**job,**values}
                modes=(info.get('native_modes') or {}).get('availableModes')
                selector=next((c for c in info.get('native_config',[]) if c.get('category')=='mode'),None)
                if selector:
                    def flatten_options(rows):
                        for row in rows:
                            if 'options' in row:yield from flatten_options(row['options'])
                            elif 'value' in row:yield {'id':row['value'],'name':row.get('name',row['value']),'description':row.get('description','')}
                    modes=list(flatten_options(selector.get('options',[])))
                if modes:chat['native_permission_modes']=modes
            if 'requests' in values:
                chat['needs_input']=any(r['status']=='pending' for r in values['requests'])
                if job['id'] not in app.jobs:app.jobs[job['id']]=job;app.executions[job['id']]=execution
                if any(r['status']=='pending' for r in values['requests']):values['progress']='Needs your input'
                elif job.get('progress')=='Needs your input' and not execution.stopped.is_set():values['progress']='Continuing your request'
            if values.get('progress') and (not job['activity'] or job['activity'][-1]['text'] != values['progress']):
                job['activity'] = [*job['activity'], {'text':values['progress'], 'at':time.time()}][-12:]
            job.update(values, updated=time.time())
            if 'requests' in values:
                for request in values['requests']:
                    ident='input-'+request['id']
                    item=next((n for n in app.preferences['notification_items'] if n['id']==ident),None)
                    if request['status']=='pending' and not item:
                        app.preferences['notification_items'].append({'id':ident,'business_id':bid,'chat_id':chat['id'],
                            'title':request['title'],'kind':'input','agent':app.agent['name'],'status':'needs_input',
                            'at':time.time(),'read':False,'delivered':False})
                    elif item and request['status']!='pending':item.update(read=True,delivered=True)
            # Plan limits reported during a request (Claude events, Codex notifications).
            if values.get('quota_windows') or values.get('limit_windows'):
                kind=self.kind;provider={'claude':'anthropic','codex':'openai'}.get(kind,kind)
                windows=values.pop('limit_windows',None) or values['quota_windows']
                saved=app.saved_account(chat.get('account_id')) if kind=='claude' and chat and chat.get('account_id') else None
                if saved:
                    # A chat on a saved Claude account: its limits belong to that account, kept as last known.
                    row=workspace_usage.account(provider,'aura:'+saved['id'],saved.get('email') or '',saved.get('plan') or '',app.agent['name'])
                    row.update(label=saved['nickname'],aura_account=saved['id'],windows=windows,checked_at=time.time(),limits_at=time.time())
                    app.usage_accounts[kind+'-events-'+saved['id']]=[row];workspace_usage.remember_accounts(app.preferences,[row])
                else:
                    row=workspace_usage.account(provider,via=app.agent['name'])
                    row.update(windows=windows,checked_at=time.time())
                    app.usage_accounts[kind+'-events']=[row]
            if chat and values.get('native_id'):
                chat['native_id'] = values['native_id']
                try:
                    app.save_preferences()
                except OSError:
                    job['preference_warning'] = 'Your AI is working, but this view could not save its chat reference. Use the native app before retrying.'
            if time.time()-job.get('_activity_at',0)>2 or 'requests' in values:
                try:workspace_activity.record(bid,job,chat);job['_activity_at']=time.time()
                except (OSError,ValueError):job['activity_warning']='Work status could not be saved locally.'

    def work(self):
        app=self.app;assistant=self.assistant;bid=self.bid;chat=self.chat;command=self.command;effort=self.effort;env=self.env;execution=self.execution;job=self.job;keep_warm_id=self.keep_warm_id;kind=self.kind;model=self.model;native=self.native;native_id=self.native_id;native_root=self.native_root;native_spec=self.native_spec;nonce=self.nonce;prompt=self.prompt;proof=self.proof;root=self.root;text=self.text;welcome=self.welcome;update=self.update
        candidate=None;terminal='error'
        try:
            try:
                if not welcome and keep_warm_id is None:job['history_observation']=workspace_history.observe(bid,'Before native work')
            except (OSError,ValueError):job['history_warning']='Local history could not be updated for this request.'
            try:workspace_activity.record(bid,job,chat)
            except (OSError,ValueError):job['activity_warning']='Work status could not be saved locally.'
            if native_spec and native_spec['protocol']=='aura-goal-v1':
                result=workspace_native_goals.custom_run(app.agent['native_goal']['argv'],native_root,env,prompt,native_id,execution,update)
                output=result['reply'];stderr='';code=0
                if result.get('native_id'):update(native_id=result['native_id'])
            elif native:
                resumed_id=native_id
                if chat.get('relocate_session'):
                    update(progress='Reconnecting your saved conversation')
                    continued=workspace_agents.relocate_pi(command,native_root,env,native_id,execution,source_file=chat.get('source_file',''))
                    with app.lock:
                        execution.check()
                        chat.setdefault('native_previous_ids',[]).append(native_id)
                        chat.update(continued);chat.pop('relocate_session',None)
                        app.save_preferences()
                    resumed_id=continued['native_id']
                def launch():
                    return (workspace_codex.run(command,native_root,prompt,resumed_id,model,effort,update,env,execution,
                        **({'child_model':assistant['child_model']} if assistant and assistant.get('child_model') else {})) if kind=='codex' else
                        workspace_agents.run(command,kind,native_root,env,prompt,resumed_id,model,effort,update,execution))
                if kind in {'codex','claude','pi','omp','hermes','antigravity','acp'} and not (kind=='antigravity' and execution.permission=='auto'):
                    settings={'command':command,'cwd':str(native_root),'env':env,'model':model,'effort':effort,'permission':execution.permission,
                              'options':execution.native_options,'handler':execution.native_handler,'goal':native_spec,'child_model':(assistant or {}).get('child_model'),'agent_revision':(assistant or {}).get('native_revision')}
                    result=app.native_sessions.run((str(root),bid,chat['id']),settings,prompt,resumed_id,execution,update,launch,root)
                else:result=launch()
                output, code = result['reply'], 0
                if not welcome and keep_warm_id is None:candidate=workspace_chats.brief(output)
                job['usage'] = result['usage']
            else:
                with execution.popen(command, cwd=root, env=env, stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      text=True, encoding='utf-8', errors='replace') as process:
                    output, stderr = process.communicate(prompt)
                code = process.returncode
            with app.lock:
                execution.check()
                terminal = 'complete' if code == 0 else 'error'
                job['reply'] = app.connections.redact(workspace_chats.clean(output)) if code == 0 else app.connections.redact(
                    (stderr or output)[-5000:].strip() or f'The agent exited with code {code}. Open your AI app to check the failure. Your request was not marked complete.')
                if not job['reply']:
                    job['reply'] = 'The command finished without a text reply. Check the agent and refresh your workspace.'
                if welcome:
                    match = re.search(r'(?m)^\s*AURA_SETUP ' + nonce + r' ([0-9a-fA-F]{64}) ([0-9a-fA-F]{64})\s*$', output)
                    confirmed = bool(code == 0 and match and [v.lower() for v in match.groups()] == proof)
                    job['reply'] = re.sub(r'(?m)^\s*AURA_SETUP[^\n]*', '', job['reply']).strip()
                    job['setup'] = {'reply_received': bool(output.strip()) and code == 0,
                                    'aura_guidance': confirmed, 'business_context': confirmed}
                    if confirmed and job['reply']:
                        app.verified_business = bid
                        view=app._view_owner
                        if view.workspace_path==app.workspace_path:view.verified_business=bid
                        if app.workspace_path in app.workspace_views:app.workspace_views[app.workspace_path]['verified_business']=bid
                        seen = app.preferences.setdefault('seen', [])
                        if bid not in seen:
                            seen.append(bid)
                        try:
                            app.save_preferences()
                        except OSError:
                            job['preference_warning'] = 'Connected, but setup preferences could not be saved on this computer.'
                    elif code == 0:
                        terminal = 'error'
                        job['reply'] = SETUP_ERRORS['proof']
        except Stopped:
            with app.lock:
                terminal='stopped';job.update(progress='Stopped', reply=job.get('reply') or '')
        except Exception as exc:
            with app.lock:
                if execution.stopped.is_set() or execution.interrupt_requested:
                    terminal='stopped';job.update(progress='Stopped')
                else:
                    detail = app.connections.redact(str(exc))
                    terminal='error';job.update(error_detail=detail, error_type=type(exc).__name__, reply=setup_error(detail))
        finally:
            if not execution.native_session:execution.requests.close()
            if hasattr(execution,'release_continuation'):execution.release_continuation()
            if execution.trace:
                try:execution.trace.save();execution.trace=None
                except OSError:job['activity_warning']='Activity details could not be saved. Your work is unaffected.'
            try:
                if not welcome and keep_warm_id is None:job['history_observation']=workspace_history.observe(bid,'Observed after native work')
            except (OSError,ValueError):job['history_warning']='Local history could not be updated for this request.'
            with app.lock:
                job['status']=terminal
                if welcome and job['status'] == 'error':
                    job['reply'] = setup_error(job['reply'])
                    job['setup_error'] = True
                job['updated'] = time.time()
                for child in job.get('subagents',[]):
                    if child.get('status') in {'working','pending'}:
                        child['status']='stopped' if job['status']=='stopped' and kind!='hermes' else 'unconfirmed'
                job['subagents']=workspace_delegation.retain(job.get('subagents',[]))
                if chat:chat['subagents']=job['subagents']
                # A finished request with nothing still running should not keep saying it is busy.
                if job['status']=='complete' and job.get('progress')=='Background work is running' and not job.get('background_processes') \
                        and not any(c.get('status') in {'working','pending'} for c in job['subagents']):
                    job['progress']='Done'
                workspace_usage.record(app.preferences,job,chat,app.agent['name'])
                try:app.check_usage_alerts(bid)
                except (OSError,ValueError):pass
                app.record_notification(job, chat)
                if chat:
                    if job['status']=='complete':
                        chat.pop('model_choice_pending',None)
                        if job.get('aura_context'):chat['aura_context']=job['aura_context']
                    uncertain=kind=='hermes' and job['status']=='stopped'
                    if uncertain:job['stop_note']='The local Hermes connection stopped. Hermes may still be working in its gateway; check its outcome before continuing.'
                    if job['status'] in {'complete','stopped'}:chat.pop('continuation',None)
                    if native_spec and job['status']=='stopped':
                        current_goal=workspace_goals.find(bid,native_spec['id'],include_deleted=True)
                        if not workspace_goals.deleted(current_goal) and current_goal.get('status')=='active':current_goal=workspace_goals.save(bid,{'id':current_goal['id'],'status':'paused'});app.read_cache.clear()
                        workspace_native_goals.control(app,bid,current_goal,'pause')
                    chat.update(status='working' if uncertain else job['status'], updated=job['updated'])
                    workspace_recovery.finish(chat,job)
                    if job.get('goal_id'):
                        chat['work_state']='waiting_for_usage' if job['status']=='error' and setup_error(job.get('error_detail') or job['reply'])==SETUP_ERRORS['limit'] else 'needs_input' if job['status']=='error' else job['status']
                    if job['status']=='error' and not welcome and keep_warm_id is None and setup_error(job.get('error_detail') or job['reply'])==SETUP_ERRORS['limit']:
                        # Follow the user's choice for plan limits (Ask by default) once this request is fully recorded.
                        owner=getattr(app,'_view_owner',app)
                        threading.Thread(target=owner.after_limit,args=(bid,chat['id'],text,'goals' if job.get('goal_id') else 'chats'),daemon=True).start()
                    try:
                        app.save_chat_turn(chat, job, text, final=True, candidate=candidate)
                        app.save_preferences()
                    except OSError:
                        job['preference_warning'] = 'Reply received, but its chat reference could not be saved. Use the native app before retrying.'
                if not chat:
                    try:
                        app.save_preferences()
                    except OSError:
                        job['preference_warning'] = 'Reply received, but its notification could not be saved.'
                try:workspace_activity.record(bid,job,chat)
                except (OSError,ValueError):job['activity_warning']='Work status could not be saved locally.'
