"""Small, machine-local chat descriptions; never canonical business memory."""
import hashlib
import json
import re
import time


PREFIX = 'AURA_CHAT_BRIEF_'


def short(value, limit):
    if not isinstance(value, str):return ''
    value=' '.join(value.split())
    if len(value)<=limit:return value
    return value[:limit-1].rsplit(' ',1)[0]+'…'


def brief(text):
    """Only a final, bounded assistant metadata line is a candidate description."""
    match=re.search(r'(?:^|\n)[ \t]*'+PREFIX+r'([a-f0-9]{16}) ([^\n]{1,1600})\s*$',str(text))
    if not match:return None
    try:data=json.loads(match[2])
    except ValueError:return None
    if not isinstance(data,dict) or not short(data.get('summary'),360):return None
    return {'token':match[1],'title':short(data.get('title'),80),'summary':short(data['summary'],360)}


def clean(text, streaming=False):
    text=re.sub(r'(?m)^[ \t]*'+PREFIX+r'[^\n]*(?:\n|$)', '',str(text))
    if streaming:
        lines=text.split('\n');last=lines[-1].strip()
        if last and (last.startswith(PREFIX) or PREFIX.startswith(last)):lines.pop()
        text='\n'.join(lines)
    return text.rstrip()


def instructions(chat,brief=False):
    if brief:
        # The app keeps the conversation, so the full request it saw earlier still applies; a reminder keeps descriptions current for ~40 tokens.
        return ('\nIf this reply changes the goal, progress or next step, end with the chat-list line '+PREFIX+chat['brief_token']+
                ' {"title":...,"summary":...} as described earlier; otherwise skip it.\n')
    previous=short(chat.get('summary'),360)
    return ('\nChat-list description (interface metadata, not business memory): if this reply changes the goal, progress or next step, '
            'end with one line: '+PREFIX+chat['brief_token']+' {"title":"short topic","summary":"purpose, progress, next step; under 360 characters"}. '
            'Skip it for trivial replies or when the current description still fits. Use only this conversation and observed outcomes: '
            'no private reasoning, credentials or internal IDs, and no planned work described as done. Do not save files for it. '
            +(f'Current description: {json.dumps(previous)}. ' if previous else '')+'\n')


def instructions_due(chat,every=5):
    """Whether this message carries the full description request: the first time, and every few messages in case the
    app has compacted its history. Other messages carry the short reminder."""
    asked=chat.get('brief_asked_ago')
    if asked is None or asked+1>=every:
        chat['brief_asked_ago']=0;return True
    chat['brief_asked_ago']=asked+1;return False


def fingerprint(messages):
    visible=[];keep_warm=False
    for m in messages:
        role=m.get('role');text=clean(m.get('text',''))
        if role=='user':keep_warm=text.startswith('Keep this chat’s cache warm. Reply with OK only.')
        if role in {'user','assistant'} and not keep_warm:visible.append((role,text))
    return hashlib.sha256(json.dumps(visible[-2:],ensure_ascii=False).encode()).hexdigest()


def update(chat, messages, candidate=None, native_summary='', native_title='', native_updated=None):
    """Keep manual titles; never date an old native summary as freshly generated."""
    basis=fingerprint(messages)
    newer_native=bool(native_summary and native_updated and native_updated>((candidate or {}).get('at') or chat.get('summary_updated') or 0))
    if candidate and candidate.get('token')==chat.get('brief_token') and not newer_native:
        provided_basis=candidate.get('basis',basis)
        if candidate['summary']!=chat.get('summary') or provided_basis!=chat.get('summary_basis'):
            chat.update(summary=candidate['summary'],summary_basis=provided_basis,summary_updated=candidate.get('at') if 'at' in candidate else time.time(),summary_source='AI')
        if candidate.get('title') and not chat.get('title_edited') and not chat.get('title_generated'):
            chat.update(title=candidate['title'],title_generated=True)
    elif native_summary and (chat.get('summary_source')!='AI' or native_updated and native_updated>(chat.get('summary_updated') or 0)):
        text=short(native_summary,360)
        if text and (text!=chat.get('summary') or chat.get('summary_source')!='App' or native_updated and native_updated>(chat.get('summary_updated') or 0)):
            chat.update(summary=text,summary_basis=basis,summary_updated=native_updated,summary_source='App')
    if native_title and not chat.get('title_edited') and not chat.get('title_generated'):
        chat.update(title=short(native_title,80),title_generated=True)
    if messages:
        latest=next((short(m.get('text'),180) for m in reversed(messages) if m.get('role')=='user' and not str(m.get('text','')).startswith('Keep this chat’s cache warm. Reply with OK only.')), '')
        if latest:chat['latest_request']=latest
    chat['summary_stale']=bool(chat.get('summary') and chat.get('summary_basis')!=basis)
    return chat
