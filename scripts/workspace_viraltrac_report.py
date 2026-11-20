"""An optional, refreshable marketing snapshot using existing SourceRecords.

Only two read-only aggregate tools are replayed. Other tools remain available
through the ordinary proxy; saving a snapshot never replays arbitrary actions.
"""
import hashlib
import json
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone

from _common import object_index
import workspace_viraltrac as vt


def envelope(bid, tool, arguments, link):
    packet = vt.call(bid, 'tools/call', {'name': tool, 'arguments': arguments})
    if not isinstance(packet, dict):
        raise ValueError('ViralTrac returned an unrecognized report. Saved evidence was kept.')
    result = packet.get('result', {})
    if not isinstance(result, dict):
        raise ValueError('ViralTrac returned an unrecognized report. Saved evidence was kept.')
    if packet.get('error') or result.get('isError'):
        raise ValueError('ViralTrac could not return ' + tool + '. Check access and try again; saved evidence was kept.')
    value = result.get('structuredContent')
    if value is None:
        for item in result.get('content') if isinstance(result.get('content'), list) else []:
            if isinstance(item, dict) and item.get('type') == 'text':
                try: value = json.loads(item['text'])
                except (ValueError, KeyError): continue
                break
    actor = value.get('auth_context') if isinstance(value, dict) and isinstance(value.get('auth_context'), dict) else {}
    if isinstance(value, dict) and value.get('tool_name') == tool and value.get('ok') is True:
        value = value.get('envelope')
    if not isinstance(value, dict) or value.get('ok') is not True or value.get('tool') != tool:
        raise ValueError('ViralTrac returned an unrecognized report. Saved evidence was kept.')
    if (value.get('auth_context') if isinstance(value.get('auth_context'), dict) else {}).get('org_id') != link['organization_id']:
        raise ValueError('The report belongs to a different ViralTrac business. Saved evidence was kept.')
    return {**value, 'authorized_actor': actor}


def comparable(report):
    # Request IDs and retrieval freshness change on every read. Compare the
    # measurements, reporting window and qualifications, not those receipts.
    result = {name: {key: deepcopy(value.get(key)) for key in ('data', 'window_applied', 'coverage', 'reason_codes', 'diagnostic_flags')}
              for name, value in report.items()}
    readiness = result.get('readiness', {}).get('data')
    rows = readiness.get('readiness') if isinstance(readiness, dict) else None
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict): row.pop('last_checked_at', None)
        rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    return result


def saved_report(obj):
    if not obj or obj.get('object_type') != 'SourceRecord':
        return None
    value = (obj.get('extensions') or {}).get('viraltrac_report')
    if not isinstance(value, dict) or not isinstance(value.get('arguments'), dict) or not isinstance(value.get('report'), dict):
        return None
    if not all(isinstance(value['report'].get(key), dict) for key in ('performance', 'readiness')):
        return None
    if not all(isinstance(value['arguments'].get(key), str) for key in ('start_date', 'end_date')):
        return None
    return value


def reports(bid):
    return [{'id': obj['id'], 'retrieved_at': obj['retrieved_at'],
             'period': saved_report(obj)['arguments']}
            for obj, _ in object_index(bid).values()
            if saved_report(obj)]


def report(bid, start=None, end=None, save=False, source=None):
    if any(value is not None and not isinstance(value, str) for value in (start, end, source)):
        raise ValueError('Use dates in YYYY-MM-DD format and a saved report ID when refreshing.')
    link, _ = vt.credentials(bid)
    previous = None
    if source:
        obj = object_index(bid).get(source, (None,))[0]
        previous = saved_report(obj)
        if not previous:
            raise ValueError('Choose a saved ViralTrac report from this AURA business.')
        if any(previous.get(key) != link.get(key) for key in ('organization_id', 'api_origin')):
            raise ValueError('This report belongs to the previous connection. Reconnect that business to refresh it.')
        start, end = previous['arguments']['start_date'], previous['arguments']['end_date']
    try:
        end = date.today().isoformat() if end is None else date.fromisoformat(end).isoformat()
        start = (date.fromisoformat(end) - timedelta(days=30)).isoformat() if start is None else date.fromisoformat(start).isoformat()
    except (ValueError, OverflowError):
        raise ValueError('Use valid reporting dates in YYYY-MM-DD format.') from None
    if start > end:
        raise ValueError('The reporting start must be on or before its end.')
    arguments = {'start_date': start, 'end_date': end}
    if save and not source:
        for obj, _ in object_index(bid).values():
            saved = saved_report(obj)
            if saved and saved.get('arguments') == arguments and all(saved.get(k) == link[k] for k in ('organization_id', 'api_origin')):
                return report(bid, source=obj['id'])
    data = {'performance': envelope(bid, 'performance_summary', arguments, link),
            'readiness': envelope(bid, 'integration_readiness', {}, link)}
    if vt.association(bid) != link:
        raise ValueError('The connection changed while reading this report. Retry with the intended business.')
    # A failed upstream is not a replacement for previously useful evidence.
    if any(value.get('coverage') == 'degraded' for value in data.values()):
        return {'status': 'unavailable', 'report': data, 'source_id': source,
                'message': 'A source is temporarily unavailable. Saved evidence was kept; retry later.'}
    payload = {**link, 'arguments': arguments, 'report': data}
    if len(json.dumps(payload).encode()) > 256 * 1024:
        raise ValueError('This summary is too large to save as durable knowledge. Request narrower evidence through your AI app.')
    before = comparable(previous['report']) if previous else None
    after = comparable(data)
    changed = before is not None and before != after
    result = {'status': 'changed' if changed else 'unchanged' if previous else 'ready',
              'report': data, 'source_id': source, 'period': arguments,
              'comparison': {'before': before, 'after': after} if changed else None}
    if save or source:
        from remember import remember
        encoded = json.dumps(data, sort_keys=True, ensure_ascii=False)
        content = {'source_type': 'viraltrac_report', 'source_reference': link['api_origin'] + '/mcp#performance_summary',
                   'origin': link['api_origin'], 'retrieved_at': datetime.now(timezone.utc).isoformat(),
                   'access_class': 'restricted', 'access_scope': 'ViralTrac organization ' + link['organization_id'] + '; saved in this AURA workspace',
                   'content_hash': hashlib.sha256(encoded.encode()).hexdigest(),
                   'extensions': {'viraltrac_report': payload}}
        item = {'object_ref': source} if source else {'object_type': 'SourceRecord'}
        item['content'] = content
        if changed: item['correction_summary'] = 'ViralTrac restated the saved reporting period or its coverage. Review dependent conclusions.'
        receipt = remember(bid, {'objects': [item]})
        result['source_id'] = receipt['objects'][0]['id']
        result['saved'] = True
    return result
