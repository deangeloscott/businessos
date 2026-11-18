/* Recorded relationships, read one way by the world, the panel and the Connections diagram.
   The feed's relationships are {nodes, edges}: each edge is {source, target, type} and the source flows into
   the target (see scripts/workspace_world_links.py for what each type records). Nothing here guesses a link. */
window.auraLinks = (() => {
  const KIND = {land:'Area', item:'Tracked result', finding:'Finding', decision:'Decision', goal:'Goal', record:'Evidence', output:'Saved output',
    file:'File', method:'Library item', chat:'Conversation', session:'AI app session', agent:'Agent', task:'Scheduled task', app:'AI app', project:'Project'};
  /* How the other end of a link reads from the selected thing: [when the other end is the source, when it is the target]. */
  const WORDS = {
    in:['Kept here', 'Where this is kept'],
    attached:['Given to this conversation', 'Conversation this was given to'],
    saved:['Where this was saved', 'Saved during this'],
    updated:['Ran the check that changed this', 'Changed by this'],
    into:['Saved work here', 'Where its work was saved'],
    supports:['Supports this', 'This supports it'],
    challenges:['Challenges this', 'This challenges it'],
    basis:['This rests on it', 'Rests on this'],
    extends:['Extends this', 'This extends it'],
    source:['Source for this', 'Cites this source'],
    shares_source:['Rests on the same source', 'Rests on the same source'],
    assigned:['Assigned to this', 'Assigned to'],
    feeds:['Feeds this goal', 'The goal this feeds'],
    member:['Project holding this', 'In this project'],
    used:['Ran this conversation', 'Conversation it ran'],
    delegated:['Handed this on', 'Work it handed on'],
    lineage:['Made from this', 'Made from it']
  };
  /* A sentence for a single line, read left to right. */
  const SENTENCE = {in:'is kept in', attached:'was given to', saved:'saved', updated:'changed', into:'saved work into', supports:'supports', challenges:'challenges',
    basis:'is a basis for', extends:'extends', source:'is a source for', shares_source:'rests on the same source as', assigned:'is assigned to',
    feeds:'feeds', member:'holds', used:'ran', delegated:'handed work to', lineage:'is an earlier version of'};
  const COLUMN = {file:0, record:0, method:0, app:0, chat:1, session:1, agent:1, task:1, project:1, land:2, item:2, finding:2, decision:2, output:2, goal:3};
  const COLUMNS = ['Inputs', 'Work', 'Saved work', 'Goals'];
  /* Groups inside a column, in the order they are drawn. A Library item is grouped by its own type. */
  const GROUP = {app:'AI apps', file:'Files', record:'Evidence', chat:'Conversations', session:'Conversations', agent:'Agents', task:'Scheduled tasks',
    project:'Projects', land:'Areas', item:'Tracked results', finding:'Findings', decision:'Decisions', output:'Saved outputs', goal:'Goals'};
  const PLURAL = {Playbook:'Playbooks', Workflow:'Workflows', Skill:'Skills', Recipe:'Recipes', Tool:'Tools', Plugin:'Plugins'};
  const group = n => n.kind === 'method' ? PLURAL[n.sub] || 'Library' : GROUP[n.kind] || KIND[n.kind] || n.kind;
  const ORDER = ['AI apps', 'Playbooks', 'Workflows', 'Skills', 'Recipes', 'Tools', 'Plugins', 'Library', 'Files', 'Evidence', 'Agents', 'Conversations', 'Scheduled tasks', 'Projects', 'Areas', 'Tracked results', 'Findings', 'Decisions', 'Saved outputs', 'Goals'];

  const indexes = new WeakMap();
  function index(feed) {
    if (indexes.has(feed)) return indexes.get(feed);
    // AI apps are recorded by AURA's own key for them (codex, claude…); show the name people know.
    const named = n => n.kind === 'app' && typeof window.appName === 'function' ? {...n, name: window.appName(n.name)} : n;
    const graph = feed?.relationships || {nodes:[], edges:[]}, nodes = new Map(graph.nodes.map(n => [n.key, named(n)])), into = new Map(), from = new Map();
    for (const edge of graph.edges) {
      if (!into.has(edge.target)) into.set(edge.target, []);
      if (!from.has(edge.source)) from.set(edge.source, []);
      into.get(edge.target).push(edge); from.get(edge.source).push(edge);
    }
    const result = {nodes, into, from, edges:graph.edges};
    indexes.set(feed, result); return result;
  }
  const key = selection => selection ? (selection.kindOf || selection.kind) + ':' + selection.id : '';
  const words = (edge, otherIsSource) => (WORDS[edge.type] || ['Linked', 'Linked'])[otherIsSource ? 0 : 1];
  const sentence = (a, edge, b) => `${a.name} ${SENTENCE[edge.type] || 'is linked to'} ${b.name}`;

  /* The whole chain through one thing: everything that flowed into it, and everything it flowed into.
     An area is not fed by everything kept in it, and a project's other members are not downstream of its work. */
  function trace(feed, start, limit = 400) {
    const ix = index(feed), up = new Set([start]), down = new Set([start]);
    let frontier = [start];
    while (frontier.length && up.size < limit) {
      const next = [];
      for (const k of frontier) for (const e of ix.into.get(k) || []) if (e.type !== 'in' && !up.has(e.source)) { up.add(e.source); next.push(e.source); }
      frontier = next;
    }
    frontier = [start];
    while (frontier.length && down.size < limit) {
      const next = [];
      for (const k of frontier) for (const e of ix.from.get(k) || []) {
        if (e.type === 'member' && k !== start) continue;
        if (!down.has(e.target)) { down.add(e.target); next.push(e.target); }
      }
      frontier = next;
    }
    const all = new Set([...up, ...down]);
    const edges = ix.edges.filter(e => (up.has(e.source) && up.has(e.target)) || (down.has(e.source) && down.has(e.target)));
    return {up, down, all, edges};
  }
  /* The places on the world a selection touches: its own, and those of everything in its chain. */
  function places(feed, start) {
    const ix = index(feed), out = new Set();
    for (const k of trace(feed, start).all) {
      const n = ix.nodes.get(k);
      if (!n) continue;
      if (n.kind === 'land') out.add(k.slice(5));
      for (const land of n.lands || []) out.add(land);
    }
    return [...out];
  }
  /* Rows for the panel: what fed this and what it led to. Direct links say how; further ones say through what. */
  function sides(feed, start) {
    const ix = index(feed), t = trace(feed, start), direct = [[], []], further = [[], []], seen = new Set([start]);
    for (const e of ix.into.get(start) || []) if (e.type !== 'in' && ix.nodes.get(e.source) && !seen.has(e.source)) { seen.add(e.source); direct[0].push({node:ix.nodes.get(e.source), how:words(e, true)}); }
    for (const e of ix.from.get(start) || []) if (ix.nodes.get(e.target) && !seen.has(e.target)) { seen.add(e.target); direct[1].push({node:ix.nodes.get(e.target), how:words(e, false)}); }
    for (const [side, set] of [[0, t.up], [1, t.down]]) for (const k of set) if (!seen.has(k) && ix.nodes.get(k)) { seen.add(k); further[side].push(ix.nodes.get(k)); }
    const kept = (ix.into.get(start) || []).filter(e => e.type === 'in').length;
    return {direct, further, kept};
  }
  /* What a line carries. 'saved' is saved work: the records a piece of work saved or changed. 'requests', 'tokens' and
     'cost_usd' are AI use, exactly as each app reported it. A line with nothing recorded is drawn thin and dashed. */
  const WORK = new Set(['chat', 'session', 'task', 'agent']);
  function measures(feed) {
    const ix = index(feed), usage = new Map();
    for (const g of feed.effort || []) for (const c of g.chats || []) if (c.id) {
      const u = usage.get('chat:' + c.id) || {requests:0, tokens:0, cost_usd:0};
      for (const f of ['requests', 'tokens', 'cost_usd']) u[f] += c[f] || 0;
      usage.set('chat:' + c.id, u);
    }
    const outputs = k => (ix.from.get(k) || []).filter(e => e.type === 'saved' || e.type === 'updated');
    const chatsOf = k => ix.nodes.get(k)?.kind === 'agent' ? (ix.from.get(k) || []).filter(e => e.type === 'used').map(e => e.target) : [k];
    /* How much one piece of work carried, optionally only into one area. */
    function carried(k, measure, land) {
      return chatsOf(k).reduce((sum, c) => {
        if (measure !== 'saved') return sum + (usage.get(c)?.[measure] || 0);
        return sum + outputs(c).filter(e => !land || (ix.nodes.get(e.target)?.lands || []).includes(land) || e.target === 'land:' + land).length;
      }, 0);
    }
    const held = landKey => { const l = (feed.lands || []).find(x => 'land:' + x.id === landKey); return l ? l.items.length + (l.more || 0) + (feed.findings || []).filter(f => f.land === l.id && f.label !== 'replaced').length : 0; };
    /* The weight of one recorded link in a traced chain. */
    function weigh(e, measure) {
      const a = ix.nodes.get(e.source), b = ix.nodes.get(e.target);
      if (!a || !b) return 0;
      if (e.type === 'saved' || e.type === 'updated') return measure === 'saved' ? 1 : carried(e.source, measure);
      if (e.type === 'into') return carried(e.source, measure, e.target.slice(5));
      if (WORK.has(a.kind)) return carried(e.source, measure);
      if (WORK.has(b.kind)) return carried(e.target, measure);
      if (e.type === 'feeds') return measure === 'saved' ? held(e.source) : 0;
      return measure === 'saved' ? 1 : 0;
    }
    return {carried, weigh, held};
  }
  /* What is moving right now: the chains of the conversations that are running. */
  function live(feed, running) {
    const out = new Set();
    for (const id of running || []) { const k = 'chat:' + id; if (!index(feed).nodes.has(k)) continue; for (const x of trace(feed, k).all) out.add(x); out.add(CHATS); }
    return out;
  }
  /* The whole flow at a glance. Conversations are many, so they are drawn as one step in the work column:
     what your AI used flows into them, and they flow to where their work went. Agents keep their own lines. */
  const CHATS = 'chats:all';
  function overview(feed, measure = 'saved') {
    const ix = index(feed), extra = new Map(), known = k => ix.nodes.get(k) || extra.get(k), m = measures(feed);
    const weights = new Map(), add = (a, b, w) => { if (!a || !b || a === b || !known(a) || !known(b)) return; const k = a + '\n' + b; weights.set(k, (weights.get(k) || 0) + w); };
    const placeOf = k => { const n = ix.nodes.get(k); if (!n) return []; if (['land', 'goal', 'project'].includes(n.kind)) return [k]; return (n.lands || []).map(id => 'land:' + id); };
    let chats = 0;
    for (const [k, n] of ix.nodes) {
      if (n.kind !== 'chat' && n.kind !== 'session') continue;
      const ins = (ix.into.get(k) || []).map(e => e.source), outs = new Set((ix.from.get(k) || []).flatMap(e => placeOf(e.target)));
      for (const e of ix.into.get(k) || []) if (e.type === 'attached' && ix.nodes.get(e.source)?.kind === 'land') outs.add(e.source);
      if (!outs.size) continue;
      chats++; if (!extra.size) extra.set(CHATS, {key:CHATS, kind:'chat', name:'Conversations', virtual:true});
      for (const i of ins) { const kind = ix.nodes.get(i)?.kind; if (['app', 'method'].includes(kind)) add(i, CHATS, m.carried(k, measure)); else if (kind === 'agent') for (const o of outs) add(i, o, o.startsWith('land:') ? m.carried(k, measure, o.slice(5)) : m.carried(k, measure)); }
      for (const o of outs) add(CHATS, o, o.startsWith('land:') ? m.carried(k, measure, o.slice(5)) : m.carried(k, measure));
    }
    if (chats) extra.get(CHATS).name = chats === 1 ? '1 conversation' : chats + ' conversations';
    for (const e of ix.edges) {
      const a = ix.nodes.get(e.source), b = ix.nodes.get(e.target);
      if (!a || !b || ['chat', 'session'].includes(a.kind) || ['chat', 'session'].includes(b.kind)) continue;
      if (['task', 'agent', 'project', 'land'].includes(a.kind) && ['land', 'goal', 'task'].includes(b.kind)) add(e.source, e.target, m.weigh(e, measure));
      else if (['saved', 'updated'].includes(e.type)) for (const o of placeOf(e.target)) add(e.source, o, measure === 'saved' ? 1 : 0);
    }
    const edges = [...weights].map(([k, w]) => { const [source, target] = k.split('\n'); return {source, target, weight:w}; });
    const score = new Map();
    for (const e of edges) for (const k of [e.source, e.target]) score.set(k, (score.get(k) || 0) + e.weight);
    for (const [k, n] of ix.nodes) if (['land', 'goal'].includes(n.kind) && !score.has(k)) score.set(k, 0);
    return {edges, score, node:known};
  }
  return {KIND, COLUMN, COLUMNS, ORDER, group, index, key, words, sentence, trace, places, sides, overview, measures, live, CHATS};
})();
