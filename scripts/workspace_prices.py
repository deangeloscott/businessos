"""Estimated cost at API prices, for AI apps that report tokens but no cost. Off unless turned on in Settings.

When it is on, AURA downloads OpenRouter's public list of model prices (nothing about you is sent) when the Library
is refreshed, and otherwise at most once a week. Only changes are kept: each model's price is stored with the date it
took effect, so a past request is always estimated at the price of its day and past estimates never shift. A model the
list does not know is left as tokens only, never guessed. Estimates are always shown as estimates, apart from cost an
app reported.
"""
import json
import os
import re
import time
import urllib.request

from workspace_startup import state_dir

SOURCE = 'https://openrouter.ai/api/v1/models'
WEEK = 7 * 86400
MAKERS = {'openai', 'anthropic', 'google', 'x-ai', 'mistralai', 'meta-llama', 'qwen', 'deepseek', 'moonshotai', 'cohere', 'amazon', 'microsoft', 'nvidia', 'z-ai'}


def _key(model):
    """A model's name without its maker or punctuation: 'openai/gpt-5.1' and 'GPT-5.1' are the same model."""
    name = str(model or '').split('/')[-1].split(':')[0]
    name = re.sub(r'[-@](?:\d{8}|\d{4}-\d{2}-\d{2})$', '', name)  # a dated release is the same model: claude-haiku-4-5-20251001
    return ''.join(c for c in name.lower() if c.isalnum())


def _store():
    return state_dir() / 'aura-prices.json'


def load():
    try:
        data = json.loads(_store().read_text(encoding='utf-8'))
        return data if isinstance(data, dict) and isinstance(data.get('models'), dict) else {'models': {}}
    except (OSError, ValueError):
        return {'models': {}}


def refresh(force=False, fetch=None):
    """Read the public price list and add any price that changed. Returns how many models changed, or None if skipped."""
    data = load()
    if not force and time.time() - data.get('checked_at', 0) < WEEK:
        return None
    if fetch is None:
        def fetch():
            request = urllib.request.Request(SOURCE, headers={'User-Agent': 'AURA', 'Accept': 'application/json'})
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.loads(response.read(8 * 1024 * 1024).decode('utf-8'))
    listed = (fetch() or {}).get('data') or []
    now, changed, chosen = time.time(), 0, {}
    for row in listed:
        pricing = (row or {}).get('pricing') or {}
        ident = str((row or {}).get('id', ''))
        try:
            prompt, completion = float(pricing.get('prompt')), float(pricing.get('completion'))
        except (TypeError, ValueError):
            continue
        # Cached input has its own, much lower price; without one listed, it is priced as ordinary input.
        cached = [float(pricing[k]) if _number(pricing.get(k)) else None for k in ('input_cache_read', 'input_cache_write')]
        if prompt <= 0 and completion <= 0 or ident.endswith(':free'):
            continue  # free variants say nothing about what the model costs
        # One price per model: its maker's own listing when there is one, otherwise always the same listing.
        rank = (ident.split('/')[0] not in MAKERS, ident)
        key = _key(ident)
        if key not in chosen or rank < chosen[key][0]:
            chosen[key] = (rank, [prompt, completion, *cached])
    for key, (_, price) in chosen.items():
        history = data['models'].setdefault(key, [])
        if not history or history[-1][1:] != price:
            history.append([now, *price]);changed += 1
    data['checked_at'] = now
    path = _store();path.parent.mkdir(parents=True, exist_ok=True);tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data), encoding='utf-8');os.replace(tmp, path)
    return changed


def _number(value):
    try:
        return float(value) >= 0
    except (TypeError, ValueError):
        return False


def estimate(model, input_tokens, output_tokens, at, prices=None, cached_tokens=0, cache_write_tokens=0):
    """US dollars at the API price in effect at `at`, or None when the model is not in the list. Input tokens include
    the cached ones, as every app reports them here; those are priced at the cache prices where the list has them."""
    history = (prices or load())['models'].get(_key(model))
    if not history or not (input_tokens or output_tokens):
        return None
    # The price of that day; work from before the first download uses the first price known.
    row = next((h for h in reversed(history) if h[0] <= (at or 0)), history[0])
    read, write = (row[3] if len(row) > 3 and row[3] is not None else row[1]), (row[4] if len(row) > 4 and row[4] is not None else row[1])
    cached, written = cached_tokens or 0, cache_write_tokens or 0
    fresh = max(0, (input_tokens or 0) - cached - written)
    return fresh * row[1] + cached * read + written * write + (output_tokens or 0) * row[2]


def refresh_quietly():
    """Refresh now, in the background; a failed download keeps the prices already known."""
    try:
        refresh(force=True)
    except (OSError, ValueError):
        pass
