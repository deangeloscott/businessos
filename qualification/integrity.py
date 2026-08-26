#!/usr/bin/env python3
from pathlib import Path
import difflib, hashlib, json, re

TEXT_EXTS={'.md','.txt','.html','.htm','.rst','.csv'}


def selector_types(items):
    out=set()
    for item in items or []:
        if isinstance(item,str):
            typ=item
        elif isinstance(item,dict):
            typ=item.get('type') or item.get('object_type')
        else:
            typ=None
        if isinstance(typ,str) and typ.strip(): out.add(typ.strip())
    return out


def resolve_workspace_ref(ref,workspace):
    if not isinstance(ref,str) or not ref.strip(): return None
    p=Path(ref).expanduser()
    if not p.is_absolute(): p=Path(workspace)/p
    try: return p.resolve()
    except OSError: return p


def existing_ref_paths(refs,workspace):
    out=[]
    for ref in refs or []:
        p=resolve_workspace_ref(ref,workspace)
        if p and p.exists() and p.is_file() and p.stat().st_size>0: out.append(p)
    return out


def _snapshot_files(checkpoint):
    snap=(checkpoint or {}).get('workspace') or {}
    return {x.get('path'):x for x in snap.get('files',[]) if isinstance(x,dict) and x.get('path')}


def event_specific_ref_paths(refs,before,after,workspace):
    before_files=_snapshot_files(before); after_files=_snapshot_files(after); out=[]
    ws=Path(workspace).resolve()
    for p in existing_ref_paths(refs,workspace):
        try: rel=str(p.resolve().relative_to(ws))
        except ValueError: continue
        b=before_files.get(rel); a=after_files.get(rel)
        if a and (not b or b.get('sha256')!=a.get('sha256')): out.append(p)
    return out


def _source_locator(value,workspace):
    if isinstance(value,dict):
        value=next((value.get(k) for k in ('source_url','url','source_ref','evidence_ref','reference') if value.get(k)),None)
    if not isinstance(value,str) or not value.strip():return False
    if re.match(r'^https?://',value.strip(),re.I):return True
    p=resolve_workspace_ref(value,workspace)
    return bool(p and p.exists() and p.is_file())


def is_reconstructable_field_snapshot(path,workspace):
    try:data=json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return False
    if not isinstance(data,dict) or not data.get('captured_at'):return False
    context=any(data.get(k) for k in ('query','surface','method','scope','research_question','channel'))
    sources=[]
    for key in ('sources','source_refs','evidence_refs'):
        value=data.get(key)
        if isinstance(value,list):sources.extend(value)
    for key in ('competitive_set','comparisons','results','examples'):
        value=data.get(key)
        if isinstance(value,list):sources.extend(value)
    locators=[x for x in sources if _source_locator(x,workspace)]
    return bool(context and len(locators)>=2)


def reconstructable_field_snapshot_paths(refs,before,after,workspace):
    return [p for p in event_specific_ref_paths(refs,before,after,workspace) if is_reconstructable_field_snapshot(p,workspace)]


def is_structured_prepublish_record(path):
    try: data=json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception: return False
    if not isinstance(data,dict): return False
    if data.get('contract_id')!='content.qa.pre-publish': return False
    if str(data.get('status','')).lower() not in {'pass','passed'}: return False
    checks=data.get('checks_performed',data.get('checks'))
    if not isinstance(checks,list) or not checks: return False
    for item in checks:
        if not isinstance(item,dict):return False
        if not any(item.get(k) for k in ('check','name','criterion','test')):return False
        if not any(item.get(k) is not None for k in ('status','result','outcome','passed')):return False
    if 'blockers' not in data: return False
    target=any(data.get(k) for k in ('tested_asset','target_asset','asset_ref','target_refs'))
    version=any(data.get(k) is not None for k in ('tested_version','asset_version','version'))
    return bool(target and version)


def structured_prepublish_refs(workspace,business_id,before,after,run_audit):
    refs=[]
    # Nested/recorded subcontract evidence inside the event's root Run(s).
    for audit in run_audit or []:
        manifest=audit.get('manifest') or {}
        entry=(manifest.get('contracts') or {}).get('content.qa.pre-publish') or {}
        refs.extend(entry.get('evidence_refs') or [])
    # A separate pre-publish Run completed during this event is also valid.
    before_runs={r.get('run_id'):(r.get('contract_id'),r.get('status')) for r in (before or {}).get('runs',[]) if r.get('run_id')}
    for r in (after or {}).get('runs',[]):
        if r.get('contract_id')!='content.qa.pre-publish' or r.get('status')!='completed': continue
        old=before_runs.get(r.get('run_id'))
        if old and old[1]=='completed': continue
        rd=Path(workspace)/'runtime'/'runs'/business_id/r['run_id']
        try: manifest=json.loads((rd/'contract-execution.json').read_text(encoding='utf-8'))
        except Exception: manifest={}
        refs.extend(manifest.get('root_evidence_refs') or [])
    paths=existing_ref_paths(refs,workspace)
    return [p for p in paths if is_structured_prepublish_record(p)]


def normalized_text(path):
    p=Path(path)
    if p.suffix.lower() not in TEXT_EXTS: return ''
    try: text=p.read_text(encoding='utf-8',errors='ignore')
    except OSError: return ''
    text=text.lower()
    text=re.sub(r'run_[a-z0-9]+','<run>',text)
    text=re.sub(r'contract-[a-z0-9-]+','<event>',text)
    text=re.sub(r'20\d\d-\d\d-\d\d[t ][0-9:.+\-z]+','<time>',text)
    text=re.sub(r'\b[a-f0-9]{8,}\b','<id>',text)
    text=re.sub(r'\s+',' ',text).strip()
    return text


def artifact_similarity_flags(results,threshold=0.88,max_examples=5):
    """Return one compressed similarity warning per affected event.

    Pairwise comparisons are still performed so templated/mass-generated work is
    detected, but thousands of mirrored pair flags are collapsed into a count,
    maximum similarity, and a few strongest examples for human/AI review.
    """
    samples=[]
    for r in results:
        if r.get('kind')!='contract_acceptance': continue
        paths=[Path(p) for p in r.get('actual_artifacts') or []]
        text=''; chosen=None
        for p in paths:
            text=normalized_text(p)
            if len(text)>=180:
                chosen=str(p); break
        if chosen: samples.append((r['event_id'],r.get('contract_id'),chosen,text))

    matches={eid:[] for eid,_,_,_ in samples}
    for i in range(len(samples)):
        e1,c1,p1,t1=samples[i]
        for j in range(i+1,len(samples)):
            e2,c2,p2,t2=samples[j]
            if c1==c2: continue
            ratio=difflib.SequenceMatcher(None,t1,t2,autojunk=True).ratio()
            if ratio< threshold: continue
            matches[e1].append({'other_event':e2,'other_contract':c2,'similarity':round(ratio,3),'artifact':p1,'other_artifact':p2})
            matches[e2].append({'other_event':e1,'other_contract':c1,'similarity':round(ratio,3),'artifact':p2,'other_artifact':p1})

    out={}
    for eid,items in matches.items():
        if not items: continue
        ranked=sorted(items,key=lambda x:(-x['similarity'],x['other_event']))
        out[eid]=[{
            'type':'high_artifact_similarity',
            'match_count':len(items),
            'max_similarity':ranked[0]['similarity'],
            'examples':ranked[:max_examples],
        }]
    return out


def exact_duplicate_artifact_flags(results):
    by_hash={}
    for r in results:
        for p in r.get('actual_artifacts') or []:
            path=Path(p)
            try: digest=hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError: continue
            by_hash.setdefault(digest,[]).append((r['event_id'],r.get('contract_id'),str(path)))
    flags={}
    for digest,items in by_hash.items():
        events={x[0] for x in items}
        if len(events)<2: continue
        for eid,cid,path in items:
            others=[{'event_id':oe,'contract_id':oc,'artifact':op} for oe,oc,op in items if oe!=eid]
            if others: flags.setdefault(eid,[]).append({'type':'exact_artifact_reuse','sha256':digest,'artifact':path,'others':others})
    return flags


def integrity_hard_failure(flags):
    for flag in flags or []:
        if flag.get('type')=='exact_artifact_reuse':return True
        if flag.get('type')=='high_artifact_similarity' and flag.get('match_count',0)>=2:return True
    return False


def run_control_flags(run_dir):
    rd=Path(run_dir)
    flags=[]
    for p in sorted(rd.glob('*.py')):
        flags.append({'type':'candidate_authored_run_control_script','path':str(p)})
    for p in sorted((rd/'candidate').glob('*.py')) if (rd/'candidate').exists() else []:
        flags.append({'type':'candidate_authored_run_control_script','path':str(p)})
    return flags
