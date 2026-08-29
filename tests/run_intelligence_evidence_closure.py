#!/usr/bin/env python3
"""Regression checks for shared evidence closure and subject-scoped intelligence provenance."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter
from completion_evidence import completion_spec
from validate_research_evidence import _subject_mismatch


def req(condition,message):
    if not condition: raise AssertionError(message)


def contains_all(text,*concepts):
    """Case-insensitive concept check; policy regressions should not depend on prose casing."""
    lowered=text.lower()
    return all(str(concept).lower() in lowered for concept in concepts)


def main():
    foundation=(ROOT/'core/policies/intelligence-foundation.md').read_text()
    evidence=(ROOT/'core/policies/research-evidence.md').read_text()
    completion=(ROOT/'core/policies/completion-evidence.md').read_text()

    # Policy regressions verify the product concepts, not frozen sentence wording.
    req('## Evidence closure and subject relevance' in foundation,
        'shared intelligence foundation must define evidence closure and subject relevance')
    req(contains_all(foundation,'evidence closure','material subjects','unknown','support-grade'),
        'shared intelligence foundation must bound confident synthesis by material evidence coverage')
    req(contains_all(foundation,'observed fact','inference','sentiment pattern','hypothesis','effectiveness/outcome evidence'),
        'shared intelligence foundation must preserve material truth-type distinctions')
    req(contains_all(foundation,'evidence about one subject','evidence about another subject'),
        'shared intelligence foundation must prevent silent cross-subject evidence reuse')
    req(contains_all(foundation,'test threshold','decision rule','forecast'),
        'shared intelligence foundation must distinguish chosen decision rules from evidence-based forecasts')

    for heading in [
        '## Observation and Insight support',
        '### Subject relevance',
        '## Evidence closure before decision-grade synthesis',
    ]:
        req(heading in evidence,f'research evidence policy missing structural section: {heading}')
    req(contains_all(evidence,'subject scopes must overlap','does not support a factual observation about another'),
        'research evidence policy must require resolved subject-relevant support')
    req(contains_all(evidence,'supported','limited','unknown/blocked','not_material','never close a gap by guessing'),
        'research evidence policy must preserve decision-relative closure states and visible gaps')
    req(contains_all(evidence,'claim-level provenance','bibliography detached from the claims'),
        'research evidence policy must keep material claims auditable rather than relying on a detached bibliography')
    req(contains_all(evidence,'test threshold','stop rule','success criterion','not a prediction'),
        'research evidence policy must distinguish test criteria from predicted outcomes')

    req(contains_all(completion,'intelligence','close evidence before confident synthesis','subject/dimension coverage','unresolved evidence gaps'),
        'completion policy must distinguish artifact existence from evidence-closed intelligence')

    schema=json.loads((ROOT/'core/schemas/intelligence/source-record.schema.json').read_text())
    subject_schema=(schema.get('properties') or {}).get('subject_refs') or {}
    req(subject_schema.get('type')=='array','SourceRecord must support resolved subject_refs')
    req(subject_schema.get('uniqueItems') is True,'SourceRecord subject_refs must be unique')

    # Functional subject-provenance behavior matters more than policy prose.
    source={'id':'src_vendor_a','subject_refs':['cmp_vendor_a']}
    matching={'id':'obs_vendor_a','subject_refs':['cmp_vendor_a']}
    mismatched={'id':'obs_vendor_b','subject_refs':['cmp_vendor_b']}
    unscoped={'id':'obs_market','subject_refs':[]}
    req(_subject_mismatch(matching,'obs_vendor_a',source,'src_vendor_a') is None,
        'matching subject-scoped evidence should remain valid')
    err=_subject_mismatch(mismatched,'obs_vendor_b',source,'src_vendor_a')
    req(err and 'cannot silently support another' in err,
        'cross-subject evidence mismatch must be rejected when both sides are resolved')
    req(_subject_mismatch(unscoped,'obs_market',source,'src_vendor_a') is None,
        'general/unresolved evidence must not be falsely rejected by subject matching')

    persist=(ROOT/'scripts/persist_research_bundle.py').read_text()
    req("'subject_refs':item.get('subject_refs',[])" in persist,
        'research persistence helper must preserve SourceRecord subject_refs')
    req('cannot attach Observation' in persist and 'cannot attach Insight' in persist,
        'competitor persistence must reject resolved wrong-subject canonical attachments')

    cpath=ROOT/'systems/competitor-intelligence/contracts/analysis/competitive-position/CONTEXT.md'
    meta,body=read_frontmatter(cpath)
    req(completion_spec(meta).get('profile')=='intelligence',
        'decision-grade competitive position must use existing auditable intelligence completion profile')
    req(contains_all(body,'evidence-closure','material competitor','requested/material dimension'),
        'competitive position must maintain proportionate decision-relevant evidence closure')
    req(contains_all(body,'run-local','intelligence analysis record'),
        'competitive position must preserve auditable analysis behind the human synthesis')

    profiling=(ROOT/'systems/competitor-intelligence/contracts/analysis/profiling/CONTEXT.md').read_text()
    coverage=(ROOT/'systems/competitor-intelligence/contracts/research/adaptive-source-coverage/CONTEXT.md').read_text()
    req('SourceRecord.subject_refs' in profiling,
        'competitor profiling must preserve resolved subject provenance')
    req(contains_all(coverage,'subject/evidence mismatches','supported','limited','unknown','not_material'),
        'adaptive source coverage must track decision-relative closure rather than raw source count')

    print('shared intelligence evidence-closure regressions passed: provenance is subject-scoped, confidence is evidence-bounded, and decision-grade synthesis must close material evidence gaps')

if __name__=='__main__': main()
