#!/usr/bin/env python3
"""File saves, conflict recovery, ownership, streamed reads and shipped components."""
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
from unittest.mock import patch
import hashlib,json,os,subprocess,sys,tempfile,threading
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import workspace_documents as docs
from _common import workspace_scope
from init_business import init_business
from workspace_ui import Workspace,handler_for,records

def rejected(fn,kind=ValueError):
    try:fn()
    except kind:return
    raise AssertionError('Expected rejection')

def main():
    with tempfile.TemporaryDirectory(prefix='aura-documents-') as temp:
        base=Path(temp);root=base/'workspace';root.mkdir()
        with patch.dict(os.environ,{'BUSINESSOS_WORKSPACE':str(root),'BUSINESSOS_WORKSPACE_CONFIG':str(base/'pointer.json')}),workspace_scope(root):
            init_business('alpha','Alpha');init_business('beta','Beta')
            folder=root/'attachments/alpha/work';folder.mkdir(parents=True)
            source=folder/'Guide.md';original=b'\xef\xbb\xbf# First\r\n\r\nNotes.\r\n';source.write_bytes(original)
            app=Workspace(settings_file=base/'ui.json')
            ref=source.relative_to(root).as_posix()
            info=app.document_info('alpha',ref);assert info['kind']=='text' and info['writable'] and info['bom']
            saved=app.document_save('alpha',ref,{'expected_revision':info['revision'],'content':'# Changed\nNotes.\n'})
            assert source.read_bytes()==b'\xef\xbb\xbf# Changed\r\nNotes.\r\n'
            rev=docs.revision(source);before=source.read_bytes()
            version=app.document_save('alpha',ref,{'mode':'version','expected_revision':rev,'content':'Version two'})
            assert source.read_bytes()==before and (root/version['path']).read_text(encoding='utf-8-sig')=='Version two'
            assets={r['ref']:r['data'] for r in records('alpha')[0] if r['type']=='Asset'}
            assert assets[version['asset']]['lineage']==[saved['asset']]
            assert len(app.document_info('alpha',ref)['related'])==2
            # The source is altered by another editor after loading.
            source.write_text('Outside edit',encoding='utf-8')
            rejected(lambda:app.document_save('alpha',ref,{'expected_revision':rev,'content':'Stale edit'}),docs.Conflict)
            copy=app.document_save('alpha',ref,{'mode':'copy','expected_revision':rev,'content':'Recovered draft'})
            assert source.read_text()=='Outside edit' and (root/copy['path']).read_text()=='Recovered draft'
            rejected(lambda:app.document_save('alpha',ref,{'mode':'copy','name':'../escape.md','expected_revision':rev,'content':'Bad'}))
            rejected(lambda:app.document_info('beta',ref))
            rejected(lambda:app.document_info('alpha','../outside.txt'))
            rejected(lambda:app.document_info('alpha','library/not-registered'))
            linked=base/'Linked';linked.mkdir();(linked/'Notes.txt').write_text('Linked original',encoding='utf-8')
            app.preferences['file_locations']['alpha']=[{'id':'linked-proof','path':str(linked),'name':'Linked','kind':'folder'}]
            assert not app.document_info('alpha','linked/linked-proof/Notes.txt')['writable']
            image=folder/'Picture.gif';image.write_bytes(b'GIF89a')
            assert docs.inspect(image)['kind']=='image' and not docs.inspect(image)['editable']
            # A link must never turn a public name into access to a private file.
            secret=folder/'.env';secret.write_text('private',encoding='utf-8')
            alias=folder/'public.txt'
            try:alias.symlink_to(secret)
            except OSError:pass # Windows without symlink privilege still exercises the other guards.
            else:rejected(lambda:app.document_info('alpha',alias.relative_to(root).as_posix()))
            # Canonical JSON is a view, never an inline write target.
            canonical=next((root/'instances/alpha').rglob('instance.json')).relative_to(root).as_posix()
            assert not app.document_info('alpha',canonical)['writable']
            rejected(lambda:app.document_save('alpha',canonical,{'expected_revision':docs.revision(root/canonical),'content':'{}'}))
            # CSV quotes, embedded newlines and the original delimiter survive.
            table=folder/'Table.csv';table.write_bytes(b'Name;Notes\r\nA;"two\r\nlines"\r\n')
            table_info=docs.inspect(table,True);assert table_info['delimiter']==';' and table_info['rows'][1][1]=='two\r\nlines'
            docs.save(table,'alpha',{'rows':[['Name','Notes'],['B','quote " and ; separator']],'expected_revision':table_info['revision']},True)
            assert docs.inspect(table)['rows'][1]==['B','quote " and ; separator']
            # Metadata errors roll back our bytes, but never erase a newer outside edit.
            rev=docs.revision(source)
            with patch.object(docs,'_asset',side_effect=ValueError('metadata rejected')):
                rejected(lambda:docs.save(source,'alpha',{'expected_revision':rev,'content':'Failed'},True))
            assert source.read_text()=='Outside edit'
            def changed_metadata(*args,**kwargs):
                source.write_text('New outside edit',encoding='utf-8');raise ValueError('metadata rejected')
            with patch.object(docs,'_asset',side_effect=changed_metadata):
                rejected(lambda:docs.save(source,'alpha',{'expected_revision':rev,'content':'Failed'},True))
            assert source.read_text()=='New outside edit'
            # Managed sources need no write permission or lock alongside the original.
            managed=base/'managed/SKILL.md';managed.parent.mkdir();managed.write_text('Managed original',encoding='utf-8')
            result=docs.save(managed,'alpha',{'mode':'copy','expected_revision':docs.revision(managed),'content':'Adaptation'},False,track_source=False)
            assert managed.read_text()=='Managed original' and result['path'].startswith('attachments/alpha/')
            assert not list(managed.parent.glob('*.lock'))
            # The standalone CLI uses the same shared implementation.
            cli=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_documents.py'),'show','--workspace',str(root),'--business-id','alpha','--path',ref,'--json'],capture_output=True,text=True)
            assert cli.returncode==0,cli.stderr
            assert json.loads(cli.stdout)['revision']==docs.revision(source)
            with patch.object(docs,'libreoffice',return_value='fixture-office'),patch.object(docs.subprocess,'Popen') as launch:
                docs.open_in(source,'libreoffice');assert launch.call_args.args[0][-1]==str(source)
            rejected(lambda:docs.open_in(folder/'program.py','default'))
            # Media cookies cannot authorize the API. Reads support native seeking.
            media=folder/'Clip.mp4'
            with media.open('wb') as f:f.write(b'0123456789');f.truncate(70*1024*1024)
            server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            origin='http://127.0.0.1:'+str(server.server_port)
            def request(path,headers=None,data=None,method=None,expect=200):
                req=Request(origin+path,headers=headers or {},data=json.dumps(data).encode() if data is not None else None,method=method)
                try:
                    with urlopen(req,timeout=20) as response:
                        assert response.status==expect,(path,response.status)
                        return response.headers,response.read()
                except HTTPError as e:
                    assert e.code==expect,(path,e.code,e.read());return e.headers,e.read()
            try:
                headers,_=request('/');cookie=headers['Set-Cookie'].split(';')[0]
                assert 'HttpOnly' in headers['Set-Cookie'] and 'SameSite=Strict' in headers['Set-Cookie']
                m='/api/media?'+urlencode({'business':'alpha','path':media.relative_to(root).as_posix(),'workspace':str(root)})
                headers,body=request(m,{'Cookie':cookie,'Range':'bytes=2-5'},expect=206)
                assert body==b'2345' and headers['Content-Range'].startswith('bytes 2-5/')
                _,body=request(m,{'Cookie':cookie,'Range':'bytes=-4'},expect=206);assert body==b'\0'*4
                request(m,{'Cookie':cookie,'Range':'bytes=999999999-'},expect=416)
                headers,body=request(m,{'Cookie':cookie},method='HEAD');assert not body and int(headers['Content-Length'])==70*1024*1024
                request('/api/state',{'Cookie':cookie},expect=403)
                payload={'business':'alpha','workspace':str(root),'path':ref,'expected_revision':docs.revision(source),'content':'HTTP save'}
                request('/api/documents/save',{'Cookie':cookie},payload,expect=403)
                auth={'X-Aura-Token':app.token,'Content-Type':'application/json'}
                request('/api/documents/save',auth,{**payload,'workspace':str(base/'other')},expect=400)
                request('/api/documents/save',{**auth,'Origin':'https://foreign.example'},payload,expect=403)
                request('/api/documents/save',auth,payload)
                request('/api/documents/save',auth,payload,expect=409)
                assert source.read_text()=='HTTP save'
                request('/vendor/../app.js',auth,expect=400)
                _,body=request('/api/components',auth);assert len(json.loads(body)['components'])==4
            finally:server.shutdown();server.server_close();thread.join()
    manifest=json.loads((ROOT/'distribution/ui-components.json').read_text())
    for item in manifest['assets']:
        path=ROOT/item['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],item['path']
    assert (ROOT/'interface/vendor/THIRD-PARTY-NOTICES.md').stat().st_size>10000
    print('workspace document integrity passed')

if __name__=='__main__':main()
