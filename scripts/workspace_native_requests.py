"""Native decisions and forms. Execution stays with the owning harness/provider."""
import json
import subprocess
import threading
import time
import base64
import mimetypes
from pathlib import Path
from urllib.parse import urlsplit
from workspace_interactions import answers_for,question
from workspace_execution import Stopped


def add(execution,ident,title,questions,send,convert,detail='',timeout=None):
    execution.requests.add(ident,title,questions,send,lambda answers:convert(answers_for(questions,answers)),detail,timeout)


def notice(execution,update,message,url=None,key=None):
    row={'text':str(message or '')[:4000],**({'key':key} if key else {})}
    if url and urlsplit(url).scheme in {'http','https'}:row['url']=url
    with execution.lock:
        previous=[r for r in execution.notices if not key or r.get('key')!=key]
        execution.notices=([*previous,row] if row['text'] or row.get('url') else previous)[-20:]
        rows=list(execution.notices)
    update(native_notices=rows)


def attachments(references,kind):
    """Only explicitly selected, already-authorized local images enter native input."""
    result=[]
    for ref in references:
        if ref.get('kind')!='file' or not ref.get('path'):continue
        path=Path(ref['path']);mime=mimetypes.guess_type(path.name)[0]
        if mime not in {'image/png','image/jpeg','image/webp','image/gif'}:continue
        if kind=='codex':result.append({'type':'localImage','path':str(path)})
        elif kind in {'claude','pi','omp','hermes','antigravity','acp'}:
            if path.stat().st_size>32*1024*1024:raise ValueError('This image is too large for native chat input. Choose a smaller image or reference its folder instead.')
            data=base64.b64encode(path.read_bytes()).decode('ascii')
            result.append({'type':'image','source':{'type':'base64','media_type':mime,'data':data}} if kind=='claude' else {'type':'image','mimeType':mime,'data':data})
    return result


def provider(execution,event,send,update=lambda **v:None):
    """Optional trusted connection command; no imported content defines a handler."""
    config=execution.native_handler or {}
    argv=config.get('argv') if isinstance(config,dict) else None
    if not isinstance(argv,list) or not argv or not all(isinstance(v,str) and v for v in argv):return False
    # Register before returning, so a simultaneous final reply cannot close stdin
    # while this native callback is starting.
    try:
        timeout=config.get('timeout',120)
        if not isinstance(timeout,(int,float)) or timeout<=0:raise ValueError('Choose a positive native provider timeout.')
        with execution.lock:
            execution.check()
            process=subprocess.Popen(argv,cwd=execution.native_cwd,env=execution.native_env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',
                                     **({'creationflags':subprocess.CREATE_NO_WINDOW} if hasattr(subprocess,'CREATE_NO_WINDOW') else {}))
            execution.helpers.add(process)
    except (OSError,ValueError):
        send({'id':event['id'],'error':{'code':-32000,'message':'The configured native provider could not start.'}})
        notice(execution,update,'The native provider could not start. Check its local command and configuration.');return True
    def work():
        try:
            output,_=process.communicate(json.dumps(event,ensure_ascii=False)+'\n',timeout=timeout)
            execution.check()
            value=json.loads(output)
            if process.returncode or not isinstance(value,dict) or not ({'result','error'}&value.keys()):raise ValueError('The native provider did not return a response.')
            send({**value,'id':event['id']})
        except Stopped:pass
        except (OSError,ValueError,subprocess.SubprocessError):
            if not execution.stopped.is_set():
                try:send({'id':event['id'],'error':{'code':-32000,'message':'The configured native provider could not complete this interaction.'}})
                except (OSError,ValueError):pass
                notice(execution,update,'The native provider needs attention. Check its authentication or configuration.')
        finally:
            if process.poll() is None:process.kill();process.wait()
            with execution.lock:execution.helpers.discard(process)
    threading.Thread(target=work,daemon=True).start();return True


def schema_questions(schema):
    fields=[]
    def walk(node,path=()):
        if node.get('properties'):
            for key,value in node.get('properties',{}).items():walk(value,(*path,key))
            return
        ident=json.dumps(path);typ=node.get('type','string');enum=node.get('enum',[])
        if isinstance(typ,list):typ=next((t for t in typ if t!='null'),'string')
        options=[json.dumps(v,ensure_ascii=False) if not isinstance(v,str) else v for v in enum]
        if typ=='boolean' and not options:options=['Yes','No']
        q=question(ident,node.get('title') or ' · '.join(path),options,free=not options)
        secret=bool(node.get('writeOnly') or node.get('format')=='password')
        q.update(required=False,description=node.get('description',''),field_type=typ,secret=secret,default=None if secret else node.get('default'))
        fields.append((path,node,q))
    walk(schema)
    return fields


def form_request(execution,event,send):
    params=event.get('params') or {};ident=event['id'];schema=params.get('requestedSchema') or params.get('schema') or {}
    if params.get('mode')=='url' or params.get('url'):
        url=params.get('url','')
        q=question('action',params.get('message') or 'Complete the native browser step, then continue.',['Continue','Decline','Cancel'])
        q['actions']=True
        add(execution,ident,'Your connected tool needs input',[q],send,lambda a:{'action':{'Continue':'accept','Decline':'decline','Cancel':'cancel'}[a['action'][0]]})
        # A separate link is display data; submitting an answer never follows a URL.
        return {'text':params.get('message') or 'Open the native authorization page.',**({'url':url} if urlsplit(url).scheme in {'http','https'} else {})}
    fields=schema_questions(schema)
    decision=question('action',params.get('message') or 'Your connected tool needs information.',['Submit','Decline','Cancel'])
    decision['actions']=True
    def convert(answers):
        action=answers['action'][0]
        if action!='Submit':return {'action':action.lower()}
        content={}
        for path,node,q in fields:
            values=answers[q['id']]
            if not values:continue
            raw=values[0];typ=q['field_type']
            try:
                value=(raw=='Yes') if typ=='boolean' and not node.get('enum') else json.loads(raw) if typ in {'integer','number','array','object','boolean','null'} else raw
            except ValueError:raise ValueError('Enter a valid '+typ+' for '+q['text']+'.') from None
            if not path:
                if not isinstance(value,dict):raise ValueError('Enter a JSON object for this form.')
                content=value;continue
            target=content
            for key in path[:-1]:target=target.setdefault(key,{})
            target[path[-1]]=value
        from jsonschema import Draft202012Validator
        errors=sorted(Draft202012Validator(schema).iter_errors(content),key=lambda e:str(e.path))
        if errors:
            error=errors[0];field=' · '.join(map(str,error.path)) or 'form'
            messages={'required':'Complete the required fields.','type':'Use the requested value type.','enum':'Choose an available value.',
                      'minimum':'The number is below the allowed minimum.','maximum':'The number is above the allowed maximum.',
                      'minLength':'The answer is too short.','maxLength':'The answer is too long.','pattern':'Use the requested format.'}
            raise ValueError('Check '+field+': '+messages.get(error.validator,'The answer does not match this form’s requirements.'))
        return {'action':'accept','content':content}
    add(execution,ident,'Your connected tool needs input',[decision,*[q for _,_,q in fields]],send,convert)


def codex_request(event,execution,send,update=lambda **v:None):
    ident=event['id'];method=event.get('method','');params=event.get('params') or {}
    reply=lambda payload:send({'id':ident,'result':payload})
    if method=='currentTime/read':reply({'currentTimeAt':int(time.time())});return
    if method in {'item/commandExecution/requestApproval','item/fileChange/requestApproval','execCommandApproval','applyPatchApproval'}:
        legacy=method in {'execCommandApproval','applyPatchApproval'}
        available=params.get('availableDecisions')
        decisions=available if available is not None else (['approved','approved_for_session','denied','abort'] if legacy else ['accept','acceptForSession','decline','cancel'])
        labels={'accept':'Approve once','acceptForSession':'Approve for this session','decline':'Decline','cancel':'Cancel request',
                'approved':'Approve once','approved_for_session':'Approve for this session','denied':'Decline','abort':'Cancel request'}
        offered=[]
        for value in decisions:
            if isinstance(value,str):label=labels.get(value,value)
            elif isinstance(value,dict):
                label='Approve and save this command rule' if 'acceptWithExecpolicyAmendment' in value else 'Apply this network rule' if 'applyNetworkPolicyAmendment' in value else 'Use the proposed native decision'
            else:continue
            offered.append((label,value))
        # Distinct proposed rules must remain independently selectable.
        counts={label:sum(l==label for l,_ in offered) for label,_ in offered}
        offered=[(label+' ('+str(i+1)+')' if counts[label]>1 else label,value) for i,(label,value) in enumerate(offered)]
        q=question('decision',params.get('reason') or 'Allow this native operation?',[label for label,_ in offered])
        detail=json.dumps({k:params[k] for k in ('command','cwd','grantRoot','networkApprovalContext','additionalPermissions','proposedExecpolicyAmendment','availableDecisions') if k in params},ensure_ascii=False,indent=2)
        add(execution,ident,'Approval needed',[q],reply,lambda a:{'decision':next(value for label,value in offered if label==a['decision'][0])},detail)
    elif method in {'item/tool/requestUserInput','tool/requestUserInput'}:
        questions=[]
        for value in params.get('questions',[]):
            q=question(value['id'],value.get('question',''),[o['label'] for o in value.get('options') or []],free=value.get('isOther',False))
            q['secret']=value.get('isSecret',False)
            for option,original in zip(q['options'],value.get('options') or []):option['description']=original.get('description','')
            questions.append(q)
        add(execution,ident,'Your AI has a question',questions,reply,lambda a:{'answers':{k:{'answers':v} for k,v in a.items()}},timeout=params.get('autoResolutionMs'))
    elif method=='item/permissions/requestApproval':
        scopes=params.get('availableScopes') or ['turn','session']
        choices=[('Approve this '+scope,scope) for scope in scopes if scope in {'turn','session'}]+[('Decline',None)]
        q=question('decision',params.get('reason') or 'Grant the requested access?',[label for label,_ in choices]);permissions=params.get('permissions') or {}
        def convert(a):
            scope=next(scope for label,scope in choices if label==a['decision'][0])
            return {'permissions':permissions if scope else {},'scope':scope or 'turn'}
        add(execution,ident,'Permission request',[q],reply,convert,json.dumps(permissions,indent=2))
    elif method=='mcpServer/elicitation/request':
        if params.get('mode','form') not in {'form','url','openai/form','openaiForm'}:
            if provider(execution,event,send,update):return
            notice(execution,update,'This verification step needs your AI app. Open the chat there to continue.')
            update(native_diagnostic={'method':method,'reason':'Native verification provider required'})
            send({'id':ident,'error':{'code':-32601,'message':'A supported native verification provider is required.'}});return
        link=form_request(execution,event,reply)
        if link:notice(execution,update,link['text'],link.get('url'))
    elif provider(execution,event,send,update):pass
    else:
        title={'attestation/generate':'This interaction needs a supported native attestation provider.',
               'account/chatgptAuthTokens/refresh':'This login needs its native credential provider.',
               'item/tool/call':'This tool needs its configured native execution provider.'}.get(method,'This AI app requested an interaction its connection has not registered: '+method)
        notice(execution,update,'This step is not available through this connection. Open the chat in your AI app to continue.')
        update(native_diagnostic={'method':method,'reason':title})
        send({'id':ident,'error':{'code':-32601,'message':title}})


def claude_request(event,execution,send):
    ident=event.get('request_id');request=event.get('request') or {}
    def reply(payload,ident=ident):send({'type':'control_response','response':{'subtype':'success','request_id':ident,'response':payload}})
    if request.get('subtype')!='can_use_tool':
        def bridge(value,ident=ident,reply=reply):
            if 'result' in value:reply(value['result'])
            else:send({'type':'control_response','response':{'subtype':'error','request_id':ident,'error':value.get('error',{}).get('message','The native provider needs attention.')}})
        if provider(execution,{'id':ident,'method':request.get('subtype'),'params':request},bridge):return
        send({'type':'control_response','response':{'subtype':'error','request_id':ident,'error':'Use the native app for this interaction.'}});return
    original=request.get('input') or {}
    if request.get('tool_name')=='AskUserQuestion':
        qs=[question(str(i),q.get('question',''),[o['label'] for o in q.get('options',[])],q.get('multiSelect'),True) for i,q in enumerate(original.get('questions',[]))]
        def convert(a,original=original,qs=qs):return {'behavior':'allow','updatedInput':{**original,'answers':{q.get('question',''):', '.join(a[str(i)]) for i,q in enumerate(original.get('questions',[]))}}}
        add(execution,ident,'Your AI has a question',qs,reply,convert)
    else:
        suggestions=request.get('permission_suggestions') or []
        options=['Approve once',*(['Approve and apply the suggested native rule'] if suggestions else []),'Decline']
        q=question('decision',request.get('description') or 'Allow this tool call?', options)
        add(execution,ident,'Approval needed: '+str(request.get('tool_name','Tool')),[q],reply,
            lambda a,original=original,suggestions=suggestions:{'behavior':'deny','message':'Declined by the user in AURA.'} if a['decision']==['Decline'] else {'behavior':'allow','updatedInput':original,**({'updatedPermissions':suggestions} if a['decision']==['Approve and apply the suggested native rule'] else {})},json.dumps({'input':original,'permission_suggestions':suggestions},ensure_ascii=False,indent=2))


def extension_request(event,execution,send):
    ident=event.get('id');method=event.get('method')
    if method=='cancel':execution.requests.resolve(event.get('targetId'))
    elif method=='ask':
        qs=[question(q['id'],q.get('question',''),[o['label'] for o in q.get('options',[])],q.get('multi'),True) for q in event.get('questions',[])]
        for q,original in zip(qs,event.get('questions',[])):
            for option,source in zip(q['options'],original.get('options',[])):option['description']=source.get('description','')
        def reply(payload,ident=ident):send({'type':'extension_ui_response','id':ident,**payload})
        def convert(a,qs=qs):
            return {'answers':[{'id':q['id'],'selectedOptions':[v for v in a[q['id']] if v in {o['value'] for o in q['options']}],
                **({'customInput':'\n'.join(v for v in a[q['id']] if v not in {o['value'] for o in q['options']})} if any(v not in {o['value'] for o in q['options']} for v in a[q['id']]) else {})} for q in qs]}
        add(execution,ident,event.get('title') or 'Your AI has a question',qs,reply,convert,timeout=event.get('timeout'))
    elif method in {'select','confirm','input','editor'}:
        options=event.get('options',[]) if method=='select' else ['Yes','No'] if method=='confirm' else []
        q=question('answer',event.get('message') or event.get('title',''),options);q.update(secret=bool(event.get('secret')),default=None if event.get('secret') else event.get('prefill'))
        def reply(payload,ident=ident):send({'type':'extension_ui_response','id':ident,**payload})
        def convert(a,method=method):return {'confirmed':a['answer']==['Yes']} if method=='confirm' else {'value':a['answer'][0]}
        add(execution,ident,event.get('title') or 'Your AI has a question',[q],reply,convert,timeout=event.get('timeout'))
    elif method in {'notify','setStatus','setWidget'}:
        text=event.get('message') or event.get('statusText') or '\n'.join(event.get('widgetLines') or [])
        key=method+':'+str(event.get('statusKey') or event.get('widgetKey') or 'default') if method!='notify' else None
        if text or key:return ({'type':'aura_notice','text':text,'key':key,'level':event.get('notifyType','info')})
    elif method=='open_url':return ({'type':'aura_notice','text':event.get('instructions') or 'Open the native sign-in page.', 'url':event.get('launchUrl') or event.get('url')})
    elif method=='set_editor_text':return ({'type':'aura_editor_text','text':event.get('text','')})
    elif method=='setTitle':return ({'type':'aura_native_title','title':event.get('title','')})
    else:return ({'type':'aura_notice','text':'Your AI requested a display this connection cannot show. Open its native app to use that display.'})


def display(event,execution,update):
    typ=event.get('type')
    if typ=='aura_notice':notice(execution,update,event.get('text',''),event.get('url'),event.get('key'))
    elif typ=='aura_editor_text':update(native_editor={'id':event.get('id') or str(time.time_ns()),'text':event.get('text','')})
    elif typ=='aura_native_title':update(native_title=event.get('title',''))
    else:return False
    return True


def save_image(content,bid):
    """Materialize a native inline output once; the normal file viewer serves it."""
    import hashlib
    from _common import workspace_root
    mime=content.get('mimeType');data=content.get('data')
    extensions={'image/png':'.png','image/jpeg':'.jpg','image/webp':'.webp','image/gif':'.gif'}
    if mime not in extensions or not isinstance(data,str) or len(data)>44*1024*1024:raise ValueError('This image cannot be displayed here. Open its saved output in the native app.')
    try:raw=base64.b64decode(data,validate=True)
    except ValueError:raise ValueError('The native app returned an incomplete image.') from None
    valid=(raw.startswith(b'\x89PNG\r\n\x1a\n') if mime=='image/png' else raw.startswith(b'\xff\xd8\xff') if mime=='image/jpeg' else raw.startswith(b'RIFF') and raw[8:12]==b'WEBP' if mime=='image/webp' else raw.startswith((b'GIF87a',b'GIF89a')))
    if not valid or len(raw)>32*1024*1024:raise ValueError('The native app returned an image that cannot be displayed here.')
    base=workspace_root().resolve()/'attachments'/bid
    path=base/'work'/('Image-'+hashlib.sha256(raw).hexdigest()[:16]+extensions[mime])
    if not path.resolve().is_relative_to(base):raise ValueError('The image output folder points outside this business. Choose a regular workspace folder.')
    path.parent.mkdir(parents=True,exist_ok=True)
    try:
        with path.open('xb') as output:output.write(raw)
    except FileExistsError:
        if path.read_bytes()!=raw:raise ValueError('This image could not be saved without replacing a different file.')
    return {'path':path.relative_to(workspace_root()).as_posix(),'name':'Image','mime':mime}
