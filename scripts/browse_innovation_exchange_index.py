#!/usr/bin/env python3
from innovation_common import validate_schema
from pathlib import Path
import argparse,json,re

def browse(index_path,query=None,owner_system=None,detail_level=None):
    idx=json.loads(Path(index_path).read_text());validate_schema('InnovationExchangeIndex',idx);q=(query or '').lower().strip();words=set(re.findall(r'[a-z0-9]{2,}',q));rows=[]
    for e in idx['entries']:
        if owner_system and e['owner_system']!=owner_system:continue
        if detail_level and e['detail_level']!=detail_level:continue
        hay=' '.join([e['title'],e['purpose'],e['owner_system'],e.get('target_contract_id') or '',e.get('local_contract_id') or '']).lower();score=sum(1 for w in words if w in hay) if words else 0
        if q and score==0 and q not in hay:continue
        row=dict(e);row['match_score']=score;rows.append(row)
    rows.sort(key=lambda x:(x['match_score'],x['title']),reverse=True);return {'exchange_id':idx['exchange_id'],'generated_at':idx['generated_at'],'entries':rows}

def main():
    ap=argparse.ArgumentParser(description='Browse/search a portable Innovation Exchange index. Download/import remain explicit separate actions.');ap.add_argument('index_path');ap.add_argument('--query');ap.add_argument('--owner-system');ap.add_argument('--detail-level');a=ap.parse_args()
    try:result=browse(a.index_path,a.query,a.owner_system,a.detail_level)
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
