#!/usr/bin/env python3
"""Regression checks for Core external ecosystem intelligence and domain radars."""
from pathlib import Path
import json, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from _common import read_frontmatter
from upsert_source_profile import _normalized_reference, _profile_id

CORE_IDS = {
    "core.intelligence.ecosystem-radar",
    "core.intelligence.ecosystem.source-discovery",
    "core.intelligence.ecosystem.evidence-triangulation",
    "core.intelligence.ecosystem.maintain-source-profile",
    "core.intelligence.ecosystem.route-learning",
}
DOMAIN_IDS = {
    "competitor.intelligence.ecosystem-radar",
    "customer.intelligence.ecosystem-radar",
    "industry.intelligence.ecosystem-radar",
    "seo.intelligence.ecosystem.tactic-radar",
    "content.intelligence.ecosystem-radar",
    "marketing.intelligence.ecosystem-radar",
    "customer-optimization.intelligence.ecosystem-radar",
}
REQUIRED_PHRASES = {
    "core.intelligence.ecosystem.source-discovery": [
        "known-source","semantic/open discovery","new authors/researchers/communities","discovery-only"
    ],
    "core.intelligence.ecosystem.evidence-triangulation": [
        "originating evidence","independent support","independent contradiction","echo","freshness","novelty"
    ],
    "core.intelligence.ecosystem.maintain-source-profile": [
        "discovery priors only","never use SourceProfile history as support"
    ],
    "core.intelligence.ecosystem.route-learning": [
        "ignore, watch, investigate, test, adopt","active-business applicability"
    ],
}

def contracts():
    out={}
    for p in ROOT.rglob("CONTEXT.md"):
        if "/contracts/" not in p.as_posix(): continue
        meta,body=read_frontmatter(p)
        if meta.get("id"): out[meta["id"]] = (p,meta,body)
    return out

def fail(msg):
    raise AssertionError(msg)

def main():
    cs=contracts()
    missing=(CORE_IDS|DOMAIN_IDS)-set(cs)
    if missing: fail("missing ecosystem contracts: "+", ".join(sorted(missing)))

    policy=(ROOT/"core/policies/external-learning.md")
    if not policy.exists(): fail("missing external-learning policy")
    ptext=policy.read_text()
    for phrase in ["watchlist is a seed","semantic variants","attention prior only","echo","Freshness is mechanism-specific","SourceRecord -> Observation -> Insight"]:
        if phrase not in ptext: fail(f"external-learning policy missing invariant: {phrase}")

    schema_path=ROOT/"core/schemas/intelligence/source-profile.schema.json"
    schema=json.loads(schema_path.read_text())
    if schema.get("title")!="SourceProfile" or schema.get("additionalProperties") is not False:
        fail("SourceProfile schema must be strict and titled SourceProfile")
    required=set(schema.get("required",[]))
    for field in ["source_reference","source_kind","owner_systems","watch_status","attention_priority","fact_type_assessments"]:
        if field not in required: fail(f"SourceProfile missing required field {field}")

    helper=(ROOT/"scripts/upsert_source_profile.py")
    htext=helper.read_text()
    for phrase in ["outcome_events","event_key","Source history changes discovery attention only"]:
        if phrase not in htext: fail(f"source profile helper missing {phrase}")

    # Equivalent URL spellings must resolve to one profile, while path case stays distinct.
    a="HTTPS://Example.COM:443/Research/Article/"
    b="https://example.com/Research/Article"
    if _normalized_reference(a) != b:
        fail("SourceProfile URL normalization must collapse scheme/host casing, default HTTPS port, and trailing slash")
    if _profile_id("test-business",a) != _profile_id("test-business",b):
        fail("equivalent SourceProfile URLs must generate the same deterministic id")
    if _profile_id("test-business",b) == _profile_id("test-business","https://example.com/research/article"):
        fail("SourceProfile normalization must preserve potentially case-sensitive URL paths")
    try:
        _normalized_reference("https://user:secret@example.com/research")
    except ValueError:
        pass
    else:
        fail("SourceProfile references must reject embedded URL credentials")

    for cid,phrases in REQUIRED_PHRASES.items():
        body=cs[cid][2]
        for phrase in phrases:
            if phrase not in body: fail(f"{cid} missing required behavior phrase: {phrase}")

    core_meta=cs["core.intelligence.ecosystem-radar"][1]

    if "schedule" in core_meta:
        fail("Core ecosystem radar must not reintroduce AURA-owned schedule metadata")

    if "SourceProfile" not in (core_meta.get("reads") or []):
        fail("Core ecosystem radar must reuse durable SourceProfile monitoring state")

    for field in ("reads", "writes"):
        if "MonitoringIntent" in (core_meta.get(field) or []):
            fail("Core ecosystem radar must not invent a duplicate MonitoringIntent canonical object")

    body=cs["core.intelligence.ecosystem-radar"][2]
    for phrase in [
        "active harness/runtime owns actual scheduling",
        "AURA does not implement the scheduler",
    ]:
        if phrase not in body:
            fail(f"Core radar must preserve runtime scheduling boundary: {phrase}")

    for cid in DOMAIN_IDS:
        meta=cs[cid][1]
        refs=[]
        sc=meta.get("subcontracts") or {}
        for kind in ("required","conditional"):
            for item in sc.get(kind,[]) or []:
                refs.append(item.get("id") if isinstance(item,dict) else item)
        for needed in ["core.intelligence.ecosystem.source-discovery","core.intelligence.ecosystem.evidence-triangulation"]:
            if needed not in refs: fail(f"{cid} does not use shared Core {needed}")

    route_expectations={
        "seo.intelligence.ecosystem.tactic-radar":["seo.learning.strategy-experiment-design","seo.learning.tactic-registry","seo.learning.tactic-promotion","seo.learning.tactic-deprecation"],
        "marketing.intelligence.ecosystem-radar":["marketing.experimentation.message-test","marketing.learning.domain-learning"],
        "customer-optimization.intelligence.ecosystem-radar":["customer-optimization.experimentation.lifecycle-test","customer-optimization.learning.domain-learning"],
        "customer.intelligence.ecosystem-radar":["customer.analysis.insight-refresh","customer.learning.domain-learning"],
        "competitor.intelligence.ecosystem-radar":["competitor.analysis.tactic-validation","competitor.learning.domain-learning"],
        "industry.intelligence.ecosystem-radar":["industry.analysis.event-verification","industry.analysis.materiality","industry.learning.domain-learning"],
        "content.intelligence.ecosystem-radar":["content.intelligence.trend-validation","content.learning.domain-learning"],
    }
    for cid,expected in route_expectations.items():
        meta=cs[cid][1]
        refs=[]
        for kind in ("required","conditional"):
            for item in (meta.get("subcontracts") or {}).get(kind,[]) or []:
                refs.append(item.get("id") if isinstance(item,dict) else item)
        for ref in expected:
            if ref not in refs: fail(f"{cid} missing end-to-end route {ref}")
            if ref not in cs: fail(f"{cid} routes to unknown contract {ref}")

    map_expected={
        "core/process-map.json":"core.intelligence.ecosystem-radar",
        "systems/competitor-intelligence/process-map.json":"competitor.intelligence.ecosystem-radar",
        "systems/customer-intelligence/process-map.json":"customer.intelligence.ecosystem-radar",
        "systems/industry-intelligence/process-map.json":"industry.intelligence.ecosystem-radar",
        "systems/seo-aeo/process-map.json":"seo.intelligence.ecosystem.tactic-radar",
        "systems/content-synthesis/process-map.json":"content.intelligence.ecosystem-radar",
        "systems/marketing-synthesis/process-map.json":"marketing.intelligence.ecosystem-radar",
        "systems/customer-optimization/process-map.json":"customer-optimization.intelligence.ecosystem-radar",
    }
    for rel,cid in map_expected.items():
        data=json.loads((ROOT/rel).read_text())
        if cid not in [a.get("entry_contract") for a in data.get("activities",[])]:
            fail(f"{rel} missing radar activity {cid}")

    print(f"ecosystem intelligence regressions passed: {len(CORE_IDS)} core + {len(DOMAIN_IDS)} domain radar contracts")

if __name__=="__main__":
    main()
