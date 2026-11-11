"""Small shared file edits. Files stay authoritative; Assets track deliberate saves."""
from pathlib import Path
import base64
import csv
import hashlib
import io
import json
import mimetypes
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from contextlib import nullcontext

from _common import workspace_root,read_json_input
from remember import remember
from workspace_sharing import destination_lock, unlinked, safe

TEXT = {'.md','.markdown','.txt','.csv','.tsv','.rst','.json','.yaml','.yml','.toml','.ini','.css','.js','.py','.html','.htm','.xml','.log'}
WEB = {'.html','.htm','.svg'}  # Opened in the person's own browser; AURA does not render web pages itself.
RASTER = {'.png','.jpg','.jpeg','.webp'}
OFFICE = {'.doc','.docx','.odt','.rtf','.xls','.xlsx','.ods','.ppt','.pptx','.odp'}
OPENABLE = TEXT - {'.js','.py','.html','.htm','.xml','.json','.yaml','.yml','.toml','.ini','.css'} | OFFICE | RASTER | WEB | {'.pdf','.gif','.avif','.mp3','.wav','.ogg','.mp4','.webm','.mov','.m4a','.flac','.opus'}
MAX_TEXT = 2*1024*1024
PREVIEW_BYTES = 256*1024
MAX_FILE = 32*1024*1024


class Conflict(ValueError):
    pass


def revision(path):
    digest=hashlib.sha256()
    digest.update(os.path.normcase(str(Path(path).resolve())).encode('utf-8'))
    digest.update(b'\0')
    with Path(path).open('rb') as stream:
        total=0
        for block in iter(lambda:stream.read(1024*1024),b''):
            total+=len(block)
            if total>MAX_FILE:raise ValueError('Use another editor for this large file.')
            digest.update(block)
    return digest.hexdigest()


def inspect(path, writable=False, asset=None):
    path=Path(path);size=path.stat().st_size;suffix=path.suffix.lower()
    result={'name':path.name,'identity':hashlib.sha256(os.path.normcase(str(path.resolve())).encode()).hexdigest(),'bytes':size,'modified':path.stat().st_mtime,'revision':revision(path) if size<=MAX_FILE else '',
            'writable':bool(writable and os.access(path,os.W_OK)), 'editable':False,'kind':'file',
            'asset':asset['id'] if asset else None,'version':asset.get('version') if asset else None}
    if suffix in TEXT:
        # A large text file shows its first part, read-only, instead of no preview at all.
        partial=size>MAX_TEXT
        with path.open('rb') as stream:raw=stream.read(PREVIEW_BYTES if partial else MAX_TEXT)
        if partial:raw=raw[:raw.rfind(b'\n')+1] or raw
        try:text=raw.decode('utf-8-sig')
        except UnicodeError:return result
        if '\x00' in text:return result
        result.update(kind='table' if suffix in {'.csv','.tsv'} else 'text',editable=not partial,text=text,bom=raw.startswith(b'\xef\xbb\xbf'))
        if partial:result['partial']=True
        if result['kind']=='table':
            delimiter='\t' if suffix=='.tsv' else ','
            try:
                if suffix=='.csv':delimiter=csv.Sniffer().sniff(text[:8192],delimiters=',;\t').delimiter
            except csv.Error:
                # Sniffer can fail on short, valid files with quoted line breaks.
                for candidate in (',',';','\t'):
                    sample=list(csv.reader(io.StringIO(text,newline=''),delimiter=candidate))[:50]
                    widths={len(row) for row in sample if row}
                    if len(widths)==1 and next(iter(widths))>1:delimiter=candidate;break
            rows=list(csv.reader(io.StringIO(text,newline=''),delimiter=delimiter))
            if sum(map(len,rows))<=100000 and max(map(len,rows),default=0)<=500:result.update(rows=rows,delimiter=delimiter)
            else:result.update(kind='text')
    elif suffix in RASTER|{'.gif','.avif','.svg'}:result.update(kind='image',editable=suffix in RASTER and size<=MAX_FILE)
    elif suffix=='.pdf':result['kind']='pdf'
    elif suffix in OFFICE:result['kind']='office'
    elif (mimetypes.guess_type(path.name)[0] or '').startswith(('video/','audio/')):result['kind']='media'
    return result


def _asset(path, bid, source, version, lineage=None, existing=None):
    root=workspace_root().resolve();location=path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)
    content={'asset_type':(existing or source or {}).get('asset_type','document' if path.suffix.lower() in TEXT|OFFICE|{'.pdf'} else 'image' if path.suffix.lower() in RASTER else 'file'),
             'business_role':(existing or source or {}).get('business_role',path.name),'location_reference':location,
             'version':str(version),'status':(existing or source or {}).get('status','draft')}
    item={'content':content}
    if existing:item['object_ref']=existing['id']
    else:item['object_type']='Asset'
    if lineage:item['lineage_refs']=lineage
    saved=remember(bid,{'objects':[item]})['objects'][0]
    return {**content,'id':saved['id']}


def save(path,bid,data,writable=False,asset=None,track_source=True):
    from _common import business_transaction
    with business_transaction(bid):return _save(path,bid,data,writable,asset,track_source)


def _save(path,bid,data,writable=False,asset=None,track_source=True):
    path=Path(path);mode=data.get('mode','save')
    if not isinstance(mode,str) or mode not in {'save','version','copy'}:raise ValueError('Choose Save, Save new version, or Save a copy.')
    if not isinstance(data.get('expected_revision'),str) or not data['expected_revision']:raise ValueError('Reopen this file before saving.')
    if path.stat().st_size>MAX_FILE:raise ValueError('Use another editor for this large file.')
    if mode=='save' and not writable:raise ValueError('Keep the original and save a workspace copy.')
    with path.open('rb') as source:original=source.read(MAX_FILE+1)
    if len(original)>MAX_FILE:raise ValueError('Use another editor for this large file.')
    suffix=path.suffix.lower()
    if data.get('encoding')=='base64':
        try:payload=base64.b64decode(data.get('content',''),validate=True)
        except (ValueError,TypeError):raise ValueError('The edited file could not be read.') from None
        if mode=='save' and suffix not in RASTER:raise ValueError('Imported documents are saved as a new version or copy.')
        if suffix in RASTER:
            valid=payload.startswith(b'\x89PNG\r\n\x1a\n') if suffix=='.png' else payload.startswith(b'\xff\xd8\xff') if suffix in {'.jpg','.jpeg'} else payload.startswith(b'RIFF') and payload[8:12]==b'WEBP'
            if not valid:raise ValueError('Keep the edited image in its original file format.')
    elif suffix in TEXT:
        try:old=original.decode('utf-8-sig')
        except UnicodeError:raise ValueError('This file needs an editor that supports its text encoding.') from None
        newline='\r\n' if '\r\n' in old and '\n' not in old.replace('\r\n','') else '\n'
        if 'rows' in data and suffix in {'.csv','.tsv'}:
            rows=data['rows']
            if not isinstance(rows,list) or any(not isinstance(row,list) or any(not isinstance(cell,str) for cell in row) for row in rows) or sum(map(len,rows))>100000:raise ValueError('This table is too large or contains unsupported cells.')
            delimiter=inspect(path).get('delimiter')
            if delimiter is None:raise ValueError('Use text editing for this large table.')
            out=io.StringIO(newline='')
            csv.writer(out,delimiter=delimiter,lineterminator=newline).writerows(rows);text=out.getvalue()
        else:
            text=data.get('content')
            if not isinstance(text,str) or '\x00' in text:raise ValueError('Enter valid text to save.')
            if newline=='\r\n':text=text.replace('\r\n','\n').replace('\n','\r\n')
        payload=(b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b'')+text.encode('utf-8')
        if len(payload)>MAX_TEXT:raise ValueError('This text file is too large for the inline editor.')
    else:raise ValueError('Use another editor, then import an edited version of this file.')
    if not payload and suffix not in TEXT:raise ValueError('The edited file is empty.')
    if len(payload)>MAX_FILE:raise ValueError('The edited file is larger than 32 MB.')
    root=workspace_root().resolve();owned=root/'attachments'/bid
    parent=path.parent if path.is_relative_to(owned) else owned/'work'/'Edited files'
    if mode=='save':target=unlinked(path)
    else:
        label=data.get('name')
        if not label:
            n=int(asset.get('version','1'))+1 if asset and str(asset.get('version','')).isdigit() else 2
            for attempt in range(1000):
                label=f'{path.stem} v{n+attempt}{path.suffix}' if mode=='version' else f'{path.stem} copy'+(f' {attempt+1}' if attempt else '')+path.suffix
                if not (parent/label).exists():break
            else:raise ValueError('Choose another file name.')
        relative=safe(label)
        if len(relative.parts)!=1 or relative.suffix.lower()!=suffix:raise ValueError('Choose a file name with the original extension.')
        target=unlinked(parent/relative)
        if target.exists():raise ValueError('That file already exists. Choose another name.')
    target.parent.mkdir(parents=True,exist_ok=True)
    with destination_lock(path) if writable else nullcontext(),destination_lock(target) if target!=path else nullcontext():
        if mode!='copy' and revision(path)!=data['expected_revision']:raise Conflict('This file changed outside the editor. Reload it, or save your edits as a separate copy.')
        if mode!='save' and target.exists():raise ValueError('That file already exists. Choose another name.')
        import workspace_history
        if mode=='save':
            try:workspace_history.managed(path,bid)
            except ValueError:pass
            else:workspace_history.capture(path,bid,'Before edit',original)
        fd,tmp=tempfile.mkstemp(prefix='.aura-edit-',suffix='.tmp',dir=target.parent)
        try:
            with os.fdopen(fd,'wb') as stream:stream.write(payload);stream.flush();os.fsync(stream.fileno())
            if mode=='save':os.chmod(tmp,stat.S_IMODE(path.stat().st_mode))
            os.replace(tmp,target);tmp=None
        finally:
            if tmp:Path(tmp).unlink(missing_ok=True)
        try:
            if mode=='save':saved=_asset(target,bid,asset,asset.get('version','1') if asset else '1',existing=asset)
            else:
                if not asset and track_source:asset=_asset(path,bid,None,'1')
                version=str(int(asset['version'])+1) if mode=='version' and asset and str(asset.get('version','')).isdigit() else '1' if mode=='copy' else target.stem
                saved=_asset(target,bid,asset,version,lineage=[asset['id']] if asset else None)
        except Exception:
            # File and metadata form one user save. Restore the pre-save bytes
            # only if another program has not changed the result in the meantime.
            with target.open('rb') as stream:unchanged=stream.read(MAX_FILE+1)==payload
            if mode=='save' and unchanged:
                fd,tmp=tempfile.mkstemp(prefix='.aura-edit-',dir=target.parent)
                with os.fdopen(fd,'wb') as stream:stream.write(original)
                os.chmod(tmp,stat.S_IMODE(target.stat().st_mode))
                os.replace(tmp,target)
            elif unchanged:target.unlink(missing_ok=True)
            raise
    return {'path':target.relative_to(root).as_posix() if target.is_relative_to(root) else str(target),'name':target.name,'revision':revision(target),'asset':saved['id'],'mode':mode}


def libreoffice():
    found=shutil.which('libreoffice') or shutil.which('soffice')
    candidates=[Path('/Applications/LibreOffice.app/Contents/MacOS/soffice')]
    if os.name=='nt':candidates=[Path(os.environ.get(key,''))/'LibreOffice/program/soffice.exe' for key in ('PROGRAMFILES','PROGRAMFILES(X86)','LOCALAPPDATA') if os.environ.get(key)]
    return found or next((str(p) for p in candidates if p.is_file()),'')


def open_in(path,application):
    path=Path(path)
    if path.suffix.lower() not in OPENABLE:raise ValueError('Open this file through your editor directly.')
    if application=='libreoffice':
        executable=libreoffice()
        if not executable:raise ValueError('Install LibreOffice, then check again.')
        subprocess.Popen([executable,'--norestore',str(path)],creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    elif application=='default':
        if os.name=='nt':os.startfile(str(path))
        else:subprocess.Popen(['open' if sys.platform=='darwin' else 'xdg-open',str(path)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    else:raise ValueError('Choose an available editor.')
    return {'opened':True}


def main():
    import argparse
    from _common import workspace_scope
    from workspace_ui import local_file,records,asset_path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['show','save']);parser.add_argument('--workspace',type=Path,default=workspace_root());parser.add_argument('--business-id',required=True);parser.add_argument('--path',required=True);parser.add_argument('--input',help='JSON save request file');parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    with workspace_scope(args.workspace):
        path=local_file(args.business_id,args.path)
        asset=next((r['data'] for r in records(args.business_id)[0] if r['type']=='Asset' and asset_path(args.business_id,r['data'].get('location_reference'))==path),None)
        writable=path.is_relative_to(workspace_root().resolve()/'attachments'/args.business_id) or path.is_relative_to(workspace_root().resolve()/'knowledge'/args.business_id)
        result=inspect(path,writable,asset) if args.action=='show' else save(path,args.business_id,read_json_input(args.input),writable,asset)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
