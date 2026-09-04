#!/usr/bin/env python3
from _common import ROOT, now, workspace_root
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import argparse, hashlib, json, re, xml.etree.ElementTree as ET

INSPECTOR_VERSION='1.1'
LOCAL_EVIDENCE_METHOD='deterministic_local_site_inspection'

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_depth=0; self.title_parts=[]; self.metas=[]; self.links=[]; self.images=[]; self.scripts=[]; self._script=None; self._script_parts=[]; self.h1_depth=0; self.h1_parts=[]
    def handle_starttag(self,tag,attrs):
        a={k.lower():v for k,v in attrs if k}
        t=tag.lower()
        if t=='title': self.title_depth+=1
        elif t=='meta': self.metas.append(a)
        elif t=='a' and a.get('href') is not None: self.links.append(a.get('href'))
        elif t=='img': self.images.append(a)
        elif t=='script' and (a.get('type') or '').lower()=='application/ld+json': self._script=a; self._script_parts=[]
        elif t=='h1': self.h1_depth+=1
    def handle_endtag(self,tag):
        t=tag.lower()
        if t=='title' and self.title_depth: self.title_depth-=1
        elif t=='script' and self._script is not None:
            self.scripts.append(''.join(self._script_parts).strip()); self._script=None; self._script_parts=[]
        elif t=='h1' and self.h1_depth: self.h1_depth-=1
    def handle_data(self,data):
        if self.title_depth: self.title_parts.append(data)
        if self._script is not None: self._script_parts.append(data)
        if self.h1_depth: self.h1_parts.append(data)

def _sha(data:bytes): return hashlib.sha256(data).hexdigest()
def _fact_id(payload):
    raw=json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    return 'lfact_'+hashlib.sha256(raw).hexdigest()[:20]

def _fact(kind,path,**fields):
    payload={'kind':kind,'path':path,**fields}
    return {'id':_fact_id(payload),**payload,'rendered':render_fact(payload)}

def render_fact(f):
    p=f.get('path'); k=f.get('kind')
    if k=='html.title': return f"{p} title is {f.get('value')!r}."
    if k=='html.h1': return f"{p} H1 is {f.get('value')!r}."
    if k=='html.meta_description':
        return f"{p} meta description is {f.get('value')!r}." if f.get('present') else f"{p} has no meta description."
    if k=='html.canonical':
        return f"{p} canonical is {f.get('value')!r}." if f.get('present') else f"{p} has no canonical tag."
    if k=='html.meta_robots':
        return f"{p} meta robots is {f.get('value')!r}." if f.get('present') else f"{p} has no meta robots directive."
    if k=='html.jsonld_block':
        if f.get('valid'):
            return f"{p} JSON-LD block {f.get('block_index')} is valid JSON with @context {f.get('context')!r} and @type {f.get('schema_type')!r}."
        return f"{p} JSON-LD block {f.get('block_index')} is invalid JSON: {f.get('parse_error')}."
    if k=='html.jsonld_count': return f"{p} contains {f.get('value')} JSON-LD block(s)."
    if k=='html.internal_link':
        state='resolves to an existing local file' if f.get('target_exists') else 'does not resolve to an existing local file'
        return f"{p} links to {f.get('href')!r}, which {state}."
    if k=='html.image_alt':
        if f.get('alt_present'): return f"{p} image {f.get('src')!r} has alt text {f.get('alt')!r}."
        return f"{p} image {f.get('src')!r} has no alt text."
    if k=='robots.disallow': return f"robots.txt disallows path prefix {f.get('value')!r} for user-agent {f.get('user_agent')!r}."
    if k=='sitemap.url': return f"sitemap.xml includes URL {f.get('value')!r}."
    if k=='page.sitemap_membership':
        state='is included in' if f.get('included') else 'is not included in'
        return f"{p} expected URL {f.get('expected_url')!r} {state} sitemap.xml."
    if k=='page.robots_blocked':
        state='is blocked' if f.get('blocked') else 'is not blocked'
        return f"{p} {state} by the parsed robots.txt rules for user-agent '*'."
    return f"{p} {k}: {f.get('value')!r}."

def render_observation_statement(facts):
    return 'Direct deterministic site inspection established: ' + ' '.join(f['rendered'] for f in facts)

def _meta(parser,name):
    name=name.lower()
    for m in parser.metas:
        if (m.get('name') or '').lower()==name: return m.get('content')
    return None

def _canonical(parser):
    # HTMLParser link collection only stores href; inspect raw parser attrs is not retained, so canonical is parsed separately by regex in inspect_html.
    return None

def _resolve_local_target(root:Path,current_rel:str,href:str):
    href=href.split('#',1)[0].split('?',1)[0]
    if not href or href.startswith(('http://','https://','mailto:','tel:','javascript:')): return None,None
    if href.startswith('/'):
        rel=href.lstrip('/')
    else:
        rel=(Path(current_rel).parent/href).as_posix()
    if rel.endswith('/'): rel += 'index.html'
    target=(root/rel)
    return rel,target.exists()

def _robots_rules(text):
    ua='*'; out=[]
    for raw in text.splitlines():
        line=raw.split('#',1)[0].strip()
        if not line or ':' not in line: continue
        key,val=[x.strip() for x in line.split(':',1)]
        if key.lower()=='user-agent': ua=val or '*'
        elif key.lower()=='disallow' and val: out.append((ua,val))
    return out

def _blocked(path, rules):
    slash='/'+path.lstrip('/')
    for ua,prefix in rules:
        if ua in {'*',''} and prefix and slash.startswith(prefix): return True
    return False

def _site_base(sitemap_urls, root):
    for u in sitemap_urls:
        try:
            q=urlparse(u)
            if q.scheme and q.netloc: return f'{q.scheme}://{q.netloc}'
        except Exception: pass
    # fallback to canonical-like strings discovered later is intentionally omitted; absence is better than guessed base.
    return None

def source_identity(source_locator):
    locator=Path(str(source_locator)).as_posix().rstrip('/') or '.'
    return 'sha256:'+_sha(locator.encode('utf-8'))

def build_manifest(source_root, business_id=None, captured_at=None, source_locator=None):
    root=Path(source_root).resolve()
    if not root.exists() or not root.is_dir(): raise ValueError(f'not a directory: {source_root}')
    files=[]; all_facts=[]
    paths=sorted(p for p in root.rglob('*') if p.is_file())
    snapshot_parts=[]
    for p in paths:
        rel=p.relative_to(root).as_posix(); data=p.read_bytes(); digest=_sha(data)
        snapshot_parts.append(f'{rel}\0{digest}\n')
        files.append({'path':rel,'sha256':'sha256:'+digest,'size_bytes':len(data)})
    snapshot='sha256:'+_sha(''.join(snapshot_parts).encode('utf-8'))

    robots_text=(root/'robots.txt').read_text(errors='replace') if (root/'robots.txt').exists() else ''
    rules=_robots_rules(robots_text)
    for ua,val in rules: all_facts.append(_fact('robots.disallow','robots.txt',user_agent=ua,value=val))

    sitemap_urls=[]
    sm=root/'sitemap.xml'
    if sm.exists():
        try:
            tree=ET.fromstring(sm.read_text(errors='replace'))
            for el in tree.iter():
                if el.tag.split('}')[-1]=='loc' and el.text and el.text.strip(): sitemap_urls.append(el.text.strip())
        except Exception:
            sitemap_urls=[]
    for u in sitemap_urls: all_facts.append(_fact('sitemap.url','sitemap.xml',value=u))
    base=_site_base(sitemap_urls,root)

    for p in sorted(root.rglob('*.html')):
        rel=p.relative_to(root).as_posix(); text=p.read_text(errors='replace'); parser=PageParser(); parser.feed(text)
        title=' '.join(''.join(parser.title_parts).split())
        h1=' '.join(''.join(parser.h1_parts).split())
        all_facts.append(_fact('html.title',rel,value=title))
        all_facts.append(_fact('html.h1',rel,value=h1))
        desc=_meta(parser,'description'); all_facts.append(_fact('html.meta_description',rel,present=desc is not None,value=desc))
        robots=_meta(parser,'robots'); all_facts.append(_fact('html.meta_robots',rel,present=robots is not None,value=robots))
        m=re.search(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*\bhref=["\']([^"\']+)["\']|<link\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\']canonical["\']',text,re.I)
        canon=(m.group(1) or m.group(2)) if m else None
        all_facts.append(_fact('html.canonical',rel,present=canon is not None,value=canon))
        all_facts.append(_fact('html.jsonld_count',rel,value=len(parser.scripts)))
        for i,raw in enumerate(parser.scripts,1):
            try:
                obj=json.loads(raw); context=obj.get('@context') if isinstance(obj,dict) else None; typ=obj.get('@type') if isinstance(obj,dict) else None
                all_facts.append(_fact('html.jsonld_block',rel,block_index=i,valid=True,context=context,schema_type=typ,parse_error=None))
            except Exception as e:
                all_facts.append(_fact('html.jsonld_block',rel,block_index=i,valid=False,context=None,schema_type=None,parse_error=str(e)))
        for href in sorted(set(parser.links)):
            target_rel,exists=_resolve_local_target(root,rel,href)
            if target_rel is not None: all_facts.append(_fact('html.internal_link',rel,href=href,target_path=target_rel,target_exists=bool(exists)))
        for img in parser.images:
            src=img.get('src') or ''; alt=img.get('alt')
            all_facts.append(_fact('html.image_alt',rel,src=src,alt_present=alt is not None and alt!='',alt=alt))
        if base:
            expected=base+'/'+rel
            all_facts.append(_fact('page.sitemap_membership',rel,expected_url=expected,included=expected in sitemap_urls))
        all_facts.append(_fact('page.robots_blocked',rel,blocked=_blocked(rel,rules)))

    all_facts=sorted(all_facts,key=lambda f:(f['path'],f['kind'],f['id']))
    locator=Path(str(source_locator if source_locator is not None else root)).as_posix().rstrip('/') or '.'
    return {
        'format_version':'1.1','evidence_type':'local_site_inspection','inspector':'scripts/inspect_site_evidence.py','inspector_version':INSPECTOR_VERSION,
        'business_id':business_id,'source_root':locator,'source_identity':source_identity(locator),'captured_at':captured_at or now(),'snapshot_hash':snapshot,
        'files':files,'facts':all_facts
    }

def _safe_rel(path):
    p=Path(path).resolve()
    try: return p.relative_to(workspace_root().resolve()).as_posix()
    except ValueError: raise ValueError('site root must be inside the BusinessOS workspace so evidence can be reproduced portably')

def persist_inspection(business_id,source_root):
    base=ROOT/'instances'/business_id
    if not base.exists(): raise ValueError(f'unknown business: {business_id}')
    source_abs=(ROOT/source_root).resolve() if not Path(source_root).is_absolute() else Path(source_root).resolve()
    source_rel=_safe_rel(source_abs)
    manifest=build_manifest(source_abs,business_id,source_locator=source_rel)
    sh=manifest['snapshot_hash'].split(':',1)[1]
    ih=manifest['source_identity'].split(':',1)[1]
    edir=base/'evidence/local-site'; edir.mkdir(parents=True,exist_ok=True)
    manifest_path=edir/f'site-inspection_{ih[:12]}_{sh[:16]}.json'
    sid=f'src_{business_id}_local-site_{ih[:10]}_{sh[:10]}'
    sp=base/'intelligence/sources'/f'{sid}.json'; sp.parent.mkdir(parents=True,exist_ok=True)

    # Same source locator + same content snapshot is idempotent. Never overwrite a
    # capture merely because a different locator has identical bytes.
    if manifest_path.exists():
        existing=json.loads(manifest_path.read_text())
        if existing.get('source_identity')!=manifest['source_identity'] or existing.get('snapshot_hash')!=manifest['snapshot_hash'] or existing.get('source_root')!=source_rel:
            raise ValueError(f'local evidence identity collision at {manifest_path.relative_to(ROOT)}')
        manifest=existing
    else:
        manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

    ts=manifest['captured_at']; rel_manifest=manifest_path.relative_to(ROOT).as_posix()
    source={
        'id':sid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,'created_at':ts,'updated_at':ts,
        'lineage':[],'source_type':'first_party_website_export','source_reference':source_rel,'origin':'user-provided local website/export',
        'retrieved_at':ts,'published_at':None,'content_hash':manifest['snapshot_hash'],'access_scope':'first_party_local',
        'extensions':{
            'businessos_evidence':{'capture_status':'captured','acquisition_method':'first_party_export','capture_method':LOCAL_EVIDENCE_METHOD,'asset_refs':[rel_manifest],'evidence_pointer':rel_manifest},
            'businessos_local_evidence':{'evidence_type':'local_site_inspection','inspector':'scripts/inspect_site_evidence.py','inspector_version':INSPECTOR_VERSION,'manifest_path':rel_manifest,'snapshot_hash':manifest['snapshot_hash'],'source_root':source_rel,'source_identity':manifest['source_identity']}
        }
    }
    if sp.exists():
        existing_source=json.loads(sp.read_text())
        ex=existing_source.get('extensions',{}).get('businessos_local_evidence',{})
        if existing_source.get('source_reference')!=source_rel or existing_source.get('content_hash')!=manifest['snapshot_hash'] or ex.get('source_identity')!=manifest['source_identity']:
            raise ValueError(f'local evidence SourceRecord identity collision: {sid}')
        source=existing_source
    else:
        sp.write_text(json.dumps(source,indent=2)+'\n')
    return source,manifest,manifest_path

def main():
    ap=argparse.ArgumentParser(description='Deterministically inspect a local website/export and preserve a reproducible evidence manifest plus SourceRecord.')
    ap.add_argument('business_id'); ap.add_argument('site_root')
    a=ap.parse_args()
    src,manifest,mp=persist_inspection(a.business_id,a.site_root)
    out={'source_ref':src['id'],'manifest_path':mp.relative_to(ROOT).as_posix(),'snapshot_hash':manifest['snapshot_hash'],'files':len(manifest['files']),'facts':len(manifest['facts']),
         'fact_index':[{'id':f['id'],'kind':f['kind'],'path':f['path'],'rendered':f['rendered']} for f in manifest['facts']]}
    print(json.dumps(out,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
