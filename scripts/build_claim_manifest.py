#!/usr/bin/env python3
from _common import *
from html.parser import HTMLParser
import argparse, json, re

class _Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,data):
        if data and data.strip(): self.parts.append(data.strip())

def _text(path):
    raw=Path(path).read_text(errors='replace')
    if str(path).lower().endswith(('.html','.htm')):
        p=_Text(); p.feed(raw); raw='\n'.join(p.parts)
    raw=re.sub(r'```.*?```',' ',raw,flags=re.S)
    raw=re.sub(r'[#*_>`~]+',' ',raw)
    return re.sub(r'[ \t]+',' ',raw)

def _units(text):
    out=[]
    for line in text.splitlines():
        line=line.strip(' -\t')
        if not line: continue
        parts=re.split(r'(?<=[.!?])\s+',line)
        for p in parts:
            p=p.strip()
            if len(p)>=4 and p not in out: out.append(p)
    return out

def business_name(business_id):
    p=ROOT/'instances'/business_id/'context/business.json'
    if p.exists():
        try:return json.loads(p.read_text()).get('name') or business_id
        except Exception:pass
    return business_id

def is_candidate(sentence,name):
    """Return customer-facing statements that need explicit classification.

    In addition to named/first-person business claims, conservatively capture operational
    promises that models often invent without naming the business: timing/duration, setup,
    availability/absolutes, demos/walkthroughs, and assurance language. False positives are
    acceptable here because the manifest can classify genuinely non-business guidance;
    false negatives can silently create an unsupported business promise.
    """
    s=sentence.lower(); n=(name or '').lower()
    if n and n in s:return True
    if re.search(r"\b(we|we'll|we’re|we're|our|ours|us)\b",s):return True
    if re.search(r'\byou\s+(get|receive|will receive|can expect|will get|are guaranteed)\b',s):return True
    if re.search(r'\b\d+\s*[- ]?(?:minute|hour|day|week|month|year)s?\b',s):return True
    if re.search(r'\b(?:no|zero)\s+(?:setup|cost|fee|fees|commitment|contract|obligation|downtime)\b',s):return True
    if re.search(r'\b(?:demo|walkthrough|onboarding|setup)\b',s) and re.search(r'\b(?:book|see|schedule|start|required?|takes?|within|minute|hour|day|week|no)\b',s):return True
    if re.search(r'\b(?:nothing|everything|always|never|ensure|ensures|ensured|make sure|makes sure|guarantee|guarantees|guaranteed)\b',s):return True
    return False

def scan_claims(business_id,asset_file):
    name=business_name(business_id)
    return [x for x in _units(_text(asset_file)) if is_candidate(x,name)]

def main():
    ap=argparse.ArgumentParser(description='Scan a customer-facing artifact for business-specific/promise-like statements that need claim-manifest classification.')
    ap.add_argument('business_id');ap.add_argument('asset_file');a=ap.parse_args()
    p=Path(a.asset_file)
    if not p.is_absolute():p=ROOT/p
    if not p.exists():raise SystemExit(f'Asset file not found: {p}')
    print(json.dumps({'business_id':a.business_id,'asset_file':str(p.relative_to(ROOT)),'candidates':scan_claims(a.business_id,p)},indent=2))
if __name__=='__main__':main()
