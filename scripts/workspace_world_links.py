"""A read-only projection of recorded relationships, shared by the world's views.

Edges describe the recorded relationship, never inferred causality or completion.
No filesystem traversal, provider calls, or second relationship store lives here.
"""


def relationships(feed, registry, bound, objects, references, item_sources=None, assistants=()):
    nodes, edges = {}, {}
    bid = feed['business']['id']

    def node(kind, ident, name, action=None, lands=()):
        key = f'{kind}:{ident}'
        if key not in nodes:
            nodes[key] = dict(key=key, kind=kind, id=ident, name=str(name or ident)[:240],
                              action=action, lands=list(lands))
        return key

    def edge(a, b, label):
        if a in nodes and b in nodes and a != b:
            edges[(a, b, label)] = dict(source=a, target=b, label=label)

    records = {o['id']: o for o in objects}
    aliases = {}
    for land in feed['lands']:
        node('land', land['id'], land['name'], lands=[land['id']])
        for item in land['items']:
            key = node('item', land['id']+'|'+item['id'], item['title'], lands=[land['id']])
            edge(key, 'land:'+land['id'], 'Saved in collection')
    for kind, rows, title in [('goal', feed['goals'], 'name'), ('finding', feed['findings'], 'statement'),
                              ('decision', feed['decisions'], 'title')]:
        for row in rows:
            key = node(kind, row['id'], row[title], {'record': row['id']} if row['id'] in records else None,
                       row.get('lands') or ([row['land']] if row.get('land') else []))
            aliases[row['id']] = key
    for obj in objects:
        collection = ((obj.get('extensions') or {}).get('businessos') or {}).get('collection') or {}
        key = 'land:'+str(collection.get('id'))
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
            return 'land:'+ident
        if kind == 'file':
            return node('file', ident, ref.get('label') or ident.replace('\\', '/').rsplit('/', 1)[-1], {'file': ident})
        if kind == 'library':
            return node('method', ident, ref.get('label') or ident, {'method': ident})
        if kind == 'task':
            return 'task:'+ident
        return None

    for land, items in (item_sources or {}).items():
        for ident, source_ids, _ in items:
            for source in sorted(source_ids):
                edge(reference({'kind': 'record', 'id': source}), 'item:'+land+'|'+ident, 'Source for tracked result')
    for task in feed['tasks']:
        key = node('task', task['id'], task['name'], {'view': 'tools'}, [task['land']] if task.get('land') else [])
        edge(key, 'land:'+str(task.get('land')), 'Bound to collection')
        edge(key, 'goal:'+str(task.get('goal')), 'Bound to goal')
    for goal in feed['goals']:
        for land in goal.get('lands', []):
            edge('land:'+land, 'goal:'+goal['id'], 'Linked to goal')
    for finding in feed['findings']:
        key = 'finding:'+finding['id']
        for land in finding.get('lands', [finding['land']]):
            edge(key, 'land:'+land, 'Saved in area')
        for item in finding.get('related_items', []):
            edge('item:'+item['land']+'|'+item['id'], key, 'Shares a saved source')
        for evidence in finding.get('source_details', []):
            source = reference({'kind': 'record', 'id': evidence['id']})
            edge(source, key, {'supports': 'Supports finding', 'contradicts': 'Challenges finding',
                              'derived_from': 'Basis for finding', 'extends': 'Extends finding'}.get(evidence['relationship'], 'Linked evidence'))
            for saved in evidence.get('sources', []):
                edge(reference({'kind': 'record', 'id': saved['id']}), source, 'Cited by evidence')
    for decision in feed['decisions']:
        for finding in decision.get('basis', []):
            edge('finding:'+finding, 'decision:'+decision['id'], 'Cited by decision')
    for project in registry.get('projects', []):
        if project.get('business_id') != bid or project.get('status', 'active') != 'active':
            continue
        key = node('project', project['id'], project['name'], {'open-project': project['id']})
        for ref in project.get('members', []) + project.get('context_refs', []):
            edge(key, reference(ref), 'Linked in project')
        for land in feed['lands']:
            if project['id'] in land.get('project_refs', []):
                edge(key, 'land:'+land['id'], 'Linked in project')
    for method in feed['methods']:
        node('method', method['id'], method['name'], {'method': method['id']}, method.get('lands', []))
    for assistant in assistants:
        if assistant.get('archived_at'):
            continue
        key = node('agent', assistant['id'], assistant['name'], {'assistant-open': assistant['id']})
        for task in assistant.get('task_ids') or []:
            edge(key, 'task:'+task, 'Assigned scheduled task')
    for chat in references:
        key = node('chat', chat['id'], chat['title'], {'chat': chat['id']})
        if chat.get('assistant_id'):
            edge('agent:'+chat['assistant_id'], key, 'Agent conversation')
        if chat.get('agent'):
            app = node('app', chat['agent'], chat['agent'])
            edge(app, key, 'Conversation in app')
        for ref in chat['references']:
            edge(reference(ref), key, 'Attached to conversation')
    for chat in references:
        children = [child for child in chat.get('subagents', []) if isinstance(child, dict) and isinstance(child.get('id'), str)]
        for child in children:
            node('agent', chat['id']+'|'+child['id'], child.get('name') or child.get('task') or 'Delegated agent',
                 {'chat': chat['id']})
        for child in children:
            parent = 'agent:'+chat['id']+'|'+str(child.get('parent_id'))
            if parent not in nodes:
                parent = 'chat:'+chat['id']
            edge(parent, 'agent:'+chat['id']+'|'+child['id'], 'Reported delegated work')
    for binding in bound:
        kind, ident = binding.get('kind'), binding.get('id')
        if kind not in {'agent', 'chat', 'task'} or not ident:
            continue
        key = f'{kind}:{ident}'
        if key not in nodes:
            if kind != 'agent':
                continue
            node(kind, ident, binding.get('name') or ident, {'view': 'assistants'})
        edge(key, 'land:'+str(binding.get('collection_id')), 'Bound to collection')
        edge(key, 'goal:'+str(binding.get('goal_ref')), 'Bound to goal')
        for project in binding.get('project_refs', []):
            edge(key, 'project:'+project, 'Bound to project')
    # A producer explicitly saved with an output establishes authorship.
    # A chat binding or an attached source on its own does not.
    for obj in objects:
        work = ((obj.get('extensions') or {}).get('businessos') or {}).get('work') or {}
        producer = work.get('producer') or {}
        if obj.get('object_type') != 'Asset' or producer.get('kind') not in {'task', 'agent', 'chat'}:
            continue
        ident = producer.get('id')
        if not isinstance(ident, str) or not ident:
            continue
        key = f"{producer['kind']}:{ident}"
        if key not in nodes:
            node(producer['kind'], ident, 'Recorded '+producer['kind'])
        output = reference({'kind': 'asset', 'id': obj['id']})
        edge(key, output, 'Produced saved asset')
        for ancestor in obj.get('lineage') or []:
            edge(reference({'kind': 'record', 'id': ancestor}), output, 'Recorded in asset lineage')
    return {'nodes': list(nodes.values()), 'edges': list(edges.values())}
