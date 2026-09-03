"""Truthful production-readiness semantics for governed customer-facing Assets.

Artifact validity, version-specific QA, production readiness, deployment, and measured
outcomes are different facts. This module validates and summarizes the explicit,
version-scoped readiness assessment stored on canonical Assets. It does not infer
readiness from loose labels, QA wording, Run state, or synonym matching.
"""

from _common import object_index, resolve_storage_ref


READINESS_STATUSES={'not_assessed','blocked','ready','not_applicable'}
DEPLOYMENT_STATUSES={'not_performed','performed','not_applicable'}
MEASUREMENT_STATUSES={'pending','in_progress','observed','not_applicable'}
BLOCKER_FIELDS=('unresolved_business_facts','missing_authorization','missing_capabilities','other_blockers')


def _businessos(asset):
    ext=asset.get('extensions') if isinstance(asset.get('extensions'),dict) else {}
    return ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}


def _nonempty_strings(value):
    return isinstance(value,list) and all(isinstance(x,str) and x.strip() for x in value)


def _refs_resolve(refs,business_id):
    idx=object_index(business_id)
    for ref in refs:
        if ref in idx:continue
        try:
            if resolve_storage_ref(ref).exists():continue
        except Exception:
            pass
        return False
    return True


def readiness_for_asset(asset):
    """Return the explicit assessment; omission truthfully means not assessed."""
    raw=_businessos(asset).get('production_readiness')
    if not isinstance(raw,dict):
        return {
            'status':'not_assessed','assessed_version':str(asset.get('version','')),
            'unresolved_business_facts':[],'missing_authorization':[],
            'missing_capabilities':[],'other_blockers':[],
            'deployment_status':'not_performed','deployment_evidence_refs':[],
            'measurement_status':'pending','measurement_evidence_refs':[],
        }
    out=dict(raw)
    for field in BLOCKER_FIELDS:out.setdefault(field,[])
    out.setdefault('deployment_evidence_refs',[]);out.setdefault('measurement_evidence_refs',[])
    return out


def readiness_errors(business_id,objects):
    """Validate explicit readiness truth without promoting unrelated fields into authority."""
    errors=[]
    for asset,path in objects:
        if asset.get('object_type')!='Asset':continue
        bos=_businessos(asset);raw=bos.get('production_readiness')
        if raw is None:continue
        if not isinstance(raw,dict):
            errors.append(f'{path} Asset extensions.businessos.production_readiness must be an object');continue
        required={'status','assessed_version','unresolved_business_facts','missing_authorization','missing_capabilities','other_blockers','deployment_status','measurement_status'}
        missing=sorted(required-set(raw))
        if missing:
            errors.append(f'{path} Asset production_readiness is missing required field(s): {", ".join(missing)}');continue
        status=raw.get('status');deployment=raw.get('deployment_status');measurement=raw.get('measurement_status')
        if status not in READINESS_STATUSES:
            errors.append(f'{path} Asset production_readiness.status must be one of {", ".join(sorted(READINESS_STATUSES))}')
        if str(raw.get('assessed_version'))!=str(asset.get('version')):
            errors.append(f'{path} Asset production_readiness.assessed_version must match Asset version {asset.get("version")!r}')
        for field in BLOCKER_FIELDS:
            if not _nonempty_strings(raw.get(field)):
                errors.append(f'{path} Asset production_readiness.{field} must be a list containing only non-empty strings')
        if deployment not in DEPLOYMENT_STATUSES:
            errors.append(f'{path} Asset production_readiness.deployment_status must be one of {", ".join(sorted(DEPLOYMENT_STATUSES))}')
        if measurement not in MEASUREMENT_STATUSES:
            errors.append(f'{path} Asset production_readiness.measurement_status must be one of {", ".join(sorted(MEASUREMENT_STATUSES))}')
        blockers=[x for field in BLOCKER_FIELDS for x in raw.get(field,[]) if isinstance(x,str) and x.strip()]
        if status=='blocked' and not blockers:
            errors.append(f'{path} Asset production_readiness.status=blocked requires at least one typed unresolved fact, authorization gap, capability gap, or other blocker')
        if status in {'ready','not_applicable'} and blockers:
            errors.append(f'{path} Asset production_readiness.status={status} cannot retain unresolved blockers')

        # This is not semantic inference: the claim manifest already explicitly marks these
        # entries as placeholders and explicitly declares whether they are launch-critical.
        manifest=bos.get('claim_manifest') if isinstance(bos.get('claim_manifest'),list) else []
        placeholders=[x for x in manifest if isinstance(x,dict) and x.get('classification')=='placeholder']
        if status=='ready':
            unresolved=[str(x.get('text') or '<unnamed placeholder>') for x in placeholders if x.get('launch_critical') is not False]
            if unresolved:
                errors.append(f'{path} Asset cannot assert production_readiness.status=ready while placeholder claim entries remain launch-critical or unassessed: {"; ".join(unresolved)}')

        deprefs=raw.get('deployment_evidence_refs',[]);measrefs=raw.get('measurement_evidence_refs',[])
        if not isinstance(deprefs,list) or not all(isinstance(x,str) and x.strip() for x in deprefs):
            errors.append(f'{path} Asset production_readiness.deployment_evidence_refs must be a list of non-empty references when supplied')
        elif deployment=='performed' and (not deprefs or not _refs_resolve(deprefs,business_id)):
            errors.append(f'{path} Asset deployment_status=performed requires resolving deployment_evidence_refs')
        if not isinstance(measrefs,list) or not all(isinstance(x,str) and x.strip() for x in measrefs):
            errors.append(f'{path} Asset production_readiness.measurement_evidence_refs must be a list of non-empty references when supplied')
        elif measurement=='observed' and (not measrefs or not _refs_resolve(measrefs,business_id)):
            errors.append(f'{path} Asset measurement_status=observed requires resolving measurement_evidence_refs')
    return errors


def summarize_readiness(assets,qa_records=None,run_completed=False):
    """Produce a user-facing truth projection without implying launch or outcomes."""
    rows=[]
    for asset,path in assets:
        assessment=readiness_for_asset(asset)
        rows.append({
            'asset_id':asset.get('id'),'asset_ref':str(path),'asset_version':str(asset.get('version','')),
            'artifact_status':asset.get('status'),'production_readiness':assessment.get('status'),
            'unresolved_business_facts':assessment.get('unresolved_business_facts',[]),
            'missing_authorization':assessment.get('missing_authorization',[]),
            'missing_capabilities':assessment.get('missing_capabilities',[]),
            'other_blockers':assessment.get('other_blockers',[]),
            'deployment_status':assessment.get('deployment_status'),
            'measurement_status':assessment.get('measurement_status'),
        })
    states=[x['production_readiness'] for x in rows]
    if not states:overall='not_applicable'
    elif 'blocked' in states:overall='blocked'
    elif 'not_assessed' in states:overall='not_assessed'
    elif all(x=='ready' for x in states):overall='ready'
    else:overall='mixed_or_not_applicable'
    def aggregate(field,empty):
        values=[x.get(field) for x in rows if x.get(field) is not None]
        if not values:return empty
        return values[0] if all(x==values[0] for x in values) else 'mixed'
    return {
        'artifact_work':'completed' if run_completed else 'in_progress',
        'assets':rows,
        'qa':list(qa_records or []),
        'production_readiness':overall,
        'deployment_status':aggregate('deployment_status','not_applicable'),
        'measurement_status':aggregate('measurement_status','not_applicable'),
        'rule':'Artifact/QA completion does not imply production readiness, deployment, authorization, capability availability, or measured outcome.',
    }
