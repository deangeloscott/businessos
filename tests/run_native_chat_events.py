"""A chat sent through AURA's own chat path reaches a reply with each interactive app's first events, and a failure while
reading those events ends the request with an error instead of leaving it waiting forever. Fixture apps only; no model calls."""
import json,os,sys,tempfile,time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

FAKE=r'''
import json,sys
kind=sys.argv[1]
def emit(value):print(json.dumps(value),flush=True)
for line in sys.stdin:
    m=json.loads(line);typ=m.get('type');ident=m.get('id')
    if kind=='claude':
        if typ=='control_request' and m.get('request_id')=='aura-init':
            emit({'type':'control_response','response':{'subtype':'success','request_id':'aura-init','response':{'commands':[{'name':'review','description':'Review changes'}]}}})
        elif typ=='control_request':emit({'type':'control_response','response':{'subtype':'success','request_id':m['request_id'],'response':{}}})
        elif typ=='user':
            emit({'type':'system','subtype':'init','session_id':'native-claude'})
            emit({'type':'assistant','session_id':'native-claude','message':{'role':'assistant','content':[{'type':'text','text':'Fixture reply.'}]}})
            emit({'type':'result','session_id':'native-claude','result':'Fixture reply.','usage':{'input_tokens':10,'output_tokens':2}})
    else:
        if typ=='get_commands':emit({'type':'response','id':ident,'success':True,'data':{'commands':[{'name':'review'}]}})
        elif typ=='get_state':emit({'type':'response','id':ident,'success':True,'data':{'sessionId':'native-'+kind,'isStreaming':False}})
        elif typ=='prompt':
            emit({'type':'response','id':ident,'success':True})
            emit({'type':'message_end','message':{'role':'assistant','content':[{'type':'text','text':'Fixture reply.'}]}})
            emit({'type':'session_settled'})
'''


def finished(app,job,seconds=20):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        if app.jobs[job['id']]['status']!='working':
            with app.lock:return app.jobs[job['id']]
        time.sleep(.03)
    raise AssertionError('The chat was still waiting after %ss: %s'%(seconds,app.jobs[job['id']].get('progress')))


def main():
    with tempfile.TemporaryDirectory(prefix='aura-native-events-') as t,patch.dict(os.environ):
        base=Path(t);fake=base/'fake_app.py';fake.write_text(FAKE,encoding='utf-8')
        os.environ.update(BUSINESSOS_WORKSPACE=str(base/'workspace'),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'),LOCALAPPDATA=str(base/'local'))
        from setup import setup
        import workspace_ui
        from workspace_native_requests import aura_helper
        from _common import PRODUCT_ROOT
        bid=setup(organization='Fixture studio')['business_id']
        # AURA's own look-up and save helpers run without an approval box; anything more still asks.
        py,helpers=sys.executable,PRODUCT_ROOT/'scripts'
        assert aura_helper(f'"{py}" "{helpers/"enter.py"}" "How did sales go?" --business-id {bid}',str(base))
        assert aura_helper(f'cd "{PRODUCT_ROOT}" && "{py}" scripts/remember.py {bid} --input \'{{"note":"$40"}}\'',str(base))
        assert aura_helper(f'"{py}" "{helpers/"set_attention_status.py"}" {bid} item resolved',str(base)),'any helper that is not on the ask-first list'
        pwsh=['C:/tools/pwsh.exe','-Command',f'& "{py}" {helpers/"workspace_context.py"} handoff {bid}']
        assert aura_helper(pwsh,str(base)),"Codex's PowerShell call, with a Windows path left as it is"
        for unsafe in (f'"{py}" "{helpers/"enter.py"}" q && del notes.txt',f'"{py}" "{helpers/"enter.py"}" q > out.txt',f'"{py}" "{helpers/"enter.py"}" "$(whoami)"',
                       f'"{py}" "{helpers/"forget.py"}" {bid} record',f'"{py}" "{helpers/"workspace_ui.py"}"',f'BUSINESSOS_WORKSPACE="{base}" "{py}" "{helpers/"remember.py"}" {bid}',
                       ['C:/tools/pwsh.exe','-Command',f'"{py}" {helpers/"setup.py"}'],['C:/tools/node.exe','-e','x']):
            assert not aura_helper(unsafe,str(base)),unsafe
        import workspace_native_requests as requests
        answered=[];execution=type('Execution',(),{'native_cwd':str(base)})()
        requests.codex_request({'id':7,'method':'item/commandExecution/requestApproval','params':{'command':pwsh,'cwd':str(base)}},execution,answered.append)
        assert answered==[{'id':7,'result':{'decision':'accept'}}],'Codex is answered for AURA helpers too'
        # Apps on the standard agent protocol (Antigravity): AURA answers for reading its own files and running its helpers.
        from workspace_acp import aura_own
        offered=[{'optionId':'once','kind':'allow_once'},{'optionId':'no','kind':'reject_once'}]
        assert aura_own({'kind':'read','locations':[{'path':str(PRODUCT_ROOT/'CONTEXT.md')}]},offered,str(base))=='once'
        assert aura_own({'kind':'execute','rawInput':{'CommandLine':f'"{py}" "{helpers/"remember.py"}" {bid}'}},offered,str(base))=='once'
        for other in ({'kind':'read','locations':[{'path':str(base/'notes.txt')}]},{'kind':'execute','rawInput':{'CommandLine':f'"{py}" -c "print(1)"'}},
                      {'kind':'edit','locations':[{'path':str(PRODUCT_ROOT/'CONTEXT.md')}]}):
            assert aura_own(other,offered,str(base)) is None,other
        for kind in ('claude','pi','omp'):
            agents=[{'id':kind,'name':kind.title(),'argv':[sys.executable,'-u',str(fake),kind]}]
            with patch('workspace_ui.installed_agents',return_value=agents):
                app=workspace_ui.Workspace();app.select_agent(agents[0])
                app.preferences['connection']={'kind':kind,'model':'fixture','effort':''}
                try:
                    job=finished(app,app.start_chat(bid,'Say hello',[],chat_id=''))
                    assert job['status']=='complete' and 'Fixture reply.' in job['reply'],(kind,job.get('status'),job.get('reply'),job.get('error_detail'))
                    assert app.preferences['app_versions'][kind]['lists']['commands']==['/review'],'The commands the app reported are kept'
                    # Anything going wrong while AURA reads the app's events ends the request with the error, not a silent wait.
                    with patch.object(app,'observe_app',side_effect=RuntimeError('fixture failure')):
                        job=finished(app,app.start_chat(bid,'Say hello again',[],chat_id=''))
                    assert job['status']=='error' and 'fixture failure' in (job.get('error_detail') or ''),(kind,job.get('status'),job.get('error_detail'))
                finally:
                    for running in app.running_jobs():app.stop_chat(bid,running['id'])
                    app.native_sessions.close()
    print('Native chat events passed: Claude Code, Pi and OMP reach a reply; a failure reading events ends with its error.')


if __name__=='__main__':main()
