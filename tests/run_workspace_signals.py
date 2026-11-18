"""What AURA notices on its own, from records the apps and AURA already keep: a connected service that work relied on
being turned off or removed, and work saved outside an AURA chat. Each rings the bell once; nothing is asked of the AI."""
import json,os,sys,tempfile,time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import workspace_scope


def main():
    with tempfile.TemporaryDirectory(prefix='aura-signals-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace';home=base/'home'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'),
                          CLAUDE_CONFIG_DIR=str(home/'.claude'),CODEX_HOME=str(home/'.codex'),USERPROFILE=str(home),HOME=str(home))
        for name in ('HERMES_HOME','PI_CODING_AGENT_DIR','AURA_PRODUCER','CLAUDE_CODE_SESSION_ID','PI_SESSION_ID','PI_SESSION_FILE','HERMES_SESSION_ID','ANTIGRAVITY_CONVERSATION_ID'):os.environ.pop(name,None)
        from setup import setup
        import workspace_ui
        bid=setup(organization='Signal studio')['business_id']
        with workspace_scope(root),patch('pathlib.Path.home',return_value=home):
            app=workspace_ui.Workspace()
            app.preferences['chats']=[{'id':'chat-1','business_id':bid,'agent':'claude','native_id':'cc-9','title':'Billing','workspace':str(root.resolve())}]
            log=home/'.claude/projects/p';log.mkdir(parents=True)
            (log/'cc-9.jsonl').write_text(json.dumps({'type':'assistant','message':{'content':[{'type':'tool_use','name':'mcp__stripe__list','input':{}}]}})+chr(10),encoding='utf-8')
            mcp=root/'.mcp.json'
            mcp.write_text(json.dumps({'mcpServers':{'stripe':{'command':'x'}}}),encoding='utf-8')
            assert app.service_problems(bid)==[],'a connected service in use is fine'
            mcp.write_text(json.dumps({'mcpServers':{'stripe':{'command':'x','disabled':True}}}),encoding='utf-8')
            assert app.service_problems(bid)==[{'service':'Stripe','app':'claude','problem':'off'}],'turned off in the app that used it'
            mcp.write_text(json.dumps({'mcpServers':{}}),encoding='utf-8')
            assert app.service_problems(bid)==[{'service':'Stripe','app':'claude','problem':'gone'}],'connected before and gone now'
            app.check_service_problems();app.check_service_problems()
            rung=[n for n in app.preferences['notification_items'] if n['kind']=='service']
            assert len(rung)==1 and 'Stripe is no longer connected in Claude Code' in rung[0]['title'],rung
            app.preferences['read_app_records']=False
            assert app.service_problems(bid)==[] and app.services_used(bid)=={'services':[],'off':True},'turned off in Settings, nothing is read'
            app.preferences['read_app_records']=True

            # Work saved outside an AURA chat says so once, grouped by where it was made. Earlier work is not news.
            from remember import remember
            insight=lambda text:{'objects':[{'object_type':'Insight','content':{'domain':'core','insight_type':'research_insight','statement':text,'status':'candidate','evidence_links':[]}}]}
            remember(bid,insight('Older finding.'))
            app.check_saved_work()
            assert not [n for n in app.preferences['notification_items'] if n['kind']=='saved'],'what was there before the first look is not announced'
            time.sleep(1.1)
            os.environ['CLAUDE_CODE_SESSION_ID']='cc-direct'
            remember(bid,insight('Weekend demand is higher.'))
            os.environ.pop('CLAUDE_CODE_SESSION_ID')
            os.environ['AURA_PRODUCER']=json.dumps({'kind':'chat','id':'chat-1','business_id':bid,'workspace':str(root.resolve())})
            remember(bid,insight('Said in its own chat.'))
            os.environ.pop('AURA_PRODUCER')
            app.check_saved_work();app.check_saved_work()
            saved=[n for n in app.preferences['notification_items'] if n['kind']=='saved']
            assert len(saved)==1 and saved[0]['title']=='Claude Code saved 1 finding: “Weekend demand is higher.”',saved
    print('Workspace signals passed: services turned off or removed, the Settings switch, and work saved outside AURA chats.')


if __name__=='__main__':main()
