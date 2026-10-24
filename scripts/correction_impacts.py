"""Correction continuity using existing ChangeEvents and inbound canonical references."""
from _common import describe_object
from validate_references import inbound_references


def _material_value(obj,key):
    if key!='extensions':return key in obj,obj.get(key)
    value=dict(obj.get('extensions') or {})
    if isinstance(value.get('businessos'),dict):
        audit=dict(value['businessos']);audit.pop('memory_provenance',None)
        if audit:value['businessos']=audit
        else:value.pop('businessos',None)
    return value


def correction_event(business_id, before, after, summary, event_id, timestamp):
    """Record possible review impacts, not inferred semantic dependencies."""
    ignored={'id','object_type','business_id','schema_version','created_at','updated_at'}
    if not summary:ignored.add('reviewed_at')
    changed=sorted(key for key in before.keys() | after.keys() if key not in ignored and _material_value(before,key)!=_material_value(after,key))
    if not changed or before.get('object_type')=='ChangeEvent':return None
    related=[row for row in inbound_references(business_id,after['id']) if row['object_type']!='ChangeEvent' and row.get('status') not in {'archived','superseded'}]
    if not related and not summary:return None
    return {
        'id':event_id,'object_type':'ChangeEvent','schema_version':'1.0.0','business_id':business_id,
        'created_at':timestamp,'updated_at':timestamp,'occurred_at':timestamp,'status':'applied',
        'summary':summary or f"Changed {after['id']}: {', '.join(changed)}; related material may need review.",
        'change_kind':'canonical_correction','target_refs':[after['id']],
        'before_state':{key:before[key] for key in changed if key in before},
        'after_state':{key:after[key] for key in changed if key in after},
        'change_details':[dict(row,relationship='possible_impact_from_reference',review_status='pending') for row in related],
        'extensions':{'changed_fields':changed,'removed_fields':[key for key in changed if key not in after]},
    }


def pending_corrections(index, limit=6):
    rows=[]
    for obj,path in index.values():
        if obj.get('object_type')!='ChangeEvent' or obj.get('change_kind')!='canonical_correction':continue
        pending=[item for item in obj.get('change_details',[]) if isinstance(item,dict) and item.get('review_status')=='pending']
        if not pending:continue
        row=describe_object(obj,path)
        row.update(target_refs=obj.get('target_refs',[]),pending_count=len(pending),possible_impacts=pending[:limit])
        rows.append(row)
    rows.sort(key=lambda row:row['object_ref'])
    return {'pending_event_count':len(rows),'events':rows[:limit],'rule':'References identify possible impacts, not confirmed dependencies. Review authored work semantically; record review_status=reviewed or not_affected with a review_note in the ChangeEvent change_details. Updating an artifact or regenerating views alone does not resolve review.'}
