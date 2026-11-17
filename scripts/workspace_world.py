"""The world: everything the aura view draws, in one read-only answer.

The aura shows an organization as a world: each collection (and each area of findings kept outside one)
is a continent, each current result a light, each finding a smaller light, each change a check noticed a
faint one, and each goal with a number a ring. This returns exactly those saved records and nothing else:
no scores, no guesses. It writes nothing. Bounded on purpose, with counts of what was left out.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from _common import workspace_root, workspace_scope, object_index, storage_ref
from workspace_lifecycle import archived
import workspace_collections as collections
import workspace_summary as summary

MAX_LANDS, MAX_ITEMS, MAX_FINDINGS, MAX_CHANGES, MAX_DECISIONS = 24, 300, 600, 800, 60
AREA_ORDER = {key: n for n, (key, _) in enumerate(summary.AREAS)}
AREA_SLOTS = len(AREA_ORDER)


def _fields(row):
    """A few of a result's own details, short enough to label a light."""
    out = {}
    for key, value in list((row.get('fields') or {}).items())[:3]:
        if isinstance(value, (dict, list)):continue
        out[str(key)[:60]] = value if isinstance(value, (bool, int, float)) or value is None else str(value)[:80]
    return out


def _trend(row):
    """The saved history of a result's first number (rank, rating, price), oldest first. Empty when it has none."""
    points = [p for p in row.get('trail') or [] if isinstance(p, dict) and isinstance(p.get('values'), dict)]
    keys = [k for k in (points[-1]['values'] if points else {})]
    if len(points) < 2 or not keys:return None
    return {'field': keys[0], 'points': [{'at': p.get('at'), 'value': p['values'].get(keys[0])} for p in points[-12:] if isinstance(p['values'].get(keys[0]), (int, float))]}


def _item(row):
    refs = [r for r in row.get('source_refs') or [] if isinstance(r, dict)]
    return {'_source_ids': {r['source_id'] for r in refs if r.get('source_id')}, '_source_refs': {r['reference'] for r in refs if r.get('reference')},
            'id': row['id'], 'title': str(row.get('title', ''))[:160], 'first_seen': row.get('first_seen'), 'updated_at': row.get('updated_at'),
            'last_seen': row.get('last_seen'), 'needs_review': bool(row.get('needs_review')), 'sources': len(row.get('source_refs') or []), 'fields': _fields(row), 'trend': _trend(row)}


def world(bid, at=None, app=None):
    at = at or datetime.now(timezone.utc)
    base = summary.summary(bid, at, days=14)
    index = object_index(bid)
    live = [(o, where) for o, where in index.values() if not archived(o)]
    objects = [o for o, _ in live]
    business = next(o for o in objects if o.get('object_type') == 'Business')
    watches, watches_total, _, _ = summary._watches(bid, at, 14, 1000, 0)
    lands = [];changes = []
    # Work that is bound to a collection (a chat, task or agent) is the one saved sign of how much it is used.
    try:registry = collections.projects.load()
    except (ValueError, OSError):registry = {}
    bound = [b for b in (registry.get('bindings') or {}).values() if isinstance(b, dict) and b.get('business_id') == bid]
    uses = {}
    for b in bound:
        if b.get('collection_id'):uses[b['collection_id']] = uses.get(b['collection_id'], 0) + 1
    # Places never move: each area keeps its own place whether or not it holds anything yet, and collections take the
    # next places in the order they were created, so a new one never shifts the others.
    docs = []
    for w in watches:
        try:d = collections.read(bid, w['id'])
        except ValueError:continue
        docs.append((str(d.get('created_at') or ''), d['id'], w, d))
    docs.sort(key=lambda row: row[:2])
    slots = {row[1]: AREA_SLOTS + n for n, row in enumerate(docs)}
    drawn = docs if len(docs) <= MAX_LANDS else docs[:MAX_LANDS - 1]
    grouped = [{'id': w['id'], 'name': w['name'], 'current': w['current']} for _, _, w, _ in docs[len(drawn):]]
    for _, _, w, d in drawn:
        rows = [collections.effective(i, d['feedback'], at) for i in d['items']]
        current = sorted((r for r in rows if r['display_state'] == 'active' and not r['hidden']), key=lambda r: str(r.get('first_seen') or ''))
        checked = summary._time(w['last_checked'])
        age = (at - checked).total_seconds() / 86400 if checked else None
        # The same test the home page uses to notice a list that was being kept current and has gone quiet.
        quiet = bool(w['_kept_current'] and age is not None and age >= max(7, 2 * (w.get('_rhythm') or 15)))
        lands.append({'id': d['id'], 'slot': slots[d['id']], 'name': d['name'], 'kind': 'collection', 'purpose': str(d.get('purpose') or '')[:240], 'task_linked': w['task_linked'],
                      'last_checked': w['last_checked'], 'quiet': quiet, 'uses': uses.get(d['id'], 0), 'project_refs': list(d.get('project_refs') or []),
                      'items': [_item(r) for r in current[:MAX_ITEMS]], 'more': max(0, len(current) - MAX_ITEMS)})
        checks = [c for c in d['checks'] if isinstance(c.get('at'), str)]
        for position, check in enumerate(checks):
            if position == 0 and len(d['checks']) < 50:continue  # filling a collection for the first time is not a change
            for change in check.get('changes') or []:
                changes.append({'at': check['at'], 'land': d['id'], 'item_id': change.get('id'), 'kind': change.get('kind', 'changed'), 'title': str(change.get('title', ''))[:160]})
    changes.sort(key=lambda c: c['at'], reverse=True)
    names = dict(summary.AREAS);known = {land['id'] for land in lands};areas = {};findings = [];decisions = []
    by_id = {o.get('id'): o for o in objects}
    item_sources = {}  # collection -> [(result id, source ids, source references)]
    for land in lands:
        item_sources[land['id']] = [(i['id'], i.pop('_source_ids'), i.pop('_source_refs')) for i in land['items']]
    given_counts = _used(bid, app, known)
    for land in lands:land['given'] = given_counts['collections'].get(land['id'], 0)
    for o, where in live:
        kind = o.get('object_type')
        if kind == 'DecisionRecord':
            decisions.append({'id': o['id'], 'kind': 'decision', 'record': storage_ref(where), 'title': str(o.get('title') or o.get('decision') or o.get('statement') or o.get('name') or '')[:200],
                              'at': o.get('made_at') or o.get('decided_at') or o.get('created_at') or o.get('updated_at'), 'area': o.get('domain') if o.get('domain') in names else 'core',
                              'basis': [r for r in o.get('basis_refs') or [] if isinstance(r, str)][:8]})
            continue
        if kind == 'Learning' and o.get('status') not in {'archived', 'retired', 'superseded'}:
            decisions.append({'id': o['id'], 'kind': 'lesson', 'record': storage_ref(where), 'title': str(o.get('statement') or '')[:200], 'at': o.get('created_at') or o.get('updated_at'),
                              'area': o.get('domain') if o.get('domain') in names else 'core', 'basis': [r for r in o.get('evidence_refs') or [] if isinstance(r, str)][:8]})
            continue
        if kind != 'Insight' or o.get('status') == 'archived':continue
        bos = (o.get('extensions') or {}).get('businessos') or {}
        refs = [r for r in bos.get('collection_refs') or [] if r in known] if isinstance(bos.get('collection_refs'), list) else []
        domain = o.get('domain') if o.get('domain') in names else 'core'
        land = refs[0] if refs else 'area:' + domain
        if not refs:areas[land] = names[domain]
        links = [l for l in o.get('evidence_links') or [] if isinstance(l, dict)]
        review = summary._time(bos.get('review_after'))
        replaced = o.get('status') == 'superseded'
        # A finding is tied to a result only when the same saved source stands behind both.
        sources = set();texts = set()
        for link in links:
            for ref in (by_id.get(link.get('ref')) or {}).get('source_refs') or []:
                sources.add(ref);text = (by_id.get(ref) or {}).get('source_reference')
                if text:texts.add(text)
        tied = [ident for ident, ids, refs in item_sources.get(land, []) if ids & sources or refs & texts][:6] if sources else []
        sides = [{'relationship': l.get('relationship'), 'statement': str((by_id.get(l.get('ref')) or {}).get('statement') or '')[:240]} for l in links if l.get('relationship') in {'supports', 'derived_from', 'contradicts'}][:6] if o.get('status') == 'contradicted' else []
        findings.append({'id': o['id'], 'evidence': [s for s in sides if s['statement']], 'items': tied, 'given': given_counts['records'].get(o['id'], 0), 'record': storage_ref(where), 'statement': str(o.get('statement', ''))[:300], 'land': land, 'area': domain,
                         'label': 'replaced' if replaced else summary.finding_label(o.get('status'), bool(review and review <= at)),
                         'at': o.get('created_at') or o.get('reviewed_at') or o.get('updated_at'), 'updated_at': o.get('updated_at'),
                         'sources': sum(l.get('relationship') in {'supports', 'derived_from', 'extends'} for l in links),
                         'challenges': sum(l.get('relationship') == 'contradicts' for l in links)})
    findings.sort(key=lambda f: str(f.get('updated_at') or ''), reverse=True)
    if grouped:
        lands.append({'id': 'group:more', 'slot': AREA_SLOTS + MAX_LANDS, 'name': f'{len(grouped)} more collections', 'kind': 'group', 'purpose': '', 'task_linked': False, 'last_checked': None, 'quiet': False, 'uses': 0,
                      'project_refs': [], 'items': [], 'more': sum(g['current'] for g in grouped), 'members': grouped[:200]})
    for key, name in sorted(areas.items())[:max(0, MAX_LANDS - len(lands))]:
        lands.append({'id': key, 'slot': AREA_ORDER[key[5:]], 'name': name, 'kind': 'area', 'purpose': '', 'task_linked': False, 'last_checked': None, 'quiet': False, 'uses': 0, 'project_refs': [], 'items': [], 'more': 0})
    # Findings whose place could not be drawn are counted, never shown somewhere they do not belong.
    shown = {land['id'] for land in lands};hidden = sum(f['land'] not in shown for f in findings);findings = [f for f in findings if f['land'] in shown]
    # A very large world keeps every light but carries less about each one; its own screen has the rest.
    if sum(len(land['items']) for land in lands) > 1500:
        for land in lands:
            for item in land['items']:
                item.pop('trend', None);item.pop('last_seen', None);item['fields'] = dict(list(item['fields'].items())[:1])
    decisions = [d for d in decisions if d['title']]
    decisions.sort(key=lambda d: str(d.get('at') or ''), reverse=True)
    from workspace_views import progress
    # A goal is fed by the collections that saved work ties to it: a task or chat bound to both, or a project holding both.
    feeds = {}
    for b in bound:
        if b.get('goal_ref') and b.get('collection_id') in known:feeds.setdefault(b['goal_ref'], set()).add(b['collection_id'])
    for p in registry.get('projects') or []:
        if not isinstance(p, dict) or p.get('business_id') != bid or p.get('status', 'active') != 'active':continue
        members = [m for m in p.get('members') or [] if isinstance(m, dict)]
        held = {m.get('id') for m in members if m.get('kind') == 'collection'} | {l['id'] for l in lands if p.get('id') in l.get('project_refs', [])}
        for m in members:
            if m.get('kind') == 'goal':feeds.setdefault(m.get('id'), set()).update(held & known)
    goals = []
    for goal in base['goals']:
        row = dict(goal);row['lands'] = sorted(feeds.get(goal['id'], ()))
        if 'target' in goal:
            try:metrics = progress(bid, goal['id'], 60)['metrics']
            except (ValueError, OSError):metrics = []
            row['points'] = [{'at': p['at'], 'value': p['value']} for p in (metrics[0]['points'] if metrics else [])]
        goals.append(row)
    # Areas the organization's focus points to that hold nothing yet: drawn as places still to chart.
    used = {f['area'] for f in findings}
    uncharted = [{'id': a['id'], 'name': a['name'], 'slot': AREA_ORDER[a['id']]} for a in base['knowledge']['by_area'] if a['relevant'] and a['id'] != 'core' and a['id'] not in used][:8]
    return {'business': {**base['business'], 'since': business.get('created_at')}, 'as_of': base['as_of'], 'focus': base['focus'],
            'lands': lands, 'findings': findings[:MAX_FINDINGS], 'changes': changes[:MAX_CHANGES], 'goals': goals, 'decisions': decisions[:MAX_DECISIONS],
            'uncharted': uncharted if len(lands) < 8 else [], 'lands_more': len(grouped), 'findings_hidden': hidden, 'tasks': _tasks(bid, bound, known), 'chat_lands': {b['id']: b['collection_id'] for b in bound if b.get('kind') == 'chat' and b.get('collection_id') in known},
            'effort': _effort(bid, app, bound, known, at), 'methods': given_counts['library'], 'work': _work(bid, app, at), 'work_by': _work_by(bid, app, bound, known, at), 'apps': _apps(bid, app, bound, known), 'attention': base['attention'], 'deadlines': base['deadlines'], 'suggestions': base['suggestions'],
            'totals': {'lands': watches_total + len(areas), 'items': sum(len(l['items']) + l['more'] for l in lands), 'findings': len(findings), 'changes': len(changes),
                       'goals': base['totals']['goals'], 'attention': base['totals']['attention'], 'decisions': len(decisions)},
            'empty': base['empty']}


def _tasks(bid, bound, known):
    """Scheduled tasks tied to this organization's collections or goals, with each app's own report of how they are doing."""
    try:
        import workspace_schedules
        native = {t['id']: t for t in workspace_schedules.inventory()['items']}
    except Exception:native = {}
    from workspace_views import _health, cadence
    out = []
    for b in bound:
        if b.get('kind') != 'task' or not (b.get('collection_id') in known or b.get('goal_ref')):continue
        row = {'id': b['id'], 'land': b.get('collection_id') if b.get('collection_id') in known else None, 'goal': b.get('goal_ref')}
        task = native.get(b['id'])
        if task:
            health, text = _health(task)
            row.update(name=str(task.get('name') or 'Scheduled task')[:120], app=task.get('app'), schedule=cadence(task.get('schedule')), health=health, status=text, next_run=task.get('next_run'), last_run=task.get('last_run'), available=True)
        else:row.update(name='Scheduled task', app=None, schedule='', health='missing', status='This task was removed from its app, so it no longer runs.', next_run=None, last_run=None, available=False)
        out.append(row)
    return out[:60]


def _used(bid, app, known):
    """How often each finding, collection and method was given to a request, counted from what each chat saved about its own requests.
    Results inside a collection are not given one by one, so there is no count for a single result."""
    out = {'records': {}, 'collections': {}, 'library': []}
    if app is None:return out
    methods = {}
    chats = [c for c in app.preferences.get('chats', []) if isinstance(c, dict) and c.get('business_id') == bid][-400:]
    for chat in chats:
        try:messages = json.loads(Path(app.chat_display_path(chat['id'])).read_text(encoding='utf-8'))
        except (OSError, ValueError, KeyError, TypeError):continue
        for message in messages if isinstance(messages, list) else []:
            refs = [r for r in (message.get('references') or []) if isinstance(r, dict) and isinstance(r.get('id'), str)] if isinstance(message, dict) else []
            together = sorted({r['id'] for r in refs if r.get('kind') == 'collection' and r['id'] in known})
            for r in refs:
                if r.get('kind') == 'record':out['records'][r['id']] = out['records'].get(r['id'], 0) + 1
                elif r.get('kind') == 'collection':out['collections'][r['id']] = out['collections'].get(r['id'], 0) + 1
                elif r.get('kind') == 'library':
                    m = methods.setdefault(r['id'], {'id': r['id'], 'name': str(r.get('label') or r['id'])[:120], 'uses': 0, 'lands': set()})
                    m['uses'] += 1;m['lands'].update(together)
    out['library'] = [{**m, 'lands': sorted(m['lands'])} for m in sorted(methods.values(), key=lambda m: -m['uses'])[:40]]
    return out


def _work(bid, app, at, weeks=26):
    """AI requests per week for the last half year, from the usage each AI app reported."""
    if app is None:return None
    end = at.timestamp();start = end - weeks * 7 * 86400;rows = [0] * weeks;tokens = [0] * weeks
    for r in app.preferences.get('usage_receipts', []):
        if r.get('business_id') != bid or not isinstance(r.get('at'), (int, float)) or not start <= r['at'] <= end:continue
        slot = min(weeks - 1, int((r['at'] - start) // (7 * 86400)));rows[slot] += 1;tokens[slot] += int(r.get('input_tokens') or 0) + int(r.get('output_tokens') or 0)
    return [{'start': datetime.fromtimestamp(start + n * 7 * 86400, timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z'), 'requests': rows[n], 'tokens': tokens[n]} for n in range(weeks)] if any(rows) else []


def _apps(bid, app, bound, known):
    """Each AI app that reported requests here, and the collections its chats were tied to."""
    if app is None:return []
    chats = {b['id']: b for b in bound if b.get('kind') == 'chat'};out = {}
    for r in app.preferences.get('usage_receipts', []):
        name = str(r.get('agent') or '')[:80]
        if r.get('business_id') != bid or not name:continue
        row = out.setdefault(name, {'name': name, 'requests': 0, 'lands': set()});row['requests'] += 1
        land = chats.get(r.get('chat_id'), {}).get('collection_id')
        if land in known:row['lands'].add(land)
    return [{**a, 'lands': sorted(a['lands'])} for a in sorted(out.values(), key=lambda a: -a['requests'])][:12]


def _work_by(bid, app, bound, known, at, weeks=26):
    """The same weekly requests, split by the project or collection each chat is tied to."""
    if app is None:return None
    end = at.timestamp();start = end - weeks * 7 * 86400;chats = {b['id']: b for b in bound if b.get('kind') == 'chat'};rows = {}
    for r in app.preferences.get('usage_receipts', []):
        if r.get('business_id') != bid or not isinstance(r.get('at'), (int, float)) or not start <= r['at'] <= end:continue
        link = chats.get(r.get('chat_id'), {})
        key = ('project', link['project_refs'][0]) if link.get('project_refs') else ('land', link['collection_id']) if link.get('collection_id') in known else ('other', '')
        rows.setdefault(key, [0] * weeks)[min(weeks - 1, int((r['at'] - start) // (7 * 86400)))] += 1
    return [{'kind': k[0], 'id': k[1], 'weeks': v} for k, v in sorted(rows.items(), key=lambda kv: -sum(kv[1]))][:12]


def _effort(bid, app, bound, known, at):
    """This month's AI requests by the collection or project their chat is tied to, exactly as each app reported them."""
    if app is None:return None
    start = at.replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
    chats = {b['id']: b for b in bound if b.get('kind') == 'chat'}
    groups = {}
    for r in app.preferences.get('usage_receipts', []):
        if r.get('business_id') != bid or not isinstance(r.get('at'), (int, float)) or r['at'] < start:continue
        link = chats.get(r.get('chat_id'), {})
        key = ('land', link['collection_id']) if link.get('collection_id') in known else ('project', link['project_refs'][0]) if link.get('project_refs') else ('other', '')
        g = groups.setdefault(key, {'kind': key[0], 'id': key[1], 'requests': 0, 'tokens': 0, 'cost_usd': 0.0, 'missing_costs': 0})
        g['requests'] += 1;g['tokens'] += int(r.get('input_tokens') or 0) + int(r.get('output_tokens') or 0)
        if isinstance(r.get('cost_usd'), (int, float)):g['cost_usd'] += r['cost_usd']
        else:g['missing_costs'] += 1
    return sorted(groups.values(), key=lambda g: (-g['tokens'], -g['requests']))[:40]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--business-id', required=True);p.add_argument('--workspace', type=Path, default=workspace_root())
    a = p.parse_args()
    with workspace_scope(a.workspace):
        result = world(a.business_id)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    try:main()
    except (ValueError, OSError) as e:raise SystemExit(str(e))
