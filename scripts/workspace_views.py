"""Other ways to see saved work: map, chart and board data, place lookups, map imagery,
and a plain-language summary of what runs for a project or goal.

The interface draws these; the CLI and API return the same data, so harness users get
the same facts and can draw them with their own tools.
"""
import argparse
import json
import re
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from _common import workspace_root, workspace_scope, object_index, write_json_atomic, PRODUCT_ROOT
from workspace_startup import state_dir
import workspace_collections as collections
import workspace_projects as projects

AGENT = 'ViralTrac-AURA/{} (+https://github.com/deangeloscott/businessos)'
LOOKUP = 'https://nominatim.openstreetmap.org/search'
TILES = 'https://tile.openstreetmap.org/{}/{}/{}.png'
TILE_FRESH = 7 * 86400          # refresh viewed imagery weekly when online
TILE_KEEP = 20000               # roughly 300-400 MB of viewed imagery at most
MISSING_RETRY = 30 * 86400      # an address that couldn't be found is retried after a month
_lookup_lock, _tile_lock = threading.Lock(), threading.Lock()
_last_lookup, _tile_writes = [0.0], [0]


def _agent():
    try:return AGENT.format((PRODUCT_ROOT / 'VERSION').read_text(encoding='utf-8').strip())
    except OSError:return AGENT.format('local')


def _number(value, low, high):
    try:v = float(value)
    except (TypeError, ValueError):return None
    return v if low <= v <= high else None


def location(fields):
    """Latitude/longitude when a result has them, otherwise its address."""
    f = fields or {}
    lat = _number(next((f[k] for k in ('latitude', 'lat') if k in f), None), -90, 90)
    lng = _number(next((f[k] for k in ('longitude', 'lng', 'lon') if k in f), None), -180, 180)
    address = f.get('address')
    return (lat, lng) if lat is not None and lng is not None else None, address.strip() if isinstance(address, str) and address.strip() else ''


def area(fields):
    """A territory or service area saved as a GeoJSON Polygon/MultiPolygon in an `area` field: (geometry, centre)."""
    g = (fields or {}).get('area')
    if isinstance(g, dict) and g.get('type') == 'Feature':g = g.get('geometry')
    if not isinstance(g, dict) or g.get('type') not in {'Polygon', 'MultiPolygon'}:return None, None
    rings = g.get('coordinates') if g['type'] == 'Polygon' else [r for p in (g.get('coordinates') or []) if isinstance(p, list) for r in p]
    points = [p for ring in (rings or []) if isinstance(ring, list) for p in ring if isinstance(p, list) and len(p) >= 2]
    if not points or any(_number(p[0], -180, 180) is None or _number(p[1], -90, 90) is None for p in points):return None, None
    lngs, lats = [float(p[0]) for p in points], [float(p[1]) for p in points]
    return {'type': g['type'], 'coordinates': g['coordinates']}, ((min(lats) + max(lats)) / 2, (min(lngs) + max(lngs)) / 2)


def radius(fields):
    """Service radius in metres from `radius_km` or `radius_miles`."""
    f = fields or {}
    km = _number(f.get('radius_km'), 0, 20000)
    miles = _number(f.get('radius_miles'), 0, 12500)
    return km * 1000 if km else miles * 1609.344 if miles else None


def shapes(rows):
    """Which views suit these results: map (places), chart (numbers), board (a small set of statuses)."""
    numbers, groups, places = {}, {}, False
    for r in rows:
        f = r.get('fields') or {};position, address = location(f);places = places or bool(position or address or area(f)[0])
        for k, v in f.items():
            if k in {'latitude', 'longitude', 'lat', 'lng', 'lon', 'radius_km', 'radius_miles'}:continue
            if isinstance(v, (int, float)) and not isinstance(v, bool):numbers[k] = True
            elif isinstance(v, str) and 0 < len(v) <= 60 and k != 'address':groups.setdefault(k, set()).add(v)
    # A status or stage field is a pipeline from the first result; other fields need at least two groups to be worth a board.
    stage = lambda k: re.fullmatch(r'(status|stage|state|pipeline|phase)', k.lower()) is not None
    return {'map': places, 'chart': sorted(numbers), 'board': sorted(k for k, values in groups.items() if stage(k) or 2 <= len(values) <= 12)}


# --- Place lookups: an address becomes coordinates once, then it is remembered ---------------

def _cache_path():return state_dir() / 'place-lookups.json'


def _key(address):return re.sub(r'\s+', ' ', address).strip().casefold()


def _cache():
    try:
        data = json.loads(_cache_path().read_text(encoding='utf-8'))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):return {}


def remembered(address):
    hit = _cache().get(_key(address))
    if not hit:return None
    if hit.get('missing'):return False if time.time() - hit.get('at', 0) < MISSING_RETRY else None
    return hit['lat'], hit['lng']


def look_up(address):
    """OpenStreetMap's free lookup allows about one request a second; each address is asked once."""
    known = remembered(address)
    if known is not None:return known or None
    with _lookup_lock:
        wait = 1.1 - (time.monotonic() - _last_lookup[0])
        if wait > 0:time.sleep(wait)
        request = urllib.request.Request(LOOKUP + '?' + urllib.parse.urlencode({'format': 'jsonv2', 'limit': 1, 'q': address}), headers={'User-Agent': _agent()})
        try:
            with urllib.request.urlopen(request, timeout=10) as response:rows = json.loads(response.read().decode('utf-8'))
        finally:_last_lookup[0] = time.monotonic()
        cache = _cache()
        place = (float(rows[0]['lat']), float(rows[0]['lon'])) if rows else None
        cache[_key(address)] = {'lat': place[0], 'lng': place[1], 'at': time.time()} if place else {'missing': True, 'at': time.time()}
        write_json_atomic(_cache_path(), cache)
        return place


def rows(bid, ident, view='current', q=''):
    """Every result in a view with its full simple fields and position, for map, chart and board."""
    d = collections.read(bid, ident);out = [];unplaced = []
    for r in collections.select(d, view, q):
        fields = {k: (v if isinstance(v, (bool, int, float)) or v is None else str(v)[:500]) for k, v in (r.get('fields') or {}).items() if not isinstance(v, (dict, list))}
        place, address = location(r.get('fields'));shape, centre = area(r.get('fields'))
        row = {k: r.get(k) for k in ('id', 'title', 'display_state', 'hidden', 'saved', 'needs_review', 'changed_since_handled', 'disposition', 'first_seen')}
        row['fields'] = fields
        if r.get('trail'):row['trail'] = r['trail']
        if shape:row['area'] = shape
        if radius(r.get('fields')):row['radius_m'] = radius(r.get('fields'))
        if place:row.update(lat=place[0], lng=place[1], placed_by='result')
        elif centre:row.update(lat=centre[0], lng=centre[1], placed_by='area')
        elif address:
            known = remembered(address)
            if known:row.update(lat=known[0], lng=known[1], placed_by='address')
            elif known is None:row['address_pending'] = True
            else:unplaced.append({'id': r['id'], 'title': r['title'], 'reason': 'Address not found'})
        else:unplaced.append({'id': r['id'], 'title': r['title'], 'reason': 'No address or coordinates'})
        out.append(row)
    return {'id': d['id'], 'name': d['name'], 'items': out, 'unplaced': unplaced, 'pending': sum(1 for r in out if r.get('address_pending')),
            'updated': (d['checks'][-1]['at'] if d['checks'] else d.get('updated_at'))}


def place(bid, ident, view='current', q='', limit=10):
    """Look up a few unplaced addresses (about one a second). Call again while some remain."""
    wanted = (location(r.get('fields')) for r in collections.select(collections.read(bid, ident), view, q))
    pending = [a for a in dict.fromkeys(address for position, address in wanted if not position and address) if remembered(a) is None]
    found, stopped = 0, ''
    for address in pending[:max(1, min(20, int(limit)))]:
        try:found += bool(look_up(address))
        except (OSError, ValueError, KeyError):
            stopped = 'Finding addresses needs an internet connection. Saved places still show.';break
    return {'placed': found, 'remaining': sum(remembered(a) is None for a in pending), **({'stopped': stopped} if stopped else {})}


# --- Map imagery: viewed areas are kept so the map still shows offline -----------------------

def tile(z, x, y):
    """Return viewed map imagery, refreshing it weekly when online. Never downloads ahead."""
    z, x, y = int(z), int(x), int(y)
    if not 0 <= z <= 19 or not 0 <= x < 2 ** z or not 0 <= y < 2 ** z:raise ValueError('This map area is unavailable.')
    path = state_dir() / 'map-tiles' / str(z) / str(x) / f'{y}.png'
    if path.is_file() and time.time() - path.stat().st_mtime < TILE_FRESH:return path.read_bytes()
    try:
        with urllib.request.urlopen(urllib.request.Request(TILES.format(z, x, y), headers={'User-Agent': _agent()}), timeout=10) as response:data = response.read()
    except OSError:
        if path.is_file():return path.read_bytes()       # offline: keep showing what was viewed before
        raise ValueError('Map imagery for this area needs an internet connection.') from None
    path.parent.mkdir(parents=True, exist_ok=True);temporary = path.with_suffix('.tmp');temporary.write_bytes(data);temporary.replace(path)
    with _tile_lock:
        _tile_writes[0] += 1
        if _tile_writes[0] % 500 == 0:_trim(state_dir() / 'map-tiles')
    return data


def _trim(folder):
    files = sorted(folder.rglob('*.png'), key=lambda p: p.stat().st_mtime)
    for old in files[:max(0, len(files) - TILE_KEEP)]:old.unlink(missing_ok=True)


# --- What's running: plain facts from saved links, never a model summary ----------------------

def _clock(h, m):return datetime(2000, 1, 1, h, m).strftime('%I:%M %p').lstrip('0')


def cadence(raw):
    raw = str(raw or '').strip();upper = raw.upper();days = {'MO': 'Monday', 'TU': 'Tuesday', 'WE': 'Wednesday', 'TH': 'Thursday', 'FR': 'Friday', 'SA': 'Saturday', 'SU': 'Sunday'}
    freq = re.search(r'(?:^|[;:])FREQ=(\w+)', upper)
    if freq:
        rule=upper.removeprefix('RRULE:')
        parts=rule.split(';')
        if any(not re.fullmatch(r'(FREQ=(HOURLY|DAILY|WEEKLY|MONTHLY|YEARLY)|INTERVAL=[1-9]\d*|BYDAY=(MO|TU|WE|TH|FR|SA|SU)(,(MO|TU|WE|TH|FR|SA|SU))*|BYHOUR=([01]?\d|2[0-3])|BYMINUTE=[0-5]?\d)', part) for part in parts):return raw
        keys=[part.split('=')[0] for part in parts]
        if len(set(keys))!=len(keys) or ('BYMINUTE' in keys and 'BYHOUR' not in keys) or ('BYDAY' in keys and freq[1]!='WEEKLY'):return raw
        h, m = re.search(r'BYHOUR=(\d{1,2})', upper), re.search(r'BYMINUTE=(\d{1,2})', upper)
        at = f' at {_clock(int(h[1]), int(m[1]) if m else 0)}' if h and int(h[1]) < 24 else ''
        every = re.search(r'INTERVAL=(\d+)', upper);n = int(every[1]) if every else 1
        unit = {'HOURLY': 'hour', 'DAILY': 'day', 'WEEKLY': 'week', 'MONTHLY': 'month', 'YEARLY': 'year'}.get(freq[1], '')
        byday = re.search(r'BYDAY=([A-Z,]+)', upper)
        if byday and freq[1] == 'WEEKLY':
            names=', '.join(days.get(d,d) for d in byday[1].split(','))
            return (('Every ' + names) if n==1 else ('Every other ' + names) if n==2 else f'Every {n} weeks on {names}') + at
        return (f'Every {n} {unit}s' if n > 1 else f'Every {unit}') + at if unit else raw
    parts = raw.split()
    if len(parts) == 6 and parts[0] == '0':parts = parts[1:]
    if len(parts) == 5 and parts[0].isdigit() and parts[1].isdigit() and int(parts[1]) < 24 and int(parts[0]) < 60:
        at = ' at ' + _clock(int(parts[1]), int(parts[0]));names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if parts[2:] == ['*', '*', '*']:return 'Every day' + at
        if parts[2:4] == ['*', '*']:return ('Every weekday' if parts[4] == '1-5' else 'Every ' + ', '.join(names[int(d)] if d.isdigit() and int(d) < 8 else d for d in parts[4].split(','))) + at
        if parts[3:] == ['*', '*']:return f'Monthly on day {parts[2]}' + at
    match = re.fullmatch(r'every (\d+)\s*([mhd])', raw, re.I)
    if match:return f'Every {match[1]} ' + {'m': 'minutes', 'h': 'hours', 'd': 'days'}[match[2].lower()]
    return raw or 'On a schedule managed in its app'


def moment(value):
    if value in (None, ''):return None
    try:
        number = float(value);stamp = datetime.fromtimestamp(number / 1000 if number > 1e11 else number)
    except (TypeError, ValueError):
        try:stamp = datetime.fromisoformat(str(value).replace('Z', '+00:00')).astimezone().replace(tzinfo=None)
        except ValueError:return None
    days = (datetime.now().date() - stamp.date()).days
    day = 'today' if days == 0 else 'yesterday' if days == 1 else 'tomorrow' if days == -1 else stamp.strftime('%a %b ') + str(stamp.day)
    return f'{day} at {_clock(stamp.hour, stamp.minute)}'


def _health(task):
    status = str(task.get('status') or '').lower();last = moment(task.get('last_run'))
    if status in {'paused', 'disabled', 'stopped', 'cancelled', 'archived'}:return 'paused', 'Paused.'
    if str(task.get('last_status') or '').lower() in {'error', 'failed', 'failure'}:
        # An app's own error text can be machine output; show AURA's plain classification instead.
        from workspace_ui import setup_error, SETUP_ERRORS
        raw = str(task.get('last_error') or '').strip();known = setup_error(raw) if raw else ''
        reason = known if known and known != SETUP_ERRORS['unknown'] else f'Open it in {task.get("app") or "its app"} for details.'
        return 'failed', f'Last run failed{" " + last if last else ""}. {reason}'
    if last:return 'ok', f'Last ran {last}.'
    following = moment(task.get('next_run'))
    return 'waiting', f'Hasn\'t run yet{"; next run " + following if following else ""}.'


def running(app, bid, project_id='', goal_id='', collection_id=''):
    """What runs for a project, goal or collection, where its results go and whether it is working."""
    import workspace_schedules, workspace_goals
    if sum(map(bool, (project_id, goal_id, collection_id))) != 1:raise ValueError('Choose a project, a goal or a collection.')
    project = projects.find(bid, project_id) if project_id else None
    goal = workspace_goals.find(bid, goal_id) if goal_id else None
    watched = collections.read(bid, collection_id) if collection_id else None
    goal_links = app.preferences.get('goal_tasks', {}).get(bid, {}) if app else {}
    bindings = {v['id']: v for v in projects.load().get('bindings', {}).values() if v['business_id'] == bid and v['kind'] == 'task'}
    ids = []
    if watched:
        ids = [i for i, v in bindings.items() if v.get('collection_id') == watched['id']]
    elif project:
        ids = [r['id'] for r in project.get('members', []) if r['kind'] == 'task'] + [i for i, v in bindings.items() if project['id'] in v.get('project_refs', [])]
    else:
        ids = [t for t, g in goal_links.items() if g == goal['id']] + [i for i, v in bindings.items() if v.get('goal_ref') == goal['id']]
    tasks = {t['id']: t for t in workspace_schedules.inventory()['items']}
    goal_names = {}
    def goal_name(ident):
        if ident not in goal_names:
            try:goal_names[ident] = workspace_goals.find(bid, ident).get('name')
            except ValueError:goal_names[ident] = None
        return goal_names[ident]
    items = []
    for ident in dict.fromkeys(ids):
        task = tasks.get(ident)
        if not task:
            items.append({'id': ident, 'name': 'Scheduled task', 'available': False, 'health': 'missing', 'text': 'A linked scheduled task is no longer listed by its app.'})
            continue
        link = bindings.get(ident, {});collection = None
        if link.get('collection_id'):
            try:
                d = collections.read(bid, link['collection_id'])
                collection = {'id': d['id'], 'name': d['name'], 'waiting': len(collections.select(d, 'changes'))}
            except ValueError:collection = {'id': link['collection_id'], 'name': 'Saved results (unavailable)', 'waiting': 0}
        serves = goal_name(link.get('goal_ref') or goal_links.get(ident) or '') if (link.get('goal_ref') or goal_links.get(ident)) else None
        health, state = _health(task)
        sentence = f'{cadence(task.get("schedule"))}, {task.get("app") or "its app"} runs “{task.get("name")}”.'
        if collection and not watched:sentence += f' Results go to {collection["name"]}' + (f' ({collection["waiting"]} waiting for review).' if collection['waiting'] else '.')
        if serves and not goal:sentence += f' Working toward: {serves}.'
        items.append({'id': ident, 'name': task.get('name'), 'app': task.get('app'), 'schedule': cadence(task.get('schedule')), 'available': True,
                      'collection': collection, 'goal': serves, 'health': health, 'status': state, 'text': sentence + ' ' + state})
    goals = [] if goal or watched else [g for g in (goal_name(r['id']) for r in (project or {}).get('members', []) if r['kind'] == 'goal') if g]
    title = (project or goal or watched)['name']
    lines = [f'What’s running for {title}:'] + [f'- {i["text"]}' for i in items] if items else [f'Nothing is scheduled for {title} yet.']
    if goals:lines.append('Working toward: ' + '; '.join(goals) + '.')
    return {'name': title, 'items': items, 'goals': goals, 'attention': sum(i['health'] in {'failed', 'missing'} for i in items), 'text': '\n'.join(lines)}


# --- Deadlines: saved results whose deadline (expiry) is close -------------------------------

DONE = {'submitted', 'awarded', 'declined', 'won', 'lost', 'done', 'complete', 'completed', 'closed', 'cancelled', 'canceled', 'withdrawn', 'archived', 'paid'}
DEADLINE_WINDOW = 14 * 86400


def deadlines(bid, now=None, window=DEADLINE_WINDOW):
    """Current results with a deadline inside the window, soonest first. Handled, dismissed or finished ones are skipped."""
    from datetime import timezone
    now = datetime.now(timezone.utc) if now is None else now
    out = []
    for summary in collections.inventory(bid)['items']:
        if summary.get('unavailable') or summary.get('mode') != 'collection':continue
        try:d = collections.read(bid, summary['id'])
        except ValueError:continue
        for r in collections.select(d, 'current', at=now):
            due = collections.timestamp(r.get('expires_at'))
            status = next((str(v).strip().lower() for k, v in (r.get('fields') or {}).items() if k.lower() in {'status', 'stage', 'state', 'pipeline', 'phase'} and isinstance(v, str)), '')
            if not due or r.get('disposition') == 'acknowledged' or status in DONE:continue
            seconds = (due - now).total_seconds()
            if 0 < seconds <= window:
                out.append({'collection_id': d['id'], 'collection': d['name'], 'item_id': r['id'], 'title': r['title'], 'due': r['expires_at'], 'days': max(0, int(seconds // 86400))})
    return sorted(out, key=lambda x: x['due'])


# --- Goal progress: recorded measurements, with their source and date -------------------------

def goal_targets(objects):
    """For goals with a measure (native metric_refs plus a target number): the latest value and whether it is reached."""
    by_id = {o.get('id'): o for o in objects}
    latest = {}
    for o in objects:
        if o.get('object_type') == 'MetricObservation' and isinstance(o.get('value'), (int, float)) and not isinstance(o.get('value'), bool):
            if o.get('metric_ref') not in latest or o.get('window_end', '') > latest[o['metric_ref']].get('window_end', ''):latest[o['metric_ref']] = o
    out = {}
    for goal in objects:
        if goal.get('object_type') != 'Objective' or not goal.get('metric_refs'):continue
        target = (((goal.get('extensions') or {}).get('businessos') or {}).get('goal') or {}).get('target_value')
        metric = by_id.get(goal['metric_refs'][0])
        if not isinstance(target, (int, float)) or not metric:continue
        seen = latest.get(metric['id']);direction = metric.get('direction')
        value = seen['value'] if seen else None
        hit = value is not None and (value >= target if direction == 'higher_better' else value <= target if direction == 'lower_better' else False)
        out[goal['id']] = {'metric': metric.get('name'), 'unit': metric.get('unit', ''), 'direction': direction, 'target': target,
                           'latest': value, 'at': seen.get('window_end') if seen else None, 'reached': hit}
    return out


def progress(bid, goal_id, limit=60):
    """Measurements linked to a goal (its metric_refs, or MetricDefinition.objective_refs), oldest first."""
    index = object_index(bid);metrics = []
    goal = index.get(goal_id, (None,))[0] or {}
    linked = set(goal.get('metric_refs') or [])
    for obj, _ in index.values():
        if obj.get('object_type') == 'MetricDefinition' and (goal_id in obj.get('objective_refs', []) or obj['id'] in linked):
            points = sorted((o for o, _ in index.values() if o.get('object_type') == 'MetricObservation' and o.get('metric_ref') == obj['id']), key=lambda o: o.get('window_end', ''))
            metrics.append({'id': obj['id'], 'name': obj['name'], 'unit': obj.get('unit', ''), 'direction': obj.get('direction'),
                            'points': [{'at': o['window_end'], 'start': o.get('window_start'), 'value': o['value'], 'source': o.get('source_ref', '')}
                                       for o in points[-max(1, int(limit)):] if isinstance(o.get('value'), (int, float)) and not isinstance(o.get('value'), bool)]})
    return {'goal_id': goal_id, 'metrics': metrics, 'target': goal_targets([o for o, _ in index.values()]).get(goal_id)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['rows', 'place', 'running', 'progress'])
    p.add_argument('--business-id', required=True);p.add_argument('--workspace', type=Path, default=workspace_root())
    p.add_argument('--id', help='Collection ID for rows/place');p.add_argument('--project', default='');p.add_argument('--goal', default='');p.add_argument('--collection', default='')
    p.add_argument('--view', default='current');p.add_argument('--search', default='');p.add_argument('--limit', type=int, default=10)
    p.add_argument('--text', action='store_true', help='Print the running summary as plain text')
    a = p.parse_args()
    with workspace_scope(a.workspace):
        projects.check_business(a.business_id)
        if a.action == 'rows':result = rows(a.business_id, a.id, a.view, a.search)
        elif a.action == 'place':result = place(a.business_id, a.id, a.view, a.search, a.limit)
        elif a.action == 'progress':result = progress(a.business_id, a.goal)
        else:
            from workspace_ui import Workspace
            result = running(Workspace(), a.business_id, a.project, a.goal, a.collection)
            if a.text:print(result['text']);return
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    try:main()
    except (ValueError, OSError) as e:raise SystemExit(str(e))
