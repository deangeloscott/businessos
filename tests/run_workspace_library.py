#!/usr/bin/env python3
"""Read-only discovery, package identity, and native result boundaries."""
from pathlib import Path
import json
import os
import sys
import tempfile
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import workspace_library as library
import workspace_schedules as schedules
import workspace_storage as storage


def main():
    with tempfile.TemporaryDirectory(prefix='aura-library-') as temp:
        base=Path(temp);home=base/'home';workspace=base/'workspace'
        def package(folder,script='first'):
            folder.mkdir(parents=True,exist_ok=True)
            (folder/'SKILL.md').write_text('---\nname: research\ndescription: Research a real market\ncompatibility: Requires web search\n---\nRead supporting instructions.\n',encoding='utf-8')
            (folder/'helper.txt').write_text(script,encoding='utf-8')
            return folder/'SKILL.md'
        a=package(home/'.codex/skills/research')
        package(home/'.claude/skills/research')
        c=package(workspace/'.pi/skills/research','different version')
        config=home/'.codex/config.toml'
        config.write_text('[mcp_servers.example]\ncommand="private-command"\nenabled=false\n[mcp_servers.example.env]\nSECRET="never-show-this"\n',encoding='utf-8')
        with patch.dict(os.environ,{'CODEX_HOME':str(home/'.codex'),'CLAUDE_CONFIG_DIR':str(home/'.claude'),'PI_CODING_AGENT_DIR':str(home/'.pi/agent')}):
            rows,notes=library.local(workspace,['codex','claude','pi'],home)
        assert not notes
        raw=json.dumps([{k:v for k,v in r.items() if not k.startswith('_')} for r in rows])
        assert 'never-show-this' not in raw and 'private-command' not in raw
        merged=library.merge(rows)
        skills=[r for r in merged if r['kind']=='Skill']
        assert len(skills)==2, 'Copies merge only if supporting files match too'
        shared=next(r for r in skills if len(r['apps'])==2)
        assert shared['apps']==['claude','codex'] and len(shared['aliases'])==1
        assert shared['requirements']=='Requires web search'
        assert library.document(shared).startswith('---')
        assert any(s['status']=='Disabled' for r in merged for s in r['sources'])
        assert len(library.merge(rows))==len(merged), 'Merging must not mutate the cached native inventory'
        assert all('_path' in r for r in rows if r['kind']=='Skill')
        same=library.merge([library.skill(a,'codex','first'),library.skill(a,'pi','second')])
        assert len(same)==1 and same[0]['apps']==['codex','pi']
        display=library.organize(merged)
        family=next(r for r in display if r['kind']=='Skill')
        assert len([r for r in display if r['kind']=='Skill'])==1 and len(family['variants'])==2
        assert len(family['apps'])==3 and shared['key'] in family['aliases']
        assert all(library.document(v) for v in family['variants']), 'Grouped options retain their actual guidance'
        tools=[library.entry('Tool','search','Search this service.',app,app+':'+service,'Reported by app',connection=service,type='Tool')
               for app,service in [('codex','Drive'),('omp','Drive'),('codex','GitHub')]]
        services=library.organize(tools)
        assert len(services)==2 and all(len(r['members'])==1 for r in services)
        assert services[0]['members'][0]['key']!=services[1]['members'][0]['key'], 'Same action names in unrelated services stay distinct'
        assert len(services[0]['members'][0]['variants'])==2
        assert library.find(services,services[1]['members'][0]['key'])['title']=='search'
        connection=library.entry('Tool','Drive','A saved connection.','hermes','saved-drive','Configured',type='Connection')
        linked=library.organize([*tools,connection])
        assert len(linked)==2 and len(linked[0]['apps'])==3, 'Connection summaries and reported actions share one service row'
        international=[library.entry('Tool','search','Search', 'codex',name,type='Tool',service=name) for name in ['百度','搜狗']]
        assert len(library.organize(international))==2, 'Different non-Latin services must not share a grouping identity'
        retained=library.retain_catalog(tools,[],True)
        assert len(retained)==len(tools) and all(s.get('stale') for r in retained for s in r['sources'])
        assert not any(s.get('stale') for r in tools for s in r['sources']), 'A failed refresh must not mutate the previous snapshot'
        partial=library.retain_catalog(tools,tools[:1],True)
        assert len(partial)==len(tools) and not partial[0]['sources'][0].get('stale')
        assert library.retain_catalog(retained,[],False)==[], 'A successful empty catalog must clear removed capabilities'
        plugin=home/'.codex/plugins/cache/example/pdf/1.0/.codex-plugin'
        plugin.mkdir(parents=True)
        (plugin/'plugin.json').write_text(json.dumps({'name':'pdf','version':'1.0','description':'PDF helpers','skills':'./skills'}))
        package(plugin.parent/'skills/pdf')
        (home/'.pi/agent').mkdir(parents=True,exist_ok=True)
        (home/'.pi/agent/settings.json').write_text(json.dumps({'packages':['npm:example@1.2.0'],'extensions':[], 'SECRET':'not-a-resource'}))
        with patch.dict(os.environ,{'CODEX_HOME':str(home/'.codex'),'CLAUDE_CONFIG_DIR':str(home/'.claude'),'PI_CODING_AGENT_DIR':str(home/'.pi/agent')}):
            local,_=library.local(workspace,['codex','pi'],home)
        grouped=library.organize(library.merge(local))
        bundle=next(r for r in grouped if r['kind']=='Plugin' and r['title']=='pdf')
        assert bundle['related'] and any(r['kind']=='Plugin' and r['title']=='example' for r in grouped)
        assert 'not-a-resource' not in json.dumps(grouped)
        class Metadata:
            calls=[]
            def __init__(self,*args):pass
            def call(self,method):
                self.calls.append(method)
                return {'commands':[{'name':'skill:research','source':'skill','sourceInfo':{'path':str(c)}}]} if method=='get_commands' else {'dumpTools':[{'name':'read','description':'Read a file.\nMore details.'}]}
            def close(self):self.calls.append('close')
        with patch('workspace_agents.Metadata',Metadata):
            native=library.native({'id':'pi','argv':['pi','--print']},workspace,{})
        assert Metadata.calls==['get_commands','get_state','close'], 'Discovery must never prompt a model'
        assert {r['kind'] for r in native}=={'Skill','Tool'}
        calls=[]
        def rpc(command,requests,cwd,env):
            if callable(requests):return requests(lambda method,params:rpc(command,[(method,params)],cwd,env)[0])
            method,params=requests[0];calls.append((method,params))
            if method=='app/installed':raise ValueError('Fixture emulates an older CLI')
            if method=='skills/list':return [{'data':[]}]
            if method=='mcpServerStatus/list':
                return [{'data':[{'name':'docs','tools':{'read':{'description':'Read docs.'}}}], 'nextCursor':'second' if not params.get('cursor') else None}]
            if method=='app/list':return [{'data':[{'id':'ok','name':'Drive','isAccessible':True,'isEnabled':True}, {'id':'directory','name':'Unconnected','isAccessible':False}]}]
            raise AssertionError('Unexpected native call')
        with patch('workspace_codex.rpc',rpc):
            reported=library.native({'id':'codex','argv':['codex','exec']},workspace,{})
        assert any(params.get('cursor')=='second' for method,params in calls if method=='mcpServerStatus/list')
        assert any(r['title']=='Drive' for r in reported) and not any(r['title']=='Unconnected' for r in reported)
        def snapshot_rpc(command,requests,cwd,env):
            if callable(requests):return requests(lambda method,params:snapshot_rpc(command,[(method,params)],cwd,env)[0])
            method,params=requests[0]
            if method=='app/installed':return [{'apps':[{'id':'connected','runtimeName':'Drive','enabled':True,'callable':True}]}]
            if method=='app/read':return [{'apps':[{'id':'connected','name':'Drive','description':'Connected documents.'}]}]
            if method=='app/list':raise AssertionError('Installed apps must not scan the public marketplace')
            return [{'data':[]}]
        with patch('workspace_codex.rpc',snapshot_rpc):
            scoped=library.native({'id':'codex','argv':['codex','exec']},workspace,{})
        assert len(scoped)==1 and scoped[0]['title']=='Drive'
        import subprocess
        with patch('workspace_library.subprocess.run',return_value=subprocess.CompletedProcess([],0,'Built-in toolsets (cli):\n  enabled terminal Terminal\nPlugin toolsets (cli):\n  enabled helper Helper tools\nMCP servers:\n','')):
            hermes_resources=library.organize(library.native({'id':'hermes','argv':['hermes','chat']},workspace,{}))
        helper=next(r for r in hermes_resources if r['kind']=='Plugin')
        assert helper['title']=='helper' and len(helper['related'])==1
        # Adaptive pages share one actual subprocess, not just the same mock.
        import workspace_codex
        server=base/'metadata.py'
        server.write_text("import json,os,sys\nfor line in sys.stdin:\n r=json.loads(line)\n if 'id' in r: print(json.dumps({'id':r['id'],'result':{'pid':os.getpid(),'method':r['method']}}),flush=True)\n",encoding='utf-8')
        command=[sys.executable,str(server),'exec']
        result=workspace_codex.rpc(command,lambda read:[read('first/page',{}),read('next/page',{'cursor':'opaque'})],base,{**os.environ})
        assert result[0]['pid']==result[1]['pid'] and result[1]['method']=='next/page'
        assert workspace_codex.rpc(command,[('plain/request',{})],base,{**os.environ})[0]['method']=='plain/request'
        prefs={'library':{'business':{'favorites':[shared['key']],'recent':[shared['key']]}}}
        storage.save_view(workspace,prefs)
        assert storage.view_preferences(workspace)['library']==prefs['library']
        assert str(home) not in (workspace/storage.VIEW_FILE).read_text(encoding='utf-8')
        hermes=base/'hermes';cron=hermes/'cron';cron.mkdir(parents=True)
        (cron/'jobs.json').write_text(json.dumps({'jobs':[{'id':'job','name':'Research','schedule':{'expr':'0 8 * * *'},
            'last_run_at':'2026-10-29T08:00:00Z','last_status':'ok','enabled':True}]}),encoding='utf-8')
        output=cron/'output/job';output.mkdir(parents=True)
        (output/'2026-10-29_08-01-00.md').write_text('The actual saved result.',encoding='utf-8')
        with patch.dict(os.environ,{'HERMES_HOME':str(hermes),'CODEX_HOME':str(base/'empty')}):
            task=next(t for t in schedules.inventory()['items'] if t['owner']=='hermes')
            assert task['last_run']=='2026-10-29T08:00:00Z' and task['last_status']=='ok' and task['has_result']
            assert schedules.result(task['id'])['text']=='The actual saved result.'
            assert schedules.result_path(hermes,'../outside') is None
            try:schedules.result('../../private')
            except ValueError:pass
            else:raise AssertionError('Client paths must never select output files')
    print('Workspace library discovery, deduplication, portability and result checks passed.')


if __name__=='__main__':main()
