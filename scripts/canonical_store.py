#!/usr/bin/env python3
"""Shared schema/path/write mechanics for canonical organization objects.

Semantic builders remain responsible for object meaning. This module only centralizes
the storage mechanics already repeated by supported persistence helpers.
"""
from _common import *
from jsonschema import Draft202012Validator
import json


INSTANCE_PATHS={
    'Business':'context/business.json',
    'Brand':'context/brand',
    'ProductService':'context/products',
    'Offer':'context/offers',
    'AudienceSegment':'context/audiences',
    'Market':'context/markets',
    'Objective':'context/objectives',
    'EconomicContext':'context/economics',
    'BusinessClaim':'context/claims',
    'ContextUpdateProposal':'context/proposals',
    'PreferenceProfile':'context/preferences',
    'SourceRecord':'intelligence/sources',
    'SourceProfile':'intelligence/source-profiles',
    'Observation':'intelligence/observations',
    'Insight':'intelligence/insights',
    'ProofRecord':'intelligence/proof',
    'PlatformChange':'intelligence/platform-changes',
    'Opportunity':'decisions/opportunities',
    'Initiative':'decisions/initiatives',
    'DecisionRecord':'decisions/records',
    'WorkRequest':'operations/work-requests',
    'ChangeEvent':'operations/change-events',
    'VerificationRecord':'operations/verifications',
    'Incident':'operations/incidents',
    'AttentionItem':'operations/attention',
    'EventReactionDecision':'operations/event-reaction-decisions',
    'Asset':'assets',
    'MetricDefinition':'measurement/metric-definitions',
    'MetricObservation':'measurement/metric-observations',
    'Experiment':'measurement/experiments',
    'OutcomeEvaluation':'measurement/outcome-evaluations',
    'Learning':'learning/business',
    'Competitor':'context/competitors',
    'CustomerJourney':'domains/customer-optimization/customer-journeys',
    'IndustryEvent':'domains/industry-intelligence/industry-events',
    'OrganicDemandUnit':'domains/seo-aeo/organic-demand-units',
    'OrganicCompetitorState':'domains/seo-aeo/organic-competitor-state',
    'SEOAssetState':'domains/seo-aeo/asset-state',
    'PlatformProfile':'domains/content-synthesis/platform-profiles',
}


def schema_entry(title):
    registry=json.loads((PRODUCT_ROOT/'generated/schema-registry.json').read_text())
    row=next((item for item in registry if item.get('title')==title),None)
    if not row:raise ValueError(f'Unknown canonical schema title: {title}')
    return row,json.loads((PRODUCT_ROOT/row['path']).read_text())


def validate_canonical(title,obj):
    _,schema=schema_entry(title)
    errors=sorted(Draft202012Validator(schema).iter_errors(obj),key=lambda e:list(e.path))
    if errors:
        raise ValueError(f'{title} invalid: '+'; '.join(f'{list(e.path)} {e.message}' for e in errors))


def canonical_path(business_id,obj):
    typ=obj.get('object_type');oid=obj.get('id');rel=INSTANCE_PATHS.get(typ)
    if not rel:raise ValueError(f'No supported active-business storage location for canonical object type: {typ}')
    path=instance_dir(business_id)/rel
    if path.suffix.lower()=='.json':return path
    return path/f'{oid}.json'


def write_canonical(obj,path=None,allow_update=False):
    business_id=obj.get('business_id');path=Path(path) if path else canonical_path(business_id,obj)
    if path.exists() and not allow_update:
        try:rel=storage_ref(path)
        except Exception:rel=str(path)
        raise FileExistsError(f'Refusing to overwrite existing canonical object: {rel}')
    return write_json_atomic(path,obj)
