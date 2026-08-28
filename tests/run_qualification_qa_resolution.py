#!/usr/bin/env python3
"""Qualification must resolve customer-facing QA from the actual Run contract graph."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qualification'));sys.path.insert(0,str(ROOT/'scripts'))
from qa_resolution import required_qa_contract_ids, recorded_required_qa_refs
from completion_evidence import completion_spec


def req(condition,message):
    if not condition:raise AssertionError(message)


def main():
    contracts={
        'content.qa.pre-publish':{'id':'content.qa.pre-publish','type':'playbook','reads':['Asset']},
        'marketing.landing-page.qa':{'id':'marketing.landing-page.qa','type':'playbook','reads':['Asset']},
    }
    content_audit=[{'run':{'contract_id':'content.production.infographic'},'manifest':{
        'required_subcontracts':['content.qa.pre-publish'],
        'contracts':{'content.qa.pre-publish':{'status':'completed','evidence_refs':['runtime/content-qa.json']}}
    }}]
    marketing_audit=[{'run':{'contract_id':'marketing.assets.landing-page'},'manifest':{
        'required_subcontracts':['marketing.landing-page.qa'],
        'contracts':{'marketing.landing-page.qa':{'status':'completed','evidence_refs':['runtime/marketing-qa.json']}}
    }}]
    content_ids=required_qa_contract_ids(content_audit,contracts,completion_spec,'content.production.infographic')
    marketing_ids=required_qa_contract_ids(marketing_audit,contracts,completion_spec,'marketing.assets.landing-page')
    req(content_ids==['content.qa.pre-publish'],'Content QA did not resolve from its actual manifest')
    req(marketing_ids==['marketing.landing-page.qa'],'Marketing QA did not resolve from its actual manifest')
    req('content.qa.pre-publish' not in marketing_ids,'qualification leaked Content QA into Marketing')
    req(recorded_required_qa_refs(content_audit,content_ids,'content.production.infographic')['content.qa.pre-publish']==['runtime/content-qa.json'],'Content QA recording was not found')
    req(recorded_required_qa_refs(marketing_audit,marketing_ids,'marketing.assets.landing-page')['marketing.landing-page.qa']==['runtime/marketing-qa.json'],'Marketing QA recording was not found')
    req(not recorded_required_qa_refs(marketing_audit,['content.qa.pre-publish'],'marketing.assets.landing-page')['content.qa.pre-publish'],'wrong-domain QA must not satisfy another contract')
    print('contract-resolved qualification QA regressions passed')


if __name__=='__main__':main()
