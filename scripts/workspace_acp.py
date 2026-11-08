"""ACP v1 native client. Agent tools, policy and authentication stay native."""
import json
import subprocess
from workspace_execution import Stopped
from workspace_interactions import question,answers_for
from workspace_native_requests import form_request,notice,provider


def usage_measure(value):
    from workspace_usage import measure,number
    result=measure(value)
    if number(value.get('used')) is not None:
        result['context']={'tokens':value['used'],**({'window':value['size']} if number(value.get('size')) else {})}
    cost=value.get('cost') or {}
    if isinstance(cost,dict) and cost.get('currency')=='USD' and number(cost.get('amount')) is not None:
        result.update(session_cost_usd=cost['amount'],cost_kind='reported')
    return result


def run(command,kind,cwd,env,prompt,native_id,model,effort,update,execution):
    from workspace_agents import base_command
    from workspace_native_io import channel
    from _process_errors import ErrorTail
    session=execution.native_session;native=native_id;final='';usage={};ready=False;capabilities={};config=[];state={};pending=[];permissions={};applied=set()
    argv=[*base_command(command),'acp'] if kind!='acp' else list(command)
    if kind=='antigravity' and getattr(execution,'native_agent',''):argv+=['--agent',execution.native_agent]
    tools=None
    if execution.native_options.get('client_tools'):
        from workspace_acp_tools import ClientTools
        tools=ClientTools(cwd,env);execution.native_client_tools=tools
    if execution.permission=='full' and kind=='antigravity':argv+=['--dangerously-skip-permissions']
    if execution.permission=='yolo' and kind=='hermes':env={**env,'HERMES_YOLO_MODE':'1'}
    with execution.popen(argv,cwd=cwd,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace') as process:
        errors=ErrorTail(process,env);raw,events,close=channel(process,execution,errors)
        def send(value):raw({'jsonrpc':'2.0',**value})
        def request(ident,method,**params):send({'id':ident,'method':method,'params':params})
        def controls():
            owner=execution
            execution.native_client_tools=tools
            def interrupt():
                if session and (not session.active or session.active.execution is not owner):return
                for ident,reply in list(permissions.items()):
                    reply({'outcome':{'outcome':'cancelled'}});execution.requests.resolve(ident)
                permissions.clear()
                send({'method':'session/cancel','params':{'sessionId':native}})
            execution.interrupt=interrupt
            # ACP v1 serializes prompt turns; do not invent same-turn steering.
            execution.steer=None
            update(native_controls={'steer':False,'interrupt':True})
        def options(rows):
            for row in rows:
                if 'options' in row:yield from options(row['options'])
                elif 'value' in row:yield row
        def configure():
            pending.clear()
            selections=[('model',model),('thought_level',effort)]
            selections.extend(('id:'+ident,value) for ident,value in execution.native_options.get('config',{}).items())
            mode=execution.permission
            launch_override=(kind=='antigravity' and mode=='full') or (kind=='hermes' and mode=='yolo')
            if mode!='native' and not launch_override:
                desired='default' if kind=='antigravity' and mode=='review' else mode
                selections.append(('mode',desired))
            for category,value in selections:
                if not value and not category.startswith('id:'):continue
                if (category,value) in applied:continue
                item=next((r for r in config if r.get('id')==category[3:]),None) if category.startswith('id:') else next((r for r in config if r.get('category')==category),None)
                if item:
                    if value==item.get('currentValue'):continue
                    if value not in {r['value'] for r in options(item.get('options',[]))}:raise ValueError('This native connection does not offer the selected '+category.replace('_',' ')+'. Choose an available option in its settings.')
                    pending.append(('session/set_config_option',{'configId':item['id'],'value':value}))
                elif category=='model':
                    catalog=state.get('models') or {}
                    if value!=catalog.get('currentModelId'):
                        if value not in {r.get('modelId') for r in catalog.get('availableModels',[])}:raise ValueError('This native connection does not offer the selected model. Refresh the model choices.')
                        pending.append(('session/set_model',{'modelId':value}))
                elif category=='mode':
                    modes=state.get('modes') or {}
                    if value!=modes.get('currentModeId'):
                        if value not in {r.get('id') for r in modes.get('availableModes',[])}:raise ValueError('This native connection does not offer that permission mode. Use its default or choose another available mode.')
                        pending.append(('session/set_mode',{'modeId':value}))
                else:raise ValueError('This native connection does not expose that reasoning setting. Use its default setting.')
                applied.add((category,value))
            advance()
        def advance():
            if pending:
                method,params=pending.pop(0);request('aura-config',method,sessionId=native,**params)
            else:
                images=execution.attachments
                if images and not (capabilities.get('promptCapabilities') or {}).get('image'):raise ValueError('This native connection does not accept image messages. Open the file through its native tools or use an image-capable connection.')
                request('aura-prompt','session/prompt',sessionId=native,prompt=[{'type':'text','text':prompt},*images])
        def incoming(event):
            nonlocal config,usage
            ident=event.get('id');method=event.get('method');p=event.get('params') or {}
            if p.get('sessionId') and p['sessionId']!=native:
                if ident is not None:send({'id':ident,'error':{'code':-32602,'message':'This interaction belongs to another conversation.'}})
                return
            def reply(payload):send({'id':ident,'result':payload})
            if method=='session/update':
                value=p.get('update') or {};typ=value.get('sessionUpdate')
                if typ=='config_option_update':config=value.get('configOptions') or [];update(native_config=config)
                elif typ=='available_commands_update':update(native_commands=value.get('availableCommands') or [])
                elif typ=='current_mode_update':
                    state.setdefault('modes',{})['currentModeId']=value.get('currentModeId');update(native_modes=state['modes'])
                elif typ=='session_info_update' and value.get('title'):update(native_title=value['title'])
                elif typ=='notice':notice(execution,update,value.get('message') or value.get('text') or '')
                elif typ=='usage_update':usage=usage_measure(value);update(usage=usage)
            elif method=='session/request_permission':
                offered=p.get('options') or [];tool=p.get('toolCall') or {}
                q=question('decision',tool.get('title') or 'Allow this native operation?',[o['optionId'] for o in offered])
                for option,original in zip(q['options'],offered):option['label']=original.get('name') or original['optionId']
                permissions[ident]=reply
                def answer(values):
                    permissions.pop(ident,None)
                    return {'outcome':{'outcome':'selected','optionId':answers_for([q],values)['decision'][0]}}
                execution.requests.add(ident,'Approval needed',[q],reply,answer,json.dumps(tool,ensure_ascii=False,indent=2))
            elif method=='elicitation/create':
                link=form_request(execution,event,reply)
                if link:notice(execution,update,link['text'],link.get('url'))
            elif method in {'elicitation/cancel','session/cancel_request'}:execution.requests.resolve(p.get('id') or p.get('requestId'))
            elif ident is not None:
                if tools and (method=='fs/read_text_file' or execution.permission in {'native','full','yolo','auto'}) and tools.handle(event,send,execution,update):return
                if not provider(execution,event,send,update):
                    send({'id':ident,'error':{'code':-32601,'message':'This client interaction needs its configured native provider.'}})
                    notice(execution,update,'This step is not available through this connection. Open the chat in your AI app to continue.')
                    update(native_diagnostic={'method':method,'reason':'Native client provider required'})
        init={'protocolVersion':1,'clientCapabilities':{'elicitation':{'form':{},'url':{}},'session':{'notices':{}}},'clientInfo':{'name':'aura-workspace','version':'1'}}
        init.update(execution.native_options.get('initialize',{}))
        if tools:
            init.setdefault('clientCapabilities',{}).update(fs={'readTextFile':True,'writeTextFile':execution.permission in {'native','full','yolo','auto'}},terminal=execution.permission in {'native','full','yolo','auto'})
        request('aura-init','initialize',**init)
        try:
            for event in events:
                method=event.get('method');ident=event.get('id');p=event.get('params') or {};result=event.get('result') or {}
                if method and ident is not None:incoming(event);continue
                if ident in {'aura-init','aura-session','aura-config','aura-prompt'} and 'error' in event:
                    raise ValueError(str((event['error'] or {}).get('message') or 'The native connection could not complete this operation.'))
                if ident=='aura-init':
                    if result.get('protocolVersion')!=1:raise ValueError('This AI app uses a different connection version. Update AURA or use its native app.')
                    capabilities=result.get('agentCapabilities') or {}
                    if native_id and not capabilities.get('loadSession',capabilities.get('load_session')):raise ValueError('This native connection cannot reopen that saved conversation. Open it in its original app.')
                    request('aura-session','session/load' if native_id else 'session/new',cwd=str(cwd),mcpServers=execution.native_options.get('mcpServers',[]),**({'sessionId':native_id} if native_id else {}))
                elif ident=='aura-session':
                    state={**state,**result};native=result.get('sessionId') or native_id
                    if not native or native_id and native!=native_id:raise ValueError('The native app returned a different conversation. No message was sent.')
                    config=result.get('configOptions',config);ready=True;execution.protocol_ready=True
                    update(native_id=native,native_capabilities=capabilities,native_config=config,native_modes=result.get('modes') or {})
                    controls();configure()
                elif ident=='aura-config':
                    if result.get('configOptions') is not None:config=result['configOptions'];update(native_config=config)
                    advance()
                elif method=='session/update' and p.get('sessionId')==native and ready:
                    if getattr(execution,'trace',None):execution.trace.observe('antigravity',event,native)
                    value=p.get('update') or {};typ=value.get('sessionUpdate');content=value.get('content') or {}
                    if typ=='agent_message_chunk' and content.get('type')=='text':final+=content.get('text','');update(reply=final)
                    elif typ in {'tool_call','tool_call_update'}:update(progress=value.get('title') or 'Using a native tool')
                    elif typ=='agent_message_chunk' and content.get('type')=='image':
                        update(native_output=content)
                        if not final:final='Image ready.';update(reply=final)
                    else:incoming(event)
                elif method:incoming(event)
                elif ident=='aura-prompt':
                    if execution.interrupt_requested or result.get('stopReason')=='cancelled':raise Stopped()
                    if not final.strip():raise ValueError('The native app finished without a text reply. Check its conversation before retrying.')
                    output={'reply':final,'native_id':native,'usage':usage}
                    if execution.native_goal:update(native_goal={'status':'needs_review','reason':'The native request ended. This connection does not report a structured goal completion verdict.'})
                    if not session:return output
                    call=session.next(output,events,incoming)
                    execution=call.execution;update=call.update;prompt=call.prompt
                    execution.protocol_ready=True;final='';usage={}
                    update(native_id=native,native_capabilities=capabilities,native_config=config,native_modes=state.get('modes') or {})
                    controls();configure()
            raise ValueError(errors.message('The native connection ended before completing. Check its saved conversation before retrying.'))
        finally:
            if tools:tools.close()
            execution.interrupt=None;execution.steer=None;execution.close_controls();close();execution.requests.close();ErrorTail.close_input(process)
            try:process.wait(timeout=3)
            except subprocess.TimeoutExpired:execution._force_stop();process.wait(timeout=5)
