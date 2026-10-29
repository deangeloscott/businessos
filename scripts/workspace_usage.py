"""Small, local usage receipts. Native accounts remain the quota/billing authority."""
from datetime import datetime, timezone
import math
import time
import hashlib
import json
import subprocess
from urllib.request import Request, build_opener, HTTPRedirectHandler


FIELDS = ('input_tokens', 'output_tokens', 'cached_input_tokens', 'cache_write_tokens')
MAX_CACHE_CHATS = 5  # Main chat plus four recent chats.


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0 else None


def timestamp(value):
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()
        except ValueError:
            return None
    value = number(value)
    return value / 1000 if value and value > 1e11 else value


def measure(raw, kind='', at=None):
    """Normalize reported fields; missing is never interpreted as zero."""
    if not isinstance(raw, dict) or not raw:
        return {}
    details = raw.get('input_tokens_details') or raw.get('prompt_tokens_details') or {}
    if not isinstance(details, dict):details={}
    read = number(raw.get('cached_input_tokens', raw.get('cache_read_input_tokens', raw.get('cacheRead', raw.get('cachedContentTokenCount',raw.get('total_cached_tokens',details.get('cached_tokens')))))))
    write = number(raw.get('cache_write_tokens', raw.get('cache_creation_input_tokens', raw.get('cacheWrite', details.get('cache_write_tokens')))))
    inp = number(raw.get('input_tokens', raw.get('prompt_tokens', raw.get('input'))))
    # Pi/OMP and Anthropic report ordinary input separately from cached input.
    if inp is not None and (kind in {'pi', 'omp', 'claude'} and 'prompt_tokens' not in raw):
        inp += (read or 0) + (write or 0)
    result = {k:v for k,v in dict(input_tokens=inp, output_tokens=number(raw.get('output_tokens', raw.get('completion_tokens', raw.get('output')))),
              cached_input_tokens=read, cache_write_tokens=write).items() if v is not None}
    cost = raw.get('cost')
    if isinstance(cost, dict) and number(cost.get('total')) is not None:
        result.update(cost_usd=cost['total'], cost_kind='est')
    elif number(cost) is not None and 'prompt_tokens' in raw:
        # Only the documented OpenRouter response field is treated as charged cost.
        result.update(cost_usd=cost, cost_kind='reported' if kind == 'openrouter' else 'est')
    if number(raw.get('total_cost_usd')) is not None:
        result.update(session_cost_usd=raw['total_cost_usd'], cost_kind='est')
    if result and (kind=='openrouter' or raw.get('_provider')=='openrouter'):
        result['billing']='api'
    if result:
        result['at'] = timestamp(at)
        cache = cache_observation(raw, at)
        if cache:result['cache'] = cache
    return result


def combine(rows):
    result = {}
    for field in (*FIELDS, 'cost_usd'):
        values = [r[field] for r in rows if number(r.get(field)) is not None]
        if values:
            result[field] = sum(values)
    if 'cost_usd' in result:
        result['cost_kind'] = 'est' if any(r.get('cost_kind') == 'est' for r in rows if 'cost_usd' in r) else 'reported'
    if rows and all(r.get('billing')=='api' for r in rows):result['billing']='api'
    return result


def message_id(message):
    if message.get('id'):
        return message['id']
    # Pi/OMP messages may omit IDs. A native timestamp plus content identifies a replay.
    if message.get('timestamp') or message.get('created_at'):
        payload=[message.get('timestamp') or message.get('created_at'),message.get('content')]
        return hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    return None


def messages_usage(messages, kind, window=None):
    rows, seen, started = [], {}, None
    policy, policy_model = None, None
    for m in messages:
        if m.get('role') in {'user','tool','toolResult'}:started=m.get('timestamp') or m.get('created_at')
        if m.get('role') != 'assistant' or not isinstance(m.get('usage'), dict):
            continue
        ident = message_id(m)
        row = measure({**m['usage'],'_provider':m.get('provider'),'_cache_started_at':started}, kind, m.get('timestamp') or m.get('created_at'))
        if kind=='claude':
            if row.get('cache'):
                policy,policy_model=row['cache'],m.get('model')
            elif (policy and policy_model and policy_model==m.get('model') and
                  row.get('cached_input_tokens',0)>0 and policy.get('refresh_seconds') and timestamp(started)):
                row['cache']={**policy,'expires_at':timestamp(started)+policy['refresh_seconds'],'observed_at':timestamp(started)}
            else:
                policy,policy_model=None,None
        if row:
            if ident and ident in seen:rows[seen[ident]]={**rows[seen[ident]],**row}
            else:
                if ident:seen[ident]=len(rows)
                rows.append(row)
    result = combine(rows)
    if rows:
        result['last'] = rows[-1]
        if rows[-1].get('cache'):result['cache']=rows[-1]['cache']
        hits=[r for r in rows if r.get('cached_input_tokens',0)>0]
        if hits:result['cache_hit']={'at':hits[-1].get('at'),'tokens':hits[-1]['cached_input_tokens']}
        used = sum(rows[-1].get(k, 0) for k in ('input_tokens', 'output_tokens'))
        if number(window) and used:
            result['context'] = {'tokens':used, 'window':window, 'est':True}
    return result


def remember(preferences, chat_id, usage, scope='request'):
    snapshots = preferences.setdefault('usage_chats', {})
    prior = snapshots.get(chat_id, {})
    if scope == 'session':
        if usage:
            snapshots[chat_id] = {**{k:prior[k] for k in ('session_cost_usd','cost_usd','cost_kind','cache_hit') if k in prior}, **usage, 'session':True}
    else:
        snapshot = combine([prior, usage])
        snapshot['last'] = usage.get('last') or usage
        if usage.get('cache') or snapshot['last'].get('cache'):
            snapshot['cache']=usage.get('cache') or snapshot['last']['cache']
        # Never extend an unobserved cache window, or carry it through a cache miss.
        if usage.get('context'):
            snapshot['context'] = usage['context']
        elif prior.get('context'):
            snapshot['context'] = prior['context']
        if 'session_cost_usd' in usage:
            snapshot['session_cost_usd'] = usage['session_cost_usd']
            snapshot['cost_usd'] = usage['session_cost_usd']
            snapshot['cost_kind'] = usage.get('cost_kind', 'est')
        last=usage.get('last') or usage
        if last.get('cached_input_tokens',0)>0:
            snapshot['cache_hit']={'at':last.get('at'),'tokens':last['cached_input_tokens']}
        elif usage.get('cache_hit') or prior.get('cache_hit'):
            snapshot['cache_hit']=usage.get('cache_hit') or prior['cache_hit']
        snapshots[chat_id] = snapshot
    return prior


def record(preferences, job, chat, agent):
    usage = dict(job.get('usage') or {})
    if not chat:
        return
    rows = preferences.setdefault('usage_receipts', [])
    if any(r.get('id') == job['id'] for r in rows):
        return
    # A cumulative session cost becomes a request cost only with a known baseline.
    previous = preferences.get('usage_chats', {}).get(chat['id'], {})
    if job.get('keep_warm') and chat.get('agent')=='claude' and not usage.get('cache'):
        policy=previous.get('cache') or previous.get('last',{}).get('cache') or {}
        last=usage.get('last') or usage
        ttl=number(policy.get('refresh_seconds'))
        if ttl and last.get('cached_input_tokens',0)>0:
            usage['cache']={**policy,'expires_at':job['created']+ttl,'observed_at':job['created']}
    if 'session_cost_usd' in usage:
        old = previous.get('session_cost_usd')
        if old is None and job.get('new_native_chat'):
            old = 0
        if number(old) is not None and usage['session_cost_usd'] >= old:
            usage['cost_usd'] = usage['session_cost_usd'] - old
    remember(preferences, chat['id'], usage)
    row = {k:usage[k] for k in (*FIELDS, 'cost_usd', 'cost_kind', 'billing') if k in usage}
    rows.append(dict(row, id=job['id'], chat_id=chat['id'], business_id=job['business_id'],
                     at=job['updated'], agent=agent, model=chat.get('model', '')))
    if len(rows) > 10000:
        preferences['usage_receipts'] = rows[-10000:]
        preferences['usage_history_limited'] = True


def summary(preferences, business, chat_id, period='chat', now=None, offset=0, since=None):
    now = now or time.time()
    offset = max(-840, min(840, int(offset))) * 60
    local = datetime.fromtimestamp(now - offset, timezone.utc)
    start = local.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == 'month':
        start = start.replace(day=1)
    start = start.timestamp() + offset
    if since is not None:
        start=float(since)
        if not math.isfinite(start) or start>now+60 or start<now-33*86400:
            raise ValueError('Refresh the usage period.')
    rows = [r for r in preferences.get('usage_receipts', []) if r.get('business_id') == business and
            ((r.get('chat_id') == chat_id) if period == 'chat' else r.get('at', 0) >= start)]
    totals = combine(rows)
    costs = [r for r in rows if number(r.get('cost_usd')) is not None]
    chat = preferences.get('usage_chats', {}).get(chat_id, {})
    if period == 'chat' and chat:
        totals = {k:chat[k] for k in (*FIELDS, 'cost_usd', 'cost_kind') if k in chat}
    groups = []
    for name in dict.fromkeys(r.get('agent', '') for r in rows):
        items = [r for r in rows if r.get('agent', '') == name]
        groups.append({'name':name, **combine(items), 'requests':len(items),
                       'missing_costs':sum('cost_usd' not in r for r in items)})
    return {'period':period, 'totals':totals, 'requests':len(rows), 'missing_costs':len(rows)-len(costs),
            'groups':groups, 'chat':chat, 'budget_costs':combine([r for r in rows if r.get('billing')=='api' or r.get('cost_kind')=='reported']),
            'limited':bool(preferences.get('usage_history_limited'))}


def chat_views(preferences, business, running_id=None):
    """Usage-only selection; never switch the user's native chat or connection."""
    snapshots = preferences.get('usage_chats', {})
    active = preferences.get('active_chats', {}).get(business)
    chats = [c for c in preferences.get('chats', []) if c.get('business_id') == business]
    chats.sort(key=lambda c: (c['id'] == running_id, c['id'] == active,
                             timestamp(c.get('updated')) or timestamp(c.get('created')) or 0), reverse=True)
    return [dict(info={k:c[k] for k in ('id','title','agent','model','effort','status','updated') if k in c},
                 usage=snapshots.get(c['id'], {}),
                 position='Running' if c['id'] == running_id else 'Selected' if c['id'] == active else 'Recent')
            for c in chats[:MAX_CACHE_CHATS]]


def cache_window(chat, snapshot):
    """Reported policy first; a labeled reference model is never stored as provider fact."""
    last=snapshot.get('last') or {}
    native=snapshot.get('cache') or last.get('cache')
    if native:return native
    # A reported miss supersedes an earlier hit. Unknown is not a new hit.
    if not (number(last.get('cached_input_tokens')) or 0)>0:return None
    hit=timestamp(snapshot.get('cache_hit',{}).get('at'))
    if not hit and last.get('cached_input_tokens',0)>0:hit=timestamp(last.get('at'))
    if not hit:return None
    model=str(chat.get('model','')).lower().rsplit('/',1)[-1].rsplit(':',1)[-1]
    if model.startswith(('gpt-','o1','o3','o4')) or chat.get('agent')=='codex':
        basis='5m reference based on earlier OpenAI in-memory guidance. This connection’s actual retention may differ; newer API policies can be longer.'
    elif model.startswith('gemini-'):
        basis='5m working assumption after observed reuse. Google publishes no fixed implicit-cache lifetime; this is not its explicit-cache TTL.'
    else:return None
    return {'expires_at':hit+300,'observed_at':hit,'est':True,'modeled':True,
            'source':'Reference estimate','basis':basis}


def can_keep_warm(chat, snapshot, connection, kind, now=None):
    cache = cache_window(chat or {}, snapshot) or {}
    expiry = timestamp(cache.get('expires_at'))
    # One manual attempt in the same native conversation, never a provider guarantee.
    model=str((chat or {}).get('model','')).lower().rsplit('/',1)[-1].rsplit(':',1)[-1]
    return bool(chat and chat.get('agent') == kind and kind in {'codex','claude','pi','omp','hermes','antigravity'} and chat.get('native_id') and
                chat.get('status') == 'complete' and chat.get('model') == connection.get('model') and
                chat.get('effort', '') == connection.get('effort', '') and
                (cache.get('modeled') or cache.get('refresh_seconds') in {300,3600}) and
                not model.startswith('gemini-4') and
                expiry and expiry > (now or time.time()))


def codex_limits(raw):
    buckets = raw.get('rateLimitsByLimitId')
    buckets = list(buckets.values()) if isinstance(buckets, dict) and buckets else [raw.get('rateLimits') or {}]
    windows = []
    for bucket in buckets:
        if not isinstance(bucket, dict):
            continue
        for key in ('primary', 'secondary'):
            w = bucket.get(key)
            if not isinstance(w, dict) or number(w.get('usedPercent')) is None:
                continue
            minutes = number(w.get('windowDurationMins'))
            name = (f'{minutes / 60:g}h' if minutes and minutes < 1440 else f'{minutes / 1440:g}d' if minutes else 'Usage')
            windows.append({'name':name, 'bucket':str(bucket.get('limitName') or bucket.get('limitId') or 'Codex')[:80],
                            'used_percent':min(100, w['usedPercent']), 'resets_at':timestamp(w.get('resetsAt'))})
    return windows


def claude_limits(raw):
    if not isinstance(raw, dict):
        return []
    result = {'name':str(raw.get('rateLimitType') or 'Plan usage')[:80], 'status':str(raw.get('status') or '')[:40],
              'resets_at':timestamp(raw.get('resetsAt'))}
    value = number(raw.get('utilization'))
    if value is not None:
        result['used_percent'] = min(100, value * 100)
    return [result] if result['status'] or value is not None else []


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('The provider usage address changed. Check your provider.')


def openrouter_limits(key):
    request = Request('https://openrouter.ai/api/v1/key', headers={'Authorization':'Bearer '+key})
    with build_opener(NoRedirect).open(request, timeout=10) as response:
        data = json.loads(response.read(1024 * 1024))['data']
    result = account('openrouter',hashlib.sha256(key.encode()).hexdigest(),via='API connection',mode='api',scope='key') | {
            'provider':'openrouter', 'mode':'api', 'scope':'key', 'via':['API connection'],
            'label':'Key '+hashlib.sha256(key.encode()).hexdigest()[:6],
            'source':'API key', 'checked_at':time.time(), 'windows':[],
            'key_limit_remaining_usd':number(data.get('limit_remaining')),
            'spend_month_usd':number(data.get('usage_monthly')), 'period_note':'Provider month (UTC)',
            'spend_today_usd':number(data.get('usage_daily')), 'spend_total_usd':number(data.get('usage'))}
    # These are the key's totals, including requests made outside AURA.
    try:
        request=Request('https://openrouter.ai/api/v1/credits',headers={'Authorization':'Bearer '+key})
        with build_opener(NoRedirect).open(request,timeout=10) as response:
            credits=json.loads(response.read(1024*1024))['data']
        paid,spent=number(credits.get('total_credits')),number(credits.get('total_usage'))
        if paid is not None and spent is not None:result['balance_usd']=max(0,paid-spent)
        if spent is not None:result['account_spend_total_usd']=spent
    except (ValueError,OSError,KeyError):pass
    return result


PROVIDERS = {'openai-codex':'openai', 'codex':'openai', 'claude':'anthropic',
             'google-antigravity':'google', 'antigravity':'google', 'google-gemini-cli':'google'}
NAMES = {'openai':'OpenAI', 'anthropic':'Anthropic', 'google':'Google', 'openrouter':'OpenRouter', 'xai':'xAI',
         'kie':'Kie AI','fal':'fal.ai','higgsfield':'Higgsfield','elevenlabs':'ElevenLabs'}


def account(provider, identity=None, email='', plan='', via='', mode='subscription', scope='account'):
    provider = PROVIDERS.get(provider, provider)
    # Opaque native account IDs are preferred. Emails never merge different workspaces.
    identity = str(identity or '').strip()
    ident = hashlib.sha256(f'{provider}|{mode}|{scope}|{identity or via+email}'.encode()).hexdigest()[:24]
    label = (email.split('@')[0][:4]+'…@'+email.split('@')[-1]) if '@' in email else 'Account '+ident[:6] if identity else 'Account unknown'
    return {'id':ident, 'provider':provider, 'name':NAMES.get(provider,provider), 'mode':mode, 'scope':scope,
            'label':label, 'identified':bool(identity), 'plan':str(plan or '')[:40], 'via':[via] if via else [],
            'windows':[], 'checked_at':None}


def codex_account(raw, limits=None, activity=None):
    native=raw.get('account') or {}
    routing=raw.get('workspaceRouting') or {}
    if native.get('type') not in {'chatgpt','chatgptAuthTokens'}:return None
    result=account('openai',native.get('accountId') or routing.get('chatgptAccountId'),native.get('email') or '',native.get('planType'), 'Codex')
    result.update(windows=codex_limits(limits or {}), checked_at=time.time())
    if activity:
        summary=activity.get('summary') or {}
        result['lifetime_tokens']=number(summary.get('lifetimeTokens'))
    return result


def service_account(provider, name, key):
    row=account(provider,hashlib.sha256(key.encode()).hexdigest(),via='API connection',mode='api',scope='key')
    row.update(name=name,label='Key '+hashlib.sha256(key.encode()).hexdigest()[:6])
    def read(url,headers):
        with build_opener(NoRedirect).open(Request(url,headers=headers),timeout=10) as response:
            return json.loads(response.read(1024*1024))
    if provider not in {'kie','elevenlabs'}:return row
    try:
        if provider=='kie':
            raw=read('https://api.kie.ai/api/v1/chat/credit',{'Authorization':'Bearer '+key})
            if raw.get('code')!=200:raise ValueError('Usage unavailable')
            row['credits_remaining']=number(raw.get('data'))
        else:
            raw=read('https://api.elevenlabs.io/v1/user/subscription',{'xi-api-key':key})
            used,limit=number(raw.get('character_count')),number(raw.get('character_limit'))
            if used is not None and limit is not None:
                row['units_remaining']=max(0,limit-used);row['units_name']='characters'
                if limit:row['windows']=[{'name':'Characters','used_percent':min(100,100*used/limit),'resets_at':timestamp(raw.get('next_character_count_reset_unix'))}]
            row['plan']=str(raw.get('tier') or '')[:40]
        row['checked_at']=time.time()
    except (ValueError,OSError,KeyError):row['note']='Usage unavailable'
    return row


def omp_accounts(raw):
    accounts=[]
    for i,report in enumerate(raw.get('reports') or []):
        provider=report.get('provider') or 'other'
        meta=report.get('metadata') or {}
        mode='api' if provider in {'openrouter','openai','xai'} else 'subscription'
        result=account(provider,meta.get('accountId') or meta.get('orgId') or meta.get('credentialId'),
                       meta.get('email') or '',meta.get('planType'), 'OMP',mode)
        if not result['identified']:
            # Distinct unknown credentials stay distinct; never match by a masked email.
            result['id']=hashlib.sha256((result['id']+str(i)).encode()).hexdigest()[:24]
        result['checked_at']=timestamp(report.get('fetchedAt'))
        if meta.get('orgName'):result['organization']=str(meta['orgName'])[:80]
        for limit in report.get('limits') or []:
            amount=limit.get('amount') or {};window=limit.get('window') or {};scope=limit.get('scope') or {}
            if amount.get('unit')=='percent':
                value=number(amount.get('used'))
            elif number(amount.get('usedFraction')) is not None:value=amount['usedFraction']*100
            else:value=None
            if value is not None:
                result['windows'].append({'name':str(window.get('label') or limit.get('label') or 'Usage')[:80],
                    'bucket':str(scope.get('meter') or scope.get('model') or 'account')[:80],
                    'duration':number(window.get('durationMs')), 'used_percent':min(100,value),
                    'resets_at':timestamp(window.get('resetsAt'))})
            elif amount.get('unit') in {'usd','USD','dollars'}:
                field='spend_month_usd' if window.get('durationMs') and 27*86400000<=window['durationMs']<=32*86400000 else 'spend_total_usd' if not window else None
                if field:result[field]=number(amount.get('used'))
                result['balance_usd']=number(amount.get('remaining'))
        if report.get('error'):result['note']='Couldn’t refresh this account.'
        accounts.append(result)
    for i,row in enumerate(raw.get('accountsWithoutUsage') or []):
        if not isinstance(row,dict):continue
        meta=row.get('metadata') or row
        provider=row.get('provider') or 'other'
        mode='api' if provider in {'openrouter','openai','xai'} else 'subscription'
        result=account(provider,meta.get('accountId') or meta.get('credentialId'),meta.get('email') or '',via='OMP',mode=mode)
        if not result['identified']:result['id']+='-'+str(i)
        result['note']='Limits not reported'
        accounts.append(result)
    return accounts


def hermes_accounts(raw):
    # Hermes exposes its provider's AccountUsageSnapshot dataclass as JSON.
    raw=raw.get('snapshot',raw)
    if not isinstance(raw,dict) or not raw.get('provider'):return []
    provider=raw['provider'];mode='api' if provider=='openrouter' else 'subscription'
    result=account(provider,raw.get('identity'),plan=raw.get('plan'),via='Hermes',mode=mode)
    result['checked_at']=timestamp(raw.get('fetched_at'))
    for w in raw.get('windows') or []:
        result['windows'].append({'name':str(w.get('label') or 'Usage')[:80], 'bucket':w.get('scope','account'),
            'used_percent':number(w.get('used_percent')), 'resets_at':timestamp(w.get('resets_at',w.get('reset_at')))})
    # Preserve structured provider values, never parse dollar amounts out of prose.
    native=raw.get('raw') or {}
    if provider=='openrouter':
        data=native.get('data',native)
        for native_field,field in [('usage_monthly','spend_month_usd'),('usage_daily','spend_today_usd'),('limit_remaining','key_limit_remaining_usd')]:
            if number(data.get(native_field)) is not None:result[field]=data[native_field]
        result['scope']='key'
        import re
        for line in raw.get('details') or []:
            match=re.fullmatch(r'Credits balance: \$([0-9]+(?:\.[0-9]+)?)',str(line))
            if match:result['balance_usd']=float(match[1])
    if raw.get('unavailable_reason'):result['note']='Limits not reported'
    return [result]


def merge_accounts(rows):
    """One snapshot per confirmed identity. Never add overlapping native/account totals."""
    result={}
    for row in rows:
        key=row['id'];prior=result.get(key)
        if not prior:result[key]=dict(row);continue
        newer,older=(row,prior) if (row.get('checked_at') or 0)>=(prior.get('checked_at') or 0) else (prior,row)
        merged={**older,**{k:v for k,v in newer.items() if v is not None}}
        merged['via']=list(dict.fromkeys(prior.get('via',[])+row.get('via',[])))
        # Keep the provider's latest entire quota snapshot; don't union slightly different reset times.
        if not newer.get('windows'):merged['windows']=older.get('windows',[])
        if not newer.get('windows') and older.get('windows'):merged['limits_at']=older.get('limits_at') or older.get('checked_at')
        result[key]=merged
    return sorted(result.values(),key=lambda a:(a['name'],a.get('mode',''),a.get('label',''),a['id']))


def remember_accounts(preferences, rows):
    history=preferences.setdefault('usage_account_history',{})
    current=merge_accounts(rows)
    seen={r['id'] for r in current}
    for row in current:
        if not row.get('identified'):continue
        old=history.get(row['id'])
        history[row['id']]=merge_accounts([old,row] if old else [row])[0]
    # An inactive account remains a dated snapshot. Refresh never signs in or rotates accounts.
    return [
        {**r,'available':r['id'] in seen} for r in merge_accounts([*history.values(),*current])]


def linked_accounts(preferences, rows):
    known={**preferences.get('usage_account_history',{}),**{r['id']:r for r in rows if r.get('identified')}}
    result=[]
    for row in rows:
        target=known.get(preferences.get('usage_account_links',{}).get(row['id']))
        if target and row.get('linkable') and not row.get('identified') and all(row.get(k)==target.get(k) for k in ('provider','mode','scope')):
            row={**row,'id':target['id'],'label':target['label'],'identified':True}
        result.append(row)
    return result


def link_account(preferences, rows, source, target):
    if not isinstance(source,str) or not isinstance(target,str):raise ValueError('Choose a matching account.')
    links=preferences.setdefault('usage_account_links',{})
    if not target:
        previous=links.pop(source,None)
        if previous:
            native=[r for r in rows if r['id']==previous and r.get('identified')]
            if native:preferences.setdefault('usage_account_history',{})[previous]=merge_accounts(native)[0]
        return
    src=next((r for r in rows if r['id']==source and r.get('linkable') and not r.get('identified')),None)
    dst=next((r for r in rows if r['id']==target and r.get('identified')),None) or preferences.get('usage_account_history',{}).get(target)
    if not src or not dst or src.get('mode')!='subscription' or not all(src.get(k)==dst.get(k) for k in ('provider','mode','scope')):
        raise ValueError('Choose a matching subscription account.')
    links[source]=target


def native_accounts(command, kind, cwd, env):
    """Help-gated metadata commands only. No auth export, resets, prompts or shell."""
    from workspace_agents import base_command
    base=base_command(command)
    flags={'creationflags':subprocess.CREATE_NO_WINDOW} if __import__('os').name=='nt' else {}
    def read(args):
        p=subprocess.run([*base,*args],cwd=cwd,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,
                         encoding='utf-8',errors='replace',timeout=25,**flags)
        if p.returncode:raise ValueError('Native usage unavailable')
        return p.stdout
    help_text=read(['--help'])
    import re
    if kind=='claude':
        if not re.search(r'^\s+auth\s',help_text,re.M):return []
        raw=json.loads(read(['auth','status']))
        if raw.get('authMethod') not in {'claude.ai','oauth_token'}:return []
        email=raw.get('email') or ''
        ident=raw.get('accountId') or (email+'|'+str(raw.get('orgId') or '') if email else None)
        row=account('anthropic',ident,email,raw.get('subscriptionType'),'Claude Code')
        row['note']='Account recognized. Limits appear when the app reports them.'
        return [row]
    if not re.search(r'^\s+usage\s',help_text,re.M):return []
    usage_help=read(['usage','--help'])
    if '--json' not in usage_help:return []
    args=['usage','--json']
    if kind=='omp' and '--no-extensions' in usage_help:args.append('--no-extensions')
    if kind=='omp':return omp_accounts(json.loads(read(args)))
    rows=[]
    # Hermes' JSON command exposes one configured credential per provider, not the whole pool.
    for provider in ('openai-codex','anthropic','openrouter') if '--provider' in usage_help else (None,):
        try:
            current=hermes_accounts(json.loads(read(args+(['--provider',provider] if provider else []))))
            if current and not current[0].get('identified') and provider and re.search(r'^\s+auth\s',help_text,re.M):
                # Native credential metadata only. Never read/export its token. A single pool
                # entry binds an optional user-confirmed link without following account switches.
                try:
                    ids=re.findall(r'^\s*#\d+\s+.*?\bid=(\S+)',read(['auth','list',provider]),re.M)
                    if len(ids)==1:
                        current[0]['id']=hashlib.sha256(f'hermes|{provider}|{ids[0]}'.encode()).hexdigest()[:24]
                        current[0]['linkable']=True
                except (ValueError,OSError,subprocess.SubprocessError):pass
            rows.extend(current)
        except (ValueError,OSError,subprocess.SubprocessError):continue
    return merge_accounts(rows)


def cache_observation(raw, at=None):
    """Use observed policy, never a provider/model-name default."""
    now=timestamp(raw.get('_cache_started_at')) or timestamp(at)
    native=raw.get('prompt_cache') or {}
    if isinstance(native,dict) and timestamp(native.get('expires_at')) is not None:
        result={'expires_at':timestamp(native['expires_at']),'est':True,'observed_at':now,'source':'Native cache policy'}
        ttl={'5m':300,'1h':3600}.get(native.get('ttl'))
        if ttl:result['refresh_seconds']=ttl
        return result
    created=raw.get('cache_creation') or {}
    if isinstance(created,dict) and now:
        ttls=[ttl for name,ttl in [('ephemeral_5m_input_tokens',300),('ephemeral_1h_input_tokens',3600)] if number(created.get(name)) and created[name]>0]
        if ttls:return {'expires_at':now+min(ttls),'refresh_seconds':min(ttls),'est':True,'observed_at':now,'source':'Observed cache write'}
    return None
