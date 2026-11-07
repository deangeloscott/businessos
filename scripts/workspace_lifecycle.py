"""Portable archive state for saved records; native execution remains native-owned."""
import copy
import math
import time


def archived(obj):
    extensions=obj.get('extensions')
    bos=extensions.get('businessos') if isinstance(extensions,dict) else None
    info=bos.get('archive') if isinstance(bos,dict) else None
    return isinstance(info,dict) and type(info.get('at')) in {int,float} and math.isfinite(info['at']) and info['at']>0


def change(bid, ident, action):
    from _common import object_index, organization_transaction, now, write_json_atomic
    from canonical_store import validate_canonical, write_canonical
    from validate_business import validate_business

    @organization_transaction
    def apply(bid):
        row = object_index(bid).get(ident)
        if not row:
            raise ValueError('This saved item is no longer available in this workspace.')
        obj = row[0]
        if obj['object_type'] in {'Business', 'Objective', 'Run'}:
            raise ValueError('Use the goal controls for goals. The business identity cannot be archived.')
        if action not in {'archive', 'restore'}:
            raise ValueError('Choose archive or restore.')
        extensions = copy.deepcopy(obj.get('extensions') or {})
        bos = extensions.setdefault('businessos', {})
        if not isinstance(bos,dict):raise ValueError('This item’s saved metadata needs attention before archiving.')
        if action == 'archive':
            if not archived(obj):bos['archive']={'at':time.time()}
        else:
            bos.pop('archive', None)
        if extensions==obj.get('extensions'):return {'id':ident,'archived':action=='archive'}
        changed={**obj,'extensions':extensions}
        if 'updated_at' in changed:changed['updated_at']=now()
        validate_canonical(obj['object_type'],changed)
        from workspace_history import capture
        capture(row[1],bid,'Before '+action)
        try:
            write_canonical(changed,row[1],allow_update=True)
            errors,_,_=validate_business(bid)
            if errors:raise ValueError('This saved item needs correction before its archive state can change.')
        except Exception:
            write_json_atomic(row[1],obj)
            raise
        return {'id':ident,'archived':action=='archive'}

    return apply(bid)
