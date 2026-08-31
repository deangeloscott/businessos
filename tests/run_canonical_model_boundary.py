#!/usr/bin/env python3
"""Protect AURA's minimal canonical organization-state boundary.

Contracts may use provider-neutral capabilities and arbitrary implementation methods,
but their durable reads/writes must stay inside the explicit organization-owned model.
Auxiliary runtime/config/package schemas must not quietly become required business state.
"""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

from _common import contract_files,read_frontmatter,selector_type
from canonical_store import INSTANCE_PATHS


def req(condition,message):
    if not condition: raise AssertionError(message)


def main():
    canonical=set(INSTANCE_PATHS)

    required={
        'Business','BusinessClaim','PreferenceProfile','SourceRecord','Observation','Insight','ProofRecord',
        'DecisionRecord','Opportunity','Initiative','WorkRequest','AttentionItem','ChangeEvent','VerificationRecord',
        'Incident','Asset','MetricDefinition','MetricObservation','Experiment','OutcomeEvaluation','Learning'
    }
    req(required<=canonical,f'canonical organization model lost expected durable types: {sorted(required-canonical)}')

    retired={
        'Approval','ActionPacket','EventReactionDecision','ReactiveMonitoringProfile','BusinessOSEventConsumerProfile',
        'CapabilityBinding','CapabilityPack','ProviderCapabilitySnapshot','ProviderCompanionProfile',
        'ProviderEventInteroperability','ProviderPreferences','ProviderRegistry','SchedulerBindings','OperatorProfile'
    }
    req(not (retired&canonical),f'retired authority/runtime type re-entered canonical state: {sorted(retired&canonical)}')

    # Support/interface schemas are deliberately outside canonical organization state.
    for typ in ('Run','PublisherMetadata','WorkspaceProfile','InnovationPackage','InnovationExchangeEntry','InnovationExchangeIndex'):
        req(typ not in canonical,f'support/interface type {typ} must not become canonical merely because a schema exists')

    errors=[]
    for path in contract_files():
        meta,_=read_frontmatter(path)
        rel=path.relative_to(ROOT)
        for selector in meta.get('reads',[]) or []:
            typ=selector_type(selector)
            if typ not in canonical: errors.append(f'{rel}: read type {typ} is outside canonical organization state')
        for item in meta.get('writes',[]) or []:
            typ=selector_type(item)
            if typ not in canonical: errors.append(f'{rel}: write type {typ} is outside canonical organization state')
    req(not errors,'\n'.join(errors[:100]))

    print(f'canonical model boundary passed: {len(canonical)} organization-owned object types')


if __name__=='__main__':main()
