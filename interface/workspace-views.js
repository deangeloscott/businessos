/* Map, chart and board views of saved results, what's running for a project or goal, and goal progress.
   Everything here only draws data from the shared API; the CLI returns the same data. */
window.auraViews=(()=>{
  const blank='data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
  const palette=['#6654ce','#d0603a','#2f8f6b','#c99a1a','#3b78c2','#b4478f','#5e6b7a','#8a5a2b','#4aa3a1','#a33b3b','#6d8f2f','#9466c8'];
  const hiddenFields=new Set(['latitude','longitude','lat','lng','lon','yours','radius_km','radius_miles','maps_url','website','url']);
  const CLUSTER_FROM=40;
  let ticket=0,map=null;
  const scope=()=>JSON.stringify([state.business,state.data?.workspace]);
  const q=(route,values)=>route+'?'+new URLSearchParams({business:state.business,...values});
  const css=href=>{if(!document.querySelector(`link[href="${href}"]`)){const el=document.createElement('link');el.rel='stylesheet';el.href=href;document.head.append(el);}};
  const value=v=>typeof v==='number'?v.toLocaleString():String(v);
  const lowerBetter=f=>/^(rank|position)$/i.test(f||'');
  const day=t=>new Date(t).toLocaleDateString(undefined,{month:'short',day:'numeric'});
  const link=v=>typeof v==='string'&&/^https?:\/\//i.test(v)?v:'';
  const miles=/^en-(US|GB|LR)$|^my/i.test(navigator.language||'');
  function saved(id){try{return localStorage.getItem('aura-view:'+id);}catch{return null;}}
  function choice(id,shape){try{if(shape===undefined)return localStorage.getItem('aura-view:'+id)||'list';localStorage.setItem('aura-view:'+id,shape);}catch{}return shape||'list';}
  function release(){ticket++;if(map){map.remove();map=null;}}
  function fields(r,skip=[]){const shown=Object.entries(r.fields).filter(([k,v])=>!hiddenFields.has(k)&&k!=='address'&&!skip.includes(k)&&v!==null&&v!=='').slice(0,5);return shown.length?`<dl class="view-fields">${shown.map(([k,v])=>`<div><dt>${esc(human(k))}</dt><dd>${esc(value(v))}</dd></div>`).join('')}</dl>`:'';}
  function card(r,skip=[]){return `<strong>${esc(r.title)}</strong>${fields(r,skip)}<button type="button" class="text-button" data-view-find="${esc(r.title)}">Show in list</button>`;}

  /* How a result's numbers moved between its last two checks. */
  function moved(r,field){const t=(r.trail||[]).filter(p=>typeof p.values[field]==='number');if(t.length<2)return 0;const a=t[t.length-2].values[field],b=t[t.length-1].values[field];return a===b?0:(lowerBetter(field)?b<a:b>a)?1:-1;}

  /* Colour by a category (distinct colours, can be hidden from the legend) or by a number (a scale). */
  function colouring(rows,field,numbers){
    if(field&&numbers.includes(field)){
      const vals=rows.map(r=>r.fields[field]).filter(v=>typeof v==='number'),min=Math.min(...vals),max=Math.max(...vals),span=max-min||1;
      const good=lowerBetter(field);
      const of=r=>{const v=r.fields[field];if(typeof v!=='number')return '#9a98a6';const t=(v-min)/span;return good?`hsl(${Math.round(140-130*t)} 55% 42%)`:`hsl(250 ${Math.round(30+35*t)}% ${Math.round(72-40*t)}%)`;};
      return {numeric:true,min,max,good,of};
    }
    const order=[...new Set(rows.map(r=>r.fields[field]).filter(v=>v!==undefined&&v!==null&&v!==''))];
    return {numeric:false,order,of:r=>field&&order.includes(r.fields[field])?palette[order.indexOf(r.fields[field])%palette.length]:palette[0]};
  }
  function sizing(rows,field){
    if(!field)return ()=>20;
    const vals=rows.map(r=>r.fields[field]).filter(v=>typeof v==='number'),min=Math.min(...vals),max=Math.max(...vals),span=max-min||1;
    return r=>{const v=r.fields[field];if(typeof v!=='number')return 16;let t=(v-min)/span;if(lowerBetter(field))t=1-t;return Math.round(16+16*Math.sqrt(t));};
  }
  function distance(a,b){const rad=x=>x*Math.PI/180,dLat=rad(b.lat-a.lat),dLng=rad(b.lng-a.lng),h=Math.sin(dLat/2)**2+Math.cos(rad(a.lat))*Math.cos(rad(b.lat))*Math.sin(dLng/2)**2;const km=12742*Math.asin(Math.sqrt(h));return miles?`${(km/1.609344).toFixed(km<16?1:0)} mi`:`${km.toFixed(km<10?1:0)} km`;}

  /* Collection views. `find` returns to the list filtered to one result. */
  async function show(host,d,shape,view,search,find,reload){
    release();const mine=ticket,key=scope();host.innerHTML='<p class="small-note">Loading…</p>';
    host.onclick=e=>{const b=e.target.closest('[data-view-find]');if(b){release();find(b.dataset.viewFind);}};
    let data;
    try{data=await api(q('/api/collection-view',{id:d.id,view,q:search}));}
    catch(error){if(mine===ticket&&host.isConnected)host.innerHTML=`<p class="small-note">${esc(humanError(error))}</p>`;return;}
    if(mine!==ticket||key!==scope()||!host.isConnected)return;
    if(shape==='map')return drawMap(host,d,data,view,search,mine,key,find);
    const list=shape==='chart'?d.views.chart:d.views.board,picked=choice(d.id+':'+shape+'-field',undefined);
    const field=list.includes(picked)?picked:(shape==='board'&&list.find(f=>/^(status|stage|state|pipeline|phase)$/i.test(f)))||list[0];let mode=choice(d.id+':chart-mode',undefined)==='time'?'time':'now';
    host.innerHTML=`<div class="view-controls"><label>${shape==='chart'?'Compare':'Group by'}<select data-view-field>${list.map(f=>`<option value="${esc(f)}" ${f===field?'selected':''}>${esc(human(f))}</option>`).join('')}</select></label>${shape==='chart'?`<label>Show<select data-view-mode><option value="now">Latest</option><option value="time" ${mode==='time'?'selected':''}>Over time</option></select></label>`:''}</div><div data-view-body></div>`;
    let current=field;
    const paint=()=>{host.querySelector('[data-view-body]').innerHTML=shape==='board'?board(data.items,current):mode==='time'?trends(data.items,current):bars(data.items,current);if(shape==='board')movable(host,d,current,reload);};
    host.querySelector('[data-view-field]').onchange=e=>{current=e.target.value;choice(d.id+':'+shape+'-field',current);paint();};
    const modeSelect=host.querySelector('[data-view-mode]');if(modeSelect)modeSelect.onchange=e=>{mode=e.target.value;choice(d.id+':chart-mode',mode);paint();};
    paint();
  }
  function bars(rows,field){
    const good=lowerBetter(field),items=rows.filter(r=>typeof r.fields[field]==='number').sort((a,b)=>good?a.fields[field]-b.fields[field]:b.fields[field]-a.fields[field]),top=items.slice(0,30),peak=Math.max(...top.map(r=>Math.abs(r.fields[field])),0)||1;
    if(!items.length)return '<p class="small-note">No results have this number.</p>';
    const arrow=r=>({1:'<span class="moved up" title="Better than last check">▲</span>','-1':'<span class="moved down" title="Worse than last check">▼</span>'})[moved(r,field)]||'';
    return `<div class="view-bars">${top.map(r=>`<button type="button" class="bar-row" data-view-find="${esc(r.title)}" title="Show in list"><span class="bar-label">${esc(r.title)}</span><span class="bar-track"><span class="bar ${r.fields[field]<0?'negative':''}" style="width:${Math.max(1,Math.abs(r.fields[field])/peak*100)}%"></span></span><span class="bar-value">${esc(value(r.fields[field]))}${arrow(r)}</span></button>`).join('')}</div>${items.length>top.length?`<p class="small-note">Showing the top ${top.length} of ${items.length}.</p>`:''}${rows.length>items.length?`<p class="small-note">${rows.length-items.length} ${rows.length-items.length===1?'result has':'results have'} no ${esc(human(field).toLowerCase())}.</p>`:''}`;
  }
  /* A number over time for the business itself and the leading results, from each result's saved trail. */
  function trends(rows,field){
    const good=lowerBetter(field),latest=r=>r.fields[field];
    const series=rows.map(r=>({r,points:(r.trail||[]).filter(p=>typeof p.values[field]==='number').map(p=>({t:Date.parse(p.at),v:p.values[field]}))})).filter(s=>s.points.length);
    if(!series.some(s=>s.points.length>1))return '<p class="small-note">Trends appear once results have been checked at least twice.</p>';
    const yours=series.filter(s=>s.r.fields.yours===true),rest=series.filter(s=>s.r.fields.yours!==true&&typeof latest(s.r)==='number').sort((a,b)=>good?latest(a.r)-latest(b.r):latest(b.r)-latest(a.r));
    const shown=[...yours,...rest].slice(0,6),all=shown.flatMap(s=>s.points),t0=Math.min(...all.map(p=>p.t)),t1=Math.max(...all.map(p=>p.t)),v0=Math.min(...all.map(p=>p.v)),v1=Math.max(...all.map(p=>p.v));
    const w=560,h=190,pad=32,x=t=>pad+(t1===t0?0.5:(t-t0)/(t1-t0))*(w-pad*2),y=v=>{const t=v1===v0?0.5:(v-v0)/(v1-v0);return good?pad+t*(h-pad*2):h-pad-t*(h-pad*2);};
    const top=good?v0:v1,bottom=good?v1:v0;
    return `<svg class="metric-line trend-lines" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(human(field))} over time"><line x1="${pad}" y1="${h-pad}" x2="${w-pad}" y2="${h-pad}" class="axis"/><text x="${pad}" y="${h-10}" class="tick">${esc(day(t0))}</text><text x="${w-pad}" y="${h-10}" class="tick end">${esc(day(t1))}</text><text x="${pad-6}" y="${pad+4}" class="tick end">${esc(value(top))}</text><text x="${pad-6}" y="${h-pad+4}" class="tick end">${esc(value(bottom))}</text>${shown.map((s,i)=>`<g style="--series:${palette[i%palette.length]}"><polyline points="${s.points.map(p=>x(p.t)+','+y(p.v)).join(' ')}" class="trend series ${s.r.fields.yours===true?'yours':''}"/>${s.points.map(p=>`<circle cx="${x(p.t)}" cy="${y(p.v)}" r="3"><title>${esc(s.r.title)}: ${esc(value(p.v))} · ${esc(day(p.t))}</title></circle>`).join('')}</g>`).join('')}</svg><div class="view-legend">${shown.map((s,i)=>`<span><i style="background:${palette[i%palette.length]}"></i>${esc(s.r.title)}</span>`).join('')}</div>${good?'<p class="small-note">Lower is better, so the best rank is at the top.</p>':''}`;
  }
  function board(rows,field){
    const groups=new Map();rows.forEach(r=>{const g=r.fields[field]===undefined||r.fields[field]===null||r.fields[field]===''?'':String(r.fields[field]);if(!groups.has(g))groups.set(g,[]);groups.get(g).push(r);});
    const order=[...groups.keys()].sort((a,b)=>(a==='')-(b==='')||groups.get(b).length-groups.get(a).length);
    const named=order.filter(Boolean),move=r=>`<label class="board-move"><span class="sr-only">Move ${esc(r.title)} to</span><select data-board-move="${esc(r.id)}"><option value="">Move to…</option>${named.filter(g=>g!==String(r.fields[field]??'')).map(g=>`<option value="${esc(g)}">${esc(g)}</option>`).join('')}<option value="__new__">New ${esc(human(field).toLowerCase())}…</option></select></label>`;
    return `<div class="view-board" data-board-field="${esc(field)}">${order.map(g=>`<section class="board-column" data-board-group="${esc(g)}"><h4>${esc(g||'No '+human(field).toLowerCase())} <small>${groups.get(g).length}</small></h4>${groups.get(g).slice(0,50).map(r=>`<div class="board-card" draggable="true" data-board-item="${esc(r.id)}">${card(r,[field])}${move(r)}</div>`).join('')}${groups.get(g).length>50?`<p class="small-note">${groups.get(g).length-50} more in the list.</p>`:''}</section>`).join('')}</div><p class="small-note">Drag a card to another column, or use Move to. Your change is saved as your correction; the original value is kept.</p>`;
  }
  /* Moving a card saves the new value as the person's correction, reusing the collection's own feedback. */
  function movable(host,d,field,reload){
    const save=(id,value,undoable=true)=>attempt(async()=>{
      value=String(value||'').trim();if(!value||value.length>60)throw new Error('Enter a stage of up to 60 characters.');
      const before=host.querySelector(`[data-board-item="${CSS.escape(id)}"]`)?.closest('[data-board-group]')?.dataset.boardGroup||'';
      const current=await api(q('/api/collections',{id:d.id,limit:1}));
      await api('/api/collections',{business:state.business,id:d.id,action:'feedback',choice:'correct',item_id:id,revision:current.revision,correction:{fields:{[field]:value}},note:'Moved on the board'});
      if(reload)await reload();
      if(typeof toast==='function')toast('Moved to '+value,undoable&&before&&before!==value?()=>save(id,before,false):null);
    });
    host.querySelectorAll('[data-board-move]').forEach(sel=>sel.onchange=()=>{
      if(sel.value!=='__new__'){if(sel.value)save(sel.dataset.boardMove,sel.value);return;}
      sel.closest('.board-move').innerHTML=`<span class="board-new"><input maxlength="60" placeholder="New ${esc(human(field).toLowerCase())}" aria-label="New ${esc(human(field).toLowerCase())}"><button type="button" class="text-button">Move</button></span>`;
      const box=host.querySelector(`[data-board-item="${CSS.escape(sel.dataset.boardMove)}"] .board-new`),input=box.querySelector('input');input.focus();
      const go=()=>save(sel.dataset.boardMove,input.value);box.querySelector('button').onclick=go;input.onkeydown=e=>{if(e.key==='Enter'){e.preventDefault();go();}};
    });
    host.querySelectorAll('[data-board-item]').forEach(c=>c.ondragstart=e=>{e.dataTransfer.setData('text/plain',c.dataset.boardItem);e.dataTransfer.effectAllowed='move';c.classList.add('dragging');});
    host.querySelectorAll('[data-board-item]').forEach(c=>c.ondragend=()=>c.classList.remove('dragging'));
    host.querySelectorAll('[data-board-group]').forEach(col=>{
      col.ondragover=e=>{e.preventDefault();col.classList.add('drop-target');};
      col.ondragleave=()=>col.classList.remove('drop-target');
      col.ondrop=e=>{e.preventDefault();col.classList.remove('drop-target');const id=e.dataTransfer.getData('text/plain'),from=host.querySelector(`[data-board-item="${CSS.escape(id)}"]`)?.closest('[data-board-group]');if(id&&col.dataset.boardGroup&&from!==col)save(id,col.dataset.boardGroup);};
    });
  }

  async function drawMap(host,d,data,view,search,mine,key,find){
    css('/vendor/map-view.css');let L;
    try{({L}=await import('/vendor/map-view.js'));}
    catch{if(mine===ticket&&host.isConnected)host.innerHTML='<p class="small-note">The map couldn’t load. Your results are still in List view; reopen AURA to try again.</p>';return;}
    if(mine!==ticket||key!==scope()||!host.isConnected)return;
    const groups=d.views.board,numbers=d.views.chart,options=[...groups,...numbers];
    const remembered=choice(d.id+':map-field',undefined),sizeRemembered=choice(d.id+':map-size',undefined);
    let colourField=options.includes(remembered)?remembered:'',sizeField=numbers.includes(sizeRemembered)?sizeRemembered:'',hidden=new Set(),fitted=false;
    host.innerHTML=`${options.length?`<div class="view-controls"><label>Colour by<select data-view-colour><option value="">One colour</option>${options.map(f=>`<option value="${esc(f)}" ${f===colourField?'selected':''}>${esc(human(f))}</option>`).join('')}</select></label>${numbers.length?`<label>Size by<select data-view-size><option value="">Same size</option>${numbers.map(f=>`<option value="${esc(f)}" ${f===sizeField?'selected':''}>${esc(human(f))}</option>`).join('')}</select></label>`:''}</div>`:''}<div class="result-map" data-view-map></div><div data-view-legend></div><p class="small-note" data-view-status role="status"></p><p class="small-note" data-view-offline hidden>Some map imagery isn’t available offline. Your saved places still show.</p><details class="map-unplaced" hidden><summary></summary><ul></ul></details>`;
    const m=map=L.map(host.querySelector('[data-view-map]'),{scrollWheelZoom:false,worldCopyJump:true});
    L.tileLayer('/api/media/map/{z}/{x}/{y}.png',{maxZoom:19,errorTileUrl:blank,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors'}).on('tileerror',()=>{const n=host.querySelector('[data-view-offline]');if(n)n.hidden=false;}).addTo(m);
    // Leaflet keeps popup clicks from reaching the page, so the popup's button gets its own handler.
    m.on('popupopen',e=>{const b=e.popup.getElement()?.querySelector('[data-view-find]');if(b)b.onclick=()=>{release();find(b.dataset.viewFind);};});
    const shapes=L.layerGroup().addTo(m);let pins=null;
    const popup=(r,home)=>{const maps=link(r.fields.maps_url)||'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(r.fields.address?r.title+', '+r.fields.address:r.lat+','+r.lng),site=link(r.fields.website)||link(r.fields.url);
      return `<div class="map-card"><strong>${esc(r.title)}</strong>${home&&home!==r?`<p class="small-note">${esc(distance(home,r))} from ${esc(home.title)}</p>`:''}${r.fields.address?`<p class="small-note">${esc(r.fields.address)}</p>`:''}${fields(r)}<div class="map-links"><a href="${esc(maps)}" target="_blank" rel="noopener noreferrer">Open in Maps</a>${site?`<a href="${esc(site)}" target="_blank" rel="noopener noreferrer">Website</a>`:''}<button type="button" class="text-button" data-view-find="${esc(r.title)}">Show in list</button></div></div>`;};
    const paint=rows=>{
      if(map!==m)return;   // a newer view replaced this map
      shapes.clearLayers();if(pins)m.removeLayer(pins);
      const all=rows.filter(r=>typeof r.lat==='number'),c=colouring(all,colourField,numbers),size=sizing(all,sizeField);
      const visible=all.filter(r=>c.numeric||!colourField||!hidden.has(String(r.fields[colourField]??'')));
      const home=all.find(r=>r.fields.yours===true);
      const newest=Date.parse(current.updated)||0,isNew=r=>r.disposition!=='acknowledged'&&!r.hidden&&Date.parse(r.first_seen||0)>=newest-120000;
      const quiet=visible.length&&visible.every(isNew);   // on the first check everything is new; don't ring them all
      pins=visible.length>=CLUSTER_FROM?L.markerClusterGroup({showCoverageOnHover:false,maxClusterRadius:45,spiderfyOnMaxZoom:true}):L.layerGroup();
      visible.forEach(r=>{
        const colour=c.of(r),yours=r.fields.yours===true,rank=r.fields.rank??r.fields.position,size_=size(r),change=moved(r,'rank')||moved(r,'position');
        if(r.area)L.geoJSON(r.area,{style:{color:colour,weight:1.5,fillColor:colour,fillOpacity:.13}}).bindPopup(popup(r,home),{maxWidth:280}).addTo(shapes);
        if(r.radius_m)L.circle([r.lat,r.lng],{radius:r.radius_m,color:colour,weight:1,fillColor:colour,fillOpacity:.07,interactive:false}).addTo(shapes);
        const classes=['map-pin',yours?'yours':'',r.display_state&&r.display_state!=='active'?'gone':'',!quiet&&isNew(r)?'fresh':''].filter(Boolean).join(' ');
        const badge=change?`<b class="moved ${change>0?'up':'down'}">${change>0?'▲':'▼'}</b>`:'';
        L.marker([r.lat,r.lng],{title:r.title,keyboard:true,riseOnHover:true,zIndexOffset:yours?1000:0,icon:L.divIcon({className:classes,html:`<span style="background:${colour};width:${size_}px;height:${size_}px">${rank!==undefined&&rank!==null&&String(rank).length<=3&&size_>=16?esc(String(rank)):''}</span>${badge}`,iconSize:[size_,size_],iconAnchor:[size_/2,size_/2],popupAnchor:[0,-size_/2]})}).bindPopup(popup(r,home),{maxWidth:280}).addTo(pins);
      });
      pins.addTo(m);
      const legend=host.querySelector('[data-view-legend]'),marks=[visible.some(r=>!quiet&&isNew(r))?'<span><i class="key fresh"></i>New this check</span>':'',visible.some(r=>moved(r,'rank')||moved(r,'position'))?'<span>▲▼ Rank moved</span>':'',visible.some(r=>r.display_state&&r.display_state!=='active')?'<span><i class="key gone"></i>No longer listed</span>':''].join('');
      legend.innerHTML=(colourField&&c.numeric?`<div class="view-legend"><span class="scale"><span>${esc(value(c.min))}</span><i class="ramp ${c.good?'good':''}"></i><span>${esc(value(c.max))}</span></span><span>${esc(human(colourField))}${c.good?' (lower is better)':''}</span>${marks}</div>`:colourField?`<div class="view-legend">${c.order.map((v,i)=>all.some(r=>r.fields[colourField]===v)?`<button type="button" class="legend-toggle" data-legend="${esc(String(v))}" aria-pressed="${!hidden.has(String(v))}"><i style="background:${palette[i%palette.length]}"></i>${esc(String(v))}</button>`:'').join('')}${marks}</div>`:marks?`<div class="view-legend">${marks}</div>`:'');
      legend.querySelectorAll('[data-legend]').forEach(b=>b.onclick=()=>{const v=b.dataset.legend;hidden.has(v)?hidden.delete(v):hidden.add(v);paint(current.items);});
      if(!fitted){
        // Bounds come from the data: a circle can't measure itself before the map has a view.
        const bounds=L.latLngBounds([]);visible.forEach(r=>{bounds.extend(r.radius_m?L.latLng(r.lat,r.lng).toBounds(r.radius_m*2):[r.lat,r.lng]);if(r.area)bounds.extend(L.geoJSON(r.area).getBounds());});
        if(bounds.isValid()){fitted=true;m.fitBounds(bounds,{padding:[34,34],maxZoom:15});}else m.setView([39,-96],3);
      }
      if(colourField&&!c.numeric&&hidden.size)host.querySelector('[data-view-status]').textContent=`${visible.length} of ${all.length} shown · Click a hidden group in the legend to show it again`;
    };
    const status=(rows,text)=>{const placed=rows.items.filter(r=>typeof r.lat==='number').length,s=host.querySelector('[data-view-status]'),u=host.querySelector('.map-unplaced');
      s.textContent=text||`${placed} of ${rows.items.length} ${rows.items.length===1?'result':'results'} on the map${rows.updated?' · Last updated '+stamp(rows.updated):''}${placed>=CLUSTER_FROM?' · Nearby places are grouped; zoom in to separate them':''}`;
      u.hidden=!rows.unplaced.length;if(rows.unplaced.length){u.querySelector('summary').textContent=`${rows.unplaced.length} couldn’t be placed`;u.querySelector('ul').innerHTML=rows.unplaced.map(r=>`<li><strong>${esc(r.title)}</strong> · ${esc(r.reason)}</li>`).join('');}};
    let current=data;paint(current.items);status(current);setTimeout(()=>map===m&&m.invalidateSize(),0);
    const colourSelect=host.querySelector('[data-view-colour]');if(colourSelect)colourSelect.onchange=e=>{colourField=e.target.value;hidden.clear();choice(d.id+':map-field',colourField);paint(current.items);status(current);};
    const sizeSelect=host.querySelector('[data-view-size]');if(sizeSelect)sizeSelect.onchange=e=>{sizeField=e.target.value;choice(d.id+':map-size',sizeField);paint(current.items);};
    // Addresses without coordinates are looked up a few at a time, only after the person agrees
    // to send them to OpenStreetMap's lookup service; each is remembered afterwards.
    let agreed=false;try{agreed=localStorage.getItem('aura-place-lookups')==='yes';}catch{}
    if(current.pending&&!agreed){
      host.querySelector('[data-view-status]').insertAdjacentHTML('afterend',`<div class="inline-actions" data-view-consent><p class="small-note">${current.pending} ${current.pending===1?'result has an address':'results have addresses'} but no map position. Finding them sends the addresses to OpenStreetMap’s free lookup service.</p><button type="button" class="secondary" data-view-agree>Find them on the map</button></div>`);
      await new Promise(resolve=>{host.querySelector('[data-view-agree]').onclick=()=>{try{localStorage.setItem('aura-place-lookups','yes');}catch{}host.querySelector('[data-view-consent]').remove();resolve();};});
    }
    while(current.pending&&mine===ticket&&host.isConnected){
      status(current,`Finding ${current.pending} ${current.pending===1?'address':'addresses'} on the map…`);
      let result;
      try{result=await api('/api/collection-view',{business:state.business,action:'place',id:d.id,view,q:search});
        if(mine!==ticket||key!==scope()||!host.isConnected)return;
        current=await api(q('/api/collection-view',{id:d.id,view,q:search}));}
      catch(error){if(mine===ticket&&host.isConnected)status(current,humanError(error));return;}
      if(mine!==ticket||key!==scope()||!host.isConnected)return;
      paint(current.items);if(result.stopped){status(current,result.stopped);return;}if(!result.placed&&result.remaining)break;
    }
    status(current);
  }

  /* What's running: plain sentences built from saved links. Changes happen in chat. */
  async function running(host,target,collection){
    const key=scope();let data;
    try{data=await api(q('/api/running',target));}catch(error){if(key===scope()&&host.isConnected)host.innerHTML=`<p class="small-note">${esc(humanError(error))}</p>`;return null;}
    if(key!==scope()||!host.isConnected)return data;
    const order=['failed','missing','waiting','ok','paused'],items=[...data.items].sort((a,b)=>order.indexOf(a.health)-order.indexOf(b.health));
    host.innerHTML=(items.length?items.map(item=>`<div class="running-item" data-health="${esc(item.health)}" ${['failed','missing'].includes(item.health)?'role="status"':''}><p>${esc(item.text)}</p>${item.available?`<div class="inline-actions"><button type="button" class="text-button" data-running-open="${esc(item.id)}">Open task</button><button type="button" class="text-button" data-running-chat="${esc(item.id)}">Change in chat</button></div>`:item.health==='missing'&&target.collection?'<div class="inline-actions"><button type="button" class="secondary compact" data-running-watch>Set it up again</button></div>':''}</div>`).join('')+(data.goals.length?`<p class="small-note">Working toward: ${esc(data.goals.join('; '))}</p>`:''):`<p class="small-note">${target.collection?'Nothing keeps this current yet.':'Nothing is scheduled here yet. Ask your AI to set up a scheduled task, then link it to this '+(target.project?'project':'goal')+'.'}</p>${target.collection?'<button type="button" class="text-button" data-running-watch>Keep this up to date</button>':''}`);
    const find=id=>items.find(i=>i.id===id);
    host.querySelectorAll('[data-running-open]').forEach(b=>b.onclick=()=>attempt(async()=>{
      const id=b.dataset.runningOpen;
      if(!state.schedules?.items.some(t=>t.id===id)){
        const schedules=await api('/api/schedules');if(key!==scope()||!b.isConnected)return;
        state.schedules=schedules;
        if(!schedules.items.some(t=>t.id===id))throw Error('This task is no longer available in its app.');
      }
      await scheduleDetails(id);
    }));
    host.querySelectorAll('[data-running-watch]').forEach(b=>b.onclick=()=>attempt(async()=>{
      if(key!==scope()||!collection)return;
      state.scheduleDraft={name:collection.name,description:collection.purpose||'Review new information and save meaningful changes.',when:'',collection_id:collection.id,collection_name:collection.name,app:state.data.connection.selected};
      $('#detail').close();state.scheduleAdding=true;state.view='tools';
      await render();recordShellRoute();await renderShell();$('#schedule-form [name=when]')?.focus();
    }));
    host.querySelectorAll('[data-running-chat]').forEach(b=>b.onclick=()=>{const t=find(b.dataset.runningChat);returnToChat();const box=$('#request');box.value=`Change my scheduled task “${t.name}” (${t.app}, ${t.schedule.toLowerCase()}): `;box.dispatchEvent(new Event('input',{bubbles:true}));box.focus();box.setSelectionRange(box.value.length,box.value.length);});
    return data;
  }

  /* Goal progress from recorded measurements, each with its source and date. */
  async function progress(host,goalId){
    const key=scope();let data;
    try{data=await api(q('/api/goal-progress',{goal:goalId}));}catch{if(host.isConnected)host.innerHTML='';return;}
    if(key!==scope()||!host.isConnected)return;
    const metrics=data.metrics.filter(m=>m.points.length),t=data.target;
    const target=t?`<p class="goal-target">Target: ${esc(value(t.target))}${t.unit&&!['count','USD','rank'].includes(t.unit)?' '+esc(t.unit):''} ${t.direction==='lower_better'?'or lower':'or more'}${t.reached?' <span class="goal-reached">Reached</span>':t.latest!=null?` · <span class="small-note">latest ${esc(value(t.latest))}</span>`:' · <span class="small-note">no measurement yet</span>'}</p>`:'';
    host.innerHTML=`<h3 class="goal-section-title">Progress</h3>${target}${metrics.map(m=>{const last=m.points[m.points.length-1];return `<div class="goal-metric"><p><strong>${esc(m.name)}</strong>: ${esc(value(last.value))}${m.unit&&!['count','rank'].includes(m.unit)?' '+esc(m.unit):''} <span class="small-note">· ${esc(stamp(last.at))}${last.source?' · from '+esc(last.source):''}</span></p>${m.points.length>1?line(m):''}</div>`;}).join('')||'<p class="small-note">No measurements yet. Ask your AI to record one for this goal from a connected source, such as new customers each week.</p>'}`;
  }
  function line(m){
    const w=560,h=150,pad=28,values=m.points.map(p=>p.value),low=Math.min(...values,0),high=Math.max(...values)||1,span=high-low||1;
    const x=i=>pad+i*(w-pad*2)/(m.points.length-1),y=v=>h-pad-(v-low)/span*(h-pad*2);
    return `<svg class="metric-line" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(m.name)} over time"><line x1="${pad}" y1="${h-pad}" x2="${w-pad}" y2="${h-pad}" class="axis"/><text x="${pad}" y="${h-8}" class="tick">${esc(day(m.points[0].at))}</text><text x="${w-pad}" y="${h-8}" class="tick end">${esc(day(m.points[m.points.length-1].at))}</text><text x="${pad-6}" y="${y(high)+4}" class="tick end">${esc(value(high))}</text><text x="${pad-6}" y="${y(low)+4}" class="tick end">${esc(value(low))}</text><polyline points="${m.points.map((p,i)=>x(i)+','+y(p.value)).join(' ')}" class="trend"/>${m.points.map((p,i)=>`<circle cx="${x(i)}" cy="${y(p.value)}" r="3.5"><title>${esc(value(p.value))} · ${esc(day(p.at))}${p.source?' · '+esc(p.source):''}</title></circle>`).join('')}</svg>`;
  }
  return {show,release,choice,saved,running,progress};
})();
