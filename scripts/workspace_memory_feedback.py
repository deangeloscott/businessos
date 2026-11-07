"""Confirmed canonical saves and revision-safe feedback, using existing history."""
import argparse
import json
import secrets
import time
from pathlib import Path
from _common import organization_transaction, workspace_root, workspace_scope, object_index, write_json_atomic
import workspace_history


def target(bid):return workspace_history.store(bid)/'feedback.json'


def rows(bid):
    try:return json.loads(target(bid).read_text(encoding='utf-8'))
    except FileNotFoundError:return []


def record(bid,prepared,snapshots):
    """Called only after the canonical transaction passes validation."""
    from workspace_documents import revision
    from correction_impacts import _material_value
    added=[]
    eligible=[]
    for item in prepared:
        obj=item['object'];before=item.get('existing');path=Path(item['path'])
        if obj['object_type'] in {'ChangeEvent','Objective','Asset','Run','AttentionItem','PlatformChange'}:continue
        if before and all(_material_value(before,k)==_material_value(obj,k) for k in before.keys()|obj.keys() if k not in {'updated_at','reviewed_at'}):continue
        eligible.append(item)
    previous={r['path']:r for r in workspace_history.capture_many(bid,{Path(r['path']):snapshots[Path(r['path'])] for r in eligible if Path(r['path']) in snapshots},'Before saved memory')}
    for item in eligible:
        obj=item['object'];before=item.get('existing');path=Path(item['path'])
        label=obj.get('name') or obj.get('title') or obj.get('summary') or obj['object_type']
        added.append({'id':secrets.token_urlsafe(12),'object_ref':obj['id'],'label':str(label)[:160],
                      'at':time.time(),'status':'pending','revision':revision(path),'operation':'updated' if before else 'created',
                      'version_id':previous.get(path.relative_to(workspace_root()).as_posix(),{}).get('id','')})
    if added:
        path=target(bid);path.parent.mkdir(parents=True,exist_ok=True)
        write_json_atomic(path,(rows(bid)+added)[-200:])
    return added


def inventory(bid,since=0):
    index=object_index(bid)
    return {'items':[r for r in rows(bid) if r['status']=='pending' and r['at']>=float(since) and r['object_ref'] in index][-5:]}


@organization_transaction
def respond(bid,ident,action):
    if action not in {'keep','undo'}:raise ValueError('Choose Keep or Undo.')
    saved=rows(bid);row=next((r for r in saved if r['id']==ident),None)
    if not row or row['status']!='pending':raise ValueError('This memory feedback has already been handled.')
    if action=='undo':
        from workspace_documents import revision
        current=object_index(bid).get(row['object_ref'])
        if not current or revision(current[1])!=row['revision']:raise ValueError('This memory changed since it was saved. Open it to review the current version.')
        if row['operation']=='updated':
            if not row['version_id']:raise ValueError('The earlier version is unavailable. Open this memory to review or correct it.')
            workspace_history.restore(bid,row['version_id'],row['revision'])
        else:
            from forget import forget
            # Save recovery even for a newly created independent memory.
            workspace_history.capture(current[1],bid,'Before undoing saved memory')
            try:forget(bid,row['object_ref'])
            except ValueError as exc:raise ValueError('Other saved work relies on this memory. Open it to correct it instead.') from exc
    # Undo may itself produce a canonical save receipt. Acknowledge its receipt too.
    latest=rows(bid)
    for r in latest:
        if r['id']==ident:r['status']=action
        elif action=='undo' and r['object_ref']==row['object_ref'] and r['at']>row['at']:r['status']='keep'
    write_json_atomic(target(bid),latest)
    return {'status':action,'object_ref':row['object_ref']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['list','keep','undo']);p.add_argument('--business-id',required=True);p.add_argument('--workspace',type=Path,default=workspace_root());p.add_argument('--id');p.add_argument('--since',type=float,default=0)
    a=p.parse_args()
    with workspace_scope(a.workspace):print(json.dumps(inventory(a.business_id,a.since) if a.action=='list' else respond(a.business_id,a.id,a.action),ensure_ascii=False))


if __name__=='__main__':main()
