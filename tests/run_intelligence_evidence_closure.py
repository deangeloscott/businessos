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


def main():
    foundation=(ROOT/'core/policies/intelligence-foundation.md').read_text()
    evidence=(ROOT/'core/policies/research-evidence.md').read_text()
    completion=(ROOT/'core/policies/completion-evidence.md').read_text()

    for phrase in [
        'Evidence closure before confident synthesis',
        'Evidence about one subject does not silently become evidence about another subject',
        'A test threshold or decision rule may be deliberately chosen without pretending it is an evidence-based forecast',
    ]:
        req(phrase in foundation,f'shared intelligence foundation missing evidence-closure invariant: {phrase}')

    for phrase in [
        '## Evidence closure before decision-grade synthesis',
        '## Observation and Insight support',
        '### Subject relevance',
        'A bibliography detached from the claims is not enough',
        'A deliberately chosen test threshold, minimum detectable effect, stop rule, or success criterion is not a prediction',
    ]:
        req(phrase in evidence,f'research evidence policy missing shared closure rule: {phrase}')

    req('close evidence before confident synthesis' in completion,'completion policy must distinguish artifact existence from evidence-closed intelligence')

    schema=json.loads((ROOT/'core/schemas/intelligence/source-record.schema.json').read_text())
    subject_schema=(schema.get('properties') or {}).get('subject_refs') or {}
    req(subject_schema.get('type')=='array','SourceRecord must support resolved subject_refs')
    req(subject_schema.get('uniqueItems') is True,'SourceRecord subject_refs must be unique')

    source={'id':'src_vendor_a','subject_refs':['cmp_vendor_a']}
    matching={'id':'obs_vendor_a','subject_refs':['cmp_vendor_a']}
    mismatched={'id':'obs_vendor_b','subject_refs':['cmp_vendor_b']}
    unscoped={'id':'obs_market','subject_refs':[]}
    req(_subject_mismatch(matching,'obs_vendor_a',source,'src_vendor_a') is None,'matching subject-scoped evidence should remain valid')
    err=_subject_mismatch(mismatched,'obs_vendor_b',source,'src_vendor_a')
    req(err and 'cannot silently support another' in err,'cross-subject evidence mismatch must be rejected when both sides are resolved')
    req(_subject_mismatch(unscoped,'obs_market',source,'src_vendor_a') is None,'general/unresolved evidence must not be falsely rejected by subject matching')

    persist=(ROOT/'scripts/persist_research_bundle.py').read_text()
    req("'subject_refs':item.get('subject_refs',[])" in persist,'research persistence helper must preserve SourceRecord subject_refs')
    req('cannot attach Observation' in persist and 'cannot attach Insight' in persist,'competitor persistence must reject resolved wrong-subject canonical attachments')

    cpath=ROOT/'systems/competitor-intelligence/contracts/analysis/competitive-position/CONTEXT.md'
    meta,body=read_frontmatter(cpath)
    req(completion_spec(meta).get('profile')=='intelligence','decision-grade competitive position must use existing auditable intelligence completion profile')
    req('evidence-closure map' in body,'competitive position must maintain proportionate evidence closure')
    req('Run-local intelligence analysis record' in body,'competitive position must preserve auditable analysis behind the human synthesis')

    profiling=(ROOT/'systems/competitor-intelligence/contracts/analysis/profiling/CONTEXT.md').read_text()
    coverage=(ROOT/'systems/competitor-intelligence/contracts/research/adaptive-source-coverage/CONTEXT.md').read_text()
    req('SourceRecord.subject_refs' in profiling,'competitor profiling must preserve resolved subject provenance')
    req('subject/evidence mismatches' in coverage and '`supported`, `limited`, `unknown`, `not_material`' in coverage,'adaptive source coverage must track decision-relative closure rather than raw source count')

    print('shared intelligence evidence-closure regressions passed: provenance is subject-scoped, confidence is evidence-bounded, and decision-grade synthesis must close material evidence gaps')

if __name__=='__main__': main()
