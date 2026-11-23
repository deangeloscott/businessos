"""Hermes messages: conversations people start with Hermes from their phone (Telegram, Discord, WhatsApp and other
platforms Hermes's own gateway connects), shown in AURA, and short notices sent back to the phone.

Hermes owns the gateway, the bot and its sign-in. AURA only reads Hermes's own records on this computer (read-only,
no AI request) and sends notices through Hermes's own `hermes send`, which reuses the gateway's credentials. AURA never
holds a bot token.
"""
import json
import os
import re
import sqlite3
import subprocess
import time
from pathlib import Path

# Sessions started on this computer rather than through the messaging gateway.
LOCAL = {'cli', 'tui', 'desktop', 'acp', 'oneshot', 'cron', 'api', 'mcp', 'batch', 'subagent', 'delegate', 'kanban', ''}
NAMES = {'telegram': 'Telegram', 'discord': 'Discord', 'whatsapp': 'WhatsApp', 'slack': 'Slack', 'signal': 'Signal',
         'teams': 'Teams', 'google_chat': 'Google Chat', 'email': 'Email', 'sms': 'SMS', 'matrix': 'Matrix',
         'homeassistant': 'Home Assistant', 'weixin': 'Weixin', 'qqbot': 'QQ', 'yuanbao': 'Yuanbao'}
# A message from the phone that Hermes has not answered for this long is no longer "being answered".
ANSWERING = 600


def home(env=None):
    env = os.environ if env is None else env
    return Path(env.get('HERMES_HOME') or Path.home() / '.hermes')


def platform_name(source):
    return NAMES.get(str(source or '').lower()) or str(source or '').replace('_', ' ').title()


def _db(env):
    path = home(env) / 'state.db'
    if not path.is_file():
        return None
    return sqlite3.connect(f'file:{path.as_posix()}?mode=ro', uri=True, timeout=2)


def _config(env):
    path = home(env) / 'config.yaml'
    try:
        import yaml
    except ImportError:
        return {}
    try:
        if path.is_file() and path.stat().st_size <= 2 * 1024 * 1024:
            data = yaml.safe_load(path.read_text(encoding='utf-8'))
            return data if isinstance(data, dict) else {}
    except (OSError, ValueError, yaml.YAMLError):
        pass  # an unreadable config reads as "not set up"
    return {}


def owners(env=None):
    """Who "you" are on each platform: the home channel Hermes's own setup recorded, {platform: {ids}}."""
    found = {}
    for platform, settings in ((_config(env).get('platforms') or {}).items()):
        channel = (settings or {}).get('home_channel') if isinstance(settings, dict) else None
        if isinstance(channel, dict):
            ids = {str(channel[k]) for k in ('user_id', 'chat_id') if channel.get(k) not in (None, '')}
            if ids:
                found[str(platform).lower()] = ids
    return found


def gateway(env=None):
    """The gateway as Hermes reports it: running or not, and each platform's connection."""
    import workspace_recovery
    state = {}
    try:
        state = json.loads((home(env) / 'gateway_state.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        pass
    pid = state.get('pid')
    alive = workspace_recovery.process_mark(pid) if isinstance(pid, int) else False
    running = state.get('gateway_state') == 'running' and alive is not False
    platforms = [{'id': k, 'name': platform_name(k), 'state': (v or {}).get('state') or 'unknown',
                  'problem': bool((v or {}).get('needs_attention') or (v or {}).get('error_message'))}
                 for k, v in (state.get('platforms') or {}).items() if isinstance(v, dict)]
    homes = owners(env)
    return {'set_up': bool(state or homes), 'running': running, 'platforms': platforms,
            'home': next(iter(homes), '')}


def _tip(db, ident):
    """Hermes continues a long conversation under a new session when it compresses it; follow it to the latest."""
    for _ in range(50):
        row = db.execute("select c.id from sessions c join sessions p on p.id=c.parent_session_id "
                         "where p.id=? and p.end_reason='compression' order by c.started_at desc limit 1", (ident,)).fetchone()
        if not row:
            return ident
        ident = row[0]
    return ident


def conversations(env=None, since=0):
    """Gateway conversations with activity since `since`, newest first. Continuations of a compressed conversation are
    part of the conversation they continue, not new ones."""
    db = _db(env)
    if db is None:
        return []
    mine = owners(env)
    out = []
    try:
        rows = db.execute(
            "select s.id, s.source, s.user_id, s.chat_id, s.chat_type, s.display_name, s.title, s.started_at, "
            "coalesce(s.last_activity_at, s.started_at), s.thread_id from sessions s "
            "left join sessions p on p.id=s.parent_session_id "
            "where coalesce(s.last_activity_at, s.started_at)>=? and coalesce(s.hidden,0)=0 and coalesce(s.archived,0)=0 "
            "and (p.id is null or p.end_reason is not 'compression') "
            "order by coalesce(s.last_activity_at, s.started_at) desc limit 200", (since,)).fetchall()
    except sqlite3.Error:
        rows = []
    finally:
        db.close()
    for ident, source, user, chat, chat_type, name, title, started, last, thread in rows:
        if str(source or '').lower() in LOCAL:
            continue
        ids = mine.get(str(source).lower(), set())
        out.append({'id': ident, 'platform': str(source).lower(), 'from': platform_name(source),
                    'yours': bool(ids) and (str(user) in ids or (chat_type == 'dm' and str(chat) in ids)),
                    'sender': name or '', 'title': title or '', 'started': started or 0, 'last': last or 0,
                    'thread': thread or ''})
    return out


def marker(env, ident):
    """A cheap change mark for one conversation: its latest session and latest message."""
    db = _db(env)
    if db is None:
        return None
    try:
        tip = _tip(db, ident)
        row = db.execute('select max(id) from messages where session_id=?', (tip,)).fetchone()
        return [tip, row[0] if row else None]
    except sqlite3.Error:
        return None
    finally:
        db.close()


def answering(env, ident):
    """True while Hermes is still answering a message that came from the phone in this conversation."""
    db = _db(env)
    if db is None:
        return False
    try:
        tip = _tip(db, ident)
        row = db.execute("select role, timestamp from messages where session_id=? and role in ('user','assistant') "
                         "order by id desc limit 1", (tip,)).fetchone()
    except sqlite3.Error:
        return False
    finally:
        db.close()
    return bool(row) and row[0] == 'user' and time.time() - float(row[1] or 0) < ANSWERING


TIMED_OUT = "Hermes took too long to confirm a notice, so it may have arrived. Check your phone."


def send(argv, env, platform, text):
    """One line to your own chat on `platform`, through Hermes's own send command (no AI, no running gateway needed
    for bot-token platforms). Returns '' when sent, otherwise a short reason; TIMED_OUT when the send started but never
    finished, so it may already have arrived."""
    text = re.sub(r'\s+', ' ', str(text)).strip()[:600]
    try:
        done = subprocess.run([*argv, 'send', '-t', platform, '-q', text], capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=45, env=env, stdin=subprocess.DEVNULL,
                              creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    except subprocess.TimeoutExpired:
        return TIMED_OUT
    except (OSError, subprocess.SubprocessError):
        return "Hermes didn't answer."
    return '' if done.returncode == 0 else "Hermes couldn't send it. Check Hermes messages."
