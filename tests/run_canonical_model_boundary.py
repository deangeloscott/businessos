#!/usr/bin/env python3
"""Protect AURA's canonical organization-state boundary without freezing its taxonomy.

Workflows may use any sound implementation method available to the active model/harness,
but durable reads/writes/context must stay inside the explicit organization-owned model.
Auxiliary runtime/config/package schemas must not quietly become required business state.
This regression protects those boundaries, not today's exact object count.
"""
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

from _common import workflow_files,read_frontmatter,selector_type
from canonical_store import INSTANCE_PATHS,schema_entry


def req(condition,message):
    if not condition: raise AssertionError(message)


def main():
    canonical=set(INSTANCE_PATHS)
    req(canonical,'canonical organization model must contain at least one durable type')

    retired={
        'Approval','ActionPacket','EventReactionDecision','ReactiveMonitoringProfile','BusinessOSEventConsumerProfile',
        'CapabilityBinding','CapabilityPack','ProviderCapabilitySnapshot','ProviderCompanionProfile',
        'ProviderEventInteroperability','ProviderPreferences','ProviderRegistry','SchedulerBindings','OperatorProfile',
        'PlaybookEvolutionProposal','WorkflowEvolutionProposal'
    }
    req(not (retired&canonical),f'retired authority/runtime/proposal type re-entered canonical state: {sorted(retired&canonical)}')

    # Support/interface schemas are deliberately outside canonical organization state.
    for typ in ('Run','PublisherMetadata','WorkspaceProfile','InnovationPackage','InnovationExchangeEntry','InnovationExchangeIndex'):
        req(typ not in canonical,f'support/interface type {typ} must not become canonical merely because a schema exists')

    # Canonical state belongs to organization-owned namespaces, never product/runtime/config surfaces.
    for typ,rel in INSTANCE_PATHS.items():
        top=str(rel).split('/',1)[0]
        req(top not in {'runtime','config','distribution','generated'},f'{typ} canonical state leaked into non-organization namespace: {rel}')

    # The organization owns durable memory. Operating-knowledge areas may classify semantic
    # domain where useful, but canonical truth must not belong to or be produced by an AURA
    # subsystem. This is intentionally dynamic so new canonical types inherit the invariant.
    retired_ownership_fields={'owner_system','owner_systems','producer_system'}
    for typ in canonical:
        _,schema=schema_entry(typ)
        props=set((schema.get('properties') or {}))
        leaked=sorted(retired_ownership_fields & props)
        req(not leaked,f'{typ} canonical schema reintroduced internal AURA ownership/producer fields: {leaked}')

    # Organization initialization must derive durable directories from the same canonical
    # model rather than a second hand-maintained list.
    init_text=(ROOT/'scripts/init_business.py').read_text()
    req('from canonical_store import INSTANCE_PATHS' in init_text,'init_business must derive organization directories from canonical_store.INSTANCE_PATHS')
    req('operations/action-packets' not in init_text and 'operations/approvals' not in init_text,'retired ActionPacket/Approval directories re-entered organization initialization')

    # ContextUpdateProposal is unresolved organizational memory, not Approval by another name.
    proposal_schema=json.loads((ROOT/'core/schemas/context/context-update-proposal.schema.json').read_text())
    proposal_props=proposal_schema.get('properties',{})
    req('approval_ref' not in proposal_props,'ContextUpdateProposal reintroduced an approval token')
    statuses=set((proposal_props.get('status') or {}).get('enum') or [])
    req(not ({'approval_required','approved'}&statuses),f'ContextUpdateProposal reintroduced approval lifecycle states: {sorted(statuses)}')
    req(statuses=={'proposed','applied','rejected','superseded','withdrawn'},f'ContextUpdateProposal lifecycle drifted from unresolved-context semantics: {sorted(statuses)}')
    req('decision_ref' in proposal_props,'ContextUpdateProposal should optionally link a real DecisionRecord when a decision resolves the proposal')

    # IndustryEvent is the evolving factual external event. Materiality interpretation belongs
    # in Insights/decisions rather than generic scoring or domain-routing fields on the event.
    event_schema=json.loads((ROOT/'systems/industry-intelligence/schemas/industry-event.schema.json').read_text())
    event_props=set((event_schema.get('properties') or {}))
    event_ghosts={'relevance','urgency','confidence','affected_domain_candidates'} & event_props
    req(not event_ghosts,f'IndustryEvent reintroduced interpretive scoring/routing fields: {sorted(event_ghosts)}')

    common=(ROOT/'scripts/_common.py').read_text()
    req('def provider_registry(' not in common,'retired provider registry helper re-entered shared Core mechanics')
    req('|act|' not in common and '|apr|' not in common,'retired ActionPacket/Approval reference prefixes re-entered shared reference scanning')
    req('def contract_files(' not in common,'retired contract-file compatibility helper re-entered shared Core mechanics')

    errors=[]
    for path in workflow_files():
        meta,_=read_frontmatter(path)
        rel=path.relative_to(ROOT)
        req(meta.get('type')=='workflow',f'{rel}: detailed operating knowledge must be typed workflow')
        for selector in meta.get('reads',[]) or []:
            typ=selector_type(selector)
            if typ not in canonical: errors.append(f'{rel}: read type {typ} is outside canonical organization state')
            if isinstance(selector,dict):
                stale=sorted({'owner_system','owner_scope'} & set(selector))
                if stale:errors.append(f'{rel}: canonical read selector reintroduced internal ownership fields {stale}; use semantic domain/scope when classification is useful')
                unsupported=sorted(set(selector)-{'type','domain','scope'})
                if unsupported:errors.append(f'{rel}: unsupported canonical read selector keys {unsupported}')
        for item in meta.get('writes',[]) or []:
            typ=selector_type(item)
            if typ not in canonical: errors.append(f'{rel}: write type {typ} is outside canonical organization state')
        for typ in meta.get('context',[]) or []:
            if typ not in canonical: errors.append(f'{rel}: context type {typ} is outside canonical organization state')
    req(not errors,'\n'.join(errors[:100]))

    print(f'canonical model boundary passed: {len(canonical)} current organization-owned object types; taxonomy remains simplifiable')


if __name__=='__main__':main()
