"""Maintained results and dated reports, shared by native producers, CLI and UI."""
import argparse
import copy
import json
import sys
from datetime import datetime,timezone
from pathlib import Path
from _common import workspace_root,workspace_scope,object_index,organization_transaction,write_json_atomic,now
import workspace_projects as projects

MAX_BYTES=32*1024*1024


def timestamp(value):
    if value is None or value=='':return None
    if not isinstance(value,str):raise ValueError('Use a date, time, and timezone.')
    try:v=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:raise ValueError('Use a date, time, and timezone.') from None
    if v.tzinfo is None:raise ValueError('Include the timezone for this date.')
    return v.astimezone(timezone.utc)


def string(value,label,limit=2000,empty=False):
    if not isinstance(value,str) or len(value)>limit or not empty and not value.strip():raise ValueError(f'Enter a valid {label}.')
    return value.strip()


def path(bid,ident):
    if not isinstance(ident,str) or not __import__('re').fullmatch(r'col_[a-f0-9]{20}',ident):raise ValueError('Choose a valid saved collection.')
    p=workspace_root()/'attachments'/bid/'collections'/(ident+'.json')
    if not p.resolve().is_relative_to(workspace_root().resolve()/'attachments'/bid):raise ValueError('Keep collections inside the workspace. Link external datasets as files instead.')
    return p


def read(bid,ident):
    projects.check_business(bid);p=path(bid,ident)
    if not p.is_file():raise ValueError('This collection is unavailable in the selected workspace.')
    if p.is_symlink() or not p.resolve().is_relative_to(workspace_root().resolve()/'attachments'/bid):raise ValueError('Reconnect the original collection file before editing.')
    try:d=json.loads(p.read_text(encoding='utf-8'))
    except (ValueError,UnicodeError):raise ValueError('This collection file could not be read. The original file was kept; restore a history copy or correct its JSON.') from None
    if not isinstance(d,dict) or d.get('format')!=1 or d.get('business_id')!=bid or d.get('id')!=ident:raise ValueError('This collection needs attention. The original file was kept.')
    if not all(isinstance(d.get(k),t) for k,t in [('items',list),('feedback',dict),('checks',list),('receipts',dict)]):raise ValueError('This collection needs attention. The original file was kept.')
    return d


def revision(d):return projects.digest(d)


def expected(d,data):
    if data.get('revision')!=revision(d):raise ValueError('This collection changed. Read its current version before saving; your changes have not been applied.')


def asset(bid,ident):
    return next((o for o,p in object_index(bid).values() if o['object_type']=='Asset' and ((o.get('extensions') or {}).get('businessos',{}).get('collection') or {}).get('id')==ident),None)


def persist(bid,d,before=None):
    from remember import remember
    from workspace_history import capture
    p=path(bid,d['id']);encoded=json.dumps(d,ensure_ascii=False,indent=2).encode()
    if len(encoded)>MAX_BYTES:raise ValueError('This collection is large. Split it by purpose or keep the larger dataset in its native tool and link it here.')
    previous=p.read_bytes() if p.exists() else None
    if previous:capture(p,bid,'Before collection change',previous)
    original=asset(bid,d['id']);bos=copy.deepcopy((original or {}).get('extensions') or {})
    bos.setdefault('businessos',{})['collection']={'id':d['id'],'mode':d['mode']}
    bos['businessos'].setdefault('work',{})['project_refs']=d.get('project_refs',[])
    if d.get('producer'):bos['businessos']['work']['producer']=d['producer']
    content={'asset_type':'collection' if d['mode']=='collection' else 'report_series','business_role':d['name'],
             'location_reference':p.relative_to(workspace_root()).as_posix(),'version':str(d['version']),'status':'active','extensions':bos}
    try:
        write_json_atomic(p,d)
        remember(bid,{'objects':[{**({'object_ref':original['id']} if original else {'object_type':'Asset'}),'content':content}]})
    except Exception:
        if previous is not None:p.write_bytes(previous)
        elif p.exists():p.unlink()
        raise
    return {'id':d['id'],'revision':revision(d),'version':d['version'],'asset_id':(asset(bid,d['id']) or {})['id']}


def references(value):
    if not isinstance(value,list) or len(value)>200:raise ValueError('Choose a bounded list of source references.')
    out=[]
    for ref in value:
        if isinstance(ref,str):ref={'reference':ref}
        if not isinstance(ref,dict):raise ValueError('Choose a valid source reference.')
        row={'reference':string(ref.get('reference'),'source reference',2000)}
        for k in ('published_at','data_as_of','last_checked_at'):
            if ref.get(k):timestamp(ref[k]);row[k]=ref[k]
        if ref.get('source_id'):row['source_id']=string(ref['source_id'],'source identity',500)
        if row not in out:out.append(row)
    return out


@organization_transaction
def create(bid,data):
    projects.check_business(bid);key=string(data.get('key'),'collection key',200)
    ident='col_'+projects.digest([bid,key])[:20];p=path(bid,ident)
    if p.exists():
        d=read(bid,ident)
        if d['name']!=data.get('name') or d['mode']!=data.get('mode','collection'):raise ValueError('This collection key already belongs to another result. Open it or choose another key.')
        return {'id':ident,'revision':revision(d),'asset_id':asset(bid,ident)['id'],'existing':True}
    mode=data.get('mode','collection')
    if mode not in {'collection','series'}:raise ValueError('Choose a maintained collection or dated reports.')
    context=projects.producer_context(bid)
    project_refs=[projects.find(bid,x)['id'] for x in data.get('project_refs',context.get('project_refs',[]))]
    d={'format':1,'id':ident,'business_id':bid,'key':key,'name':string(data.get('name'),'collection name',160),
       'mode':mode,'purpose':string(data.get('purpose',''),'purpose',2000,True),'project_refs':list(dict.fromkeys(project_refs)),
       'source_refs':references(data.get('source_refs',[])),'created_at':now(),'updated_at':now(),'version':1,
       'items':[],'feedback':{},'checks':[],'receipts':{}}
    if data.get('producer') or context:
        v=data.get('producer') or context
        if not isinstance(v,dict) or v.get('kind') not in {'chat','task','agent'}:raise ValueError('Choose a chat, task, or agent producer.')
        d['producer']={'kind':v['kind'],'id':string(v.get('id'),'producer identity',1000)}
    return persist(bid,d)


@organization_transaction
def configure(bid,ident,data):
    d=read(bid,ident);expected(d,data)
    if 'name' in data:d['name']=string(data['name'],'collection name',160)
    if 'purpose' in data:d['purpose']=string(data['purpose'],'purpose',2000,True)
    if 'source_refs' in data:d['source_refs']=references(data['source_refs'])
    if 'project_refs' in data:
        values=data['project_refs']
        if not isinstance(values,list) or len(values)>100:raise ValueError('Choose a bounded list of projects.')
        d['project_refs']=list(dict.fromkeys(projects.find(bid,p)['id'] for p in values))
    d['version']+=1;d['updated_at']=now();return persist(bid,d)


def material(item):return {k:item[k] for k in ('title','summary','fields','state','expires_at','review_after','supersedes','source_refs') if k in item}


def item_value(raw,before=None):
    if not isinstance(raw,dict):raise ValueError('Each result needs a stable identity and title.')
    ident=string(raw.get('id'),'item identity',500);old=before or {};item=copy.deepcopy(old)
    item['id']=ident
    for k,limit in [('title',500),('summary',12000)]:
        if k in raw:item[k]=string(raw[k],k,limit,k=='summary')
    if not item.get('title'):raise ValueError('Each result needs a title.')
    if 'fields' in raw:
        if not isinstance(raw['fields'],dict) or len(json.dumps(raw['fields']))>50000:raise ValueError('Keep each result bounded; link larger documents or native datasets.')
        item['fields']=raw['fields']
    for k in ('expires_at','review_after'):
        if k in raw:timestamp(raw[k]);item[k]=raw[k] or None
    if 'source_refs' in raw:item['source_refs']=references(raw['source_refs'])
    if 'state' in raw:
        if raw['state'] not in {'active','closed','superseded'}:raise ValueError('Choose Active, Closed, or Superseded.')
        item['state']=raw['state']
    item.setdefault('state','active')
    if 'supersedes' in raw:item['supersedes']=string(raw['supersedes'],'earlier result identity',500)
    if item.get('supersedes')==ident:raise ValueError('A result cannot replace itself.')
    # Checking a source again does not make its meaning a new finding.
    compare=lambda x:{**material(x),'source_refs':[{k:v for k,v in r.items() if k!='last_checked_at'} for r in x.get('source_refs',[])]}
    changed=compare(item)!=compare(old)
    significant=changed and raw.get('material_change',True) is not False
    if 'material_change' in raw and not isinstance(raw['material_change'],bool):raise ValueError('Material change must be true or false.')
    if significant:item['change_reason']=string(raw.get('change_reason') or ('New result' if not old else 'Saved details changed'),'change reason',1000)
    item.update(first_seen=old.get('first_seen') or now(),last_seen=now(),updated_at=now() if changed else old.get('updated_at',now()),
                attention_revision=old.get('attention_revision',0)+int(significant),revision=projects.digest(compare(item)))
    return item,changed,significant


def coverage(data,doc):
    v=data.get('coverage') or {}
    if not isinstance(v,dict):raise ValueError('Coverage needs expected, checked, and failed source identities.')
    expected_sources=v.get('expected')
    configured=[r.get('source_id') or r['reference'] for r in doc.get('source_refs',[])]
    if expected_sources is None:expected_sources=configured
    checked=v.get('checked',[]);failed=v.get('failed',[])
    for values in (expected_sources,checked,failed):
        if not isinstance(values,list) or len(values)>2000 or any(not isinstance(s,str) or not s or len(s)>2000 for s in values):raise ValueError('Coverage needs bounded source identities for expected, checked, and failed sources.')
    expected_sources=list(dict.fromkeys([*configured,*expected_sources]))
    complete=data.get('status')=='complete' and bool(checked) and bool(expected_sources or v.get('scope')) and not failed and set(expected_sources)<=set(checked)
    status='complete' if complete else 'failed' if data.get('status')=='failed' else 'partial' if checked else 'unknown'
    return {'status':status,'expected':list(dict.fromkeys(expected_sources)),'checked':list(dict.fromkeys(checked)),
            'failed':list(dict.fromkeys(failed)),'scope':str(v.get('scope',''))[:1000],'basis':'Producer-reported checks; not independent factual verification.'}


@organization_transaction
def apply(bid,ident,data):
    d=read(bid,ident);run_id=string(data.get('run_id'),'native run or request identity',500)
    payload_hash=projects.digest({k:v for k,v in data.items() if k!='revision'})
    prior=d['receipts'].get(run_id)
    if prior:
        if prior['payload_hash']!=payload_hash:raise ValueError('This run identity was already used for different results. Read the current collection before retrying.')
        return {**prior,'replayed':True,'revision':revision(d)}
    expected(d,data);values=data.get('items',[])
    if not isinstance(values,list) or len(values)>2000:raise ValueError('Submit up to 2,000 results per update.')
    index={i['id']:i for i in d['items']};seen=set();changes=[]
    for raw in values:
        if not isinstance(raw,dict) or raw.get('id') in seen:raise ValueError('Submit each result identity once per update.')
        seen.add(raw.get('id'));old=index.get(raw.get('id'));item,changed,significant=item_value(raw,old)
        index[item['id']]=item
        if d['mode']=='series' and old and changed and not (data.get('amend') is True and raw.get('change_reason')):
            raise ValueError('Keep dated reports as separate installments. Use a new item identity, or explicitly amend this report with a reason.')
        if significant:
            kind='new' if old is None else 'closed' if item['state']=='closed' and old.get('state')!='closed' else 'changed'
            changes.append({'id':item['id'],'title':item['title'],'kind':kind,'reason':str(raw.get('change_reason') or ('New result' if old is None else 'Saved details changed'))[:1000]})
        if item.get('supersedes'):
            previous=index.get(item['supersedes'])
            if not previous:raise ValueError('Choose an existing result to replace. Nothing has been saved.')
            if previous['state']!='superseded':
                previous.update(state='superseded',superseded_by=item['id'],updated_at=now(),attention_revision=previous.get('attention_revision',0)+1)
                previous['revision']=projects.digest(material(previous));changes.append({'id':previous['id'],'title':previous['title'],'kind':'superseded','reason':'Replaced by '+item['title']})
    order=data.get('order',[])
    if not isinstance(order,list) or any(not isinstance(i,str) or i not in index for i in order) or len(set(order))!=len(order):raise ValueError('Order must contain distinct saved result identities.')
    for item in index.values():
        seen_chain=set();cursor=item
        while cursor.get('supersedes'):
            if cursor['id'] in seen_chain:raise ValueError('Replacement links cannot form a cycle.')
            seen_chain.add(cursor['id']);cursor=index[cursor['supersedes']]
    cov=coverage(data,d);d['items']=[index[i] for i in order]+[v for k,v in index.items() if k not in set(order)];d['version']+=1;d['updated_at']=now()
    check={'run_id':run_id,'at':now(),'coverage':cov,'changes':changes[:250],'change_count':len(changes),
           'no_change_verified':cov['status']=='complete' and not changes,'changes_truncated':len(changes)>250}
    d['checks']=(d['checks']+[check])[-50:]
    receipt={'run_id':run_id,'payload_hash':payload_hash,'version':d['version'],'coverage':cov,'changes':changes[:250],'change_count':len(changes),'no_change_verified':check['no_change_verified']}
    d['receipts'][run_id]=receipt;d['receipts']=dict(list(d['receipts'].items())[-500:])
    saved=persist(bid,d)
    return {**receipt,**saved,'replayed':False}


def effective(item,feedback,at=None):
    at=at or datetime.now(timezone.utc);row=copy.deepcopy(item);f=feedback.get(item['id'],{});overrides=f.get('correction',{})
    row['reported']={k:item.get(k) for k in overrides}
    for k,v in overrides.items():row[k]={**row.get(k,{}),**v} if k=='fields' else v
    baseline=f.get('correction_reported',{})
    def differs(k,v):
        if k=='fields':return any(item.get(k,{}).get(field)!=baseline.get(k,{}).get(field) and item.get(k,{}).get(field)!=value for field,value in v.items())
        return item.get(k)!=baseline.get(k) and item.get(k)!=v
    row['corrected']=bool(overrides);row['correction_conflict']=any(differs(k,v) for k,v in overrides.items())
    row['correction_note']=f.get('correction_note','')
    expired=bool(timestamp(row.get('expires_at')) and timestamp(row['expires_at'])<=at)
    row['display_state']='expired' if expired and row.get('state')=='active' else row.get('state','active')
    row['needs_review']=bool(timestamp(row.get('review_after')) and timestamp(row['review_after'])<=at)
    row['disposition']=f.get('disposition','');row['saved']=f.get('saved',False)
    row['snoozed']=bool(timestamp(f.get('snoozed_until')) and timestamp(f['snoozed_until'])>at)
    row['changed_since_handled']=bool(f.get('attention_basis') is not None and item.get('attention_revision',0)>f['attention_basis'])
    row['hidden']=row['snoozed'] or row['disposition']=='dismissed' and not row['changed_since_handled']
    return row


@organization_transaction
def feedback(bid,ident,data):
    d=read(bid,ident);expected(d,data);item=next((i for i in d['items'] if i['id']==data.get('item_id')),None)
    if not item:raise ValueError('This result is no longer available.')
    f=d['feedback'].setdefault(item['id'],{});action=data.get('action')
    if action in {'dismiss','acknowledge','restore'}:
        f['disposition']={'dismiss':'dismissed','acknowledge':'acknowledged','restore':''}[action];f['attention_basis']=item.get('attention_revision',0)
        if action=='restore':f.pop('snoozed_until',None)
    elif action=='save':f['saved']=not f.get('saved',False)
    elif action=='snooze':timestamp(data.get('until'));f['snoozed_until']=data.get('until')
    elif action=='correct':
        correction=data.get('correction')
        if not isinstance(correction,dict) or not correction or set(correction)-{'title','summary','fields','expires_at','review_after'}:raise ValueError('Correct the title, summary, fields, or dates.')
        item_value({**item,**correction},item)
        old=f.get('correction',{});merged={**old,**correction}
        if 'fields' in correction:merged['fields']={**old.get('fields',{}),**correction['fields']}
        baseline=f.get('correction_reported',{}).copy()
        for k in correction:
            baseline[k]={**baseline.get(k,{}),**{field:item.get(k,{}).get(field) for field in correction[k]}} if k=='fields' else item.get(k)
        f['correction']=merged;f['correction_reported']=baseline;f['correction_note']=string(data.get('note') or 'User correction','correction note',2000)
    elif action=='clear-correction':f.pop('correction',None);f.pop('correction_note',None)
    else:raise ValueError('Choose a result action.')
    f['at']=now();d['version']+=1;d['updated_at']=now();return persist(bid,d)


def check_summary(c):
    if not c:return None
    cov=c['coverage'];missing=sorted(set(cov['expected'])-set(cov['checked']))
    return {**{k:c[k] for k in ('run_id','at','change_count','no_change_verified')},'changes':c.get('changes',[])[:20],
            'coverage':{'status':cov['status'],'checked':len(cov['checked']),'expected':len(cov['expected']),
                        'failed':cov['failed'][:10],'missing':missing[:10],'scope':cov.get('scope',''),'basis':cov['basis']}}


def show(bid,ident,q='',view='current',offset=0,limit=50,at=None,item_id='',history=False):
    d=read(bid,ident);needle=str(q).casefold();rows=[effective(i,d['feedback'],at) for i in d['items']]
    if view not in {'current','all','saved','handled','review','changes'}:raise ValueError('Choose Current, Changes, Saved, Review, Handled, or All.')
    if view=='current':rows=[r for r in rows if r['display_state']=='active' and not r['hidden']]
    elif view=='saved':rows=[r for r in rows if r['saved']]
    elif view=='handled':rows=[r for r in rows if r['hidden'] or r['disposition']=='acknowledged' or r['display_state']!='active']
    elif view=='review':rows=[r for r in rows if r['needs_review'] or r['correction_conflict']]
    elif view=='changes':
        rows=[r for r in rows if not r['hidden'] and (r['changed_since_handled'] or r['disposition']!='acknowledged')]
    if needle:rows=[r for r in rows if needle in json.dumps({k:r.get(k) for k in ('title','summary','fields','source_refs')},ensure_ascii=False).casefold()]
    offset=max(0,int(offset));limit=max(1,min(100,int(limit)))
    if item_id:
        selected=next((effective(i,d['feedback'],at) for i in d['items'] if i['id']==item_id),None)
        if not selected:raise ValueError('This result is unavailable. Refresh the collection.')
        return {'item':selected,'revision':revision(d),'collection_id':d['id']}
    def compact(r):
        return {**{k:v for k,v in r.items() if k not in {'fields','reported','summary','source_refs','correction_note'}},'summary':r.get('summary','')[:800],
                'fields':{k:(v if isinstance(v,(bool,int,float)) or v is None else str(v)[:200]) for k,v in list(r.get('fields',{}).items())[:6]},'excerpt':True}
    return {**{k:d[k] for k in ('id','name','mode','purpose','project_refs','version','producer') if k in d},'revision':revision(d),
            'items':[compact(r) for r in rows[offset:offset+limit]],'total':len(rows),'offset':offset,'limit':limit,'latest_check':check_summary(d['checks'][-1]) if d['checks'] else None,
            'history':[check_summary(c) for c in reversed(d['checks'])] if history else [],'history_count':len(d['checks']),
            'asset_id':(asset(bid,ident) or {}).get('id'),'location':str(path(bid,ident)),'search_scope':'Saved collection text and fields; linked file bodies and native-only data are not searched.'}


def inventory(bid,project=''):
    out=[]
    p=projects.find(bid,project) if project else {};linked={r['id'] for r in p.get('members',[])};excluded={r['id'] for r in p.get('excluded_members',[])}
    for obj,p in object_index(bid).values():
        info=((obj.get('extensions') or {}).get('businessos',{}).get('collection') or {})
        if obj['object_type']!='Asset' or not info.get('id'):continue
        if project and (obj['id'] in excluded or info['id'] in excluded or project not in ((obj.get('extensions') or {}).get('businessos',{}).get('work') or {}).get('project_refs',[]) and not linked.intersection({obj['id'],info['id']})):continue
        try:
            d=read(bid,info['id']);rows=[effective(i,d['feedback']) for i in d['items']]
            out.append({'id':d['id'],'name':d['name'],'mode':d['mode'],'asset_id':obj['id'],'project_refs':d.get('project_refs',[]),
                        'current_count':sum(r['display_state']=='active' and not r['hidden'] for r in rows),'latest_check':check_summary(d['checks'][-1]) if d['checks'] else None})
        except (OSError,ValueError):out.append({'id':info['id'],'name':obj.get('business_role','Saved collection'),'unavailable':True})
    return {'items':out}


def instructions(bid,ident):
    from _common import PRODUCT_ROOT
    d=read(bid,ident)
    argv=[sys.executable,str(PRODUCT_ROOT/'scripts/workspace_collections.py'),'show','--workspace',str(workspace_root()),'--business-id',bid,'--id',ident,'--limit','5']
    return ('\n\n[Aura results]\nCollection: '+ident+'. '+d['purpose']+'\n'+
            'Read the current collection by executing this argument list (each string is a separate argument): '+json.dumps(argv)+'. '+
            'Use the helper apply action with JSON on standard input (--input -), the current revision, stable result identities, '+
            'and a stable native run identity reused on retries. Report only sources actually checked in coverage; a failed or missing source is not evidence that an opportunity disappeared. '+
            ('Keep dated reports as separate item identities. ' if d['mode']=='series' else 'Update the current entries; preserve user feedback and keep source dates distinct from report time. ')+
            'Save only useful results, explain material changes, and avoid repeating unchanged findings as alerts. '+
            'Use actual native scheduling and tools normally. Full helper examples: '+str(PRODUCT_ROOT/'docs/projects-and-results.md')+'.\n[/Aura results]')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['list','create','show','apply','feedback','configure']);p.add_argument('--business-id',required=True);p.add_argument('--workspace',type=Path,default=workspace_root());p.add_argument('--id');p.add_argument('--input',default='{}');p.add_argument('--search',default='');p.add_argument('--view',default='current');p.add_argument('--offset',type=int,default=0);p.add_argument('--limit',type=int,default=50);p.add_argument('--item',default='');p.add_argument('--history',action='store_true')
    a=p.parse_args()
    with workspace_scope(a.workspace):
        data=json.loads(__import__('sys').stdin.read() if a.input=='-' else a.input)
        result=inventory(a.business_id) if a.action=='list' else show(a.business_id,a.id,a.search,a.view,a.offset,a.limit,item_id=a.item,history=a.history) if a.action=='show' else create(a.business_id,data) if a.action=='create' else apply(a.business_id,a.id,data) if a.action=='apply' else configure(a.business_id,a.id,data) if a.action=='configure' else feedback(a.business_id,a.id,data)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as e:raise SystemExit(str(e))
