"""Activity is observational; recall is scoped; memory feedback never overwrites newer work."""
from pathlib import Path
from unittest.mock import patch
import json
import os
import sys
import tempfile
import time
import subprocess

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import object_index,workspace_scope,write_json_atomic
from init_business import init_business
from remember import remember
from workspace_ui import Workspace
import workspace_context as context
import workspace_memory_feedback as feedback
import workspace_trace as trace
import workspace_chat_organization as organization
import workspace_assistants as assistants
import workspace_storage as storage


def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Invalid or stale change was accepted')


def main():
    with tempfile.TemporaryDirectory(prefix='aura-insight-') as temp,patch.dict(os.environ):
        base=Path(temp);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        bid='insight';init_business(bid,'Insight')
        app=Workspace()
        original=next(obj for obj,path in object_index(bid).values() if obj['object_type']=='Business')
        result=remember(bid,{'objects':[{'object_ref':original['id'],'content':{'name':'A clearer name'}}]})
        saved=feedback.inventory(bid)['items'];assert len(saved)==1 and result['memory_feedback']==[saved[0]['id']]
        # Missing recovery must never turn an update's Undo into deletion.
        journal=feedback.rows(bid);version_id=journal[-1]['version_id'];journal[-1]['version_id']='';write_json_atomic(feedback.target(bid),journal)
        rejects(lambda:feedback.respond(bid,saved[0]['id'],'undo'))
        assert object_index(bid)[original['id']][0]['name']=='A clearer name'
        journal[-1]['version_id']=version_id;write_json_atomic(feedback.target(bid),journal)
        feedback.respond(bid,saved[0]['id'],'undo')
        assert object_index(bid)[original['id']][0]['name']=='Insight'
        assert not feedback.inventory(bid)['items']
        first=remember(bid,{'objects':[{'object_ref':original['id'],'content':{'name':'First edit'}}]})['memory_feedback'][0]
        remember(bid,{'objects':[{'object_ref':original['id'],'content':{'name':'Newer edit'}}]})
        rejects(lambda:feedback.respond(bid,first,'undo'))
        assert object_index(bid)[original['id']][0]['name']=='Newer edit'
        # Public turns from multiple apps share one retrieval boundary.
        for ident,agent,project,archived in [('pi-chat','pi','Launch',False),('codex-chat','codex','Launch',False),('archived','omp','Launch',True),('other-project','hermes','Other',False)]:
            app.preferences['chats'].append({'id':ident,'business_id':bid,'workspace':str(root),'title':agent+' research','agent':agent,'project':project,'archived':archived,'updated':time.time()})
            p=app.chat_display_path(ident);p.parent.mkdir(parents=True,exist_ok=True)
            write_json_atomic(p,[{'role':'user','text':'Research cobalt supply','request_id':'turn'},
                                 {'role':'assistant','text':'Cobalt result from '+agent,'at':time.time(),'request_id':'turn','status':'complete'}])
        found=context.recall(app,bid,'cobalt',project='Launch')['items'];assert len(found)==2
        assert {r['app'] for r in found}=={'pi','codex'}
        assert not context.recall(app,'another-business','cobalt')['items']
        with workspace_scope(base/'other'):assert not context.recall(app,bid,'cobalt')['items']
        resolved=context.resolve(app,bid,[found[0]]);assert 'Cobalt result' in resolved['text'] and 'not established business truth' in resolved['text']
        # References are pointers and survive portable workspace settings.
        refs=[{'kind':'record','id':original['id']}]
        organization.change_project(app,bid,{'action':'edit','name':'Launch','context_refs':refs})
        a=assistants.save(app.preferences,bid,{'name':'Research partner','context_refs':refs})
        assert context.inherited(app,bid,project='Launch',assistant=a)==refs
        storage.save_view(root,app.preferences);assert next(p for p in storage.view_preferences(root)['chat_projects'] if p['name']=='Launch')['context_refs']==refs
        pinned=context.saved_result(app,bid,found[0]['id'],found[0]['variant'])
        assert 'Cobalt result' in pinned['text']
        result=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_context.py'),'result','--business-id',bid,'--workspace',str(root),'--chat',found[0]['id'],'--variant',found[0]['variant']],capture_output=True,text=True,check=True)
        assert 'Cobalt result' in json.loads(result.stdout)['text']
        lazy=context.resolve(app,bid,[found[0]],pointers=True)
        assert 'Retrieve only if relevant' in lazy['text'] and 'Cobalt result from' not in lazy['text']
        app.profile({'activity_view':'off','working_preferences':'Concise replies, with sources when useful.'})
        assert app.profile()['activity_view']=='off'
        rejects(lambda:app.profile({'activity_view':'unknown'}))
        # A corrected source must not silently become an authoritative historic reply.
        p=app.chat_display_path(found[0]['id']);messages=json.loads(p.read_text(encoding='utf-8'))
        messages[0]['references']=refs;messages[1]['at']=time.time()-10;write_json_atomic(p,messages)
        remember(bid,{'objects':[{'object_ref':original['id'],'content':{'name':'Correct current name'},'correction_summary':'Use the corrected name.'}]})
        assert 'Sources were corrected' in context.saved_result(app,bid,found[0]['id'],found[0]['variant'])['text']
        rejects(lambda:assistants.save(app.preferences,bid,{'id':a['id'],'context_refs':[{'kind':'unknown','id':'bad'}]}))
        # Representative native public events from each protocol, including child details.
        recorder=trace.Recorder('proof',bid,lambda s:s.replace('secret-value','[redacted]'))
        recorder.observe('codex',{'method':'turn/plan/updated','params':{'threadId':'parent','plan':[{'step':'Verify','status':'in_progress'}]}},'parent')
        recorder.observe('codex',{'method':'item/reasoning/summaryTextDelta','params':{'threadId':'child','itemId':'r','delta':'Public summary'}},'parent')
        recorder.observe('codex',{'method':'item/reasoning/textDelta','params':{'itemId':'private','delta':'MUST NOT STORE'}})
        recorder.observe('omp',{'type':'subagent_event','payload':{'id':'omp-child','event':{'type':'tool_execution_end','toolName':'read','toolCallId':'t','result':{'content':[{'type':'text','text':'secret-value file read'}]}}}})
        recorder.observe('pi',{'type':'message_update','message':{'timestamp':1},'assistantMessageEvent':{'type':'thinking_delta','contentIndex':0,'delta':'Visible Pi thinking'}})
        recorder.observe('antigravity',{'params':{'update':{'sessionUpdate':'plan','entries':[{'content':'Review','status':'completed'}]}}})
        recorder.observe('hermes',{'params':{'type':'subagent.tool','payload':{'subagent_id':'h-child','tool_name':'read','tool_preview':'Read file'}}})
        recorder.observe('claude',{'type':'assistant','parent_tool_use_id':'c-child','message':{'id':'m','content':[{'type':'thinking','thinking':'Visible summary'}]}})
        recorder.put('thinking','Streaming','secret-',ident='split',delta=True);recorder.put('thinking','Streaming','value',ident='split',delta=True)
        snapshot=recorder.snapshot();raw=json.dumps(snapshot)
        assert 'MUST NOT STORE' not in raw and 'secret-value' not in raw and '[redacted]' in raw
        assert {'child','omp-child','h-child','c-child'}<={r['owner'] for r in snapshot['items']}
        small=trace.public(snapshot);tool=next(r for r in small['items'] if r['kind']=='tool');assert not tool['text'] and tool['has_detail']
        assert trace.public(snapshot,tool['id'])['text']
        assert trace.public(snapshot,after=snapshot['revision'])['unchanged']
        recorder.save();assert trace.read('proof')['items']==snapshot['items']
        for i in range(550):recorder.put('tool','Bounded','x'*10000,ident=str(i))
        assert len(recorder.rows)<=500 and recorder.bytes<=1000000 and recorder.truncated
        rejects(lambda:trace.read('../outside'))
        print('Insight passed: native public activity, child ownership, redaction, lazy details, scoped cross-app recall, portable references and revision-safe memory undo.')


if __name__=='__main__':main()
