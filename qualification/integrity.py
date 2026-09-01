#!/usr/bin/env python3
"""Integrity helpers for AURA qualification.

Qualification protects the realism of the benchmark: event-specific evidence, evaluator
blindness, and non-templated deliverables. It does not require or interpret AURA Runs,
contract-execution manifests, subcontract ledgers, or production completion ceremonies.
"""
from pathlib import Path
from urllib.parse import urlparse
import difflib,hashlib,json,re

TEXT_EXTS={'.md','.txt','.html','.htm','.rst','.csv'}
EVALUATOR_MARKERS=(
    'evaluator/suite.json','evaluator\\suite.json','evaluator/queue.json','evaluator\\queue.json',
    'evaluator/product-snapshot.json','evaluator\\product-snapshot.json',
    'qualification/evaluate_run.py','qualification\\evaluate_run.py',
    'qualification/task_controller.py','qualification\\task_controller.py',
)


def resolve_workspace_ref(ref,workspace):
    if not isinstance(ref,str) or not ref.strip():return None
    p=Path(ref).expanduser()
    if not p.is_absolute():p=Path(workspace)/p
    try:return p.resolve()
    except OSError:return p


def existing_ref_paths(refs,workspace):
    out=[]
    for ref in refs or []:
        p=resolve_workspace_ref(ref,workspace)
        if p and p.exists() and p.is_file() and p.stat().st_size>0:out.append(p)
    return out


def _snapshot_files(checkpoint):
    snap=(checkpoint or {}).get('workspace') or {}
    return {str(x.get('path')).replace('\\','/'):x for x in snap.get('files',[]) if isinstance(x,dict) and x.get('path')}


def checkpoint_chain_contiguous(previous_after,current_before):
    prior=((previous_after or {}).get('workspace') or {}).get('digest');current=((current_before or {}).get('workspace') or {}).get('digest')
    return bool(prior and current and prior==current)


def event_specific_ref_paths(refs,before,after,workspace):
    before_files=_snapshot_files(before);after_files=_snapshot_files(after);out=[];ws=Path(workspace).resolve()
    for p in existing_ref_paths(refs,workspace):
        try:rel=p.resolve().relative_to(ws).as_posix()
        except ValueError:continue
        b=before_files.get(rel);a=after_files.get(rel)
        if a and (not b or b.get('sha256')!=a.get('sha256')):out.append(p)
    return out


def _unwrap_locator_text(value):
    value=value.strip();markdown=re.fullmatch(r'\[[^\]]*\]\((https?://[^)\s]+)\)',value,re.I)
    if markdown:return markdown.group(1)
    if value.startswith('<') and value.endswith('>'):
        inner=value[1:-1].strip()
        if re.match(r'^https?://',inner,re.I):return inner
    return value


def _source_locator_key(value,workspace):
    if isinstance(value,dict):value=next((value.get(k) for k in ('source_url','url','source_ref','source_reference','evidence_ref','reference') if value.get(k)),None)
    if not isinstance(value,str) or not value.strip():return None
    value=_unwrap_locator_text(value)
    if re.match(r'^https?://',value,re.I):
        host=(urlparse(value).hostname or '').lower().rstrip('.')
        if not host or host in {'localhost','example.com','example.org','example.net'} or host.endswith(('.invalid','.test','.localhost')):return None
        return value
    p=resolve_workspace_ref(value,workspace);return str(p) if p and p.exists() and p.is_file() else None


def _snapshot_views(data):
    if not isinstance(data,dict):return []
    out=[data];extensions=data.get('extensions')
    if isinstance(extensions,dict):
        out.append(extensions)
        for key in ('field_snapshot','research','search','serp','evidence','live_field'):
            nested=extensions.get(key)
            if isinstance(nested,dict):out.append(nested)
    return out


def is_reconstructable_field_snapshot(path,workspace):
    """Require dated field context plus at least two real independently resolvable sources."""
    try:data=json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return False
    views=_snapshot_views(data)
    captured=any(view.get(k) for view in views for k in ('captured_at','retrieved_at','observed_at','collected_at'))
    context=any(view.get(k) for view in views for k in ('query','search_query','intent','target_intent','target_query','surface','method','scope','research_question','channel','market_context','query_context','research_context'))
    sources=[]
    for view in views:
        for key in ('source_reference','source_url','url','source_ref','evidence_ref','reference'):
            if view.get(key):sources.append(view.get(key))
        for key in ('sources','source_refs','source_references','evidence_refs','competitive_set','comparisons','results','examples','analyzed_urls','visited_urls','retrieved_urls','observed_urls'):
            value=view.get(key)
            if isinstance(value,list):sources.extend(value)
    locators={key for item in sources if (key:=_source_locator_key(item,workspace))}
    return bool(captured and context and len(locators)>=2)


def reconstructable_field_snapshot_paths(refs,before,after,workspace):
    return [p for p in event_specific_ref_paths(refs,before,after,workspace) if is_reconstructable_field_snapshot(p,workspace)]


def normalized_text(path):
    p=Path(path)
    if p.suffix.lower() not in TEXT_EXTS:return ''
    try:text=p.read_text(encoding='utf-8',errors='ignore')
    except OSError:return ''
    text=text.lower();text=re.sub(r'run_[a-z0-9]+','<run>',text);text=re.sub(r'contract-[a-z0-9-]+','<event>',text);text=re.sub(r'20\d\d-\d\d-\d\d[t ][0-9:.+\-z]+','<time>',text);text=re.sub(r'\b[a-f0-9]{8,}\b','<id>',text);return re.sub(r'\s+',' ',text).strip()


def artifact_similarity_flags(results,threshold=0.88,max_examples=5):
    """Surface suspiciously similar cross-job artifacts without prescribing artifact form."""
    samples=[]
    for result in results:
        if result.get('kind')!='contract_acceptance':continue
        chosen=None;text=''
        for p in [Path(x) for x in result.get('actual_artifacts') or []]:
            text=normalized_text(p)
            if len(text)>=180:chosen=str(p);break
        if chosen:samples.append((result['event_id'],result.get('contract_id'),chosen,text))
    matches={eid:[] for eid,_,_,_ in samples}
    for i in range(len(samples)):
        e1,c1,p1,t1=samples[i]
        for j in range(i+1,len(samples)):
            e2,c2,p2,t2=samples[j]
            if c1==c2:continue
            ratio=difflib.SequenceMatcher(None,t1,t2,autojunk=True).ratio()
            if ratio<threshold:continue
            matches[e1].append({'other_event':e2,'other_contract':c2,'similarity':round(ratio,3),'artifact':p1,'other_artifact':p2});matches[e2].append({'other_event':e1,'other_contract':c1,'similarity':round(ratio,3),'artifact':p2,'other_artifact':p1})
    out={}
    for eid,items in matches.items():
        if not items:continue
        ranked=sorted(items,key=lambda x:(-x['similarity'],x['other_event']));out[eid]=[{'type':'high_artifact_similarity','match_count':len(items),'max_similarity':ranked[0]['similarity'],'examples':ranked[:max_examples]}]
    return out


def exact_duplicate_artifact_flags(results):
    by_hash={}
    for result in results:
        for raw in result.get('actual_artifacts') or []:
            path=Path(raw)
            try:digest=hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:continue
            by_hash.setdefault(digest,[]).append((result['event_id'],result.get('contract_id'),str(path)))
    flags={}
    for digest,items in by_hash.items():
        if len({x[0] for x in items})<2:continue
        for eid,cid,path in items:
            others=[{'event_id':oe,'contract_id':oc,'artifact':op} for oe,oc,op in items if oe!=eid]
            if others:flags.setdefault(eid,[]).append({'type':'exact_artifact_reuse','sha256':digest,'artifact':path,'others':others})
    return flags


def _strings(value):
    if isinstance(value,dict):
        for item in value.values():yield from _strings(item)
    elif isinstance(value,(list,tuple)):
        for item in value:yield from _strings(item)
    elif value is not None:yield str(value)


def _log_requested_evaluator_material(text):
    for raw in text.splitlines():
        line=raw.strip()
        if not line:continue
        try:payload=json.loads(line)
        except json.JSONDecodeError:
            if any(marker in line.lower() for marker in EVALUATOR_MARKERS):return True
            continue
        if not isinstance(payload,dict):continue
        step=payload.get('step_update') if isinstance(payload.get('step_update'),dict) else payload;info=step.get('tool_info') if isinstance(step.get('tool_info'),dict) else {};requested=[]
        if isinstance(info.get('parameters'),dict):requested.append(info['parameters'])
        for key in ('tool','command','command_line','input'):
            if step.get(key) is not None:requested.append(step[key])
        if any(marker in '\n'.join(_strings(requested)).lower() for marker in EVALUATOR_MARKERS):return True
    return False


def run_control_flags(run_dir,workspace=None):
    """Surface attempts to inspect/manipulate evaluator-private control surfaces.

    Ordinary batch automation, AURA helper use, or creating several artifacts is not a
    benchmark-integrity problem. The boundary is candidate access to evaluator-private
    specifications/queues/snapshots or candidate-authored benchmark-control scripts.
    """
    rd=Path(run_dir);flags=[]
    for p in sorted(rd.glob('*.py')):flags.append({'type':'candidate_authored_run_control_script','path':str(p)})
    for p in sorted((rd/'candidate').glob('*.py')) if (rd/'candidate').exists() else []:flags.append({'type':'candidate_authored_run_control_script','path':str(p)})
    roots=[]
    if workspace:
        ws=Path(workspace);roots.extend([ws/'scratch',ws/'runtime'])
    for root in roots:
        if not root.exists():continue
        for p in root.rglob('*'):
            if not p.is_file() or p.suffix.lower() not in {'.py','.sh','.md','.txt','.json'}:continue
            try:text=p.read_text(encoding='utf-8',errors='ignore').lower()
            except OSError:continue
            hits=sum(1 for marker in EVALUATOR_MARKERS if marker in text)
            if hits:flags.append({'type':'candidate_evaluator_spec_access','path':str(p),'marker_count':hits})
            if hits>=2 and re.search(r'\b(for|while)\b',text):flags.append({'type':'mass_completion_runner','path':str(p),'marker_count':hits,'reason':'loops over evaluator-private qualification surfaces'})
    for logs in (rd/'evaluator'/'logs',rd/'candidate-logs'):
        if not logs.exists():continue
        for p in sorted(logs.glob('*.stdout.log')):
            try:text=p.read_text(encoding='utf-8',errors='ignore').lower()
            except OSError:continue
            if _log_requested_evaluator_material(text):flags.append({'type':'candidate_evaluator_spec_access','path':str(p)})
    return flags
