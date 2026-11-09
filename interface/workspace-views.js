/* Map, chart and board views of saved results, what's running for a project or goal, and goal progress.
   Everything here only draws data from the shared API; the CLI returns the same data. */
window.auraViews=(()=>{
  const blank='data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
  const palette=['#6654ce','#d0603a','#2f8f6b','#c99a1a','#3b78c2','#b4478f','#5e6b7a','#8a5a2b','#4aa3a1','#a33b3b','#6d8f2f','#9466c8'];
  const coords=new Set(['latitude','longitude','lat','lng','lon','yours']);
  let ticket=0,map=null;
  const scope=()=>JSON.stringify([state.business,state.data?.workspace]);
  const q=(route,values)=>route+'?'+new URLSearchParams({business:state.business,...values});
  const css=href=>{if(!document.querySelector(`link[href="${href}"]`)){const el=document.createElement('link');el.rel='stylesheet';el.href=href;document.head.append(el);}};
  const value=v=>typeof v==='number'?v.toLocaleString():String(v);
  function choice(id,shape){try{if(shape===undefined)return localStorage.getItem('aura-view:'+id)||'list';localStorage.setItem('aura-view:'+id,shape);}catch{}return shape||'list';}
  function release(){ticket++;if(map){map.remove();map=null;}}
  function card(r,skip=[]){const shown=Object.entries(r.fields).filter(([k,v])=>!coords.has(k)&&!skip.includes(k)&&v!==null&&v!=='').slice(0,5);return `<strong>${esc(r.title)}</strong>${shown.length?`<dl class="view-fields">${shown.map(([k,v])=>`<div><dt>${esc(human(k))}</dt><dd>${esc(value(v))}</dd></div>`).join('')}</dl>`:''}<button type="button" class="text-button" data-view-find="${esc(r.title)}">Show in list</button>`;}
  function colours(rows,field){const order=[...new Set(rows.map(r=>r.fields[field]).filter(v=>v!==undefined&&v!==null&&v!==''))];return {order,of:r=>field&&order.includes(r.fields[field])?palette[order.indexOf(r.fields[field])%palette.length]:palette[0]};}
  function legend(c,field,shown){const present=new Set(shown.map(r=>r.fields[field]));return field&&c.order.length?`<div class="view-legend">${c.order.map((v,i)=>present.has(v)?`<span><i style="background:${palette[i%palette.length]}"></i>${esc(String(v))}</span>`:'').join('')}</div>`:'';}

  /* Collection views. `find` returns to the list filtered to one result. */
  async function show(host,d,shape,view,search,find){
    release();const mine=ticket,key=scope();host.innerHTML='<p class="small-note">Loading…</p>';
    host.onclick=e=>{const b=e.target.closest('[data-view-find]');if(b){release();find(b.dataset.viewFind);}};
    const data=await api(q('/api/collection-view',{id:d.id,view,q:search}));if(mine!==ticket||key!==scope()||!host.isConnected)return;
    if(shape==='map')return drawMap(host,d,data,view,search,mine,key,find);
    const fields=shape==='chart'?d.views.chart:d.views.board,picked=choice(d.id+':'+shape+'-field',undefined);
    const field=fields.includes(picked)?picked:fields[0];
    host.innerHTML=`<div class="view-controls"><label>${shape==='chart'?'Compare':'Group by'}<select data-view-field>${fields.map(f=>`<option value="${esc(f)}" ${f===field?'selected':''}>${esc(human(f))}</option>`).join('')}</select></label></div><div data-view-body></div>`;
    const paint=f=>{host.querySelector('[data-view-body]').innerHTML=shape==='chart'?bars(data.items,f):board(data.items,f);};
    host.querySelector('[data-view-field]').onchange=e=>{choice(d.id+':'+shape+'-field',e.target.value);paint(e.target.value);};paint(field);
  }
  function bars(rows,field){
    const items=rows.filter(r=>typeof r.fields[field]==='number').sort((a,b)=>b.fields[field]-a.fields[field]),top=items.slice(0,30),peak=Math.max(...top.map(r=>Math.abs(r.fields[field])),0)||1;
    if(!items.length)return '<p class="small-note">No results have this number.</p>';
    return `<div class="view-bars">${top.map(r=>`<button type="button" class="bar-row" data-view-find="${esc(r.title)}" title="Show in list"><span class="bar-label">${esc(r.title)}</span><span class="bar-track"><span class="bar ${r.fields[field]<0?'negative':''}" style="width:${Math.max(1,Math.abs(r.fields[field])/peak*100)}%"></span></span><span class="bar-value">${esc(value(r.fields[field]))}</span></button>`).join('')}</div>${items.length>top.length?`<p class="small-note">Showing the top ${top.length} of ${items.length}.</p>`:''}${rows.length>items.length?`<p class="small-note">${rows.length-items.length} ${rows.length-items.length===1?'result has':'results have'} no ${esc(human(field).toLowerCase())}.</p>`:''}`;
  }
  function board(rows,field){
    const groups=new Map();rows.forEach(r=>{const g=r.fields[field]===undefined||r.fields[field]===null||r.fields[field]===''?'':String(r.fields[field]);if(!groups.has(g))groups.set(g,[]);groups.get(g).push(r);});
    const order=[...groups.keys()].sort((a,b)=>(a==='')-(b==='')||groups.get(b).length-groups.get(a).length);
    return `<div class="view-board">${order.map(g=>`<section class="board-column"><h4>${esc(g||'No '+human(field).toLowerCase())} <small>${groups.get(g).length}</small></h4>${groups.get(g).slice(0,50).map(r=>`<div class="board-card">${card(r,[field])}</div>`).join('')}${groups.get(g).length>50?`<p class="small-note">${groups.get(g).length-50} more in the list.</p>`:''}</section>`).join('')}</div>`;
  }
  async function drawMap(host,d,data,view,search,mine,key,find){
    css('/vendor/map-view.css');const {L}=await import('/vendor/map-view.js');if(mine!==ticket||key!==scope()||!host.isConnected)return;
    const groups=d.views.board,picked=choice(d.id+':map-field',undefined),field=groups.includes(picked)?picked:'';
    host.innerHTML=`${groups.length?`<div class="view-controls"><label>Colour by<select data-view-field><option value="">One colour</option>${groups.map(f=>`<option value="${esc(f)}" ${f===field?'selected':''}>${esc(human(f))}</option>`).join('')}</select></label></div>`:''}<div class="result-map" data-view-map></div><div data-view-legend></div><p class="small-note" data-view-status role="status"></p><p class="small-note" data-view-offline hidden>Some map imagery isn’t available offline. Your saved places still show.</p><details class="map-unplaced" hidden><summary></summary><ul></ul></details>`;
    map=L.map(host.querySelector('[data-view-map]'),{scrollWheelZoom:false,worldCopyJump:true});
    L.tileLayer('/api/media/map/{z}/{x}/{y}.png',{maxZoom:19,errorTileUrl:blank,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors'}).on('tileerror',()=>{const n=host.querySelector('[data-view-offline]');if(n)n.hidden=false;}).addTo(map);
    // Leaflet keeps popup clicks from reaching the page, so the popup's button gets its own handler.
    map.on('popupopen',e=>{const b=e.popup.getElement()?.querySelector('[data-view-find]');if(b)b.onclick=()=>{release();find(b.dataset.viewFind);};});
    const layer=L.layerGroup().addTo(map);let colourField=field,fitted=false;
    const paint=rows=>{
      layer.clearLayers();const c=colours(rows,colourField),placed=rows.filter(r=>typeof r.lat==='number');
      placed.forEach(r=>{const rank=r.fields.rank??r.fields.position,yours=r.fields.yours===true||r.fields.yours==='true';
        L.marker([r.lat,r.lng],{title:r.title,keyboard:true,zIndexOffset:yours?1000:0,icon:L.divIcon({className:'map-pin'+(yours?' yours':''),html:`<span style="background:${c.of(r)}">${rank!==undefined&&rank!==null&&String(rank).length<=3?esc(String(rank)):''}</span>`,iconSize:[28,28],iconAnchor:[14,14],popupAnchor:[0,-12]})}).bindPopup(`<div class="map-card">${card(r)}</div>`,{maxWidth:260}).addTo(layer);});
      host.querySelector('[data-view-legend]').innerHTML=legend(c,colourField,placed);
      if(!fitted&&placed.length){fitted=true;map.fitBounds(L.latLngBounds(placed.map(r=>[r.lat,r.lng])),{padding:[34,34],maxZoom:15});}
      if(!placed.length&&!fitted)map.setView([39,-96],3);
      return placed.length;
    };
    const status=(rows,text)=>{const placed=rows.items.filter(r=>typeof r.lat==='number').length,s=host.querySelector('[data-view-status]'),u=host.querySelector('.map-unplaced');
      s.textContent=text||`${placed} of ${rows.items.length} ${rows.items.length===1?'result':'results'} on the map${rows.updated?' · Last updated '+stamp(rows.updated):''}`;
      u.hidden=!rows.unplaced.length;if(rows.unplaced.length){u.querySelector('summary').textContent=`${rows.unplaced.length} couldn’t be placed`;u.querySelector('ul').innerHTML=rows.unplaced.map(r=>`<li><strong>${esc(r.title)}</strong> · ${esc(r.reason)}</li>`).join('');}};
    let rows=data;paint(rows.items);status(rows);setTimeout(()=>map&&map.invalidateSize(),0);
    const select=host.querySelector('[data-view-field]');if(select)select.onchange=e=>{colourField=e.target.value;choice(d.id+':map-field',colourField);paint(rows.items);};
    // Addresses without coordinates are looked up a few at a time, only after the person agrees
    // to send them to OpenStreetMap's lookup service; each is remembered afterwards.
    let agreed=false;try{agreed=localStorage.getItem('aura-place-lookups')==='yes';}catch{}
    if(rows.pending&&!agreed){
      host.querySelector('[data-view-status]').insertAdjacentHTML('afterend',`<div class="inline-actions" data-view-consent><p class="small-note">${rows.pending} ${rows.pending===1?'result has an address':'results have addresses'} but no map position. Finding them sends the addresses to OpenStreetMap’s free lookup service.</p><button type="button" class="secondary" data-view-agree>Find them on the map</button></div>`);
      await new Promise(resolve=>{host.querySelector('[data-view-agree]').onclick=()=>{try{localStorage.setItem('aura-place-lookups','yes');}catch{}host.querySelector('[data-view-consent]').remove();resolve();};});
    }
    while(rows.pending&&mine===ticket&&host.isConnected){
      status(rows,`Finding ${rows.pending} ${rows.pending===1?'address':'addresses'} on the map…`);
      const result=await api('/api/collection-view',{business:state.business,action:'place',id:d.id,view,q:search});
      if(mine!==ticket||key!==scope()||!host.isConnected)return;
      rows=await api(q('/api/collection-view',{id:d.id,view,q:search}));if(mine!==ticket||key!==scope()||!host.isConnected)return;
      paint(rows.items);if(result.stopped){status(rows,result.stopped);return;}if(!result.placed&&result.remaining)break;
    }
    status(rows);
  }

  /* What's running: plain sentences built from saved links. Changes happen in chat. */
  async function running(host,target){
    const key=scope();let data;
    try{data=await api(q('/api/running',target));}catch(error){if(key===scope()&&host.isConnected)host.innerHTML=`<p class="small-note">${esc(humanError(error))}</p>`;return null;}
    if(key!==scope()||!host.isConnected)return data;
    host.innerHTML=data.items.length?data.items.map((item,i)=>`<div class="running-item" data-health="${esc(item.health)}"><p>${esc(item.text)}</p>${item.available?`<div class="inline-actions"><button type="button" class="text-button" data-running-open="${i}">Open task</button><button type="button" class="text-button" data-running-chat="${i}">Change in chat</button></div>`:''}</div>`).join('')+(data.goals.length?`<p class="small-note">Working toward: ${esc(data.goals.join('; '))}</p>`:''):`<p class="small-note">Nothing is scheduled here yet. Ask your AI to set up a scheduled task, then link it to this ${target.project?'project':'goal'}.</p>`;
    host.querySelectorAll('[data-running-open]').forEach(b=>b.onclick=()=>attempt(()=>scheduleDetails(data.items[Number(b.dataset.runningOpen)].id)));
    host.querySelectorAll('[data-running-chat]').forEach(b=>b.onclick=()=>{const t=data.items[Number(b.dataset.runningChat)];returnToChat();const box=$('#request');box.value=`Change my scheduled task “${t.name}” (${t.app}, ${t.schedule.toLowerCase()}): `;box.dispatchEvent(new Event('input',{bubbles:true}));box.focus();box.setSelectionRange(box.value.length,box.value.length);});
    return data;
  }

  /* Goal progress from recorded measurements, each with its source and date. */
  async function progress(host,goalId){
    const key=scope();let data;
    try{data=await api(q('/api/goal-progress',{goal:goalId}));}catch{if(host.isConnected)host.innerHTML='';return;}
    if(key!==scope()||!host.isConnected)return;
    const metrics=data.metrics.filter(m=>m.points.length);
    host.innerHTML=`<h3 class="goal-section-title">Progress</h3>${metrics.map(m=>{const last=m.points[m.points.length-1];return `<div class="goal-metric"><p><strong>${esc(m.name)}</strong>: ${esc(value(last.value))}${m.unit?' '+esc(m.unit):''} <span class="small-note">· ${esc(stamp(last.at))}${last.source?' · from '+esc(last.source):''}</span></p>${m.points.length>1?line(m):''}</div>`;}).join('')||'<p class="small-note">No measurements yet. Ask your AI to record one for this goal from a connected source, such as new customers each week.</p>'}`;
  }
  function line(m){
    const w=560,h=150,pad=28,values=m.points.map(p=>p.value),low=Math.min(...values,0),high=Math.max(...values)||1,span=high-low||1;
    const x=i=>pad+i*(w-pad*2)/(m.points.length-1),y=v=>h-pad-(v-low)/span*(h-pad*2);
    const day=t=>new Date(t).toLocaleDateString(undefined,{month:'short',day:'numeric'});
    return `<svg class="metric-line" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(m.name)} over time"><line x1="${pad}" y1="${h-pad}" x2="${w-pad}" y2="${h-pad}" class="axis"/><text x="${pad}" y="${h-8}" class="tick">${esc(day(m.points[0].at))}</text><text x="${w-pad}" y="${h-8}" class="tick end">${esc(day(m.points[m.points.length-1].at))}</text><text x="${pad-6}" y="${y(high)+4}" class="tick end">${esc(value(high))}</text><text x="${pad-6}" y="${y(low)+4}" class="tick end">${esc(value(low))}</text><polyline points="${m.points.map((p,i)=>x(i)+','+y(p.value)).join(' ')}" class="trend"/>${m.points.map((p,i)=>`<circle cx="${x(i)}" cy="${y(p.value)}" r="3.5"><title>${esc(value(p.value))} · ${esc(day(p.at))}${p.source?' · '+esc(p.source):''}</title></circle>`).join('')}</svg>`;
  }
  return {show,release,choice,running,progress};
})();
