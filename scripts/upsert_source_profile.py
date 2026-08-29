#!/usr/bin/env python3
"""Create or update a business-scoped external SourceProfile deterministically."""
from _common import *
from jsonschema import Draft202012Validator
from urllib.parse import urlsplit, urlunsplit
import argparse, hashlib, json, os

KINDS = {
    "official","regulator","primary_researcher","academic","publication","practitioner",
    "vendor","data_provider","community","social_account","other"
}
WATCH = {"seed","candidate","active","deprioritized","blocked","unavailable"}
PRIORITIES = {"low","medium","high"}
OUTCOMES = {"original","supported","contradicted"}
METHOD_QUALITY = {"unknown","weak","mixed","strong"}
QUALITY_RANK = {"unknown":0,"weak":1,"mixed":2,"strong":3}
SUBJECT_KINDS = {"organization","person","brand","product","creator","publication","channel","platform","regulator","community","other"}
SUBJECT_RELATIONSHIPS = {"own_organization","competitor","substitute","partner","creator","thought_leader","publication","regulator","platform","vendor","benchmark","ecosystem_actor","monitored_subject","other"}
SOURCE_MODALITIES = {"text","image","audio","video","document","structured","mixed"}

def _normalized_reference(value):
    """Normalize only URL components that are semantically case-insensitive.

    Scheme/host casing, default ports, and trailing path slashes should not create
    duplicate SourceProfiles. Path/query/fragment casing is preserved because it
    can be semantically meaningful on real web servers.
    """
    value = " ".join(str(value or "").strip().split())
    if not value:
        raise ValueError("source_reference is required")
    parts = urlsplit(value)
    if parts.scheme.lower() in {"http", "https"} and parts.netloc:
        if parts.username or parts.password:
            raise ValueError("source_reference URL must not contain embedded credentials")
        scheme = parts.scheme.lower()
        hostname = (parts.hostname or "").lower()
        try:
            port = parts.port
        except ValueError as e:
            raise ValueError(f"invalid source_reference URL: {e}") from e
        host = f"[{hostname}]" if ":" in hostname and not hostname.startswith("[") else hostname
        if port and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
            host = f"{host}:{port}"
        path = parts.path.rstrip("/")
        return urlunsplit((scheme, host, path, parts.query, parts.fragment))
    return value

def _profile_id(business_id, source_reference):
    canonical = _normalized_reference(source_reference)
    seed = f"{business_id}:{canonical}".encode("utf-8")
    return "sprof_" + hashlib.sha256(seed).hexdigest()[:16]

def _schema():
    return json.loads((ROOT/"core/schemas/intelligence/source-profile.schema.json").read_text())

def _validate(obj):
    errors = sorted(Draft202012Validator(_schema()).iter_errors(obj), key=lambda e:list(e.path))
    if errors:
        raise ValueError("SourceProfile invalid: " + "; ".join(f"{list(e.path)} {e.message}" for e in errors))

def _path(business_id, profile_id):
    return ROOT/"instances"/business_id/"intelligence"/"source-profiles"/f"{profile_id}.json"

def _merge_unique(old, new):
    return list(dict.fromkeys([*(old or []), *(new or [])]))

def _rebuild_assessments(events, previous):
    prior = {x.get("fact_type"):dict(x) for x in previous or [] if isinstance(x,dict) and x.get("fact_type")}
    grouped = {}
    for event in events:
        fact = event["fact_type"]
        grouped.setdefault(fact, []).append(event)
    out = []
    for fact in sorted(set(prior) | set(grouped)):
        base = prior.get(fact, {})
        evs = grouped.get(fact, [])
        quality = base.get("method_quality","unknown")
        for event in evs:
            q = event.get("method_quality","unknown")
            if QUALITY_RANK[q] > QUALITY_RANK.get(quality,0):
                quality = q
        original = sum(1 for e in evs if e["outcome"]=="original")
        supported = sum(1 for e in evs if e["outcome"]=="supported")
        contradicted = sum(1 for e in evs if e["outcome"]=="contradicted")
        if not evs:
            original = int(base.get("original_source_count",0))
            supported = int(base.get("later_supported_count",0))
            contradicted = int(base.get("later_contradicted_count",0))
        row = {
            "fact_type": fact,
            "sample_count": original + supported + contradicted,
            "original_source_count": original,
            "later_supported_count": supported,
            "later_contradicted_count": contradicted,
            "method_quality": quality,
            "last_evaluated_at": max([e.get("recorded_at") for e in evs if e.get("recorded_at")], default=base.get("last_evaluated_at")),
            "notes": base.get("notes")
        }
        out.append(row)
    return out

def upsert(args):
    base = ROOT/"instances"/args.business_id
    if not base.exists():
        raise ValueError(f"Unknown business: {args.business_id}")
    ref = _normalized_reference(args.source_reference)
    profile_id = _profile_id(args.business_id, ref)
    path = _path(args.business_id, profile_id)
    ts = now()
    if path.exists():
        obj = json.loads(path.read_text())
        if _normalized_reference(obj.get("source_reference")) != ref:
            raise ValueError("existing SourceProfile reference mismatch")
        obj["source_reference"] = ref
    else:
        obj = {
            "id":profile_id,"object_type":"SourceProfile","schema_version":"1.1.0",
            "business_id":args.business_id,"created_at":ts,"updated_at":ts,"lineage":[],
            "source_reference":ref,"display_name":None,"source_kind":"other","owner_systems":[],
            "topic_tags":[],"watch_status":"candidate","attention_priority":"medium",
            "discovery_reason":None,"commercial_context":None,
            "subject_key":None,"subject_name":None,"subject_kind":None,"subject_aliases":[],
            "subject_relationships":[],"source_modalities":[],"monitoring_questions":[],
            "material_change_signals":[],"last_material_change_at":None,
            "fact_type_assessments":[],"last_checked_at":None,"next_check_at":None,
            "extensions":{"external_learning":{"outcome_events":[]}}
        }

    for key, default in {
        "subject_key":None,"subject_name":None,"subject_kind":None,"subject_aliases":[],
        "subject_relationships":[],"source_modalities":[],"monitoring_questions":[],
        "material_change_signals":[],"last_material_change_at":None
    }.items():
        obj.setdefault(key, default)

    if args.display_name is not None: obj["display_name"] = args.display_name
    if args.source_kind is not None: obj["source_kind"] = args.source_kind
    if args.owner_system: obj["owner_systems"] = _merge_unique(obj.get("owner_systems"), args.owner_system)
    if args.topic_tag: obj["topic_tags"] = _merge_unique(obj.get("topic_tags"), args.topic_tag)
    if args.watch_status is not None: obj["watch_status"] = args.watch_status
    if args.attention_priority is not None: obj["attention_priority"] = args.attention_priority
    if args.discovery_reason is not None: obj["discovery_reason"] = args.discovery_reason
    if args.commercial_context is not None: obj["commercial_context"] = args.commercial_context
    if args.subject_key is not None: obj["subject_key"] = args.subject_key
    if args.subject_name is not None: obj["subject_name"] = args.subject_name
    if args.subject_kind is not None: obj["subject_kind"] = args.subject_kind
    if args.subject_alias: obj["subject_aliases"] = _merge_unique(obj.get("subject_aliases"), args.subject_alias)
    if args.subject_relationship: obj["subject_relationships"] = _merge_unique(obj.get("subject_relationships"), args.subject_relationship)
    if args.source_modality: obj["source_modalities"] = _merge_unique(obj.get("source_modalities"), args.source_modality)
    if args.monitoring_question: obj["monitoring_questions"] = _merge_unique(obj.get("monitoring_questions"), args.monitoring_question)
    if args.material_change_signal: obj["material_change_signals"] = _merge_unique(obj.get("material_change_signals"), args.material_change_signal)
    if args.last_material_change_at is not None: obj["last_material_change_at"] = args.last_material_change_at
    if args.last_checked_at is not None: obj["last_checked_at"] = args.last_checked_at
    if args.next_check_at is not None: obj["next_check_at"] = args.next_check_at

    ext = obj.setdefault("extensions",{}).setdefault("external_learning",{})
    events = ext.setdefault("outcome_events",[])
    if args.outcome:
        if not args.fact_type or not args.evidence_ref:
            raise ValueError("--outcome requires --fact-type and --evidence-ref")
        key = f"{args.fact_type}|{args.outcome}|{args.evidence_ref}"
        if not any(e.get("event_key")==key for e in events):
            events.append({
                "event_key":key,"fact_type":args.fact_type,"outcome":args.outcome,
                "evidence_ref":args.evidence_ref,"method_quality":args.method_quality or "unknown",
                "recorded_at":ts
            })
    obj["fact_type_assessments"] = _rebuild_assessments(events, obj.get("fact_type_assessments"))
    obj["updated_at"] = ts
    _validate(obj)

    path.parent.mkdir(parents=True,exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
    os.replace(tmp,path)
    return path,obj

def main():
    p=argparse.ArgumentParser(description="Create/update a SourceProfile. Source history changes discovery attention only; subject/watch history guides research attention and never proves a current claim.")
    p.add_argument("business_id")
    p.add_argument("--source-reference",required=True)
    p.add_argument("--display-name")
    p.add_argument("--source-kind",choices=sorted(KINDS))
    p.add_argument("--owner-system",action="append",choices=sorted(SYSTEMS))
    p.add_argument("--topic-tag",action="append")
    p.add_argument("--watch-status",choices=sorted(WATCH))
    p.add_argument("--attention-priority",choices=sorted(PRIORITIES))
    p.add_argument("--discovery-reason")
    p.add_argument("--commercial-context")
    p.add_argument("--subject-key")
    p.add_argument("--subject-name")
    p.add_argument("--subject-kind",choices=sorted(SUBJECT_KINDS))
    p.add_argument("--subject-alias",action="append")
    p.add_argument("--subject-relationship",action="append",choices=sorted(SUBJECT_RELATIONSHIPS))
    p.add_argument("--source-modality",action="append",choices=sorted(SOURCE_MODALITIES))
    p.add_argument("--monitoring-question",action="append")
    p.add_argument("--material-change-signal",action="append")
    p.add_argument("--last-material-change-at")
    p.add_argument("--last-checked-at")
    p.add_argument("--next-check-at")
    p.add_argument("--fact-type")
    p.add_argument("--outcome",choices=sorted(OUTCOMES))
    p.add_argument("--evidence-ref")
    p.add_argument("--method-quality",choices=sorted(METHOD_QUALITY))
    args=p.parse_args()
    try:
        path,obj=upsert(args)
    except ValueError as e:
        raise SystemExit(str(e))
    print(json.dumps({"path":str(path.relative_to(ROOT)),"id":obj["id"],"watch_status":obj["watch_status"],"attention_priority":obj["attention_priority"],"subject_key":obj.get("subject_key")},indent=2))

if __name__=="__main__":
    main()
