"""Existing business goals with scoped work links and bounded native continuation intent."""
from _common import organization_transaction
from pathlib import Path
import argparse
import hashlib
import json
import re
import time

from _common import workspace_root,workspace_scope,resolve_business,read_json_input


def metadata(goal):
    value=goal.get('extensions') or {}
    for key in ('businessos','goal'):
        if not isinstance(value,dict):return {}
        value=value.get(key,{})
    return value if isinstance(value,dict) else {}


def scope(goal):return 'chat' if metadata(goal).get('scope')=='chat' else 'workspace'


def deleted(goal):return bool(metadata(goal).get('deleted_at'))


def available(goal):return not deleted(goal) and goal.get('status','active')=='active'


def discoverable(obj):
    """Ordinary organization context uses active shared goals, never another chat's effort."""
    from workspace_lifecycle import archived
    return not archived(obj) and (obj.get('object_type')!='Objective' or available(obj) and scope(obj)=='workspace')


def extensions(goal,info):
    value=json.loads(json.dumps(goal.get('extensions') or {}))
    if not isinstance(value.get('businessos',{}),dict):raise ValueError('This goal’s saved metadata needs attention before editing.')
    value.setdefault('businessos',{})['goal']=info
    return value


def related(bid,goal):
    """At most one effort and its explicitly selected workspace outcome."""
    result=[goal];parent=metadata(goal).get('workspace_goal_ref')
    if scope(goal)=='chat' and parent:
        try:item=find(bid,parent)
        except ValueError:return result
        if scope(item)=='workspace':result.append(item)
    return result


def check_chat(bid,ident,chat_id):
    goal=find(bid,ident);owner=metadata(goal).get('chat_id')
    if scope(goal)=='chat' and owner and owner!=chat_id:
        raise ValueError('This goal belongs to another chat. Choose a workspace goal or create a goal for this chat.')
    return goal


@organization_transaction
def bind_chat(bid,ident,chat_id):
    from remember import remember
    goal=check_chat(bid,ident,chat_id)
    if scope(goal)=='chat' and not metadata(goal).get('chat_id'):
        info={**metadata(goal),'chat_id':chat_id}
        remember(bid,{'objects':[{'object_ref':ident,'content':{'extensions':extensions(goal,info)},'replace_extensions':True}]})
    return find(bid,ident)


@organization_transaction
def remove(bid,ident,restore=False):
    from remember import remember
    goal=find(bid,ident,include_deleted=True);info=dict(metadata(goal))
    if restore:
        if not deleted(goal):return goal
        status=info.pop('deleted_status',goal.get('status','active'));info.pop('deleted_at',None)
    else:
        if deleted(goal):return goal
        info.update(deleted_at=time.time(),deleted_status=goal.get('status','active'));status='paused'
    info['revision']=time.time_ns()
    remember(bid,{'objects':[{'object_ref':ident,'content':{'status':status,'extensions':extensions(goal,info)},'replace_extensions':True}]})
    return find(bid,ident,include_deleted=True)


def changed(app,bid,ident,remove_links=False):
    affected={ident,*[g['id'] for g in goals(bid,include_deleted=True) if metadata(g).get('workspace_goal_ref')==ident]}
    for chat in app.preferences['chats']:
        if chat['business_id']!=bid or chat.get('goal_id') not in affected:continue
        history=chat.setdefault('goal_history',[])
        for value in (chat.get('goal_id'),ident):
            if value and value not in history:history.append(value)
        chat.pop('continuation',None)
        if remove_links and chat.get('goal_id')==ident:chat['goal_id']=''


def goals(bid,include_deleted=False):
    if resolve_business(bid)['status']!='resolved':raise ValueError('Choose an existing business.')
    from workspace_ui import records
    return [row['data'] for row in records(bid)[0] if row['type']=='Objective' and (include_deleted or not deleted(row['data']))]


def find(bid,ident,include_deleted=False):
    if resolve_business(bid)['status']!='resolved' or not isinstance(ident,str) or not re.fullmatch(r'obj_[A-Za-z0-9_-]+',ident):raise ValueError('Choose an existing goal in this business.')
    from canonical_store import canonical_path
    from workspace_sharing import unlinked
    path=unlinked(canonical_path(bid,{'object_type':'Objective','id':ident}))
    try:goal=json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:raise ValueError('This goal is no longer available in the selected business.') from None
    if goal.get('id')!=ident or goal.get('business_id')!=bid or goal.get('object_type')!='Objective':raise ValueError('This goal does not belong to the selected business.')
    if deleted(goal) and not include_deleted:raise ValueError('This goal was deleted. Restore it from Deleted goals or choose another goal.')
    return goal


def fingerprint(goal):
    value={k:goal.get(k) for k in ('name','target','horizon','status')}
    info=metadata(goal)
    if info:value['scope']={k:info[k] for k in ('scope','workspace_goal_ref','deleted_at','revision') if k in info}
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()


def continuation_basis(bid,goal):
    items=related(bid,goal)
    return fingerprint(goal) if len(items)==1 else hashlib.sha256(json.dumps([fingerprint(g) for g in items]).encode()).hexdigest()


def guidance(goal):
    return ('Goal context: '+json.dumps({k:goal[k] for k in ('id','name','target','horizon','status') if k in goal},ensure_ascii=False)+
        '\nThis is a '+scope(goal)+' goal. Follow the user’s latest assignment; this goal never overrides newer instructions. A finished reply does not complete the goal. '
        'Preserve meaningful artifacts, decisions and a concise next step at natural stopping points, without repeated summary calls. '
        'When preserving a relevant Asset, its extensions.businessos.goal_ref can link it to this goal. '
        'Use normal memory helpers; do not save a full conversation or private reasoning as goal history. '
        'If this is a continuation, first check what already succeeded and avoid duplicating external actions. '
        'A paused/completed goal is context for this deliberate user request, not authorization for unattended continuation.')


@organization_transaction
def save(bid,data):
    from remember import remember
    ident=data.get('id');old=find(bid,ident) if ident else None
    content={}
    info=dict(metadata(old or {}));chosen=data.get('scope',scope(old or {}))
    if chosen not in {'chat','workspace'}:raise ValueError('Choose a chat goal or workspace goal.')
    if old and scope(old)=='workspace' and chosen=='chat':raise ValueError('Create a separate chat goal instead of moving a shared workspace goal.')
    if not old or 'scope' in data:info['scope']=chosen
    if chosen=='chat':
        owner=data.get('chat_id',info.get('chat_id',''))
        if not isinstance(owner,str) or owner and not re.fullmatch(r'[A-Za-z0-9_-]{1,100}',owner):raise ValueError('Choose a valid chat for this goal.')
        if info.get('chat_id') and owner!=info['chat_id']:raise ValueError('A chat goal keeps its original chat.')
        if owner:info['chat_id']=owner
        if 'workspace_goal_id' in data:
            parent=data['workspace_goal_id']
            if parent:
                if not isinstance(parent,str) or parent==ident or (parent!=info.get('workspace_goal_ref') and scope(find(bid,parent))!='workspace'):raise ValueError('Choose a workspace goal to connect.')
                info['workspace_goal_ref']=parent
            else:info.pop('workspace_goal_ref',None)
    else:
        if data.get('workspace_goal_id'):raise ValueError('Workspace goals cannot be nested.')
        info.pop('chat_id',None);info.pop('workspace_goal_ref',None)
    if info!=metadata(old or {}):content['extensions']=extensions(old or {},info)
    for key,limit in [('name',2000),('horizon',300),('status',20)]:
        if key in data:
            value=data[key]
            if key=='horizon' and isinstance(value,str) and not value.strip():continue
            if not isinstance(value,str) or not value.strip() or len(value)>limit:raise ValueError('Enter a valid goal '+key+'.')
            content[key]=value.strip()
    if 'status' in content and content['status'] not in {'active','paused','completed'}:raise ValueError('Choose Active, Paused or Completed.')
    if not old and not content.get('name'):raise ValueError('Give this goal a name.')
    if 'target' in data:
        if not isinstance(data['target'],str) or len(data['target'])>5000:raise ValueError('Keep the goal outcome within 5,000 characters.')
        if data['target'].strip():content['target']=data['target'].strip()
    remove=[k for k in ('target','horizon') if k in data and not str(data[k]).strip() and old and k in old]
    content={k:v for k,v in content.items() if k not in remove}
    if not content and not remove:raise ValueError('Choose a goal change to save.')
    if old and not remove and all(old.get(k)==v for k,v in content.items()):return old
    info['revision']=time.time_ns();content['extensions']=extensions(old or {},info)
    item={'object_ref':ident} if old else {'object_type':'Objective'}
    result=remember(bid,{'objects':[{**item,'content':content,**({'replace_extensions':True} if old and 'extensions' in content else {}),**({'remove_fields':remove} if remove else {})}]})
    return find(bid,result['objects'][0]['id'])


def link_chat(preferences,bid,chat_id,goal_id):
    chat=next((c for c in preferences['chats'] if c['id']==chat_id and c['business_id']==bid and c.get('workspace',str(workspace_root()))==str(workspace_root())),None)
    if not chat:raise ValueError('Choose a chat in this workspace and business.')
    if goal_id:remember_link(bid,chat,bind_chat(bid,goal_id,chat_id))
    chat['goal_id']=goal_id or ''
    # A new assignment needs its own deliberate continuation authorization.
    chat.pop('continuation',None)
    return chat


def remember_link(bid,chat,goal):
    history=chat.setdefault('goal_history',[])
    for item in related(bid,goal):
        if item['id'] not in history:history.append(item['id'])


@organization_transaction
def link_asset(bid,asset_id,goal_id):
    from remember import remember
    from workspace_ui import records
    if goal_id:find(bid,goal_id)
    asset=next((r['data'] for r in records(bid)[0] if r['ref']==asset_id and r['type']=='Asset'),None)
    if not asset:raise ValueError('Choose a saved file in this business.')
    extensions=json.loads(json.dumps(asset.get('extensions') or {}));bos=extensions.setdefault('businessos',{})
    if goal_id:bos['goal_ref']=goal_id
    else:bos.pop('goal_ref',None)
    return remember(bid,{'objects':[{'object_ref':asset_id,'content':{'extensions':extensions},'replace_extensions':True}]})


def set_continuation(preferences,bid,chat_id,mode='manual',until=None):
    chat=next((c for c in preferences['chats'] if c['id']==chat_id and c['business_id']==bid and c.get('workspace',str(workspace_root()))==str(workspace_root())),None)
    if not chat or not chat.get('goal_id'):raise ValueError('Choose a goal for this chat first.')
    goal=find(bid,chat['goal_id'])
    if mode=='native' and metadata(goal).get('workspace_goal_ref'):find(bid,metadata(goal)['workspace_goal_ref'])
    if mode=='native' and any(not available(g) for g in related(bid,goal)):raise ValueError('Activate the chat goal and connected workspace goal before authorizing automatic continuation.')
    policy=continuation(chat['agent'],mode,until);policy['goal_basis']=continuation_basis(bid,goal)
    chat['continuation']=policy
    return policy


def select_goals(items,show='active',scope_filter='workspace',chat_id=None):
    if show not in {'active','current','completed','deleted','all'} or scope_filter not in {'workspace','chat','all'}:raise ValueError('Choose an available goal view.')
    def matches(goal):
        if scope_filter!='all' and scope(goal)!=scope_filter:return False
        if chat_id and (scope(goal)!='chat' or metadata(goal).get('chat_id')!=chat_id):return False
        if show=='deleted':return deleted(goal)
        if deleted(goal):return False
        if show=='active':return available(goal)
        if show=='completed':return goal.get('status','active')=='completed'
        return show=='all' or goal.get('status','active')!='completed'
    return [g for g in items if matches(g)]


def inventory(app,bid,ident=None,show='active',scope_filter='workspace',chat_id=None,connection_kind=None):
    from workspace_ui import records
    rows=app.cached_read(('context-records',bid),lambda:records(bid)[0],seconds=3)
    all_items=[r['data'] for r in rows if r['type']=='Objective'];selected=find(bid,ident,include_deleted=True) if ident else None
    if chat_id and not any(c['id']==chat_id and c['business_id']==bid and c.get('workspace',app.workspace_path)==app.workspace_path for c in app.preferences['chats']):raise ValueError('Choose a chat in this workspace and business.')
    chat=next((c for c in app.preferences['chats'] if c['id']==chat_id and c['business_id']==bid),None) if chat_id else None
    history=set((chat or {}).get('goal_history',[]))|{(chat or {}).get('goal_id')}
    choices=[g for g in all_items if not chat_id or metadata(g).get('chat_id')==chat_id or g['id'] in history]
    items=select_goals(choices,show,scope_filter)
    linked_ids={ident,*[g['id'] for g in all_items if selected and metadata(g).get('workspace_goal_ref')==ident]}
    owners={metadata(g).get('chat_id') for g in all_items if selected and g['id'] in linked_ids}
    chats=[{k:c[k] for k in ('id','title','agent','summary','status','updated','goal_id','work_state','continuation') if k in c} for c in app.preferences['chats']
           if c['business_id']==bid and c.get('workspace',app.workspace_path)==app.workspace_path and
              (c.get('goal_id') or c.get('goal_history') or c['id'] in owners) and (not ident or c.get('goal_id')==ident or ident in c.get('goal_history',[]) or c['id'] in owners)]
    links=app.preferences.get('goal_tasks',{}).get(bid,{})
    chats.sort(key=lambda c:c.get('updated',0),reverse=True)
    assets=[]
    for row in rows:
        obj=row['data']
        owner=(obj.get('extensions') or {}).get('businessos',{}).get('goal_ref')
        if ident and row['type']=='Asset' and owner in linked_ids:assets.append({'id':obj['id'],'name':obj.get('business_role') or obj['id'],'path':obj.get('location_reference',''),'goal_id':owner})
    deleted_items=select_goals(choices,'deleted',scope_filter) if show=='all' else []
    owner=next((c for c in app.preferences['chats'] if selected and c['id']==metadata(selected).get('chat_id') and c['business_id']==bid and Path(c.get('workspace') or app.workspace_path).resolve()==Path(app.workspace_path).resolve()),None)
    native_support=None
    if selected and scope(selected)=='chat':
        from workspace_native_goals import support
        from workspace_ui import installed_agents
        kind=owner['agent'] if owner else connection_kind or app.connection_kind
        agent=app.native_choice(kind) or {}
        if (owner or {}).get('native_settings'):agent={**agent,'native_options':{**agent.get('native_options',{}),'config':owner['native_settings']}}
        permission=(owner or {}).get('permission_mode') or app.preferences.get('harness_permissions',{}).get(kind,'native')
        native_support=support(app.native_kind(kind),agent,permission)
        if not agent.get('argv'):native_support={**native_support,'supported':False,'reason':'Connect this chat’s AI app before starting native goal mode.'}

    return {'items':items,'deleted_items':deleted_items,'goal':selected,'scope':scope(selected) if selected else None,'deleted':deleted(selected) if selected else False,
            'workspace_goal':next(iter(related(bid,selected)[1:]),None) if selected else None,
            'chat_goals':[g for g in all_items if selected and scope(selected)=='workspace' and scope(g)=='chat' and metadata(g).get('workspace_goal_ref')==ident and not deleted(g)],
            'goal_basis':continuation_basis(bid,selected) if selected else None,'native_goal_support':native_support,'native_goal':owner.get('native_goal') if owner else None,'chats':chats,'task_links':{task:goal for task,goal in links.items() if not ident or goal==ident},'assets':assets,
            'running_chats':[j['chat_id'] for j in app.running_jobs(workspace_root()) if j['business_id']==bid],'workspace':app.workspace_path}


def mutate(app,bid,data):
    """One live lifecycle path for current UI/API and compatible older interfaces."""
    action=data.get('action','save');goal=None
    if data.get('basis') and data.get('id') and action in {'save','delete','restore','native_start'}:
        current=find(bid,data['id'],include_deleted=True)
        if continuation_basis(bid,current)!=data['basis']:raise ValueError('This goal changed elsewhere. Reopen it to review the latest version before changing it.')
    if action=='native_start':
        goal=find(bid,data.get('id'));owner=metadata(goal).get('chat_id')
        if scope(goal)!='chat':raise ValueError('Create a chat goal for this workspace outcome before starting native work.')
        reason=review_reason(bid,goal['id'])
        if reason:raise ValueError(reason)
        job=app.start_chat(bid,'Work toward this chat goal and verify its completion criteria.',[],chat_id=owner or '',connection=data.get('connection') if not owner else None,goal_id=goal['id'],native_goal={k:data[k] for k in ('token_budget',) if k in data})
        return {'job':job,'chat_id':job['chat_id']}
    if action=='save':
        if data.get('chat_id') and not any(c['id']==data['chat_id'] and c['business_id']==bid and c.get('workspace',app.workspace_path)==app.workspace_path for c in app.preferences['chats']):raise ValueError('Choose a chat in this workspace and business.')
        prior=find(bid,data['id']) if data.get('id') else None
        goal=save(bid,data);changed(app,bid,goal['id'])
        semantic_change=bool(prior and (any(prior.get(k)!=goal.get(k) for k in ('name','target')) or scope(prior)!=scope(goal)))
        if data.get('status') in {'paused','completed'} or semantic_change:
            from workspace_native_goals import control
            control(app,bid,prior or goal,'clear' if semantic_change else 'complete' if data.get('status')=='completed' else 'pause')
    elif action in {'delete','restore'}:
        goal=remove(bid,data.get('id'),restore=action=='restore')
        if action=='delete':
            from workspace_native_goals import control
            control(app,bid,goal,'clear')
        changed(app,bid,goal['id'],remove_links=action=='delete')
    elif action=='link_chat':link_chat(app.preferences,bid,data.get('chat_id'),data.get('goal_id'))
    elif action=='continuation':set_continuation(app.preferences,bid,data.get('chat_id'),data.get('mode','manual'),data.get('until'))
    elif action=='link_asset':link_asset(bid,data.get('asset_id'),data.get('goal_id'))
    else:raise ValueError('Choose a supported goal action.')
    app.read_cache.clear();app.save_preferences()
    for pending in app.running_jobs(workspace_root()):
        execution=app.executions.get(pending['id'])
        if not execution or not hasattr(execution,'continuation'):continue
        current=next((c for c in app.preferences['chats'] if c['id']==pending.get('chat_id')),None)
        if current:execution.continuation=dict(current.get('continuation') or {'mode':'manual'})
        if execution.retry_check_at is not None:execution.retry_check_at=time.time()
    return inventory(app,bid,(goal['id'] if goal else data.get('goal_id')) or None)


def continuation(kind,mode='manual',until=None):
    supported=kind in {'pi','omp'}
    if not isinstance(mode,str) or mode not in {'manual','native'}:raise ValueError('Choose manual continuation or native retries.')
    if mode=='native':
        if not supported:raise ValueError('This connection does not expose bounded native retry control. Continue manually in the saved chat.')
        if isinstance(until,bool) or not isinstance(until,(float,int)) or not time.time()<until<=time.time()+7*86400:
            raise ValueError('Choose a continuation expiry within the next seven days.')
    return {'mode':mode,'until':until if mode=='native' else None,'native_supported':supported,
            'note':'Uses retries already enabled by the native app. No scheduled restart or guarantee of quota availability. Aura and the native connection must remain running.'}


def review_reason(bid,goal_id,basis=None):
    try:goal=find(bid,goal_id)
    except ValueError:return 'The selected goal is no longer available.'
    if metadata(goal).get('workspace_goal_ref'):
        try:find(bid,metadata(goal)['workspace_goal_ref'])
        except ValueError:return 'The connected workspace goal is no longer available. Review the link.'
    if any(not available(g) for g in related(bid,goal)):return 'A selected goal is paused or completed.'
    if basis and continuation_basis(bid,goal)!=basis:return 'The goal changed. Review it before continuing.'
    return ''


def guard(bid,goal_id,basis,policy):
    if policy.get('mode')!='native':return 'Automatic continuation is off.'
    if time.time()>policy.get('until',0):return 'Automatic continuation has expired.'
    return review_reason(bid,goal_id,basis)


def live_change(url,bid,payload,route='/api/goals'):
    """Live chat history and choices use their existing owner, never competing settings writes."""
    from urllib.parse import urlparse
    from urllib.request import Request,urlopen
    from _common import PRODUCT_ROOT
    parts=urlparse(url)
    if parts.scheme!='http' or parts.hostname not in {'127.0.0.1','localhost','::1'} or parts.username or parts.password or parts.path not in {'','/'} or parts.query or parts.fragment:
        raise ValueError('Use the local Aura address, such as http://127.0.0.1:4187.')
    base=url.rstrip('/')
    with urlopen(base,timeout=10) as response:page=response.read().decode('utf-8')
    token=re.search(r'<meta name="aura-token" content="([^"]+)"',page)
    if not token:raise ValueError('This address is not an Aura interface.')
    headers={'X-Aura-Token':token[1],'X-Aura-Workspace':str(workspace_root()),'Content-Type':'application/json'}
    with urlopen(Request(base+'/api/state',headers=headers),timeout=15) as response:state=json.load(response)
    if Path(state['product']).resolve()!=PRODUCT_ROOT.resolve():raise ValueError('Choose the Aura instance running this product copy.')
    body=json.dumps({'business':bid,**payload}).encode() if payload is not None else None
    with urlopen(Request(base+route,headers=headers,data=body),timeout=15) as response:return json.load(response)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['list','show','save','check','link-chat','link-asset','continuation','delete','restore','native-start','pause','resume','complete'])
    parser.add_argument('--workspace',type=Path,default=workspace_root());parser.add_argument('--business-id',required=True);parser.add_argument('--id');parser.add_argument('--basis');parser.add_argument('--input');parser.add_argument('--json',action='store_true')
    parser.add_argument('--token-budget',type=int);parser.add_argument('--chat');parser.add_argument('--asset');parser.add_argument('--mode',choices=['manual','native'],default='manual');parser.add_argument('--until',type=float)
    parser.add_argument('--scope',choices=['workspace','chat','all'],default='workspace');parser.add_argument('--show',choices=['active','current','completed','deleted','all'],default='active')
    parser.add_argument('--url',default='http://127.0.0.1:4187',help='Running local Aura address for chat links, deletion/recovery and continuation choices')
    args=parser.parse_args()
    with workspace_scope(args.workspace):
        if args.action=='list' and args.chat:
            from urllib.parse import urlencode
            result=live_change(args.url,args.business_id,None,'/api/goals?'+urlencode({'business':args.business_id,'chat_id':args.chat,'scope':args.scope,'show':args.show}))
        elif args.action in {'pause','resume','complete'}:result=live_change(args.url,args.business_id,{'action':'save','id':args.id,'status':{'pause':'paused','resume':'active','complete':'completed'}[args.action]})
        elif args.action=='native-start':result=live_change(args.url,args.business_id,{'action':'native_start','id':args.id,**({'token_budget':args.token_budget} if args.token_budget is not None else {})})
        elif args.action in {'delete','restore'}:result=live_change(args.url,args.business_id,{'action':args.action,'id':args.id})
        elif args.action in {'link-chat','link-asset','continuation'}:
            result=link_asset(args.business_id,args.asset,args.id) if args.action=='link-asset' else live_change(args.url,args.business_id,
                {'action':'link_chat','chat_id':args.chat,'goal_id':args.id} if args.action=='link-chat' else {'action':'continuation','chat_id':args.chat,'mode':args.mode,'until':args.until})
        else:result=save(args.business_id,read_json_input(args.input)) if args.action=='save' else find(args.business_id,args.id,include_deleted=args.action=='check' or args.show=='deleted') if args.action in {'show','check'} else {'items':select_goals(goals(args.business_id,include_deleted=True),args.show,args.scope,args.chat)}
        if args.action=='check':
            reason=review_reason(args.business_id,args.id,args.basis)
            result={'eligible':not reason,'goal':result,'reason':reason}
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
