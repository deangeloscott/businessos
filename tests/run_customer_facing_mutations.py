#!/usr/bin/env python3
"""RC7 regressions for claim-safe mutation of existing customer-facing surfaces."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]; SCRIPTS=ROOT/'scripts'; sys.path.insert(0,str(SCRIPTS))
from bootstrap_explicit_context import build_objects, _path
from capture_customer_facing_state import capture
from build_mutation_claim_manifest import build
from validate_customer_facing_mutations import mutation_errors
from context_plan import build_plan
from validate_business import validate_business

BID='customer-facing-mutation-regression'; BASE=ROOT/'instances'/BID; WORK=ROOT/'runtime'/BID/'site'; ART=ROOT/'runtime'/BID/'artifacts'
SOURCE='My business is Northstar HVAC, a residential HVAC company serving the Baltimore area. We provide residential HVAC repair and residential HVAC replacement services. Our goal is qualified homeowner inquiries.'

def require(c,m):
    if not c: raise AssertionError(m)

def write_json(p,obj): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2)+'\n')

def reset_site():
    if WORK.exists(): shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    (WORK/'index.html').write_text('''<!doctype html><html><head><title>Northstar HVAC</title></head><body><h1>Northstar HVAC</h1><div class="card"><h2>Maintenance</h2><p>Looking for ongoing system care?</p><a href="/services/maintenance.html">Learn about maintenance</a></div></body></html>''')

def action_packet():
    return {'id':f'act_{BID}_edit','object_type':'ActionPacket','schema_version':'1.0.0','business_id':BID,'owner_system':'seo-aeo','opportunity_ref':f'opp_{BID}_fixture','status':'approved','actions':[],'extensions':{'businessos':{'origin':'preexisting'}}}

def change(before_rel,delta_rel,targets=None):
    targets=targets or [f'file:{WORK.relative_to(ROOT).as_posix()}/index.html']
    return {'id':f'chg_{BID}_edit','object_type':'ChangeEvent','schema_version':'1.0.0','business_id':BID,'action_packet_ref':f'act_{BID}_edit','target_refs':targets,'actions_applied':[],'executor':'test','status':'verified','timestamp':'2026-08-24T08:30:00Z','extensions':{'businessos':{'origin':'preexisting','customer_facing_mutations':[{'surface_root':WORK.relative_to(ROOT).as_posix(),'before_capture':before_rel,'claim_delta':delta_rel}]}}}

def capture_before(name):
    d=capture(BID,WORK); p=ART/f'{name}-before.json';write_json(p,d);return p

def delta_after(before,name):
    d=build(BID,before,WORK); p=ART/f'{name}-delta.json';write_json(p,d);return p,d

def main():
    if BASE.exists(): shutil.rmtree(BASE)
    if (ROOT/'runtime'/BID).exists(): shutil.rmtree(ROOT/'runtime'/BID)
    try:
        subprocess.run([sys.executable,str(SCRIPTS/'init_business.py'),BID,'--name','Northstar HVAC'],cwd=ROOT,check=True,capture_output=True,text=True)
        objs=build_objects(BID,industries=['residential HVAC'],markets=['Baltimore area'],services=['residential HVAC repair','residential HVAC replacement'],objectives=['qualified homeowner inquiries'],source_text=SOURCE)
        for obj in objs:
            path=_path(BASE,obj); path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')
        repair=next(o['id'] for o in objs if o.get('object_type')=='ProductService' and 'repair' in o.get('name','').lower())
        act=action_packet()

        # Missing delta evidence is a hard error for a verified customer-facing HTML mutation.
        reset_site(); before=capture_before('missing')
        (WORK/'index.html').write_text('<html><body><h1>Northstar HVAC</h1></body></html>')
        chg=change(str(before.relative_to(ROOT)),'runtime/missing.json')
        errs=mutation_errors(BID,[(act,'act.json'),(chg,'chg.json')])
        require(any('does not exist' in e for e in errs),f'missing mutation evidence should fail, got {errs}')

        # A post-hoc capture taken after the edit cannot masquerade as before-state evidence.
        reset_site(); (WORK/'index.html').write_text('<html><body><h1>Northstar HVAC</h1></body></html>')
        before=capture_before('posthoc'); dp,d=delta_after(before,'posthoc')
        chg=change(str(before.relative_to(ROOT)),str(dp.relative_to(ROOT)))
        errs=mutation_errors(BID,[(act,'act.json'),(chg,'chg.json')])
        require(any('capture the surface before editing rather than post-hoc' in e for e in errs),f'post-hoc before capture should fail, got {errs}')

        # Safe removal/narrowing introduces no new business claim and passes.
        reset_site(); before=capture_before('remove')
        (WORK/'index.html').write_text('<!doctype html><html><head><title>Northstar HVAC</title></head><body><h1>Northstar HVAC</h1></body></html>')
        dp,d=delta_after(before,'remove');require(not d['introduced_claims'],f'safe removal should introduce no claim, got {d}')
        chg=change(str(before.relative_to(ROOT)),str(dp.relative_to(ROOT)))
        errs=mutation_errors(BID,[(act,'act.json'),(chg,'chg.json')]);require(not errs,f'safe removal should pass, got {errs}')

        # Exact live failure: replacing a broken maintenance link with a maintenance CTA is a new active-business predicate.
        reset_site(); before=capture_before('maintenance-cta')
        (WORK/'index.html').write_text('''<!doctype html><html><head><title>Northstar HVAC</title></head><body><h1>Northstar HVAC</h1><div class="card"><h2>Maintenance</h2><p>Looking for ongoing system care? Contact us to discuss options for your system.</p><a href="/contact.html">Contact us about maintenance</a></div></body></html>''')
        dp,d=delta_after(before,'maintenance-cta');require(any('maintenance' in x['text'].lower() and 'us' in x['text'].lower() for x in d['introduced_claims']),f'maintenance CTA should be detected, got {d}')
        chg=change(str(before.relative_to(ROOT)),str(dp.relative_to(ROOT)))
        errs=mutation_errors(BID,[(act,'act.json'),(chg,'chg.json')]);require(any('invalid classification' in e for e in errs),f'unclassified maintenance CTA should fail, got {errs}')
        d=json.loads(dp.read_text())
        for x in d['introduced_claims']: x['classification']='general_guidance';x['support_refs']=[]
        write_json(dp,d);errs=mutation_errors(BID,[(act,'act.json'),(chg,'chg.json')])
        require(any('cannot be classified as general_guidance' in e for e in errs),f'first-person maintenance CTA cannot hide as guidance, got {errs}')
        d=json.loads(dp.read_text())
        for x in d['introduced_claims']: x['classification']='approved_business_claim';x['support_refs']=[repair]
        write_json(dp,d);errs=mutation_errors(BID,[(act,'act.json'),(chg,'chg.json')])
        require(any('do not substantively authorize' in e for e in errs),f'repair support must not authorize maintenance CTA, got {errs}')

        # A supported new repair CTA may be authorized by the grounded repair ProductService.
        reset_site(); before=capture_before('repair-cta')
        (WORK/'index.html').write_text('<!doctype html><html><head><title>Northstar HVAC</title></head><body><h1>Northstar HVAC</h1><a href="/contact.html">Contact us about residential HVAC repair</a></body></html>')
        dp,d=delta_after(before,'repair-cta')
        for x in d['introduced_claims']: x['classification']='approved_business_claim';x['support_refs']=[repair]
        write_json(dp,d);chg=change(str(before.relative_to(ROOT)),str(dp.relative_to(ROOT)))
        errs=mutation_errors(BID,[(act,'act.json'),(chg,'chg.json')]);require(not errs,f'grounded repair CTA should pass, got {errs}')

        # Added customer-facing files are part of the mutation surface and cannot be hidden from target_refs.
        reset_site(); before=capture_before('new-page');(WORK/'maintenance.html').write_text('<html><head><title>HVAC Maintenance | Northstar HVAC</title></head><body><h1>HVAC Maintenance</h1><p>Northstar HVAC offers maintenance.</p></body></html>')
        dp,d=delta_after(before,'new-page');require('maintenance.html' in d['added_customer_facing_files'],'new page must be in delta')
        chg=change(str(before.relative_to(ROOT)),str(dp.relative_to(ROOT)))
        errs=mutation_errors(BID,[(act,'act.json'),(chg,'chg.json')]);require(any('missing from ChangeEvent.target_refs' in e for e in errs),f'hidden new page should fail, got {errs}')

        # Integration: validate_business must surface the shared mutation gate, not only the focused validator.
        reset_site(); before=capture_before('integration-maintenance')
        (WORK/'index.html').write_text('<html><head><title>Northstar HVAC</title></head><body><h1>Northstar HVAC</h1><a href="/contact.html">Contact us about maintenance</a></body></html>')
        dp,d=delta_after(before,'integration-maintenance')
        objref=next(o['id'] for o in objs if o.get('object_type')=='Objective')
        opp={'id':f'opp_{BID}_fixture','object_type':'Opportunity','schema_version':'1.0.0','business_id':BID,'owner_system':'seo-aeo','title':'Fixture edit','statement':'Remove a broken link without introducing unsupported business claims.','status':'candidate','objective_refs':[objref],'confidence':0.8,'extensions':{'businessos':{'origin':'preexisting'}}}
        write_json(BASE/'decisions/opportunities'/f"{opp['id']}.json",opp)
        write_json(BASE/'decisions/action-packets'/f"{act['id']}.json",act)
        chg=change(str(before.relative_to(ROOT)),str(dp.relative_to(ROOT)))
        write_json(BASE/'decisions/change-events'/f"{chg['id']}.json",chg)
        verrs,_,_=validate_business(BID,True)
        require(any('customer_facing_mutations' in e and ('invalid classification' in e or 'claim' in e) for e in verrs),f'validate_business must enforce mutation claim safety, got {verrs}')
        shutil.rmtree(BASE/'decisions',ignore_errors=True)

        policy=(ROOT/'core/policies/customer-facing-mutations.md').read_text()
        require('Contact us about maintenance' in policy and 'capture_customer_facing_state.py' in policy and 'build_mutation_claim_manifest.py' in policy,'RC7 mutation policy missing exact boundary/helper path')
        plan=build_plan(BID,'seo.execution.technical.indexability')
        require('core/policies/customer-facing-mutations.md' in plan['files'],'ChangeEvent-writing SEO execution must load mutation policy')
        require(any(x.get('type')=='BusinessClaim' for x in plan.get('unresolved_selectors',[]) if isinstance(x,dict)) or any('claims/' in x for x in plan.get('object_files',[])),'ChangeEvent execution must request/load BusinessClaim context')
        print('customer-facing mutation regressions passed')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
        if (ROOT/'runtime'/BID).exists(): shutil.rmtree(ROOT/'runtime'/BID)

if __name__=='__main__':main()
