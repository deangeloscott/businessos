/* Recorded relationships, read one way by the world, the panel and the Connections diagram.
   The feed's relationships are {nodes, edges}: each edge is {source, target, type} and the source flows into
   the target (see scripts/workspace_world_links.py for what each type records). Nothing here guesses a link. */
window.auraLinks = (() => {
  const KIND = {land:'Area', item:'Tracked result', finding:'Finding', decision:'Decision', goal:'Goal', record:'Evidence',
    file:'File', method:'Library item', chat:'Conversation', agent:'Agent', task:'Scheduled task', app:'AI app', project:'Project'};
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
  const COLUMN = {file:0, record:0, method:0, app:0, chat:1, agent:1, task:1, project:1, land:2, item:2, finding:2, decision:2, goal:3};
  const COLUMNS = ['Inputs', 'Work', 'Saved work', 'Goals'];

  const indexes = new WeakMap();
  function index(feed) {
    if (indexes.has(feed)) return indexes.get(feed);
    const graph = feed?.relationships || {nodes:[], edges:[]}, nodes = new Map(graph.nodes.map(n => [n.key, n])), into = new Map(), from = new Map();
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
  /* The whole flow at a glance. Conversations are many, so they are drawn as one step in the work column:
     what your AI used flows into them, and they flow to where their work went. Agents keep their own lines. */
  const CHATS = 'chats:all';
  function overview(feed) {
    const ix = index(feed), extra = new Map(), known = k => ix.nodes.get(k) || extra.get(k);
    const weights = new Map(), add = (a, b, w = 1) => { if (!a || !b || a === b || !known(a) || !known(b)) return; const k = a + '\n' + b; weights.set(k, (weights.get(k) || 0) + w); };
    const placeOf = k => { const n = ix.nodes.get(k); if (!n) return []; if (['land', 'goal', 'project'].includes(n.kind)) return [k]; return (n.lands || []).map(id => 'land:' + id); };
    let chats = 0;
    for (const [k, n] of ix.nodes) {
      if (n.kind !== 'chat') continue;
      const ins = (ix.into.get(k) || []).map(e => e.source), outs = new Set((ix.from.get(k) || []).flatMap(e => placeOf(e.target)));
      for (const e of ix.into.get(k) || []) if (e.type === 'attached' && ix.nodes.get(e.source)?.kind === 'land') outs.add(e.source);
      if (!outs.size) continue;
      chats++; if (!extra.size) extra.set(CHATS, {key:CHATS, kind:'chat', name:'Conversations', virtual:true});
      for (const i of ins) { const kind = ix.nodes.get(i)?.kind; if (['app', 'method'].includes(kind)) add(i, CHATS); else if (kind === 'agent') for (const o of outs) add(i, o); }
      for (const o of outs) add(CHATS, o);
    }
    if (chats) extra.get(CHATS).name = chats === 1 ? '1 conversation' : chats + ' conversations';
    for (const e of ix.edges) {
      const a = ix.nodes.get(e.source), b = ix.nodes.get(e.target);
      if (!a || !b || a.kind === 'chat' || b.kind === 'chat') continue;
      if (['task', 'agent', 'project', 'land'].includes(a.kind) && ['land', 'goal', 'task'].includes(b.kind)) add(e.source, e.target);
      else if (['saved', 'updated'].includes(e.type)) for (const o of placeOf(e.target)) add(e.source, o);
    }
    const edges = [...weights].map(([k, w]) => { const [source, target] = k.split('\n'); return {source, target, weight:w}; });
    const score = new Map();
    for (const e of edges) for (const k of [e.source, e.target]) score.set(k, (score.get(k) || 0) + e.weight);
    for (const [k, n] of ix.nodes) if (['land', 'goal'].includes(n.kind) && !score.has(k)) score.set(k, 0);
    return {edges, score, node:known};
  }
  return {KIND, COLUMN, COLUMNS, index, key, words, sentence, trace, places, sides, overview};
})();
