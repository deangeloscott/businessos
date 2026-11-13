"""A short, read-only picture of one organization: what is known, what changed, what needs someone.

The home page draws this; the CLI and API return the same data, so any AI app or custom view gets the
same facts in one step. It reads existing memory and adds nothing: no scores, no guesses, and counts
only of what was actually saved. Bounded on purpose: a few recent items of each kind, never whole
datasets. Open the record or collection itself for more.
"""
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from _common import workspace_root, workspace_scope, object_index
from workspace_lifecycle import archived
import workspace_collections as collections

# Every finding belongs to one operating area. Shown in this order, including areas with nothing yet.
AREAS = [('competitor-intelligence', 'Competitors'), ('customer-intelligence', 'Customers'), ('industry-intelligence', 'Industry'),
         ('seo-aeo', 'Search and AI answers'), ('content-synthesis', 'Content'), ('marketing-synthesis', 'Marketing'),
         ('customer-optimization', 'Customer growth'), ('funding-impact', 'Funding'), ('core', 'General')]
SEVERITY = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'informational': 0}
FRESH_DAYS = 30


def _time(value):
    try:return collections.timestamp(value)
    except ValueError:return None


def finding_label(status, due):
    """The same words the interface uses for a finding's status."""
    if status == 'contradicted':return 'challenged'
    if due:return 'needs_review'
    return {'supported': 'supported', 'active': 'supported', 'candidate': 'unverified', 'stale': 'out_of_date'}.get(status, 'unverified')


def _knowledge(objects, at):
    labels = dict.fromkeys(('supported', 'unverified', 'challenged', 'needs_review', 'out_of_date'), 0)
    areas = dict.fromkeys((key for key, _ in AREAS), 0)
    dated = fresh = total = 0
    for o in objects:
        if o.get('object_type') != 'Insight' or o.get('status') in {'superseded', 'archived'}:continue
        total += 1
        review = _time((((o.get('extensions') or {}).get('businessos')) or {}).get('review_after'))
        labels[finding_label(o.get('status'), bool(review and review <= at))] += 1
        if o.get('domain') in areas:areas[o['domain']] += 1
        reviewed = _time(o.get('reviewed_at'))
        if reviewed:
            dated += 1
            if at - reviewed <= timedelta(days=FRESH_DAYS):fresh += 1
    return {'findings': total, 'by_status': labels, 'by_area': [{'id': key, 'name': name, 'findings': areas[key]} for key, name in AREAS],
            # How current the findings are, only among those that record when they were last reviewed.
            'reviewed': {'with_date': dated, 'within_days': FRESH_DAYS, 'recent': fresh}}


def _attention(objects, limit):
    rows = [o for o in objects if o.get('object_type') == 'AttentionItem' and o.get('status') in {'open', 'acknowledged'}]
    rows.sort(key=lambda o: str(o.get('last_seen') or ''), reverse=True)
    rows.sort(key=lambda o: -SEVERITY.get(o.get('severity'), 0))
    return [{'id': o['id'], 'title': o.get('title', ''), 'reason': str(o.get('reason', ''))[:300], 'severity': o.get('severity'),
             'recommended_action': str(o.get('recommended_action') or '')[:300]} for o in rows[:limit]], len(rows)


def _goals(objects, limit):
    from workspace_views import goal_targets
    targets = goal_targets(objects);out = []
    for o in objects:
        if o.get('object_type') != 'Objective' or (o.get('status') or 'active') != 'active':continue
        info = ((o.get('extensions') or {}).get('businessos') or {}).get('goal') or {}
        if info.get('scope') == 'chat' or info.get('deleted_at'):continue
        row = {'id': o['id'], 'name': o.get('name', '')}
        measure = targets.get(o['id'])
        if measure:row.update({k: measure.get(k) for k in ('metric', 'unit', 'direction', 'target', 'latest', 'reached')})
        out.append(row)
    out.sort(key=lambda g: 'target' not in g)  # goals that track a number first
    return out[:limit], len(out)


def _watches(bid, at, days, limit, change_limit):
    """Collections kept current, most recently checked first, and what their recent checks changed."""
    since = at - timedelta(days=days);watches = [];changes = []
    for row in collections.inventory(bid)['items']:
        if row.get('unavailable'):continue
        try:d = collections.read(bid, row['id'])
        except ValueError:continue
        checks = [c for c in d['checks'] if isinstance(c.get('at'), str)]
        last = checks[-1] if checks else None
        watches.append({'id': d['id'], 'name': d['name'], 'kind': 'reports' if d['mode'] == 'series' else 'results', 'current': row['current_count'],
                        'last_checked': last['at'] if last else None, 'last_changes': int(last.get('change_count') or 0) if last else 0})
        for position, check in enumerate(checks):
            when = _time(check['at'])
            if not when or when < since:continue
            # Filling a collection for the first time is not a change; later checks are.
            if position == 0 and len(d['checks']) < 50:continue
            for change in check.get('changes') or []:
                changes.append({'kind': change.get('kind', 'changed'), 'title': change.get('title', ''), 'reason': str(change.get('reason', ''))[:300],
                                'at': check['at'], 'collection_id': d['id'], 'collection': d['name'], 'item_id': change.get('id')})
    watches.sort(key=lambda w: w['last_checked'] or '', reverse=True)
    changes.sort(key=lambda c: c['at'], reverse=True)
    return watches[:limit], len(watches), changes[:change_limit], len(changes)


def _challenged(objects, at, days, limit):
    """Findings that new evidence contradicted recently: the kind of change worth seeing first."""
    since = at - timedelta(days=days);rows = []
    for o in objects:
        when = _time(o.get('updated_at'))
        if o.get('object_type') == 'Insight' and o.get('status') == 'contradicted' and when and when >= since:
            rows.append({'kind': 'challenged', 'title': str(o.get('statement', ''))[:200], 'reason': 'New evidence challenges this finding.', 'at': o['updated_at'], 'record': o['id']})
    return sorted(rows, key=lambda r: r['at'], reverse=True)[:limit]


def _results(objects, limit):
    rows = [o for o in objects if o.get('object_type') == 'Asset' and not (((o.get('extensions') or {}).get('businessos')) or {}).get('collection')]
    rows.sort(key=lambda o: str(o.get('updated_at') or o.get('created_at') or ''), reverse=True)
    name = lambda o: str(o.get('business_role') or Path(str(o.get('location_reference') or '')).name or o.get('asset_type') or 'Saved result')[:160]
    return [{'id': o['id'], 'title': name(o), 'type': o.get('asset_type', ''), 'updated_at': o.get('updated_at') or o.get('created_at')} for o in rows[:limit]], len(rows)


def _agents(bid):
    """Named agents saved with the workspace. Reading them never starts one."""
    try:
        import workspace_storage
        saved = (workspace_storage.view_preferences(workspace_root()).get('assistants') or {}).get(bid) or []
    except (OSError, ValueError, TypeError, KeyError, ImportError):return []
    return [{'id': a.get('id'), 'name': a.get('name', ''), 'tasks': len(a.get('task_ids') or [])} for a in saved if isinstance(a, dict) and a.get('id') and not a.get('archived_at')][:12]


def summary(bid, at=None, days=7):
    """One bounded picture of the organization. `days` is how far back "what changed" looks."""
    import workspace_focus
    from workspace_views import deadlines
    at = at or datetime.now(timezone.utc);days = max(1, min(int(days), 90))
    objects = [o for o, _ in object_index(bid).values() if not archived(o)]
    business = next((o for o in objects if o.get('object_type') == 'Business'), None)
    if not business:raise ValueError('This business is unavailable in the selected workspace.')
    try:focus = [{'id': a['id'], 'name': a['name']} for a in workspace_focus.get(bid)['areas']]
    except ValueError:focus = []
    knowledge = _knowledge(objects, at)
    attention, attention_total = _attention(objects, 5)
    goals, goals_total = _goals(objects, 6)
    watches, watches_total, changes, changes_total = _watches(bid, at, days, 8, 8)
    changes = sorted(_challenged(objects, at, days, 4) + changes, key=lambda c: c['at'], reverse=True)[:8]
    results, results_total = _results(objects, 6)
    agents = _agents(bid)
    try:due = [{k: d[k] for k in ('collection_id', 'collection', 'item_id', 'title', 'due', 'days')} for d in deadlines(bid, now=at)][:5]
    except (OSError, ValueError):due = []
    example = (((business.get('extensions') or {}).get('businessos')) or {}).get('example')
    return {'business': {'id': bid, 'name': business.get('name', ''), 'description': str(business.get('description') or '')[:600],
                         # AURA's made-up example business says so wherever it is shown.
                         **({'example': True, 'example_built': example.get('built_at')} if isinstance(example, dict) else {})},
            'focus': focus, 'as_of': at.isoformat(timespec='seconds').replace('+00:00', 'Z'), 'changes_days': days,
            'knowledge': knowledge, 'changes': changes, 'attention': attention, 'deadlines': due, 'goals': goals,
            'watches': watches, 'results': results, 'agents': agents,
            'totals': {'findings': knowledge['findings'], 'changes': changes_total, 'attention': attention_total, 'goals': goals_total,
                       'watches': watches_total, 'results': results_total, 'agents': len(agents)},
            # Nothing saved beyond the organization itself: the home page shows first steps instead of empty tiles.
            'empty': not (knowledge['findings'] or goals_total or watches_total or results_total or attention_total)}


def text(s):
    """The same picture in plain words, for a morning brief or any AI app without the interface."""
    b = s['business'];k = s['knowledge'];lines = [b['name'] + (': ' + b['description'] if b['description'] else '')]
    if b.get('example'):lines.append("This is AURA's example business. Everything in it is made up.")
    if s['focus']:lines.append('Focus: ' + ', '.join(a['name'] for a in s['focus']))
    if s['empty']:
        lines.append('Nothing has been saved yet beyond the organization itself.')
        return '\n'.join(lines)
    by = k['by_status']
    if k['findings']:
        parts = [f"{by[key]} {label}" for key, label in (('supported', 'supported'), ('unverified', 'unverified'), ('challenged', 'challenged'), ('needs_review', 'due for review'), ('out_of_date', 'out of date')) if by[key]]
        lines.append(f"What we know: {k['findings']} finding{'' if k['findings'] == 1 else 's'} ({', '.join(parts)}).")
        known = [f"{a['name']} {a['findings']}" for a in k['by_area'] if a['findings']]
        if known:lines.append('By area: ' + ', '.join(known) + '.')
    if s['changes']:
        lines.append(f"Changed in the last {s['changes_days']} days:")
        lines += [f"- {c['title']} ({c['kind']}{', ' + c['collection'] if c.get('collection') else ''}): {c['reason']}" for c in s['changes']]
    else:lines.append(f"No recorded changes in the last {s['changes_days']} days.")
    if s['attention']:
        lines.append('Needs someone:')
        lines += [f"- {a['title']}: {a['reason']}" for a in s['attention']]
    if s['deadlines']:
        lines.append('Deadlines coming up:')
        lines += [f"- {d['title']} ({d['collection']}): due {d['due'][:10]}, {d['days']} days" for d in s['deadlines']]
    if s['goals']:
        lines.append('Goals:')
        for g in s['goals']:
            if 'target' in g:
                latest = 'no measurement yet' if g.get('latest') is None else f"{g['latest']:g}"
                joiner = ', target ' if g.get('direction') == 'lower_better' else ' of '
                lines.append(f"- {g['name']}: {latest}{joiner}{g['target']:g}" + (' (reached)' if g.get('reached') else ''))
            else:lines.append('- ' + g['name'])
    if s['watches']:
        lines.append('Kept current:')
        lines += [f"- {w['name']}: {w['current']} current, last checked {w['last_checked'][:10] if w['last_checked'] else 'never'}" for w in s['watches']]
    if s['agents']:lines.append('Agents: ' + ', '.join(a['name'] for a in s['agents']))
    lines.append('Counts are of saved records only. Open a record or collection for its evidence.')
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--business-id', required=True);p.add_argument('--workspace', type=Path, default=workspace_root())
    p.add_argument('--days', type=int, default=7, help='How far back "what changed" looks (1-90)')
    p.add_argument('--text', action='store_true', help='Print plain words instead of JSON')
    a = p.parse_args()
    with workspace_scope(a.workspace):
        result = summary(a.business_id, days=a.days)
    print(text(result) if a.text else json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    try:main()
    except (ValueError, OSError) as e:raise SystemExit(str(e))
