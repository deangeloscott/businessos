"""Local HTTP surface of the visual workspace: request guard, static files and the JSON API.

Workspace behavior lives in workspace_ui.Workspace; this module only routes requests to it.
`installed_agents` is read through the module so tests and callers can substitute it.
"""
import workspace_ui as ui
from workspace_ui import (BaseHTTPRequestHandler, MAX_BODY, MEDIA, NATIVE_AGENTS, PRODUCT_ROOT, Path,
    SETUP_ERRORS, STATIC, business_directory, copy, files, json, local_file, mimetypes, os, parse_qs,
    private_path, quote, re, records, remember, secrets, selected, setup, setup_error, subprocess, sys,
    threading, time, urlsplit, workspace_activity, workspace_agents, workspace_archive, workspace_catalog,
    workspace_chat_organization, workspace_chats, workspace_codex, workspace_collections, workspace_context,
    workspace_custom_agent, workspace_documents, workspace_exchange, workspace_goals, workspace_guidance,
    workspace_history, workspace_library, workspace_locations, workspace_organization, workspace_permissions,
    workspace_projects, workspace_recovery, workspace_root, workspace_schedules, workspace_scope,
    workspace_sharing, workspace_startup, workspace_storage, workspace_support, workspace_usage)


def handler_for(app):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'AURA-local'

        def log_message(self, *args):
            pass  # No request URLs, prompts or private file paths in access logs.

        def send(self, status, data, content_type='application/json; charset=utf-8', headers=None):
            body = json.dumps(data, ensure_ascii=False).encode() if content_type.startswith('application/json') else data
            if urlsplit(self.path).path.startswith('/api/'):
                app.performance.record(self.command,urlsplit(self.path).path,status,1000*(time.monotonic()-getattr(self,'request_started',time.monotonic())),len(body))
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'nonce-"+app.token+"'; style-src-attr 'unsafe-inline'; worker-src 'self' blob:; font-src 'self' blob: data:; img-src 'self' blob: data:; media-src 'self' blob:; connect-src 'self'; object-src 'none'; frame-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
            for key, value in (headers or {}).items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)

        def failure(self,error,status=400):
            from _process_errors import redact
            route=urlsplit(self.path).path
            operation=route if route.removeprefix('/api/') in workspace_support.ROUTES else '/api/other'
            ident=app.errors.record(error,operation,app.connections.redact)
            self.send(status,{'error':app.connections.redact(redact(workspace_support.human_error(error))),'error_id':ident})

        def stream_file(self,path,download=False):
            # Resolve permission under the short UI lock, stream bytes outside
            # it. Native media controls can seek without buffering the file.
            started=time.monotonic()
            with Path(path).open('rb') as source:
                info=os.fstat(source.fileno());length=info.st_size;start=0;end=length-1;partial=False
                etag=f'"{info.st_mtime_ns:x}-{length:x}"'
                requested=self.headers.get('Range','')
                if requested and self.headers.get('If-Range',etag)==etag:
                    match=re.fullmatch(r'bytes=(\d*)-(\d*)',requested)
                    if not match or not any(match.groups()):
                        self.send(416,{'error':'This byte range is unavailable.'},headers={'Content-Range':f'bytes */{length}'});return
                    first,last=match.groups()
                    if first:start=int(first);end=min(int(last) if last else end,end)
                    else:start=max(0,length-int(last))
                    if not length or start>=length or start>end:
                        self.send(416,{'error':'This byte range is unavailable.'},headers={'Content-Range':f'bytes */{length}'});return
                    partial=True
                mime=(mimetypes.guess_type(path.name)[0] or 'application/octet-stream') if path.suffix.lower() in MEDIA|{'.pdf'} else 'application/octet-stream'
                self.send_response(206 if partial else 200)
                for key,value in {'Content-Type':mime,'Content-Length':str(max(0,end-start+1)),'Accept-Ranges':'bytes','ETag':etag,'Cache-Control':'private, no-cache','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Content-Disposition':('attachment' if download or mime=='application/octet-stream' else 'inline')+"; filename*=UTF-8''"+quote(path.name)}.items():self.send_header(key,value)
                if partial:self.send_header('Content-Range',f'bytes {start}-{end}/{length}')
                self.end_headers()
                if self.command!='HEAD':
                    source.seek(start);remaining=max(0,end-start+1)
                    try:
                        while remaining:
                            block=source.read(min(256*1024,remaining))
                            if not block:break
                            self.wfile.write(block);remaining-=len(block)
                    except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass
            app.performance.record(self.command,'/api/media',206 if partial else 200,1000*(time.monotonic()-started),max(0,end-start+1))

        def do_HEAD(self):
            if urlsplit(self.path).path=='/api/media':self.do_GET()
            else:self.send_response(405);self.end_headers()

        def guard(self):
            expected = f'127.0.0.1:{self.server.server_port}'
            if self.headers.get('Host') != expected:
                raise PermissionError('Open the local address printed by AURA.')
            origin = self.headers.get('Origin')
            if origin and origin != 'http://' + expected:
                raise PermissionError('Requests must come from the local AURA view.')
            media_authorized=False
            if urlsplit(self.path).path=='/api/media':
                from http.cookies import SimpleCookie,CookieError
                try:
                    cookies=SimpleCookie(self.headers.get('Cookie',''));cookie=cookies.get('aura_media_'+str(self.server.server_port))
                    media_authorized=bool(cookie and secrets.compare_digest(cookie.value,app.media_token))
                except CookieError:pass
            if self.path.startswith('/api/') and not media_authorized and not secrets.compare_digest(self.headers.get('X-Aura-Token', ''), app.token):
                raise PermissionError('Refresh the AURA page to reconnect.')
            expected_workspace=self.headers.get('X-Aura-Workspace')
            if self.command=='POST' and expected_workspace and expected_workspace!=str(workspace_root()):
                raise ValueError('The workspace changed in another window. Refresh before making changes.')

        def do_GET(self):
            self.request_started=time.monotonic()
            if urlsplit(self.path).path in {'/api/context','/api/goals','/api/activity','/api/activity/result','/api/history','/api/history/version','/api/archive','/api/permissions','/api/state','/api/file','/api/sharing','/api/chat','/api/chats','/api/notifications'}:
                with app.lock:self.read_GET()
            else:self.read_GET()

        def read_GET(self):
            try:
                self.guard()
                parsed = urlsplit(self.path)
                query = {key: val[0] for key, val in parse_qs(parsed.query).items()}
                route = parsed.path
                if route == '/':
                    page = (app.static / 'index.html').read_text(encoding='utf-8').replace('__AURA_TOKEN__', app.token)
                    self.send(200, page.encode(), 'text/html; charset=utf-8',{'Set-Cookie':f'aura_media_{self.server.server_port}={app.media_token}; HttpOnly; SameSite=Strict; Path=/api/media'})
                elif route in {'/app.js', '/style.css'}:
                    path = app.static / route[1:]
                    self.send(200, path.read_bytes(), 'text/javascript; charset=utf-8' if path.suffix == '.js' else 'text/css; charset=utf-8')
                elif route in {'/file-editor.js','/file-editor.css','/workspace-work.js','/workspace-continuity.js','/workspace-compose.js','/workspace-insight.js','/workspace-projects.js'} or route.startswith('/vendor/'):
                    relative=Path(route.lstrip('/'))
                    path=(STATIC/relative).resolve()
                    base=(STATIC/'vendor').resolve() if route.startswith('/vendor/') else STATIC.resolve()
                    if not path.is_relative_to(base) or private_path(path.relative_to(base)) or not path.is_file():raise ValueError('This interface component is unavailable.')
                    self.send(200,path.read_bytes(),mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
                elif route == '/api/components':
                    self.send(200,workspace_catalog.read_json(PRODUCT_ROOT/'distribution/ui-components.json',{'components':[]}))
                elif route in {'/api/project-resources','/api/project-binding','/api/collections'}:
                    with app.lock:root=app.workspace_path
                    with workspace_scope(root):
                        bid=selected(query.get('business'))
                        if route=='/api/project-resources':result=workspace_projects.resources(app,bid,query.get('id'))
                        elif route=='/api/project-binding':result=workspace_projects.binding(bid,query.get('kind'),query.get('id'))
                        else:result=workspace_collections.show(bid,query['id'],query.get('q',''),query.get('view','current'),query.get('offset',0),query.get('limit',50),item_id=query.get('item',''),history=query.get('history')=='1') if query.get('id') else workspace_collections.inventory(bid,query.get('project',''))
                    self.send(200,result)
                elif route == '/api/memory-feedback':
                    import workspace_memory_feedback
                    self.send(200,workspace_memory_feedback.inventory(selected(query.get('business')),query.get('since',0)))
                elif route == '/api/context/result':
                    bid=selected(query.get('business'))
                    with app.lock:owner=copy.copy(app)
                    self.send(200,workspace_context.saved_result(owner,bid,query.get('chat_id'),query.get('variant',''),query.get('request_id','')))
                elif route == '/api/recall':
                    bid=selected(query.get('business'))
                    with app.lock:owner=copy.copy(app)
                    self.send(200,workspace_context.recall(owner,bid,query.get('q',''),query.get('project',''),query.get('assistant',''),query.get('exclude_chat',''),query.get('limit',20)))
                elif route == '/api/context':
                    self.send(200,workspace_context.inventory(app,selected(query.get('business')),query.get('q',''),query.get('kind',''),query.get('limit',20),query.get('assistant')))
                elif route == '/api/goals':
                    self.send(200,workspace_goals.inventory(app,selected(query.get('business')),query.get('id'),query.get('show','active'),query.get('scope','workspace'),query.get('chat_id'),query.get('kind')))
                elif route == '/api/activity/result':
                    self.send(200,workspace_activity.result(selected(query.get('business')),query.get('chat_id'),query.get('max_chars',6000)))
                elif route == '/api/activity':
                    bid=selected(query.get('business'));result=workspace_activity.inventory(bid,query.get('search',''),query.get('exclude_chat',''),query.get('limit',20),app.running_jobs(workspace_root()))
                    result['running_chats']=[j['chat_id'] for j in app.running_jobs(workspace_root()) if j['business_id']==bid]
                    self.send(200,result)
                elif route == '/api/chat/activity':
                    import workspace_trace
                    bid=selected(query.get('business'));ident=query.get('request','')
                    with app.lock:
                        chat=next((c for c in workspace_chat_organization.items(app,bid) if c['id']==query.get('chat_id')),None)
                        if not chat:raise ValueError('Choose a chat in this workspace.')
                        messages_path=app.chat_display_path(chat['id'])
                        messages=json.loads(messages_path.read_text(encoding='utf-8')) if messages_path.is_file() else []
                        if ident!=chat.get('trace_id') and not any(m.get('request_id')==ident for m in messages):raise ValueError('Choose an activity request from this chat.')
                        execution=app.executions.get(ident);trace=execution.trace if execution else None
                    data=trace.snapshot() if trace else workspace_trace.read(ident)
                    if data.get('business_id',bid)!=bid:raise ValueError('This activity belongs to another business.')
                    self.send(200,workspace_trace.public(data,query.get('item',''),query.get('after','')))
                elif route == '/api/history/version':
                    self.send(200,workspace_history.version(selected(query.get('business')),query.get('id')))
                elif route == '/api/history':
                    bid=selected(query.get('business'))
                    path=app.document_source(bid,query.get('path',''),query.get('option',''))[0] if query.get('path') else None
                    self.send(200,workspace_history.inventory(bid,path))
                elif route == '/api/archive':
                    self.send(200,workspace_archive.inventory(app,selected(query.get('business'))))
                elif route in {'/api/context-settings','/api/delegation-settings'}:
                    self.send(200,app.context_settings(selected(query.get('business')),query.get('kind'),query.get('chat_id'),section='delegation' if route=='/api/delegation-settings' else 'context',profile=query.get('profile')))
                elif route == '/api/native-agents':
                    self.send(200,app.native_agents(selected(query.get('business')),query.get('kind'),query))
                elif route == '/api/permissions':
                    bid=selected(query.get('business'));kind=query.get('kind') or app.connection_kind
                    chat=next((c for c in app.preferences['chats'] if c['id']==query.get('chat_id') and c['business_id']==bid),None)
                    if query.get('chat_id') and not chat:raise ValueError('Choose a chat in this business.')
                    if chat:kind=chat['agent']
                    default=app.preferences.get('harness_permissions',{}).get(kind,'native')
                    job=app.chat_job(bid,chat['id']) if chat else None
                    self.send(200,{**workspace_permissions.describe(kind,chat.get('permission_mode',default) if chat else default,app.permission_modes(kind,chat)),'default':default,'override':chat.get('permission_mode','') if chat else '', 'last_effective':(job or {}).get('permission_effective')})
                elif route == '/api/documents':
                    with app.lock:owner=copy.copy(app)
                    if query.get('workspace') and query['workspace']!=owner.workspace_path:raise ValueError('The workspace changed. Reopen this file.')
                    with workspace_scope(owner.workspace_path):self.send(200,owner.document_info(selected(query.get('business')),query.get('path',''),query.get('option','')))
                elif route == '/api/state':
                    current = app.state(query.get('business'),query.get('revision'))
                    app.update_business = current.get('business_id') or ''
                    self.send(200, current)
                elif route == '/api/profile':
                    self.send(200,app.profile())
                elif route == '/api/support/environment':
                    self.send(200,app.support_environment(query.get('names')=='1'))
                elif route == '/api/diagnostics':
                    self.send(200,app.diagnostics())
                elif route == '/api/notifications':
                    bid = selected(query.get('business'))
                    with app.lock:
                        if query.get('foreground') == '1':
                            app.notification_focus_until = time.time() + 12
                        self.send(200, {**app.notifications(bid),'workspace':str(workspace_root())})
                elif route == '/api/agent-options':
                    self.send(200, app.agent_options(query.get('kind'), query.get('refresh') == '1'))
                elif route == '/api/model-catalog':
                    self.send(200, app.model_catalog(query.get('refresh') == '1', query.get('kind'),query.get('profile')))
                elif route == '/api/agent-efforts':
                    self.send(200, app.agent_efforts(query.get('kind'), query.get('model'),query.get('profile')))
                elif route == '/api/connections':
                    self.send(200, app.connections.rows())
                elif route == '/api/usage':
                    self.send(200,app.usage(selected(query.get('business')),query.get('period','chat'),query.get('refresh')=='1',query.get('offset','0'),query.get('since'),query.get('month_start')))
                elif route == '/api/workspaces':
                    roots = [workspace_root(), *(r['path'] for r in app.recent_workspaces()),
                        workspace_catalog.default_home(), Path.home() / 'Downloads', Path.home() / 'Documents', Path.home() / 'Desktop']
                    discovered = workspace_catalog.discover(roots)
                    for row in discovered['items']:
                        if row['kind']=='workspace':row['organization_destination']=workspace_catalog.organization_destination(row)
                    missing = [workspace_catalog.preview(r['path']) for r in app.recent_workspaces() if not Path(r['path']).is_dir()]
                    self.send(200, {'current':str(workspace_root()), 'recent':app.recent_workspaces(),
                        **discovered, 'items':discovered['items'] + missing, 'default_home':str(workspace_catalog.default_home())})
                elif route == '/api/sharing':
                    bid = selected(query.get('business'))
                    if query.get('workspace') and query['workspace']!=app.workspace_path:raise ValueError('The workspace changed. Reopen sharing from the file.')
                    locations=app.preferences['file_locations'].get(bid, [])
                    selected_path=local_file(bid,query['file'],locations) if query.get('file') else None
                    result = workspace_sharing.public_inventory(workspace_root(), bid, locations, selected_path=selected_path)
                    destinations = []
                    for path in dict.fromkeys([str(workspace_root()), *(r['path'] for r in app.recent_workspaces())]):
                        row = workspace_catalog.preview(path)
                        for item in row['businesses']:
                            if row['path'] != str(workspace_root()) or item['id'] != bid:
                                destinations.append({'path':row['path'], 'business':item['id'], 'name':item['name']})
                    self.send(200, {**result, **workspace_sharing.history(workspace_root(), bid), 'destinations':destinations,
                                    'default_home':str(workspace_catalog.default_home()), 'workspace':str(workspace_root()), 'business':bid})
                elif route == '/api/organization':
                    self.send(200,{'job':app.organization_job,'history':workspace_organization.history(app.settings_file.parent)})
                elif route == '/api/recovery':
                    self.send(200,{'items':workspace_organization.recovery(app.settings_file.parent)})
                elif route in {'/api/assistants','/api/agents'}:
                    with app.lock:self.send(200,app.assistants(selected(query.get('business'))))
                elif route == '/api/chats':
                    bid = selected(query.get('business'))
                    watched=app.chat_job(bid,query.get('chat_id')) if query.get('chat_id') else None
                    events={k:watched.get(k) for k in ('id','chat_id','workspace','business_id','created','status','updated','requests','native_notices','native_editor','native_controls')} if watched else None
                    self.send(200, {'workspace':str(workspace_root()),'items': sorted(({k:v for k,v in c.items() if k not in {'brief_token','subagents'}} for c in app.preferences['chats'] if c['business_id'] == bid),key=workspace_chat_organization.sort_key,reverse=True),
                                    'projects':workspace_chat_organization.projects(app,bid),'active': app.preferences['active_chats'].get(bid), 'native_events':events, 'running': [{k:j.get(k) for k in ('id','chat_id','workspace','business_id','status','agent','model')} for j in app.running_jobs()]})
                elif route == '/api/projects':
                    self.send(200,{'projects':workspace_chat_organization.projects(app,selected(query.get('business')))})
                elif route == '/api/chats/native':
                    self.send(200,app.native_chats(selected(query.get('business')),query.get('kind'),query.get('id')))
                elif route == '/api/chats/changes':
                    self.send(200,app.conversation_changes(selected(query.get('business')),query.get('id')))
                elif route == '/api/chats/detail':
                    result=app.conversation(selected(query.get('business')),query.get('id',''),refresh=True)
                    note='This chat has no saved app session. Showing its saved details.' if not result['chat'].get('native_id') else ''
                    if result.get('history_note'):
                        reason=setup_error(result['history_note'])
                        note='This app could not refresh the chat. Its saved details are still available.' if reason==SETUP_ERRORS['unknown'] else reason
                    self.send(200, {'chat':result['chat'],'history_note':note})
                elif route == '/api/chats/handoff':
                    with app.lock:self.send(200,workspace_context.handoff(app,selected(query.get('business')),query.get('id')))
                elif route == '/api/conversation':
                    self.send(200, app.conversation(selected(query.get('business')),query.get('chat_id'),query.get('refresh')=='1'))
                elif route == '/api/chats/recovery':
                    with app.lock:owner=copy.copy(app);bid=selected(query.get('business'))
                    with workspace_scope(owner.workspace_path):self.send(200,workspace_recovery.check(owner,bid,query.get('id')))
                elif route == '/api/library':
                    result=app.cached_read(('library',),lambda:app.library_items(query.get('discover')=='1'),force=query.get('discover')=='1' or query.get('refresh')=='1')
                    self.send(200, result if query.get('details')=='1' else result['items'])
                elif route == '/api/library/item':
                    item=workspace_library.find(app.library_items()['items'],query.get('key'))
                    if not item:raise ValueError('This item is no longer available. Refresh the library.')
                    variants=item.get('variants') or [item]
                    preferred=max(variants,key=lambda v:max((-1 if s.get('status')=='Disabled' else 10*(s.get('app')==query.get('app'))+({'Reported by app':4,'Installed':3,'Configured':2,'Found locally':1}.get(s.get('status'),0)) for s in v.get('sources',[])),default=0))
                    option=next((v for v in variants if v['key']==query.get('option')),preferred)
                    if query.get('option') and not any(v['key']==query['option'] or query['option'] in v.get('aliases',[]) for v in variants):
                        raise ValueError('That option is no longer available. Refresh the library and choose again.')
                    if query.get('option'):option=next(v for v in variants if v['key']==query['option'] or query['option'] in v.get('aliases',[]))
                    text=workspace_library.document(option) if item['kind']=='Skill' else option.get('guidance','')
                    if item.get('path'):text=(PRODUCT_ROOT/item['path']).read_text(encoding='utf-8')[:100000]
                    location=str((PRODUCT_ROOT/item['path']).resolve()) if item.get('path') else str(PRODUCT_ROOT/'scripts/operating_knowledge.py') if item.get('subtype')=='Playbook' else ''
                    self.send(200, {'item':item,'option':option,'text':text,'location':location})
                elif route == '/api/schedules':
                    self.send(200, workspace_schedules.inventory(workspaces=[workspace_root(),
                        *(row['path'] for row in app.recent_workspaces() if query.get('scope')!='workspace')]))
                elif route == '/api/schedules/operation':
                    self.send(200, {'job':app.schedule_state(selected(query.get('business')))})
                elif route == '/api/schedules/result':
                    result=workspace_schedules.result(query.get('id',''),[workspace_root(),*(row['path'] for row in app.recent_workspaces())],query.get('run_id'))
                    self.send(200,{k:app.connections.redact(v) if isinstance(v,str) else v for k,v in result.items()})
                elif route == '/api/schedules/history':
                    result=workspace_schedules.history(query.get('id',''),[workspace_root(),*(row['path'] for row in app.recent_workspaces())])
                    self.send(200,json.loads(app.connections.redact(json.dumps(result))))
                elif route == '/api/startup':
                    self.send(200, workspace_startup.status())
                elif route == '/api/updates':
                    if query.get('editing') == '1':
                        app.update_editing_until = time.time() + 8
                    update = app.updates.state()
                    if update['can_install'] and workspace_root().resolve().is_relative_to(PRODUCT_ROOT.resolve()):
                        update.update(can_install=False, manual_reason='Move your workspace outside the app folder before updating. Use Add or open a workspace.')
                    self.send(200, update)
                elif route == '/api/connection-check':
                    self.send(200, app.check_connections(selected(query.get('business'))))
                elif route == '/api/files':
                    bid = selected(query.get('business'))
                    self.send(200,app.file_inventory(bid,query))
                elif route == '/api/document':
                    path = (PRODUCT_ROOT / query.get('path', '')).resolve()
                    allowed = any(entry.get('path') and path == (PRODUCT_ROOT / entry['path']).resolve() for entry in app.catalog)
                    if not allowed or path.suffix != '.md' or not path.is_file():
                        raise ValueError('Choose an installed Workflow or recipe.')
                    self.send(200, {'text': path.read_text(encoding='utf-8')[:100000]})
                elif route == '/api/file':
                    bid = selected(query.get('business'))
                    path = local_file(bid, query.get('path', ''), app.preferences['file_locations'].get(bid, []))
                    if path.stat().st_size > 2 * 1024 * 1024:
                        raise ValueError('This file is too large for a text preview. Use its location to open the original.')
                    try:
                        text = path.read_text(encoding='utf-8')
                    except UnicodeDecodeError:
                        raise ValueError('This file has no text preview. Use its location to open the original.')
                    self.send(200, {'text': text})
                elif route == '/api/media':
                    with app.lock:
                        if query.get('workspace') and query['workspace']!=app.workspace_path:raise ValueError('The workspace changed. Reopen this file.')
                        bid=selected(query.get('business'));path=app.document_source(bid,query.get('path',''),query.get('option',''),include_asset=False)[0]
                    self.stream_file(path,query.get('download')=='1')
                elif route == '/api/chat':
                    bid = selected(query.get('business'))
                    with app.lock:
                        job = app.find_job(query.get('id'),bid)
                        self.send(200, dict(job))
                else:
                    self.send(404, {'error': 'Not found.'})
            except PermissionError as exc:
                self.failure(exc,403)
            except Exception as exc:
                self.failure(exc,400 if isinstance(exc,(ValueError,OSError,KeyError)) else 500)

        def do_POST(self):
            self.request_started=time.monotonic()
            try:
                self.guard()
                if self.headers.get_content_type() != 'application/json':
                    raise ValueError('Send JSON from the local view.')
                length = int(self.headers.get('Content-Length', '0'))
                if length <= 0 or length > (6*1024*1024 if urlsplit(self.path).path in {'/api/support/test','/api/support/prepare'} else 45*1024*1024 if urlsplit(self.path).path=='/api/documents/save' else MAX_BODY):
                    raise ValueError('Request is empty or too large.')
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict):
                    raise ValueError('Expected an object.')
                route = urlsplit(self.path).path
                if route == '/api/native-agents':
                    # Native profile creation may seed bundled skills. Keep other chats responsive.
                    with app.lock:
                        if getattr(app,'update_restart',False):raise ValueError('AURA is restarting. Try again when your workspace reopens.')
                        if app.organization_job and app.organization_job['status']=='working':raise ValueError('Wait for workspace organization before changing native agents.')
                        owner=copy.copy(app)
                    with workspace_scope(owner.workspace_path):result=owner.native_agents(selected(data.get('business')),data.get('kind'),data)
                    self.send(200,result);return
                if route in {'/api/documents/save','/api/documents/open'}:
                    with app.lock:
                        expected=data.get('workspace') or self.headers.get('X-Aura-Workspace')
                        if expected!=app.workspace_path:raise ValueError('The workspace changed. Reopen this file before saving.')
                        if app.organization_job and app.organization_job['status']=='working':raise ValueError('Wait for workspace organization before changing files.')
                        owner=copy.copy(app)
                    with workspace_scope(owner.workspace_path):
                        bid=selected(data.get('business'))
                        if route.endswith('/save'):
                            try:result=owner.document_save(bid,data.get('path',''),data)
                            except workspace_documents.Conflict as error:self.send(409,{'error':str(error)});return
                        else:
                            path=owner.document_source(bid,data.get('path',''),data.get('option',''))[0]
                            result=workspace_documents.open_in(path,data.get('application'))
                    self.send(200,result);return
                if route == '/api/context/message':
                    if not isinstance(data.get('digest'),str):raise ValueError('Reopen this message before reusing it.')
                    with app.lock:self.send(200,workspace_context.reusable(app,selected(data.get('business')),data.get('chat_id'),data.get('index'),data['digest']))
                    return
                if route == '/api/chats/recovery':
                    with app.lock:owner=copy.copy(app);bid=selected(data.get('business'))
                    with workspace_scope(owner.workspace_path):
                        action=data.get('action','check')
                        if action=='check':result=workspace_recovery.check(owner,bid,data.get('id'))
                        elif action=='prepare':
                            if not isinstance(data.get('revision'),str) or len(data['revision'])!=64:raise ValueError('Check this chat’s latest work before continuing.')
                            result=workspace_recovery.prepare(owner,bid,data.get('id'),data['revision'],data.get('reviewed') is True)
                        else:raise ValueError('Choose Check or Continue chat.')
                    self.send(200,result);return
                if route in {'/api/project-resources','/api/project-binding','/api/collections'}:
                    # Pin the selected workspace before a slower file mutation;
                    # another window can switch selection without redirecting it.
                    with app.lock:
                        root=app.workspace_path
                        expected=self.headers.get('X-Aura-Workspace')
                        if expected and expected!=root:raise ValueError('The workspace changed. Refresh before saving.')
                    with workspace_scope(root):
                        bid=selected(data.get('business'))
                        if route=='/api/project-resources':result=workspace_projects.change(bid,data)
                        elif route=='/api/project-binding':result=workspace_projects.bind(bid,data.get('kind'),data.get('id'),data.get('project_refs',[]),data.get('collection_id'))
                        else:
                            action=data.get('action')
                            if action=='create':result=workspace_collections.create(bid,data)
                            elif action=='apply':result=workspace_collections.apply(bid,data.get('id'),data)
                            elif action=='configure':result=workspace_collections.configure(bid,data.get('id'),data)
                            elif action=='feedback':result=workspace_collections.feedback(bid,data.get('id'),{**data,'action':data.get('choice')})
                            else:raise ValueError('Choose a collection action.')
                    app.read_cache.clear();self.send(200,result);return
                if route == '/api/memory-feedback':
                    import workspace_memory_feedback
                    self.send(200,workspace_memory_feedback.respond(selected(data.get('business')),data.get('id'),data.get('action')));return
                if route == '/api/context/resolve':
                    with app.lock:self.send(200,workspace_context.resolve(app,selected(data.get('business')),data.get('references'),data.get('goal_id')))
                    return
                if route == '/api/chat/answer':
                    with app.lock:
                        bid=selected(data.get('business'));job=app.find_job(data.get('job_id'),bid)
                        if job.get('chat_id')!=data.get('chat_id'):raise ValueError('This native request is no longer waiting in this chat.')
                        execution=app.executions.get(job['id'])
                    if not execution:raise ValueError('This request expired when AURA restarted. Check the native chat.')
                    if execution.interrupt_requested:raise ValueError('This request is stopping. Wait for it to finish.')
                    self.send(200,execution.requests.answer(data.get('id'),data.get('answers')));return
                if route == '/api/chat/steer':
                    text=data.get('text')
                    if not isinstance(text,str) or not text.strip() or len(text)>1024*1024:raise ValueError('Enter an update of up to 1 million characters, or attach a file for larger text.')
                    with app.lock:
                        bid=selected(data.get('business'));job=app.find_job(data.get('job_id'),bid)
                        if job['status']!='working' or job.get('chat_id')!=data.get('chat_id'):raise ValueError('This request has ended. Send a new message instead.')
                        execution=app.executions.get(job['id'])
                        if not execution or not execution.steer:raise ValueError('This connection cannot receive an update while running. Wait for its reply.')
                        if execution.interrupt_requested:raise ValueError('This request is stopping. Wait for it to finish.')
                        steer=execution.steer
                        chat=next(c for c in app.preferences['chats'] if c['id']==job['chat_id'] and c['business_id']==bid)
                        files=data.get('files') or [];refs=data.get('references') or []
                        if not isinstance(files,list) or any(not isinstance(p,str) for p in files) or not isinstance(refs,list):raise ValueError('Choose valid context references.')
                        context=workspace_context.resolve(app,bid,[*refs,*[{'kind':'file','id':p} for p in files]])
                        from workspace_native_requests import attachments
                        images=attachments(context['references'],execution.native_kind)
                    # Native acknowledgements arrive on the worker thread; do not
                    # hold the workspace lock while waiting for one.
                    steer((context['text']+'\n\n' if context['text'] and not text.lstrip().startswith('/') else '')+text,images)
                    with app.lock:
                        message={'role':'user','text':app.connections.redact(text),'at':time.time(),'request_id':job['id'],'native_update':True,'files':files,'references':json.loads(app.connections.redact(json.dumps(context['references'])))}
                        job.setdefault('messages',[]).append(message)
                        path=app.chat_display_path(chat['id'])
                        shown=json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
                        insert=next((i for i,r in enumerate(shown) if r.get('request_id')==job['id'] and r.get('role')=='assistant'),len(shown))
                        shown.insert(insert,message)
                        from _common import write_json_atomic
                        write_json_atomic(path,shown)
                    self.send(200,{'message':message});return
                if route == '/api/history/restore':
                    with app.lock:
                        bid=selected(data.get('business'))
                        if app.running_jobs(workspace_root()):raise ValueError('Wait for active work before restoring a file.')
                        if app.organization_job and app.organization_job['status']=='working':raise ValueError('Wait for workspace organization before restoring.')
                        result=workspace_history.restore(bid,data.get('id'),data.get('expected_revision'));app.read_cache.clear()
                    self.send(200,result);return
                if route == '/api/chats/import':
                    if data.get('confirmed') is not True:raise ValueError('Review the native chat and destination before adding it.')
                    self.send(200,app.native_chats(selected(data.get('business')),data.get('kind'),data.get('id'),True))
                    return
                if route in {'/api/support/test','/api/support/prepare'}:
                    with app.lock:owner=copy.copy(app)
                    environment=owner.support_environment(data.get('include_names') is True) if data.get('include_environment') is True else None
                    self.send(200,workspace_support.prepare(data,environment,owner.settings_file.parent/'support-drafts',persist=route=='/api/support/test'))
                    return
                if route == '/api/locations/browse':
                    if data.get('kind') not in {'folder', 'file'}:
                        raise ValueError('Choose a file or folder.')
                    self.send(200, {'path': workspace_locations.choose(data['kind'])})
                    return
                with app.lock:
                    for key in list(app.read_cache):
                        if key[0] not in {'records','support-machine'}:app.read_cache.pop(key,None)
                    if getattr(app, 'update_restart', False):
                        raise ValueError('AURA is restarting. Your workspace will reopen in a moment.')
                    if app.organization_job and app.organization_job['status']=='working' and route not in {'/api/organization/stop','/api/notifications','/api/usage/settings','/api/updates'}:
                        raise ValueError('Workspace organization is running. Wait or stop it before making changes.')
                    if app.schedule_job and app.schedule_job['status']=='working' and (route in {'/api/lifecycle','/api/workspaces/open','/api/workspaces/create','/api/workspaces/relocate','/api/workspaces/restore'} or route.startswith('/api/organization/')):
                        raise ValueError('Wait for task setup or stop it before changing workspaces or restarting AURA.')
                    if app.running_jobs(None if route in {'/api/lifecycle','/api/workspaces/relocate','/api/workspaces/restore'} else workspace_root()) and route not in {'/api/goals','/api/chat/answer','/api/archive','/api/permissions','/api/assistants','/api/agents','/api/native-agents','/api/delegation-settings','/api/preferences','/api/profile','/api/interface/reset','/api/chats/recover','/api/chats/archive','/api/chats/reconnect','/api/notifications','/api/chat','/api/chat/stop','/api/chats/new','/api/chats/open','/api/chats/rename','/api/chats/organize','/api/projects','/api/chats/model','/api/chats/personalization','/api/chats/context','/api/connect','/api/workspaces/open','/api/usage/settings','/api/context-settings','/api/updates','/api/schedules/action','/api/schedules/stop'}:
                        raise ValueError('Your agent is working. Wait for its reply before changing this workspace.')
                    if route in {'/api/preferences','/api/locations'}:
                        app.load_portable()
                    if route.startswith('/api/sharing/'):
                        bid = selected(data.get('business'))
                        action = route.rsplit('/', 1)[1]
                        store = app.settings_file.parent
                        if action in {'prepare', 'prepare-public', 'package'}:
                            if action == 'prepare-public':
                                result = workspace_exchange.prepare(workspace_root(),bid,data.get('keys'),data.get('name',''),data.get('note',''),
                                    data.get('kind','starter'),data.get('description',''),data.get('author',''),data.get('based_on',''),store,app.preferences['file_locations'].get(bid,[]))
                            elif action == 'prepare':
                                result = workspace_sharing.prepare(workspace_root(), bid, data.get('keys'), data.get('name',''), data.get('note',''), store,
                                                                   app.preferences['file_locations'].get(bid, []))
                            else:
                                result = workspace_exchange.import_package(data.get('path',''), store)
                                try:
                                    workspace_sharing.remember_package(workspace_root(), bid, data['path'])
                                except (OSError, ValueError):
                                    result['catalog_note'] = 'The package was read, but its recent location could not be remembered.'
                            workspace_catalog.write_json(workspace_sharing._job(result['id'], store) / 'ui-scope.json', {'workspace':str(workspace_root()), 'business':bid})
                        elif action == 'file-key':
                            original = local_file(bid, str(data.get('ref','')), app.preferences['file_locations'].get(bid, []))
                            inventory = workspace_sharing.public_inventory(workspace_root(),bid,app.preferences['file_locations'].get(bid, []),selected_path=original)
                            result = {'key':inventory['selected_key']}
                        elif action == 'selection':
                            result = workspace_sharing.save_selection(workspace_root(), bid, data.get('name',''), data.get('keys'), data.get('note',''), data.get('selection_id',''), app.preferences['file_locations'].get(bid, []))
                        elif action == 'discover':
                            result = workspace_sharing.discover_packages(workspace_root(), bid, app.preferences['file_locations'].get(bid, []), data.get('path') or None)
                        elif action == 'destination':
                            row = workspace_catalog.preview(data.get('path',''))
                            if row['kind'] != 'workspace':
                                raise ValueError('Choose a saved workspace, or select A new workspace to start one.')
                            result = {'path':row['path'], 'businesses':row['businesses']}
                        elif action == 'detail':
                            result = workspace_sharing.imported_detail(workspace_root(), bid, data.get('receipt'))
                        elif action == 'undo':
                            result = workspace_sharing.undo(workspace_root(), bid, data.get('receipt'), data.get('apply') is True)
                        else:
                            scope = workspace_catalog.read_json(workspace_sharing._job(data.get('id'), store) / 'ui-scope.json', {})
                            if scope != {'workspace':str(workspace_root()), 'business':bid}:
                                raise ValueError('Prepare this sharing review in the currently selected workspace.')
                            if action == 'select':
                                result=workspace_sharing.select_package(data['id'],data.get('keys'),store)
                                workspace_catalog.write_json(workspace_sharing._job(result['id'],store)/'ui-scope.json',scope)
                            elif action == 'review':
                                result = workspace_sharing.review(data['id'], data.get('path',''), data.get('target_business',''), data.get('new_name',''), store)
                                if result['destination'] == str(workspace_root()) and result['business'] == bid and (workspace_sharing._job(data['id'], store) / 'source.json').exists():
                                    raise ValueError('Choose a different business or workspace to receive the copy.')
                            elif action == 'apply':
                                result = workspace_sharing.apply(data['id'], data.get('include_updates') is True, store)
                            elif action == 'export':
                                result = workspace_sharing.export_package(data['id'], data.get('path',''), store)
                            else:
                                raise ValueError('Choose a supported sharing action.')
                        self.send(200, result)
                    elif route == '/api/updates':
                        if data.get('action') in {'install', 'rollback'} and workspace_root().resolve().is_relative_to(PRODUCT_ROOT.resolve()):
                            raise ValueError('Move your workspace outside the app folder before updating. Use Add or open a workspace.')
                        self.send(200, app.updates.action(data.get('action'), data.get('policy')))
                    elif route == '/api/usage/settings':
                        bid=selected(data.get('business'))
                        value=data.get('budget_usd')
                        blank=value is None or value==''
                        if not blank and (isinstance(value,bool) or not isinstance(value,(str,int,float))):
                            raise ValueError('Enter a monthly budget, or leave it blank.')
                        budget=None if blank else workspace_usage.number(float(value))
                        if not blank and (budget is None or budget<=0 or budget>1000000000):
                            raise ValueError('Enter a monthly budget above zero, or leave it blank.')
                        app.preferences.setdefault('usage_settings',{})[bid]={'alerts':data.get('alerts') is True,'budget_usd':budget}
                        app.save_preferences()
                        self.send(200,{'saved':True})
                    elif route == '/api/usage/link':
                        selected(data.get('business'))
                        workspace_usage.link_account(app.preferences,[a for group in app.usage_accounts.values() for a in group],data.get('source'),data.get('target'))
                        app.save_preferences()
                        self.send(200,{'saved':True})
                    elif route == '/api/usage/keep-warm':
                        bid=selected(data.get('business'))
                        if not isinstance(data.get('chat_id'),str) or not data['chat_id']:
                            raise ValueError('Choose a supported chat to refresh its cache.')
                        self.send(202,app.start_chat(bid,None,None,keep_warm_id=data['chat_id']))
                    elif route == '/api/organization/folder':
                        path=workspace_organization.folder(data['path'])
                        row=workspace_catalog.preview(path)
                        if row['kind'] not in {'workspace','unrecognized'}:raise ValueError('Choose a saved workspace or a folder of useful project files.')
                        if row['kind']=='workspace':row['organization_destination']=workspace_catalog.organization_destination(row)
                        self.send(200,row)
                    elif route == '/api/organization/plan':
                        self.send(202,app.organize('plan',data))
                    elif route == '/api/organization/apply':
                        self.send(202,app.organize('apply',data))
                    elif route == '/api/organization/stop':
                        if app.organization_job and app.organization_job['status']=='working':app.organization_cancel.set()
                        self.send(200,{'ok':True})
                    elif route == '/api/organization/cleanup-preview':
                        self.send(200,workspace_organization.retirement_review(data['id'],app.settings_file.parent,app.organization_references()))
                    elif route == '/api/organization/retire':
                        self.send(200,workspace_organization.retire(data['id'],data['path'],int(data.get('days',0)),app.settings_file.parent,app.organization_references()))
                    elif route == '/api/organization/discard':
                        self.send(200,workspace_organization.discard(data['id'],app.settings_file.parent))
                    elif route == '/api/archive':
                        bid=selected(data.get('business'))
                        self.send(200,workspace_archive.change(app,bid,data.get('kind'),data.get('id'),data.get('action','restore')))
                    elif route == '/api/recovery/update':
                        self.send(200,workspace_organization.recover(data['id'],data['action'],app.settings_file.parent,
                            int(data['days']) if 'days' in data else None,app.organization_references()))
                    elif route == '/api/lifecycle':
                        if data.get('action') not in {'quit', 'restart'}:
                            raise ValueError('Choose Restart AURA or Quit AURA.')
                        business = selected(data['business']) if data['action'] == 'restart' and data.get('business') else ''
                        app.restart_business = business
                        app.restart_requested = data['action'] == 'restart'
                        app.close_reason = data['action']
                        self.send(200, {'status':data['action']})
                        threading.Thread(target=self.server.shutdown, daemon=True).start()
                    elif route == '/api/setup':
                        name = str(data.get('name', '')).strip()
                        if not name or len(name) > 160:
                            raise ValueError('Enter a business name of up to 160 characters.')
                        result = setup(organization=name)
                        if result['status'] != 'ready':
                            raise ValueError('Setup needs attention. Ask your agent to run AURA doctor.')
                        app.remember_workspace()
                        app.save_preferences(portable=True)
                        self.send(200, result)
                    elif route == '/api/workspaces/preview':
                        result = workspace_catalog.candidates(str(data.get('path','')))
                        for row in result['items']:
                            if row['kind'] == 'workspace':
                                plan = workspace_storage.backup_plan(row['path'])
                                row.update(files=plan['files'], bytes=plan['bytes'])
                        self.send(200,result)
                    elif route == '/api/workspaces/create':
                        name = str(data.get('name','')).strip()
                        if not name or len(name) > 160:
                            raise ValueError('Enter a workspace name of up to 160 characters.')
                        from setup import _stable_business_id
                        parent = Path(str(data.get('parent') or workspace_catalog.default_home())).expanduser().resolve()
                        target = parent / _stable_business_id(name)
                        if target.is_relative_to(PRODUCT_ROOT):
                            raise ValueError('Choose a folder outside the AURA application for new workspaces.')
                        if target.exists() and any(target.iterdir()):
                            raise ValueError('That workspace folder already exists. Open it or choose a different name.')
                        env = dict(os.environ, BUSINESSOS_WORKSPACE=str(target), BUSINESSOS_WORKSPACE_CONFIG=str(target / '.businessos/workspace.json'))
                        flags = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
                        subprocess.run([sys.executable,str(PRODUCT_ROOT / 'scripts/setup.py'),'--organization',name,'--no-link','--json'],
                            env=env,check=True,capture_output=True,timeout=90,**flags)
                        self.send(200,app.open_workspace(str(target)))
                    elif route == '/api/workspaces/open':
                        opened = app.open_workspace(str(data.get('path','')),preserve_local=bool(data.get('replace') and Path(data['replace']).resolve()==Path(app.workspace_path).resolve()))
                        if data.get('replace'):
                            recent = [r for r in app.recent_workspaces() if r['path']!=data['replace']]
                            workspace_catalog.write_json(app.settings_file.parent / 'recent-workspaces.json',recent)
                        self.send(200,opened)
                    elif route == '/api/workspaces/relocate':
                        app.save_preferences()
                        copied = workspace_storage.relocate(workspace_root(),str(data.get('path','')))
                        self.send(200,{**app.open_workspace(copied['path'],preserve_local=True), **copied})
                    elif route == '/api/workspaces/backup-preview':
                        app.save_preferences()
                        plan = workspace_storage.backup_plan(workspace_root(),data.get('include_linked') is True)
                        self.send(200,{k:plan[k] for k in ('files','bytes','links','excluded')})
                    elif route == '/api/workspaces/backup':
                        app.save_preferences()
                        self.send(200, workspace_storage.backup(workspace_root(), str(data.get('path','')),data.get('include_linked') is True))
                    elif route == '/api/workspaces/restore':
                        self.send(200, workspace_storage.restore(str(data.get('archive','')), str(data.get('path',''))))
                    elif route == '/api/connections/session-only':
                        app.connections.session_only = True
                        self.send(200, {'ok':True})
                    elif route == '/api/save':
                        bid = selected(data.get('business'))
                        kind = data.get('kind')
                        name = str(data.get('name', '')).strip()
                        description = str(data.get('description') or '').strip() if 'description' in data else None
                        if (name or kind != 'business' or description is None) and (not name or len(name) > 2000):
                            raise ValueError('Enter a name of up to 2,000 characters.')
                        if description is not None and len(description) > 2000:
                            raise ValueError('Keep the description under 2,000 characters.')
                        rows, _ = records(bid)
                        if kind == 'business':
                            obj = next(row for row in rows if row['type'] == 'Business')
                            content = {'name': name} if name else {}
                            if description:content['description'] = description
                            item = {'object_ref': obj['ref'], 'content': content}
                            if description == '' and obj['data'].get('description'):item['remove_fields'] = ['description']
                            if not content and 'remove_fields' not in item:
                                self.send(200, {'status': 'unchanged'});return
                        elif kind == 'goal':
                            result=workspace_goals.mutate(app,bid,{'action':'save','id':data.get('ref'),'name':name})
                            self.send(200,{**result,'objects':[{'id':result['goal']['id'],'object_type':'Objective'}]});return
                        else:
                            raise ValueError('Unsupported edit. Use your agent for this change.')
                        self.send(200, remember(bid, {'objects': [item]}))
                    elif route == '/api/custom-agent':
                        if app.launch_agent:raise ValueError('This view was opened with an agent file. Change that file instead.')
                        if data.get('remove'):
                            workspace_custom_agent.remove();agent=None
                            app.preferences['connected_apps'].pop('configured',None)
                            if app.connection_kind=='configured':app.agent,app.connection_kind=None,''
                        else:
                            agent=workspace_custom_agent.save(data.get('name'),data.get('command'))
                            app.preferences['connected_apps'].setdefault('configured',{'kind':'configured','model':'','effort':''})
                        app.configured_agent=agent
                        for view in app.workspace_views.values():view['configured_agent']=agent
                        app.save_preferences()
                        self.send(200,{'status':'removed' if agent is None else 'saved','name':(agent or {}).get('name','')})
                    elif route == '/api/connect':
                        model, effort, attachment, chosen = '', '', None, None
                        if app.native_kind(data.get('kind')) in NATIVE_AGENTS:
                            options = app.agent_options(data['kind'])
                            model = data.get('model')
                            chosen = next((m for m in options['models'] if m['id'] == model), None)
                            effort = data.get('effort') or ''
                            if chosen:
                                app.agent_efforts(data['kind'], model)
                            # An empty effort keeps the app's own default; Codex needs an explicit level.
                            app_default = effort == '' and app.native_kind(data['kind']) != 'codex'
                            if not chosen or (chosen['efforts'] and effort not in chosen['efforts'] and not app_default) or (not chosen['efforts'] and effort):
                                raise ValueError('Choose an available model and its supported effort level.')
                        if data.get('kind') == 'configured' and app.configured_agent:
                            app.agent = app.configured_agent
                            app.connection_kind = 'configured'
                            app.handoff = False
                            app.verified_business = None
                        elif data.get('kind') == 'handoff':
                            app.agent = None
                            app.connection_kind = ''
                            app.handoff = True
                            app.verified_business = None
                        else:
                            choice = next((a for a in ui.installed_agents() if a['id'] == data.get('kind') and a['argv']), None)
                            if not choice:
                                raise ValueError('This app needs a one-time command connection. Copy the setup instructions to your AI app.')
                            app.select_agent(choice, data.get('workspace_write', True) is True)
                        if app.connection_kind == 'codex':
                            attachment = workspace_codex.attach(PRODUCT_ROOT, workspace_root())
                            attachment = workspace_codex.verify_attachment(app.agent['argv'], workspace_root(), attachment)
                        elif app.connection_kind in NATIVE_AGENTS:
                            attachment = workspace_guidance.attach(app.connection_kind, PRODUCT_ROOT, workspace_root())
                        app.preferences['connection'] = {'kind': 'handoff' if app.handoff else app.connection_kind,
                                                         'workspace_write': data.get('workspace_write', True) is True,
                                                         'model': model, 'model_name': (chosen or {}).get('name', '') if model else '',
                                                         'effort': effort, 'attachment': attachment}
                        if app.connection_kind in NATIVE_AGENTS | {'configured'} and not app.handoff:
                            app.preferences['connected_apps'][app.connection_kind] = dict(app.preferences['connection'])
                        app.save_preferences()
                        self.send(200, app.connection())
                    elif route == '/api/connections/save':
                        app.connections.save(data.get('provider'), data.get('key'), data.get('storage', 'session'),
                                             str(data.get('name', '')), str(data.get('env', '')), data.get('category', 'tools'))
                        app.option_cache.clear()
                        self.send(200, app.connections.rows())
                    elif route == '/api/connections/remove':
                        app.connections.remove(data.get('provider'))
                        app.option_cache.clear()
                        self.send(200, app.connections.rows())
                    elif route == '/api/startup':
                        if not isinstance(data.get('enabled'), bool):
                            raise ValueError('Choose whether AURA should start when you sign in.')
                        self.send(200, workspace_startup.configure(data['enabled'], PRODUCT_ROOT,
                            workspace_root(), selected(data.get('business')) if data.get('business') else '',
                            getattr(app, 'launch_extra', ())))
                    elif route == '/api/schedules/action':
                        self.send(202, app.schedule_action(selected(data.get('business')),data))
                    elif route == '/api/schedules/stop':
                        bid=selected(data.get('business'))
                        job=app.schedule_job
                        if not job or job['business_id']!=bid or job['id']!=data.get('operation_id'):
                            raise ValueError('This task setup is no longer running in this workspace.')
                        if job['status']=='working':
                            app.schedule_execution.stop()
                            job['message']='Stopping task setup…'
                        self.send(200,{'job':app.schedule_state(bid)})
                    elif route == '/api/schedules/update':
                        choice = app.native_choice('hermes')
                        command = workspace_agents.base_command(choice['argv']) if choice else None
                        if 'model' in data:
                            model = str(data['model'])
                            if model:
                                if not any(m['id'] == model for m in app.agent_options('hermes')['models']):
                                    raise ValueError('Choose a model reported by Hermes, or refresh its model choices.')
                                parts = model.split(':', 2 if model.startswith('custom:') else 1)
                                if len(parts) < 2:
                                    raise ValueError('Hermes did not identify the provider for this model.')
                                data['provider'], data['model'] = ':'.join(parts[:-1]), parts[-1]
                            else:
                                data['provider'] = ''
                        result = workspace_schedules.update(data.get('id'), data, command, app.agent_environment(choice))
                        self.send(200, {'task':result})
                    elif route == '/api/files/reconnect':
                        bid = selected(data.get('business'))
                        asset = next((r for r in records(bid,include_archived=True)[0] if r['type']=='Asset' and r['ref']==data.get('ref')),None)
                        if not asset:
                            raise ValueError('That saved file is no longer available.')
                        path = workspace_locations.validate(str(data.get('path','')),workspace_root(),business_directory(),bid,private_path)
                        value = path.relative_to(workspace_root()).as_posix() if path.is_relative_to(workspace_root()) else str(path)
                        remember(bid,{'objects':[{'object_ref':asset['ref'],'content':{'location_reference':value}}]})
                        self.send(200,{'ok':True})
                    elif route == '/api/locations':
                        bid = selected(data.get('business'))
                        items = app.preferences['file_locations'].setdefault(bid, [])
                        if data.get('remove'):
                            app.preferences['file_locations'][bid] = [i for i in items if i['id'] != data['remove']]
                        else:
                            path = workspace_locations.validate(str(data.get('path', '')), workspace_root(), business_directory(), bid, private_path)
                            if data.get('replace'):
                                item = next((i for i in items if i['id']==data['replace']),None)
                                if not item:
                                    raise ValueError('This linked location is no longer available.')
                                if (item['kind']=='folder') != path.is_dir():
                                    raise ValueError('Choose the same kind of file or folder as the original link.')
                                old_path = Path(item['path'])
                                updates = []
                                for asset in records(bid)[0]:
                                    value = asset['data'].get('location_reference') if asset['type']=='Asset' else None
                                    if not isinstance(value,str):continue
                                    try:relative = Path(value).relative_to(old_path)
                                    except ValueError:continue
                                    replacement = path / relative if item['kind']=='folder' else path
                                    if not replacement.exists():continue
                                    reference = replacement.relative_to(workspace_root()).as_posix() if replacement.is_relative_to(workspace_root()) else str(replacement)
                                    updates.append({'object_ref':asset['ref'],'content':{'location_reference':reference}})
                                if updates:remember(bid,{'objects':updates})
                                item['path'] = str(path)
                            elif not any(Path(i['path']) == path for i in items):
                                if len(items) >= 20:
                                    raise ValueError('You can link up to 20 files or folders per business.')
                                items.append({'id':secrets.token_hex(8), 'path':str(path), 'name':str(data.get('name') or path.name)[:100],
                                              'kind':'folder' if path.is_dir() else 'file'})
                        app.save_preferences(portable=True)
                        self.send(200, {'ok':True})
                    elif route == '/api/notifications':
                        bid = selected(data.get('business'))
                        items = [n for n in app.preferences['notification_items'] if n['business_id'] == bid]
                        action = data.get('action')
                        claimed = []
                        if action == 'read':
                            for item in items:
                                if data.get('all') is True or item['id'] == data.get('id'):
                                    item['read'] = True
                        elif action == 'claim':
                            now = time.time()
                            # Batch close arrivals, avoid replaying stale alerts, and
                            # share delivery ownership across tabs under this lock.
                            if (app.preferences.get('notifications') is True and
                                    now >= app.notification_focus_until and
                                    now - app.preferences.get('notification_sent_at', 0) >= 30):
                                claimed = [n for n in items if not n['read'] and not n['delivered'] and now - n['at'] < 120]
                                if claimed:
                                    for item in claimed:
                                        item['delivered'] = True
                                    app.preferences['notification_sent_at'] = now
                        else:
                            raise ValueError('Choose a notification action.')
                        if action == 'read' or claimed:
                            app.save_preferences()
                        self.send(200, {**app.notifications(bid), 'claimed': claimed})
                    elif route == '/api/interface/reset':
                        app.static=STATIC
                        extra=list(getattr(app,'launch_extra',[]))
                        if '--interface-dir' in extra:
                            n=extra.index('--interface-dir');del extra[n:n+2]
                        app.launch_extra=extra
                        self.send(200,{'ok':True})
                    elif route == '/api/profile':
                        self.send(200,app.profile(data))
                    elif route == '/api/chats/recover':
                        bid=selected(data.get('business'))
                        # Legacy clients explicitly confirm that they checked the
                        # native chat. Still protect any surviving exact process.
                        chat=next((c for c in app.preferences['chats'] if c['id']==data.get('id') and c['business_id']==bid),None)
                        if not chat:raise ValueError('Choose a chat in this workspace.')
                        if any(j.get('chat_id')==chat['id'] for j in app.running_jobs(workspace_root())) or workspace_recovery.process_state(chat.get('recovery') or {})=='running':raise ValueError('This request is still running. Check it before continuing.')
                        chat['status']='stopped';chat.pop('continuation',None)
                        if chat.get('recovery'):chat['recovery']['status']='reviewed'
                        app.save_preferences();self.send(200,{'ok':True})
                    elif route == '/api/preferences':
                        if 'native_idle_timeout_seconds' in data:
                            seconds=data['native_idle_timeout_seconds']
                            if workspace_usage.number(seconds) is None or seconds>86400:raise ValueError('Use an idle timeout from 0 to 86,400 seconds. Zero keeps settled connections open.')
                            app.preferences['native_idle_timeout_seconds']=seconds
                        if 'library' in data:
                            bid=selected(data.get('business'))
                            prefs=data['library']
                            if not isinstance(prefs,dict):raise ValueError('Choose items from the library.')
                            clean={}
                            for field,limit in [('favorites',500),('recent',24)]:
                                values=prefs.get(field,[])
                                if not isinstance(values,list) or len(values)>limit or any(not isinstance(v,str) or len(v)>2005 or not re.fullmatch(r'(?:workflow|recipe|skill|tool|plugin|file):[^\r\n\x00]+',v) for v in values):
                                    raise ValueError('Choose items from the library.')
                                clean[field]=list(dict.fromkeys(values))
                            app.preferences['library'][bid]=clean
                        if 'preferred_app' in data:
                            if data['preferred_app'] not in NATIVE_AGENTS | {'configured'}:
                                raise ValueError('Choose a supported AI app.')
                            app.preferences['preferred_app'] = data['preferred_app']
                        if 'model_picker' in data:
                            picker = data['model_picker']
                            if not isinstance(picker, dict) or picker.get('kind') not in NATIVE_AGENTS | {'all','configured'} or picker.get('view') not in {'favorites', 'all'}:
                                raise ValueError('Choose Favorites or All models for a supported AI app.')
                            for field, limit in (('favorites', 2000), ('providers', 200)):
                                values = picker.get(field)
                                if not isinstance(values, list) or len(values) > limit or any(not isinstance(v, str) or not v or len(v) > 300 for v in values):
                                    raise ValueError('Choose models and providers from the picker.')
                            self_picker = {field: list(dict.fromkeys(picker[field])) for field in ('favorites', 'providers')}
                            self_picker['view'] = picker['view']
                            efforts = picker.get('efforts', app.preferences['model_picker'].get(picker['kind'], {}).get('efforts', {}))
                            if (not isinstance(efforts, dict) or len(efforts) > 2000 or
                                    any(not isinstance(key, str) or not key or len(key) > 300 or
                                        not isinstance(value, str) or len(value) > 64 for key, value in efforts.items())):
                                raise ValueError('Choose an effort level for each model from its available settings.')
                            self_picker['efforts'] = efforts
                            app.preferences['model_picker'][picker['kind']] = self_picker
                        if 'notifications' in data:
                            app.preferences['notifications'] = data['notifications'] is True
                            # Enabling alerts must not announce old activity.
                            for item in app.preferences['notification_items']:
                                item['delivered'] = True
                        if 'appearance' in data:
                            if data['appearance'] not in {'system', 'light', 'dark'}:
                                raise ValueError('Choose System, Light, or Dark.')
                            app.preferences['appearance'] = data['appearance']
                        if data.get('dismiss_setup'):
                            bid = selected(data.get('business'))
                            seen = app.preferences.setdefault('seen', [])
                            if bid not in seen:
                                seen.append(bid)
                        app.save_preferences(portable=any(k in data for k in ('appearance','model_picker','library')))
                        self.send(200, {'ok': True})
                    elif route == '/api/goals':
                        self.send(200,workspace_goals.mutate(app,selected(data.get('business')),data))
                    elif route in {'/api/context-settings','/api/delegation-settings'}:
                        self.send(200,app.context_settings(selected(data.get('business')),data.get('kind'),data.get('chat_id'),data.get('changes'),data.get('revision'),section='delegation' if route=='/api/delegation-settings' else 'context',profile=data.get('profile')))
                    elif route == '/api/permissions':
                        bid=selected(data.get('business'));kind=data.get('kind') or app.connection_kind
                        chat=next((c for c in app.preferences['chats'] if c['id']==data.get('chat_id') and c['business_id']==bid),None)
                        if data.get('chat_id') and not chat:raise ValueError('Choose a chat in this business.')
                        if chat:kind=chat['agent']
                        mode=data.get('mode')
                        if chat and mode=='inherit':chat.pop('permission_mode',None)
                        else:
                            workspace_permissions.validate(kind,mode,app.permission_modes(kind,chat))
                            if chat:chat['permission_mode']=mode
                            else:app.preferences.setdefault('harness_permissions',{})[kind]=mode
                        app.save_preferences();self.send(200,{'saved':True,'applies':'Next request; running native requests keep their permissions.'})
                    elif route in {'/api/assistants','/api/agents'}:
                        self.send(200,app.assistants(selected(data.get('business')),data))
                    elif route == '/api/chats/personalization':
                        self.send(200,app.personalization_chat(selected(data.get('business')),data.get('connection')))
                    elif route == '/api/chats/context':
                        self.send(200,app.workspace_chat(selected(data.get('business')),'context',data.get('connection')))
                    elif route == '/api/chats/new':
                        bid = selected(data.get('business'))
                        app.preferences['active_chats'][bid] = None
                        app.save_preferences()
                        self.send(200, {'ok': True})
                    elif route == '/api/chats/organize':
                        self.send(200,workspace_chat_organization.mutate(app,selected(data.get('business')),data))
                    elif route == '/api/projects':
                        self.send(200,workspace_chat_organization.change_project(app,selected(data.get('business')),data))
                    elif route == '/api/chats/rename':
                        bid=selected(data.get('business'))
                        chat=next((c for c in app.preferences['chats'] if c['id']==data.get('id') and c['business_id']==bid),None)
                        if not chat:raise ValueError('This chat does not belong to the selected business.')
                        title=workspace_chats.short(data.get('title'),80)
                        if not title:raise ValueError('Enter a chat title.')
                        chat.update(title=app.connections.redact(title),title_edited=True)
                        app.save_preferences()
                        self.send(200,{'chat':chat})
                    elif route == '/api/chats/reconnect':
                        self.send(200,app.reconnect_chat(selected(data.get('business')),data.get('id')))
                    elif route == '/api/chats/archive':
                        self.send(200,app.archive_chat(selected(data.get('business')),data.get('id'),data.get('archived',True)))
                    elif route == '/api/chats/model':
                        bid=selected(data.get('business'))
                        chat=next((c for c in app.preferences['chats'] if c['id']==data.get('id') and c['business_id']==bid),None)
                        if not chat:raise ValueError('Choose a chat in this workspace.')
                        if data.get('kind',chat['agent'])!=chat['agent']:raise ValueError('An existing chat stays in its original AI app. Start a new chat to use another app.')
                        if any(j.get('chat_id')==chat['id'] for j in app.running_jobs(workspace_root())) or chat.get('status')=='working':raise ValueError('Wait for this request to finish before changing its model.')
                        if app.native_kind(chat['agent']) not in NATIVE_AGENTS:raise ValueError('This connection uses its own model settings.')
                        profile_options={'profile':chat['native_profile']} if app.native_kind(chat['agent'])=='hermes' and chat.get('native_profile') else {}
                        options=app.agent_options(chat['agent'],**profile_options)
                        model=next((m for m in options['models'] if m['id']==data.get('model')),None)
                        if not model:raise ValueError('Choose an available model for this AI app.')
                        effort=data.get('effort','')
                        efforts=app.agent_efforts(chat['agent'],model['id'],**profile_options).get('efforts',model.get('efforts',[]))
                        if effort and effort not in efforts:raise ValueError('Choose a supported effort for this model.')
                        if chat['agent']=='codex' and not effort:raise ValueError('Choose an effort for this Codex model.')
                        if 'native_settings' in data:
                            from workspace_native_settings import selections
                            native_settings=selections(chat.get('native_config',[]),data['native_settings'])
                            chat['native_settings']=native_settings
                        workspace_usage.invalidate(app.preferences,chat['id'])
                        chat.update(model=model['id'],effort=effort,connection={**chat.get('connection',{}),'kind':chat['agent'],'model':model['id'],'effort':effort},model_choice_pending=True)
                        app.save_preferences();self.send(200,{'chat':chat})
                    elif route == '/api/chats/open':
                        bid = selected(data.get('business'))
                        chat = next((c for c in app.preferences['chats'] if c['id'] == data.get('id') and c['business_id'] == bid), None)
                        if not chat:
                            raise ValueError('This chat does not belong to the selected business.')
                        choice = ({'id':'configured',**app.configured_agent} if chat['agent']=='configured' and app.configured_agent else next((a for a in ui.installed_agents() if a['id'] == chat['agent'] and a['argv']), None))
                        if choice:app.select_agent(choice, app.preferences.get('connection', {}).get('workspace_write') is True)
                        app.preferences['connection'].update(chat.get('connection',{}))
                        app.preferences['connection'].update(kind=chat['agent'], model=chat['model'], effort=chat['effort'])
                        if chat['agent'] != 'codex':
                            app.preferences['connection']['attachment'] = None
                        app.preferences['active_chats'][bid] = chat['id']
                        app.save_preferences()
                        self.send(200, app.conversation(bid))
                    elif route == '/api/request':
                        bid = selected(data.get('business'))
                        context=workspace_context.resolve(app,bid,[*(data.get('references') or []),*[{'kind':'file','id':f} for f in data.get('files') or []]],data.get('goal_id'))
                        text=app.request_text(bid,str(data.get('text','')),data.get('history'),data.get('schedule_id'),data.get('organization_id'))
                        self.send(200,{'text':text.replace('\nUser request:\n',context['text']+'\nUser request:\n',1),'references':context['references']})
                    elif route == '/api/chat/stop':
                        self.send(200, app.stop_chat(selected(data.get('business')), data.get('id')))
                    elif route == '/api/chat':
                        bid = selected(data.get('business'))
                        self.send(202, app.start_chat(bid, data.get('text'), data.get('history'), data.get('welcome') is True, data.get('schedule_id'),data.get('organization_id'),chat_id=data.get('chat_id'),files=data.get('files'),connection=data.get('connection'),assistant_id=data.get('assistant_id'),references=data.get('references'),goal_id=data.get('goal_id'),permission_mode=data.get('permission_mode'),project=data.get('project')))
                    else:
                        self.send(404, {'error': 'Not found.'})
            except PermissionError as exc:
                self.failure(exc,403)
            except Exception as exc:
                self.failure(exc,400 if isinstance(exc,(ValueError,OSError,KeyError,StopIteration)) else 500)
    return Handler
