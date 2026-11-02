// File widgets are optional views over the shared document API, never file owners.
const $=s=>document.querySelector(s),esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const drafts=new Map(),imports=new Map();let current=null;
function css(href){if(!document.querySelector(`link[href="${href}"]`)){const el=document.createElement('link');el.rel='stylesheet';el.href=href;document.head.append(el);}}
css('/file-editor.css');
function live(view){return current===view&&view.host.isConnected&&$('#detail').open&&view.ctx.current();}
function mounted(view,area){return live(view)&&view.host.contains(area);}
function key(view){return 'aura-file-draft:v1:'+JSON.stringify([view.ctx.workspace,view.ctx.business,view.info.identity]);}
function readDraft(view){try{return drafts.get(key(view))||JSON.parse(sessionStorage.getItem(key(view))||'null');}catch{return null;}}
function snapshot(view){
  if(view.editor)view.edit.text=view.editor.state.doc.toString();
  if(view.table&&!view.building)view.edit.rows=tableRows(view);
  if(view.cropper)view.edit.image=view.cropper.getData(true);
  if(!view.dirty)return;
  const saved={...view.edit,revision:view.info.revision,dirty:true,mode:view.mode,name:view.name,memoryOnly:view.memoryOnly};drafts.set(key(view),saved);
  try{sessionStorage.setItem(key(view),JSON.stringify(saved));}catch{view.memoryOnly=true;saved.memoryOnly=true;}
}
function changed(view){if(!live(view)||view.building)return;view.dirty=true;snapshot(view);status(view,'Unsaved changes');const save=view.host.querySelector('#file-save');if(save)save.disabled=false;}
function status(view,message,error=false){if(!live(view))return;const el=view.host.querySelector('#file-status');if(el){el.textContent=message;el.classList.toggle('error',error);}}
function destroyWidgets(view){snapshot(view);view.editor?.destroy();view.editor=null;view.table?.destroy();view.table=null;if(view.cropper){view.cropper.destroy();view.cropper=null;}view.pdfTask?.cancel();view.pdfTask=null;}
export function detach(){if(!current)return;const view=current;destroyWidgets(view);view.pdf?.destroy();view.pdf=null;view.loadingTask?.destroy();if(view.objectURL)URL.revokeObjectURL(view.objectURL);current=null;$('#detail')?.removeAttribute('data-file-wide');}
function media(view,download=false){return '/api/media?'+new URLSearchParams({business:view.ctx.business,workspace:view.ctx.workspace,path:view.ctx.ref,option:view.ctx.option||'',...(download?{download:'1'}:{})});}
function api(view,path,data){return view.ctx.api(path,data);}
function tableRows(view){const data=view.table.getData('active');return data.map(row=>Array.from({length:view.columns},(_,i)=>String(row['c'+i]??'')));}
function label(n){let name='';for(n++;n;n=Math.floor((n-1)/26))name=String.fromCharCode(65+(n-1)%26)+name;return name;}
function nextName(view){const dot=view.info.name.lastIndexOf('.'),stem=dot<0?view.info.name:view.info.name.slice(0,dot),ext=dot<0?'':view.info.name.slice(dot);return view.mode==='copy'?stem+' copy'+ext:stem+' v'+Math.max(2,...(view.info.related||[]).map(r=>Number(r.version)+1).filter(Number.isFinite))+ext;}

export async function openFile(ctx){
  detach();ctx.details('File',`<div id="file-workspace"><p>Opening file…</p></div>`,'context');
  const view={ctx,host:$('#file-workspace'),dirty:false,editing:false,edit:{},mode:'save',columns:0};current=view;
  try{
    const info=await api(view,'/api/documents?'+new URLSearchParams({business:ctx.business,workspace:ctx.workspace,path:ctx.ref,option:ctx.option||''}));
    if(!live(view)||info.workspace!==ctx.workspace)return;
    view.info=info;view.imported=imports.get(key(view));view.edit={text:info.text,rows:info.rows?.map(r=>[...r])};view.mode=info.writable?(info.kind==='image'?'version':'save'):'copy';view.name=nextName(view);
    const saved=readDraft(view);if(saved){view.edit={...view.edit,...saved};view.dirty=true;view.mode=saved.mode||view.mode;view.name=saved.name||view.name;view.info.revision=saved.revision;view.editing=info.editable;}
    if(view.imported){view.dirty=true;view.mode='version';}$('#detail-title').textContent=info.name;await render(view);
  }catch(error){if(live(view))view.host.innerHTML=`<p class="error">${esc(error.message)}</p>`;}
}
async function render(view){
  if(!live(view))return;destroyWidgets(view);const info=view.info;
  const editing=view.editing||view.dirty;
  view.host.innerHTML=`
    <div class="file-toolbar">
      <div class="filters file-modes">
        <button type="button" data-file-mode="preview" class="${view.editing?'':'active'}" aria-pressed="${!view.editing}">Preview</button>
        ${info.editable&&!view.imported?`<button type="button" data-file-mode="edit" class="${view.editing?'active':''}" aria-pressed="${view.editing}">Edit</button>`:''}
      </div>
      <div class="file-toolbar-actions">
        <button type="button" class="text-button" data-file-action="expand">${$('#detail').hasAttribute('data-file-wide')?'Reduce':'Expand'}</button>
        <button type="button" class="secondary" data-file-action="open" aria-controls="file-open-panel" aria-expanded="false">Open in…</button>
      </div>
    </div>
    <div id="file-open-panel" class="file-open-panel" hidden></div>
    <div id="file-tools"></div>
    <div id="file-canvas" class="file-canvas" tabindex="-1"></div>
    <div id="file-savebar" class="file-savebar" ${editing?'':'hidden'}>
      <label>Save to<select id="file-save-mode">
        ${info.writable&&!view.imported?'<option value="save">Original file</option>':`<option value="save" disabled>Original file (${view.imported?'keep original':'read-only'})</option>`}
        <option value="version">New version</option><option value="copy">Workspace copy</option>
      </select></label>
      <label id="file-name-field">File name<input id="file-save-name" maxlength="120" value="${esc(view.name)}"></label>
    </div>
    <div class="file-save-actions">
      <button type="button" id="file-save" class="primary" ${editing?'':'hidden'} ${view.dirty?'':'disabled'}>Save</button>
      <button type="button" id="file-download" class="secondary">Download copy</button>
      <button type="button" class="text-button" data-file-action="revert" ${editing?'':'hidden'}>${view.imported?'Cancel import':'Revert edits'}</button>
    </div>
    <p id="file-status" class="file-status" role="status">${view.imported?'Edited file ready to save.':view.dirty?'Unsaved changes':''}</p>
    <div id="file-conflict" class="file-conflict" hidden>
      <button type="button" class="secondary" data-file-action="reload">Reload file</button>
      <button type="button" class="secondary" data-file-action="conflict-copy">Save edits as a copy</button>
    </div>
    <div class="file-secondary-actions">
      ${info.revision?'<button type="button" class="text-button" id="file-import-choose">Import edited version…</button><input id="file-import-edited" type="file" hidden>':''}
      ${!view.ctx.ref.startsWith('library/')?'<button type="button" class="text-button" id="file-share-copy" title="Share a copy with another workspace">Share…</button>':''}
    </div>
    ${info.related?.length>1?`<details class="file-related"><summary>Versions &amp; copies · ${info.related.length}</summary>${info.related.map(r=>`<button type="button" class="row compact" data-file-related="${esc(r.ref)}"><span>${esc(r.name)}</span><small>v${esc(r.version)}</small></button>`).join('')}</details>`:''}
    <button type="button" id="file-copy-location" class="file-location" title="${esc(info.location||view.ctx.ref)}" aria-label="Copy file location">
      <span class="file-location-caption">Location</span><span class="file-location-path">${esc(info.location||view.ctx.ref)}</span>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h4"/></svg>
    </button>`;
  const mode=view.host.querySelector('#file-save-mode');mode.value=view.mode;
  if(!mode.value||mode.selectedOptions[0]?.disabled){mode.value='copy';view.mode='copy';}
  view.host.querySelector('#file-name-field').hidden=view.mode==='save';
  mode.onchange=()=>{view.mode=mode.value;view.name=nextName(view);view.host.querySelector('#file-save-name').value=view.name;view.host.querySelector('#file-name-field').hidden=view.mode==='save';snapshot(view);};
  view.host.querySelector('#file-save-name').oninput=e=>{view.name=e.target.value;snapshot(view);};
  view.host.querySelector('#file-save').onclick=()=>save(view);
  view.host.querySelector('#file-download').onclick=()=>download(view);
  view.host.querySelector('#file-copy-location').onclick=async()=>{try{await navigator.clipboard.writeText(info.location||view.ctx.ref);status(view,'File location copied.');}catch(e){status(view,e.message,true);}};
  view.host.querySelector('#file-share-copy')?.addEventListener('click',()=>view.ctx.share?.(view.ctx.ref));
  const importer=view.host.querySelector('#file-import-edited');
  if(importer){
    importer.accept=info.name.includes('.')?'.'+info.name.split('.').at(-1):'';
    view.host.querySelector('#file-import-choose').onclick=()=>importer.click();
    importer.onchange=()=>prepareImport(view,importer.files[0]);
  }
  view.host.onclick=event=>{const button=event.target.closest('button');if(!button)return;const action=button.dataset.fileAction;
    if(button.dataset.fileMode){snapshot(view);view.editing=button.dataset.fileMode==='edit';render(view).catch(e=>status(view,e.message,true));}
    if(button.dataset.fileRelated)openFile({...view.ctx,ref:button.dataset.fileRelated});
    if(action==='expand'){$('#detail').toggleAttribute('data-file-wide');button.textContent=$('#detail').hasAttribute('data-file-wide')?'Reduce':'Expand';if(info.kind==='pdf')renderPdf(view);view.table?.redraw(true);}
    if(action==='open')openPanel(view);
    if(action==='revert'||action==='reload'){if(view.dirty&&!confirm('Discard these unsaved edits and reload the file?'))return;clearDraft(view);openFile(view.ctx);}
    if(action==='conflict-copy'){view.mode='copy';view.name=nextName(view);save(view);}
  };
  const area=view.host.querySelector('#file-canvas');
  if(view.imported){area.innerHTML=`<div class="file-pending-import"><strong>${esc(view.imported.name)}</strong><p>Save as a new version or copy to keep the original.</p></div>`;}
  else if(view.editing&&info.kind==='text'){
    const {EditorView,basicSetup,markdown}=await import('/vendor/text-editor.js');if(!mounted(view,area))return;
    const extensions=[basicSetup,EditorView.lineWrapping,EditorView.cspNonce.of(view.ctx.token),EditorView.updateListener.of(update=>{if(update.docChanged)changed(view);})];
    if(/\.m(?:d|arkdown)$/i.test(info.name))extensions.push(markdown());
    view.editor=new EditorView({doc:view.edit.text||'',extensions,parent:area});view.editor.contentDOM.setAttribute('aria-label','Edit '+info.name);
  }else if(view.editing&&info.kind==='table')await editTable(view,area);
  else if(view.editing&&info.kind==='image')await editImage(view,area);
  else if(info.kind==='text')area.innerHTML=/\.m(?:d|arkdown)$/i.test(info.name)?`<article class="file-markdown">${view.ctx.markdown(view.edit.text||'')}</article>`:`<pre>${esc(view.edit.text||'')}</pre>`;
  else if(info.kind==='table')area.innerHTML=`<div class="file-table-preview"><table>${(view.edit.rows||[]).slice(0,200).map(row=>`<tr>${row.map(cell=>`<td>${esc(cell)}</td>`).join('')}</tr>`).join('')}</table></div>${view.edit.rows?.length>200?'<p>Previewing the first 200 rows. Choose Edit to see the full table.</p>':''}`;
  else if(info.kind==='image')await previewImage(view,area);
  else if(info.kind==='pdf')await previewPdf(view,area);
  else if(info.kind==='media'){
    const audio=/\.(mp3|wav|ogg|m4a|aac|flac|opus)$/i.test(info.name),element=document.createElement(audio?'audio':'video');element.controls=true;element.preload='metadata';element.src=media(view);element.className='media-preview';area.replaceChildren(element);
  }else area.innerHTML=`<div class="empty"><strong>${info.kind==='office'?'Open this document in an editor':'No inline preview'}</strong><p>${info.kind==='office'?'Choose an editor with Open in above.':''}</p></div>`;
}
async function editTable(view,area){
  css('/vendor/data-grid.css');const {Tabulator}=await import('/vendor/data-grid.js');if(!mounted(view,area))return;
  view.columns=Math.max(1,...(view.edit.rows||[]).map(r=>r.length));view.nextRow=(view.edit.rows||[]).length;
  const columns=Array.from({length:view.columns},(_,i)=>({title:label(i),field:'c'+i,editor:'input',formatter:'plaintext',width:135}));
  const data=(view.edit.rows||[]).map((row,i)=>Object.fromEntries([['_row',i],...Array.from({length:view.columns},(_,c)=>['c'+c,row[c]??''])]));
  view.host.querySelector('#file-tools').innerHTML='<div class="file-tool-row"><button type="button" class="secondary" id="file-add-row">Add row</button><button type="button" class="secondary" id="file-add-column">Add column</button><button type="button" class="text-button" id="file-delete-rows">Remove selected rows</button></div>';
  view.building=true;view.table=new Tabulator(area,{data,index:'_row',columns,height:380,layout:'fitData',renderHorizontal:'virtual',selectableRows:true,rowHeader:{formatter:'rowSelection',titleFormatter:'rowSelection',headerSort:false,width:38},clipboard:true});
  view.table.on('tableBuilt',()=>{view.building=false;});view.table.on('cellEdited',()=>changed(view));view.table.on('dataChanged',()=>changed(view));view.table.on('dataSorted',sorters=>{if(sorters.length)changed(view);});
  view.host.querySelector('#file-add-row').onclick=()=>view.table.addRow({_row:view.nextRow++});
  view.host.querySelector('#file-add-column').onclick=async()=>{const c=view.columns++;await view.table.addColumn({title:label(c),field:'c'+c,editor:'input',formatter:'plaintext',width:135});changed(view);};
  view.host.querySelector('#file-delete-rows').onclick=()=>view.table.deleteRow(view.table.getSelectedData().map(r=>r._row));
}
function applyImageData(cropper,data){
  cropper.clear();cropper.rotateTo(data.rotate||0);
  const canvas=cropper.getCanvasData(),box=cropper.getContainerData(),scale=Math.min(box.width/canvas.naturalWidth,box.height/canvas.naturalHeight),width=canvas.naturalWidth*scale,height=canvas.naturalHeight*scale;
  cropper.setCanvasData({left:(box.width-width)/2,top:(box.height-height)/2,width,height});cropper.crop();cropper.setData(data);
}
function rotateImage(view,angle){
  const cropper=view.cropper,data=cropper.getData(),canvas=cropper.getCanvasData();
  const rotated=angle>0?{x:canvas.naturalHeight-data.y-data.height,y:data.x,width:data.height,height:data.width}:{x:data.y,y:canvas.naturalWidth-data.x-data.width,width:data.height,height:data.width};
  applyImageData(cropper,{...data,...rotated,rotate:(data.rotate||0)+angle});changed(view);
}
async function editImage(view,area){
  css('/vendor/image-editor.css');const {Cropper}=await import('/vendor/image-editor.js');if(!mounted(view,area))return;
  const img=document.createElement('img');img.src=media(view);img.alt=view.info.name;area.replaceChildren(img);area.classList.add('file-image-edit');
  view.host.querySelector('#file-tools').innerHTML='<div class="file-tool-row"><button type="button" class="secondary" id="file-rotate-left">Rotate left</button><button type="button" class="secondary" id="file-rotate-right">Rotate right</button><button type="button" class="text-button" id="file-image-reset">Reset</button><label>Width<input id="file-image-width" type="number" min="1" max="12000" placeholder="Original"></label></div>';
  view.building=true;view.cropper=new Cropper(img,{viewMode:1,autoCropArea:1,checkOrientation:false,ready(){if(view.edit.image)applyImageData(view.cropper,view.edit.image);view.building=false;},cropend(){changed(view);},zoom(){}});
  view.host.querySelector('#file-rotate-left').onclick=()=>rotateImage(view,-90);view.host.querySelector('#file-rotate-right').onclick=()=>rotateImage(view,90);view.host.querySelector('#file-image-reset').onclick=()=>{view.cropper.reset();view.edit.width=null;view.host.querySelector('#file-image-width').value='';changed(view);};
  const width=view.host.querySelector('#file-image-width');width.value=view.edit.width||'';width.oninput=()=>{view.edit.width=Number(width.value)||null;changed(view);};
}
async function imageCanvas(view){
  if(view.cropper)return view.cropper.getCroppedCanvas({maxWidth:12000,maxHeight:12000,...(view.edit.width?{width:view.edit.width}:{})});
  const {Cropper}=await import('/vendor/image-editor.js');
  const box=document.createElement('div');box.className='file-image-scratch';document.body.append(box);const img=document.createElement('img');img.src=media(view);box.append(img);
  return await new Promise((resolve,reject)=>{const cropper=new Cropper(img,{viewMode:1,autoCropArea:1,ready(){if(view.edit.image)applyImageData(cropper,view.edit.image);const canvas=cropper.getCroppedCanvas({maxWidth:12000,maxHeight:12000,...(view.edit.width?{width:view.edit.width}:{})});cropper.destroy();box.remove();resolve(canvas);}});img.onerror=()=>{box.remove();reject(Error('The image could not be opened.'));};});
}
async function previewImage(view,area){
  const image=view.dirty&&view.edit.image?await imageCanvas(view):document.createElement('img');if(!mounted(view,area))return;
  if(image.tagName==='IMG'){image.src=media(view);image.alt=view.info.name;}image.className='file-image-preview';area.replaceChildren(image);area.classList.add('file-image-area');
  view.host.querySelector('#file-tools').innerHTML='<div class="file-tool-row"><button type="button" class="text-button" id="file-image-fit">Fit</button><button type="button" class="text-button" id="file-image-zoom-in">Zoom in</button><button type="button" class="text-button" id="file-image-zoom-out">Zoom out</button></div>';
  const zoom=factor=>{image.style.width=Math.max(40,image.getBoundingClientRect().width*factor)+'px';image.style.maxWidth='none';};view.host.querySelector('#file-image-zoom-in').onclick=()=>zoom(1.25);view.host.querySelector('#file-image-zoom-out').onclick=()=>zoom(.8);view.host.querySelector('#file-image-fit').onclick=()=>{image.style.width='';image.style.maxWidth='100%';};
}
async function previewPdf(view,area){
  view.host.querySelector('#file-tools').innerHTML='<div class="file-tool-row file-pdf-tools"><button type="button" class="secondary" id="file-pdf-prev" aria-label="Previous page">‹</button><label>Page<input id="file-pdf-page" type="number" min="1" value="1"></label><span id="file-pdf-count"></span><button type="button" class="secondary" id="file-pdf-next" aria-label="Next page">›</button><button type="button" class="text-button" id="file-pdf-zoom-out" aria-label="Zoom out">−</button><button type="button" class="text-button" id="file-pdf-zoom-in" aria-label="Zoom in">+</button><label class="file-pdf-search"><span class="sr-only">Find in PDF</span><input id="file-pdf-find" type="search" placeholder="Find in PDF"></label><button type="button" class="text-button" id="file-pdf-search">Find next</button></div>';
  area.innerHTML='<p>Opening PDF…</p>';
  if(!view.pdf){const pdfjs=await import('/vendor/pdf.mjs');if(!live(view))return;pdfjs.GlobalWorkerOptions.workerSrc='/vendor/pdf.worker.mjs';view.loadingTask=pdfjs.getDocument({url:media(view),httpHeaders:{'X-Aura-Token':view.ctx.token},isEvalSupported:false,cMapUrl:'/vendor/pdf-resources/cmaps/',cMapPacked:true,standardFontDataUrl:'/vendor/pdf-resources/standard_fonts/',wasmUrl:'/vendor/pdf-resources/wasm/'});view.pdf=await view.loadingTask.promise;view.loadingTask=null;}
  if(!live(view))return;view.page=view.page||1;view.zoom=view.zoom||1;view.host.querySelector('#file-pdf-count').textContent='of '+view.pdf.numPages;view.host.querySelector('#file-pdf-page').max=view.pdf.numPages;
  const turn=delta=>{view.page=Math.max(1,Math.min(view.pdf.numPages,view.page+delta));renderPdf(view);};view.host.querySelector('#file-pdf-prev').onclick=()=>turn(-1);view.host.querySelector('#file-pdf-next').onclick=()=>turn(1);view.host.querySelector('#file-pdf-page').onchange=e=>{view.page=Math.max(1,Math.min(view.pdf.numPages,Number(e.target.value)||1));renderPdf(view);};
  view.host.querySelector('#file-pdf-zoom-in').onclick=()=>{view.zoom=Math.min(3,view.zoom+.25);renderPdf(view);};view.host.querySelector('#file-pdf-zoom-out').onclick=()=>{view.zoom=Math.max(.5,view.zoom-.25);renderPdf(view);};
  view.host.querySelector('#file-pdf-search').onclick=async()=>{const ticket=view.searchTicket=(view.searchTicket||0)+1;try{const query=view.host.querySelector('#file-pdf-find').value.trim().toLocaleLowerCase();if(!query)return;status(view,'Searching…');for(let offset=1;offset<=view.pdf.numPages&&live(view)&&ticket===view.searchTicket;offset++){const index=(view.page-1+offset)%view.pdf.numPages+1,text=await(await view.pdf.getPage(index)).getTextContent();if(text.items.map(i=>i.str).join(' ').toLocaleLowerCase().includes(query)){view.page=index;await renderPdf(view);status(view,'Found on page '+index);return;}}if(ticket===view.searchTicket)status(view,'No matching text found.');}catch(e){if(live(view))status(view,e.message,true);}};
  await renderPdf(view);
}
async function renderPdf(view){
  if(!live(view)||!view.pdf)return;view.pdfTask?.cancel();const ticket=view.pdfTicket=(view.pdfTicket||0)+1;
  try{const page=await view.pdf.getPage(view.page);if(!live(view)||ticket!==view.pdfTicket)return;const area=view.host.querySelector('#file-canvas'),base=page.getViewport({scale:1}),width=Math.max(200,area.clientWidth-18),viewport=page.getViewport({scale:width/base.width*view.zoom});const canvas=document.createElement('canvas'),ratio=Math.min(devicePixelRatio||1,2,Math.sqrt(16000000/(viewport.width*viewport.height)));canvas.width=Math.floor(viewport.width*ratio);canvas.height=Math.floor(viewport.height*ratio);canvas.style.width=viewport.width+'px';canvas.style.height=viewport.height+'px';canvas.setAttribute('aria-label','PDF page '+view.page);area.replaceChildren(canvas);view.host.querySelector('#file-pdf-page').value=view.page;view.host.querySelector('#file-pdf-prev').disabled=view.page===1;view.host.querySelector('#file-pdf-next').disabled=view.page===view.pdf.numPages;view.pdfTask=page.render({canvasContext:canvas.getContext('2d'),viewport,transform:[ratio,0,0,ratio,0,0]});await view.pdfTask.promise;view.pdfTask=null;}catch(e){if(e.name!=='RenderingCancelledException')status(view,e.message,true);}
}
function clearDraft(view){drafts.delete(key(view));imports.delete(key(view));view.imported=null;try{sessionStorage.removeItem(key(view));}catch{}view.dirty=false;}
function toBase64(file){return new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(String(reader.result).split(',')[1]);reader.onerror=()=>reject(Error('This file could not be read.'));reader.readAsDataURL(file);});}
async function editedPayload(view,imported=view.imported){
  if(imported){if(imported.size>32*1048576)throw Error('Choose an edited file smaller than 32 MB.');return {encoding:'base64',content:await toBase64(imported)};}
  if(view.info.kind==='image'){const canvas=await imageCanvas(view),mime=/\.png$/i.test(view.info.name)?'image/png':/\.webp$/i.test(view.info.name)?'image/webp':'image/jpeg';return {encoding:'base64',content:canvas.toDataURL(mime,.95).split(',')[1]};}
  if(view.info.kind==='table')return {rows:view.edit.rows||[]};
  return {content:view.edit.text||''};
}
async function download(view){
  if(!live(view))return;const button=view.host.querySelector('#file-download');button.disabled=true;
  try{
    document.activeElement?.blur();snapshot(view);let href=media(view,true),name=view.info.name,temporary=false;
    if(view.dirty){
      const payload=await editedPayload(view);if(!live(view))return;
      let content;
      if(payload.encoding==='base64')content=Uint8Array.from(atob(payload.content),c=>c.charCodeAt(0));
      else{
        const original=view.info.text||'',newline=original.includes('\r\n')&&!original.replaceAll('\r\n','').includes('\n')?'\r\n':'\n',delimiter=view.info.delimiter||',';
        let text=payload.rows?payload.rows.map(row=>row.map(cell=>/["\r\n]/.test(cell)||cell.includes(delimiter)?'"'+cell.replaceAll('"','""')+'"':cell).join(delimiter)).join(newline)+(payload.rows.length?newline:''):payload.content;
        if(!payload.rows&&newline==='\r\n')text=text.replaceAll('\r\n','\n').replaceAll('\n',newline);
        content=(view.info.bom?'\uFEFF':'')+text;
      }
      href=URL.createObjectURL(new Blob([content],{type:'application/octet-stream'}));temporary=true;name=view.mode==='save'?name:view.name||name;
    }
    const link=document.createElement('a');link.href=href;link.download=name;document.body.append(link);link.click();link.remove();
    if(temporary)setTimeout(()=>URL.revokeObjectURL(href),10000);
  }catch(e){status(view,e.message,true);}finally{if(button.isConnected)button.disabled=false;}
}
async function save(view,imported=null){
  if(!live(view)||view.saving)return;view.saving=true;document.activeElement?.blur();snapshot(view);const button=view.host.querySelector('#file-save');button.disabled=true;status(view,'Saving…');
  if(imported){view.imported=imported;view.dirty=true;imports.set(key(view),imported);}
  imported=imported||view.imported;
  try{
    let data={business:view.ctx.business,workspace:view.ctx.workspace,path:view.ctx.ref,option:view.ctx.option||'',expected_revision:view.info.revision,mode:view.mode,...(view.mode!=='save'?{name:view.name}:{})};
    data={...data,...await editedPayload(view,imported)};
    if(!live(view))return;
    const saved=await api(view,'/api/documents/save',data);if(!live(view))return;
    clearDraft(view);await view.ctx.saved?.(saved).catch(()=>{});if(!live(view))return;await openFile({...view.ctx,ref:'asset/'+saved.asset,option:''});if(current)status(current,saved.mode==='save'?'Saved.':saved.mode==='version'?'New version saved.':'Copy saved.');
  }catch(e){status(view,e.message,true);if(e.status===409){view.host.querySelector('#file-conflict').hidden=false;}if(button.isConnected)button.disabled=false;}finally{view.saving=false;}
}
async function prepareImport(view,file){
  if(!file||!live(view)||view.saving)return;
  const ext=view.info.name.split('.').at(-1).toLowerCase();
  if(!file.name.toLowerCase().endsWith('.'+ext)){status(view,'Choose the edited file in its original format.',true);return;}
  if(file.size>32*1048576){status(view,'Choose an edited file smaller than 32 MB.',true);return;}
  if(view.dirty&&!confirm('Replace these unsaved edits with the imported file?'))return;
  clearDraft(view);view.imported=file;imports.set(key(view),file);view.dirty=true;view.editing=false;view.mode='version';view.name=nextName(view);
  try{await render(view);}catch(e){status(view,e.message,true);}
}
function openPanel(view){
  const panel=view.host.querySelector('#file-open-panel');panel.hidden=!panel.hidden;
  view.host.querySelector('[data-file-action=open]').setAttribute('aria-expanded',String(!panel.hidden));
  if(panel.hidden)return;
  panel.innerHTML=`<div class="file-open-row"><label>Open in<select id="file-open-app"><option value="default">Default app</option><option value="google">Google Office</option><option value="libreoffice">LibreOffice</option></select></label><button type="button" class="secondary" id="file-open-go">Open</button></div><div id="file-open-help"></div>`;
  const select=panel.querySelector('#file-open-app'),go=panel.querySelector('#file-open-go'),help=panel.querySelector('#file-open-help');select.value=view.application||'default';
  const update=()=>{
    view.application=select.value;const missing=select.value==='libreoffice'&&!view.info.libreoffice_installed;go.hidden=missing;
    help.innerHTML=missing?'<p>Install LibreOffice, then check again.</p><div class="file-install-actions"><a class="secondary" href="https://www.libreoffice.org/download/" target="_blank" rel="noopener noreferrer">Get LibreOffice ↗</a><button type="button" class="text-button" id="file-open-check">Check again</button></div>':select.value==='google'?'<p>Opens Google Drive. Use Download copy below, upload it there, then bring your edits back with Import edited version.</p>':'';
    help.querySelector('#file-open-check')?.addEventListener('click',async event=>{
      const button=event.currentTarget;button.disabled=true;button.textContent='Checking…';
      try{const fresh=await api(view,'/api/documents?'+new URLSearchParams({business:view.ctx.business,workspace:view.ctx.workspace,path:view.ctx.ref,option:view.ctx.option||''}));if(!live(view))return;view.info.libreoffice_installed=fresh.libreoffice_installed;update();status(view,fresh.libreoffice_installed?'LibreOffice is ready.':'LibreOffice was not found yet.');}
      catch(e){status(view,e.message,true);if(button.isConnected){button.disabled=false;button.textContent='Check again';}}
    });
  };
  select.onchange=update;update();
  go.onclick=async()=>{
    if(select.value==='google'){window.open('https://drive.google.com/drive/u/0/my-drive','_blank','noopener,noreferrer');return;}
    if(view.dirty){status(view,'Save your edits or download a copy before opening the file in another app.');return;}
    go.disabled=true;
    try{await api(view,'/api/documents/open',{business:view.ctx.business,workspace:view.ctx.workspace,path:view.ctx.ref,option:view.ctx.option||'',application:select.value});status(view,'Opening in '+(select.value==='libreoffice'?'LibreOffice':'your default app')+'…');}
    catch(e){if(select.value==='libreoffice'&&e.message.includes('Install LibreOffice')){view.info.libreoffice_installed=false;update();}status(view,e.message,true);}finally{go.disabled=false;}
  };
  select.focus();
}
window.auraFiles={detach,hasUnsaved:()=>[...drafts.values()].some(d=>d.dirty)};
$('#detail').addEventListener('close',()=>{if(!$('#detail').open)detach();});
document.addEventListener('keydown',event=>{if(current&&live(current)&&(event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='s'){event.preventDefault();if(current.dirty)save(current);}});
window.addEventListener('beforeunload',event=>{if(imports.size||[...drafts.values()].some(d=>d.memoryOnly)||(current?.memoryOnly&&current.dirty)){event.preventDefault();event.returnValue='';}});
window.addEventListener('focus',async()=>{const view=current;if(!view||!live(view)||view.dirty)return;try{const fresh=await api(view,'/api/documents?'+new URLSearchParams({business:view.ctx.business,workspace:view.ctx.workspace,path:view.ctx.ref,option:view.ctx.option||''}));if(live(view)&&fresh.workspace===view.ctx.workspace&&fresh.revision!==view.info.revision){await openFile(view.ctx);if(current)status(current,'Updated from the file.');}}catch{/* The current preview remains available. */}});
