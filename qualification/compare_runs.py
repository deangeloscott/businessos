#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from common import read_json, write_json

GOOD={'ACCEPTABLE','COMPETITIVE','EXCEPTIONAL'}
BAD={'FAIL','FUNCTIONAL-NOT-ACCEPTABLE'}

def index_results(run_dir):
    rows=read_json(Path(run_dir)/'evaluator/hard-and-merged-results.json')
    if rows is None: raise SystemExit(f'Evaluation results missing in {run_dir}')
    return {x['event_id']:x for x in rows}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('run_a'); ap.add_argument('run_b'); ap.add_argument('--out'); a=ap.parse_args()
    ra=Path(a.run_a).expanduser().resolve(); rb=Path(a.run_b).expanduser().resolve(); A=index_results(ra); B=index_results(rb); ids=sorted(set(A)|set(B)); rows=[]
    for eid in ids:
        x=A.get(eid); y=B.get(eid); va=(x or {}).get('verdict','MISSING'); vb=(y or {}).get('verdict','MISSING')
        failed_a=sorted(g for g,v in (x or {}).get('hard_gates',{}).items() if not v); failed_b=sorted(g for g,v in (y or {}).get('hard_gates',{}).items() if not v)
        if va in GOOD and vb in GOOD: classification='ROBUST-PASS'
        elif va in BAD and vb in BAD: classification='REPEATED-FAILURE / AURA-HOTSPOT'
        elif va=='BLOCKED-EXTERNAL' or vb=='BLOCKED-EXTERNAL': classification='ENVIRONMENT-SENSITIVE'
        else: classification='CANDIDATE-SENSITIVE'
        rows.append({'event_id':eid,'run_a_verdict':va,'run_b_verdict':vb,'run_a_score':(x or {}).get('overall_quality_score'),'run_b_score':(y or {}).get('overall_quality_score'),'run_a_failed_gates':failed_a,'run_b_failed_gates':failed_b,'common_failed_gates':sorted(set(failed_a)&set(failed_b)),'classification':classification})
    counts={}
    for r in rows: counts[r['classification']]=counts.get(r['classification'],0)+1
    out=Path(a.out).expanduser().resolve() if a.out else ra.parent/f'comparison-{ra.name}-vs-{rb.name}.json'; write_json(out,{'run_a':str(ra),'run_b':str(rb),'counts':counts,'events':rows})
    md=out.with_suffix('.md'); lines=['# AURA Qualification Run Comparison','',f'- Run A: `{ra}`',f'- Run B: `{rb}`','','## Summary','']+[f'- **{k}**: {v}' for k,v in sorted(counts.items())]+['','## Repeated AURA hotspots','']
    hot=[r for r in rows if r['classification']=='REPEATED-FAILURE / AURA-HOTSPOT']; lines += [f"- `{r['event_id']}` — common failed gates: {', '.join(r['common_failed_gates']) or 'quality/result failure'}" for r in hot] or ['- None']
    md.write_text('\n'.join(lines)+'\n',encoding='utf-8'); print(json.dumps({'json':str(out),'markdown':str(md),'counts':counts},indent=2))
if __name__=='__main__': main()
