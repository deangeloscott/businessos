"""Existing business goals with scoped work links and bounded native continuation intent."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import time

from _common import workspace_root,workspace_scope,resolve_business
from remember import remember


def goals(bid):
    if resolve_business(bid)['status']!='resolved':raise ValueError('Choose an existing business.')
    from workspace_ui import records
    return [row['data'] for row in records(bid)[0] if row['type']=='Objective']


def find(bid,ident):
    if resolve_business(bid)['status']!='resolved' or not isinstance(ident,str) or not re.fullmatch(r'obj_[A-Za-z0-9_-]+',ident):raise ValueError('Choose an existing goal in this business.')
    from canonical_store import canonical_path
    from workspace_sharing import unlinked
    path=unlinked(canonical_path(bid,{'object_type':'Objective','id':ident}))
    try:goal=json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:raise ValueError('This goal is no longer available in the selected business.') from None
    if goal.get('id')!=ident or goal.get('business_id')!=bid or goal.get('object_type')!='Objective':raise ValueError('This goal does not belong to the selected business.')
    return goal


def fingerprint(goal):return hashlib.sha256(json.dumps({k:goal.get(k) for k in ('name','target','horizon','status')},sort_keys=True).encode()).hexdigest()


def guidance(goal):
    return ('Goal context: '+json.dumps({k:goal[k] for k in ('id','name','target','horizon','status') if k in goal},ensure_ascii=False)+
        '\nWork toward the user’s actual assignment. A finished reply does not complete the goal. '
        'Preserve meaningful artifacts, decisions and a concise next step at natural stopping points, without repeated summary calls. '
        'When preserving a relevant Asset, its extensions.businessos.goal_ref can link it to this goal. '
        'Use normal memory helpers; do not save a full conversation or private reasoning as goal history. '
        'If this is a continuation, first check what already succeeded and avoid duplicating external actions. '
        'A paused/completed goal is context for this deliberate user request, not authorization for unattended continuation.')


def save(bid,data):
    ident=data.get('id');old=find(bid,ident) if ident else None
    content={}
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
    item={'object_ref':ident} if old else {'object_type':'Objective'}
    result=remember(bid,{'objects':[{**item,'content':content,**({'remove_fields':remove} if remove else {})}]})
    return find(bid,result['objects'][0]['id'])


def link_chat(preferences,bid,chat_id,goal_id):
    chat=next((c for c in preferences['chats'] if c['id']==chat_id and c['business_id']==bid and c.get('workspace',str(workspace_root()))==str(workspace_root())),None)
    if not chat:raise ValueError('Choose a chat in this workspace and business.')
    if goal_id:find(bid,goal_id)
    chat['goal_id']=goal_id or ''
    # A new assignment needs its own deliberate continuation authorization.
    chat.pop('continuation',None)
    return chat


def link_asset(bid,asset_id,goal_id):
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
    if mode=='native' and goal.get('status','active')!='active':raise ValueError('Activate the goal before authorizing automatic continuation.')
    policy=continuation(chat['agent'],mode,until);policy['goal_basis']=fingerprint(goal)
    chat['continuation']=policy
    return policy


def inventory(app,bid,ident=None):
    from workspace_ui import records
    rows=app.cached_read(('context-records',bid),lambda:records(bid)[0],seconds=3)
    items=[r['data'] for r in rows if r['type']=='Objective'];selected=find(bid,ident) if ident else None
    chats=[{k:c[k] for k in ('id','title','agent','summary','status','updated','goal_id','work_state','continuation') if k in c} for c in app.preferences['chats']
           if c['business_id']==bid and c.get('workspace',app.workspace_path)==app.workspace_path and c.get('goal_id') and (not ident or c['goal_id']==ident)]
    links=app.preferences.get('goal_tasks',{}).get(bid,{})
    chats.sort(key=lambda c:c.get('updated',0),reverse=True)
    assets=[]
    for row in rows:
        obj=row['data']
        if ident and row['type']=='Asset' and (obj.get('extensions') or {}).get('businessos',{}).get('goal_ref')==ident:assets.append({'id':obj['id'],'name':obj.get('business_role') or obj['id'],'path':obj.get('location_reference','')})
    return {'items':items,'goal':selected,'goal_basis':fingerprint(selected) if selected else None,'chats':chats,'task_links':{task:goal for task,goal in links.items() if not ident or goal==ident},'assets':assets,
            'running_chats':[j['chat_id'] for j in app.running_jobs(workspace_root()) if j['business_id']==bid],'workspace':app.workspace_path}


def continuation(kind,mode='manual',until=None):
    supported=kind in {'pi','omp'}
    if not isinstance(mode,str) or mode not in {'manual','native'}:raise ValueError('Choose manual continuation or native retries.')
    if mode=='native':
        if not supported:raise ValueError('This connection does not expose bounded native retry control. Continue manually in the saved chat.')
        if isinstance(until,bool) or not isinstance(until,(float,int)) or not time.time()<until<=time.time()+7*86400:
            raise ValueError('Choose a continuation expiry within the next seven days.')
    return {'mode':mode,'until':until if mode=='native' else None,'native_supported':supported,
            'note':'Uses retries already enabled by the native app. No scheduled restart or guarantee of quota availability. Aura and the native connection must remain running.'}


def guard(bid,goal_id,basis,policy):
    if policy.get('mode')!='native':return 'Automatic continuation is off.'
    if time.time()>policy.get('until',0):return 'Automatic continuation has expired.'
    try:goal=find(bid,goal_id)
    except ValueError:return 'The selected goal is no longer available.'
    if goal.get('status','active')!='active':return 'The goal is paused or completed.'
    if fingerprint(goal)!=basis:return 'The goal changed. Review it before continuing.'
    return ''


def live_change(url,bid,payload):
    """Runtime chat choices go through their existing owner, never competing settings writes."""
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
    with urlopen(Request(base+'/api/goals',headers=headers,data=json.dumps({'business':bid,**payload}).encode()),timeout=15) as response:return json.load(response)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['list','show','save','check','link-chat','link-asset','continuation'])
    parser.add_argument('--workspace',type=Path,default=workspace_root());parser.add_argument('--business-id',required=True);parser.add_argument('--id');parser.add_argument('--basis');parser.add_argument('--input',type=Path);parser.add_argument('--json',action='store_true')
    parser.add_argument('--chat');parser.add_argument('--asset');parser.add_argument('--mode',choices=['manual','native'],default='manual');parser.add_argument('--until',type=float)
    parser.add_argument('--url',default='http://127.0.0.1:4187',help='Running local Aura address for chat links and continuation choices')
    args=parser.parse_args()
    with workspace_scope(args.workspace):
        if args.action in {'link-chat','link-asset','continuation'}:
            result=link_asset(args.business_id,args.asset,args.id) if args.action=='link-asset' else live_change(args.url,args.business_id,
                {'action':'link_chat','chat_id':args.chat,'goal_id':args.id} if args.action=='link-chat' else {'action':'continuation','chat_id':args.chat,'mode':args.mode,'until':args.until})
        else:result=save(args.business_id,json.loads(args.input.read_text(encoding='utf-8'))) if args.action=='save' else find(args.business_id,args.id) if args.action in {'show','check'} else {'items':goals(args.business_id)}
        if args.action=='check':
            eligible=result.get('status','active')=='active' and (not args.basis or args.basis==fingerprint(result))
            result={'eligible':eligible,'goal':result,'reason':'' if eligible else 'The goal is paused, completed or changed; review before continuing.'}
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
