"""A read-only projection of recorded relationships, shared by every view of the world.

Each edge is {source, target, type}: the source flows into the target. The type says what was recorded,
never an inferred cause or a completion. The interface words each type for the direction it is read in.

  in             a finding kept in an area; followed only from the finding to its place
  attached       something given to a conversation
  saved          first saved while that chat, task or agent was working (AURA notes this on its own saves)
  updated        a check run by that chat, task or agent changed this tracked result
  into           the area that work saved into (derived from saved and updated, so an area's chain reaches its work)
  supports, challenges, basis, extends
                 evidence behind a finding, or findings a decision rests on (basis)
  source         a saved source behind evidence or behind a tracked result
  shares_source  a tracked result and a finding that rest on the same saved source
  assigned       work assigned to a collection, goal, project or scheduled task
  feeds          a collection linked to a goal
  member         something a project holds
  used           the AI app or agent a conversation ran in
  delegated      work a conversation or agent handed on
  lineage        an earlier record an asset was made from

A tracked result's place in its collection is not an edge: it is in the result's key (item:<collection>|<id>),
so a collection with thousands of results adds nothing here. A result becomes a node only when something
else is recorded about it. No filesystem traversal, provider calls, or second relationship store lives here.
"""

EVIDENCE = {'supports': 'supports', 'contradicts': 'challenges', 'derived_from': 'basis', 'extends': 'extends'}
# Saves worth showing as a piece of work's output. Raw sources and observations stay behind their findings.
OUTPUTS = {'Insight', 'DecisionRecord', 'Learning', 'Asset'}


def relationships(feed, registry, bound, objects, references, item_sources=None, assistants=()):
    nodes, edges = {}, {}
    bid = feed['business']['id']
    titles = {}  # 'land|item' -> title, so a result can become a node when something is recorded about it
    for land in feed['lands']:
        for item in land['items']:
            titles[land['id'] + '|' + item['id']] = item['title']

    def node(kind, ident, name, action=None, lands=()):
        key = f'{kind}:{ident}'
        if key not in nodes:
            row = {'key': key, 'kind': kind, 'name': str(name or ident)[:240]}
            if action:row['action'] = action
            if lands:row['lands'] = list(lands)
            nodes[key] = row
        return key

    def item(land, ident):
        ref = f'{land}|{ident}'
        return node('item', ref, titles[ref], lands=[land]) if ref in titles else None

    def edge(a, b, kind):
        if a and b and a in nodes and b in nodes and a != b:
            edges[(a, b, kind)] = {'source': a, 'target': b, 'type': kind}

    records = {o['id']: o for o in objects}
    aliases = {}
    for land in feed['lands']:
        node('land', land['id'], land['name'], lands=[land['id']])
    for kind, rows, title in [('goal', feed['goals'], 'name'), ('finding', feed['findings'], 'statement'),
                              ('decision', feed['decisions'], 'title')]:
        for row in rows:
            key = node(kind, row['id'], row[title], {'record': row['id']} if row['id'] in records else None,
                       row.get('lands') or ([row['land']] if row.get('land') else []))
            aliases[row['id']] = key
    for obj in objects:
        collection = ((obj.get('extensions') or {}).get('businessos') or {}).get('collection') or {}
        key = 'land:' + str(collection.get('id'))
        if obj.get('object_type') == 'Asset' and key in nodes:
            aliases[obj['id']] = key

    def reference(ref):
        kind, ident = ref.get('kind'), ref.get('id')
        if not isinstance(ident, str):
            return None
        if kind in {'record', 'asset', 'goal'}:
            if ident in aliases:
                return aliases[ident]
            obj = records.get(ident)
            if not obj:
                return None  # Never expose an unrelated organization's record.
            key = node('record', ident, obj.get('title') or obj.get('name') or obj.get('statement') or obj.get('business_role') or obj.get('object_type'),
                       {'record': ident})
            aliases[ident] = key
            return key
        if kind == 'collection':
            return 'land:' + ident
        if kind == 'file':
            return node('file', ident, ref.get('label') or ident.replace('\\', '/').rsplit('/', 1)[-1], {'file': ident})
        if kind == 'library':
            return node('method', ident, ref.get('label') or ident, {'method': ident})
        if kind == 'task':
            return 'task:' + ident
        return None

    for land, rows in (item_sources or {}).items():
        for ident, source_ids, _ in rows:
            for source in sorted(source_ids):
                if source in records:
                    edge(reference({'kind': 'record', 'id': source}), item(land, ident), 'source')
    for task in feed['tasks']:
        key = node('task', task['id'], task['name'], {'view': 'tools'}, [task['land']] if task.get('land') else [])
        edge(key, 'land:' + str(task.get('land')), 'assigned')
        edge(key, 'goal:' + str(task.get('goal')), 'assigned')
    for goal in feed['goals']:
        for land in goal.get('lands', []):
            edge('land:' + land, 'goal:' + goal['id'], 'feeds')
    for finding in feed['findings']:
        key = 'finding:' + finding['id']
        for land in finding.get('lands', [finding['land']]):
            edge(key, 'land:' + land, 'in')
        for related in finding.get('related_items', []):
            edge(item(related['land'], related['id']), key, 'shares_source')
        for evidence in finding.get('source_details', []):
            source = reference({'kind': 'record', 'id': evidence['id']})
            edge(source, key, EVIDENCE.get(evidence['relationship'], 'supports'))
            for saved in evidence.get('sources', []):
                edge(reference({'kind': 'record', 'id': saved['id']}), source, 'source')
    for decision in feed['decisions']:
        for finding in decision.get('basis', []):
            edge('finding:' + finding, 'decision:' + decision['id'], 'basis')
    for project in registry.get('projects', []):
        if project.get('business_id') != bid or project.get('status', 'active') != 'active':
            continue
        key = node('project', project['id'], project['name'], {'open-project': project['id']})
        for ref in project.get('members', []) + project.get('context_refs', []):
            edge(key, reference(ref), 'member')
        for land in feed['lands']:
            if project['id'] in land.get('project_refs', []):
                edge(key, 'land:' + land['id'], 'member')
    for method in feed['methods']:
        node('method', method['id'], method['name'], {'method': method['id']}, method.get('lands', []))
    for assistant in assistants:
        if assistant.get('archived_at'):
            continue
        key = node('agent', assistant['id'], assistant['name'], {'assistant-open': assistant['id']})
        for task in assistant.get('task_ids') or []:
            edge(key, 'task:' + task, 'assigned')
    for chat in references:
        key = node('chat', chat['id'], chat['title'], {'chat': chat['id']})
        if chat.get('assistant_id'):
            edge('agent:' + chat['assistant_id'], key, 'used')
        if chat.get('agent'):
            edge(node('app', chat['agent'], chat['agent']), key, 'used')
        for ref in chat['references']:
            edge(reference(ref), key, 'attached')
    for chat in references:
        children = [child for child in chat.get('subagents', []) if isinstance(child, dict) and isinstance(child.get('id'), str)]
        for child in children:
            node('agent', chat['id'] + '|' + child['id'], child.get('name') or child.get('task') or 'Delegated agent', {'chat': chat['id']})
        for child in children:
            parent = 'agent:' + chat['id'] + '|' + str(child.get('parent_id'))
            if parent not in nodes:
                parent = 'chat:' + chat['id']
            edge(parent, 'agent:' + chat['id'] + '|' + child['id'], 'delegated')
    for binding in bound:
        kind, ident = binding.get('kind'), binding.get('id')
        if kind not in {'agent', 'chat', 'task'} or not ident:
            continue
        key = f'{kind}:{ident}'
        if key not in nodes:
            if kind != 'agent':
                continue
            node(kind, ident, binding.get('name') or ident, {'view': 'assistants'})
        edge(key, 'land:' + str(binding.get('collection_id')), 'assigned')
        edge(key, 'goal:' + str(binding.get('goal_ref')), 'assigned')
        for project in binding.get('project_refs', []):
            edge(key, 'project:' + project, 'assigned')

    def producer(by):
        """The chat, task or agent AURA started when this was saved. It establishes where, not why."""
        kind, ident = (by or {}).get('kind'), (by or {}).get('id')
        if kind not in {'task', 'agent', 'chat'} or not isinstance(ident, str) or not ident:
            return None
        return node(kind, ident, {'chat': 'A saved conversation', 'task': 'A scheduled task', 'agent': 'An agent'}[kind],
                    {'chat': ident} if kind == 'chat' else None)

    for obj in objects:
        by = (((obj.get('extensions') or {}).get('businessos') or {}).get('work') or {}).get('producer')
        if obj.get('object_type') not in OUTPUTS or not by:
            continue
        output = reference({'kind': 'record', 'id': obj['id']})
        edge(producer(by), output, 'saved')
        if obj.get('object_type') == 'Asset':
            for ancestor in obj.get('lineage') or []:
                edge(reference({'kind': 'record', 'id': ancestor}), output, 'lineage')
    for change in feed.get('changes', []):
        if change.get('by') and change.get('item_id'):
            edge(producer(change['by']), item(change['land'], change['item_id']) or 'land:' + change['land'], 'updated')
    # The area a piece of work saved into, so an area's chain reaches the work behind it without listing everything kept there.
    for (a, b, kind) in list(edges):
        if kind in {'saved', 'updated'} and nodes[b]['kind'] != 'land':
            for land in nodes[b].get('lands', []):
                edge(a, 'land:' + land, 'into')
    return {'nodes': list(nodes.values()), 'edges': list(edges.values())}
