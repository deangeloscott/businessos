#!/usr/bin/env python3
"""Shared schema/path/write mechanics for canonical organization objects."""
from _common import *
from jsonschema import Draft202012Validator,FormatChecker
import json

# jsonschema's optional RFC3339 dependency is absent in some bundled runtimes.
# Use the standard library so validation is the same on every installation.
DATE_FORMATS=FormatChecker(formats=[])


@DATE_FORMATS.checks('date-time',raises=ValueError)
def _date_time(value):
    if not isinstance(value,str):return True
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})',value):return False
    return datetime.datetime.fromisoformat(value.upper().replace('Z','+00:00')).tzinfo is not None


@DATE_FORMATS.checks('date',raises=ValueError)
def _date(value):
    if not isinstance(value,str):return True
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):return False
    datetime.date.fromisoformat(value)
    return True

INSTANCE_PATHS={
    'Business':'context/business.json','Brand':'context/brand','ProductService':'context/products','Offer':'context/offers',
    'AudienceSegment':'context/audiences','Market':'context/markets','Objective':'context/objectives','EconomicContext':'context/economics',
    'BusinessClaim':'context/claims','ContextUpdateProposal':'context/proposals','PreferenceProfile':'context/preferences',
    'SourceRecord':'intelligence/sources','SourceProfile':'intelligence/source-profiles','Observation':'intelligence/observations',
    'Insight':'intelligence/insights','ProofRecord':'intelligence/proof','PlatformChange':'intelligence/platform-changes',
    'Opportunity':'decisions/opportunities','Initiative':'decisions/initiatives','DecisionRecord':'decisions/records',
    'WorkRequest':'operations/work-requests','ChangeEvent':'operations/change-events','VerificationRecord':'operations/verifications',
    'Incident':'operations/incidents','AttentionItem':'operations/attention','Asset':'assets',
    'MetricDefinition':'measurement/metric-definitions','MetricObservation':'measurement/metric-observations',
    'Experiment':'measurement/experiments','OutcomeEvaluation':'measurement/outcome-evaluations',
    'Learning':'learning/business','ProcessExtension':'learning/process-extensions',
    'Competitor':'context/competitors','CustomerJourney':'domains/customer-optimization/customer-journeys',
    'IndustryEvent':'domains/industry-intelligence/industry-events','OrganicDemandUnit':'domains/seo-aeo/organic-demand-units',
    'OrganicCompetitorState':'domains/seo-aeo/organic-competitor-state','SEOAssetState':'domains/seo-aeo/asset-state',
    'PlatformProfile':'domains/content-synthesis/platform-profiles',
}


def schema_entry(title):
    registry=json.loads((PRODUCT_ROOT/'generated/schema-registry.json').read_text(encoding='utf-8'))
    row=next((item for item in registry if item.get('title')==title),None)
    if not row:raise ValueError(f'Unknown canonical schema title: {title}')
    return row,json.loads((PRODUCT_ROOT/row['path']).read_text(encoding='utf-8'))


def validate_canonical(title,obj):
    _,schema=schema_entry(title)
    errors=sorted(Draft202012Validator(schema,format_checker=DATE_FORMATS).iter_errors(obj),key=lambda e:list(e.path))
    if errors:raise ValueError(f'{title} invalid: '+'; '.join(f'{list(e.path)} {e.message}' for e in errors))


def canonical_path(business_id,obj):
    typ=obj.get('object_type');oid=obj.get('id');rel=INSTANCE_PATHS.get(typ)
    if not rel:raise ValueError(f'No supported active-business storage location for canonical object type: {typ}')
    path=instance_dir(business_id)/rel
    if path.suffix.lower()=='.json':return path
    return path/f'{oid}.json'


def write_canonical(obj,path=None,allow_update=False):
    with business_transaction(obj.get('business_id')):
        return _write_canonical(obj,path,allow_update)


def _write_canonical(obj,path=None,allow_update=False):
    business_id=obj.get('business_id');path=Path(path) if path else canonical_path(business_id,obj)
    if path.exists() and not allow_update:
        try:rel=storage_ref(path)
        except Exception:rel=str(path)
        raise FileExistsError(f'Refusing to overwrite existing canonical object: {rel}')
    return write_json_atomic(path,obj)
