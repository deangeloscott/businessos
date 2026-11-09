/* Focus: the organization's description plus the focus areas it chose. Areas change emphasis, never
   capability: they order suggestions and give the AI short guidance. Data comes from /api/focus. */
window.auraFocus=(()=>{
  let data=null,key='';
  const scope=()=>JSON.stringify([state.business,state.data?.workspace]);
  const label=a=>a.origin==='imported'?'Imported':a.origin==='yours'?(a.customized?'Your version':'Yours'):'';
  async function load(force=false){
    if(!state.business)return null;
    const k=scope();if(!force&&data&&key===k)return data;
    key=k;
    try{const d=await api('/api/focus?business='+encodeURIComponent(state.business));if(key===scope())data=d;}catch{if(key===k)data=null;}
    return key===k?data:null;
  }

  /* Home: up to three quick starts under the message box. They only fill the box; nothing runs until you send. */
  async function paint(){
    const box=document.querySelector('.suggestions');if(!box)return;
    const d=await load();box.querySelectorAll('.quick-start').forEach(b=>b.remove());if(!d||!state.business)return;
    const starts=d.quick_starts.map(s=>`<button type="button" class="quick-start" data-prompt="${esc(s.prompt)}" title="${esc(s.area)}${s.kind==='watch'?' · ongoing':''}">${esc(s.title)}${s.kind==='watch'?`<small> · ${esc(s.cadence||'ongoing')}</small>`:''}</button>`).join('');
    box.insertAdjacentHTML('beforeend',starts||'<button type="button" class="quick-start" data-focus-picker>Choose your focus areas</button>');
  }

  /* Business & memory: what this organization focuses on, and a way to change it. */
  async function panel(host){
    if(!host)return;const d=await load(true);if(!host.isConnected||!d)return;
    host.innerHTML=`<div class="section-head"><h3>Focus</h3><button type="button" class="text-button" data-focus-picker>${d.areas.length?'Change':'Choose focus areas'}</button></div>${d.description?`<p class="focus-description">${esc(d.description)}</p>`:'<p class="small-note">Add what your business does (Edit name) to get suggested focus areas.</p>'}${d.areas.length?`<div class="focus-chips">${d.areas.map(a=>`<span class="focus-chip" title="${esc(a.summary)}">${esc(a.name)}${label(a)?` <small>${esc(label(a))}</small>`:''}</span>`).join('')}</div>`:'<p class="small-note">Focus areas tailor suggestions and give your AI useful context. Nothing is hidden or required.</p>'}${d.missing.length?`<p class="small-note">${d.missing.length===1?'One chosen focus area is':'Some chosen focus areas are'} no longer available. Choose again to tidy up.</p>`:''}`;
  }

  async function picker(){
    const d=await load(true);if(!d)return;
    const chosen=new Set(d.areas.length?d.areas.map(a=>a.id):d.suggested);
    details('Focus areas',`<p class="shell-help">Pick what fits${d.description?' — suggestions come from your description':''}. Combine as many as you like; you can change them any time.</p>${d.description?`<p class="focus-description">${esc(d.description)}</p>`:''}<form id="focus-form" class="focus-options">${d.available.map(a=>`<label class="focus-option"><input type="checkbox" name="area" value="${esc(a.id)}" ${chosen.has(a.id)?'checked':''}><span><strong>${esc(a.name)}</strong>${label(a)?` <small class="muted">${esc(label(a))}</small>`:''}<small>${esc(a.summary)}</small></span></label>`).join('')}<div class="inline-actions"><button class="primary">Save</button><button type="button" class="text-button" data-focus-ask>Ask my AI to suggest</button><button type="button" class="text-button" data-focus-own>Make your own</button></div><p id="focus-status" class="small-note" role="status"></p></form>${d.problems.length?`<details><summary>Some focus area files need attention</summary><ul>${d.problems.map(p=>`<li>${esc(p)}</li>`).join('')}</ul></details>`:''}`);
    const k=scope();
    $('#focus-form').onsubmit=e=>{e.preventDefault();attempt(async()=>{
      const areas=[...e.target.querySelectorAll('input[name=area]:checked')].map(i=>i.value);
      data=await api('/api/focus',{business:state.business,areas});key=k;
      if(k!==scope())return;$('#detail').close();notice(areas.length?'Focus saved.':'Focus areas cleared.');paint();panel($('#focus-panel'));
    });};
    $('[data-focus-ask]').onclick=()=>prompt('Suggest focus areas for our business from AURA\'s focus area list (scripts/workspace_focus.py areas). Use what you know about us, explain each choice in one line, and save them with scripts/workspace_focus.py set once I confirm. If you learn how I like information presented, offer to add it to my working preferences.');
    $('[data-focus-own]').onclick=()=>prompt('Help me create a focus area of our own. Follow focus-areas/README.md in the AURA product folder, ask what you need, and save it in our workspace\'s knowledge/focus-areas folder. Keep its guidance about what to find out, not facts that vary between organizations.');
  }

  /* After the description changes, offer focus areas when none are chosen yet. */
  async function afterDescription(text){
    const d=await load(true);paint();
    if(d&&text&&!d.areas.length&&d.suggested.length)picker();
  }

  document.addEventListener('click',e=>{if(e.target.closest('[data-focus-picker]'))attempt(picker);});
  return {load,paint,panel,picker,afterDescription,cached:()=>data&&key===scope()?data:null,goals:async()=>((await load())?.goals||[]),views:async()=>((await load())?.views||[])};
})();
