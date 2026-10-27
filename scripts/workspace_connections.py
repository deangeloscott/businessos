"""Optional machine-local API keys. Business files never contain credentials."""
from pathlib import Path
import ctypes
import json
import os
import re


PRESETS = [
    ('openai', 'OpenAI', 'OPENAI_API_KEY', 'https://platform.openai.com/api-keys'),
    ('anthropic', 'Anthropic', 'ANTHROPIC_API_KEY', 'https://console.anthropic.com/settings/keys'),
    ('google', 'Google Gemini', 'GEMINI_API_KEY', 'https://aistudio.google.com/apikey'),
    ('xai', 'xAI / Grok', 'XAI_API_KEY', 'https://console.x.ai/'),
    ('openrouter', 'OpenRouter', 'OPENROUTER_API_KEY', 'https://openrouter.ai/settings/keys'),
    ('kie', 'Kie AI', 'KIE_API_KEY', 'https://kie.ai/api-key'),
    ('fal', 'fal.ai', 'FAL_KEY', 'https://fal.ai/dashboard/keys'),
    ('higgsfield', 'Higgsfield', 'HF_API_KEY', 'https://open.higgsfield.ai/api-keys'),
    ('elevenlabs', 'ElevenLabs', 'ELEVENLABS_API_KEY', 'https://elevenlabs.io/app/settings/api-keys'),
]
MODEL_PROVIDERS = {'openai', 'anthropic', 'google', 'xai', 'openrouter'}


def protect(data, decrypt=False):
    """Windows CurrentUser DPAPI, with no plaintext fallback."""
    from ctypes import wintypes
    class Blob(ctypes.Structure):
        _fields_ = [('length', wintypes.DWORD), ('data', ctypes.POINTER(ctypes.c_ubyte))]
    raw = ctypes.create_string_buffer(data)
    source = Blob(len(data), ctypes.cast(raw, ctypes.POINTER(ctypes.c_ubyte)))
    target = Blob()
    api = ctypes.WinDLL('crypt32', use_last_error=True)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    fn = api.CryptUnprotectData if decrypt else api.CryptProtectData
    fn.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                   ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
    fn.restype = wintypes.BOOL
    if not fn(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(target)):
        raise ValueError('Windows could not open the protected API keys for this user. No keys were overwritten.')
    try:
        return ctypes.string_at(target.data, target.length)
    finally:
        kernel.LocalFree(target.data)


class Connections:
    def __init__(self, folder):
        self.path = Path(folder) / 'api-keys.bin'
        self.session = {}

    @property
    def persistent(self):
        return os.name == 'nt'

    def stored(self):
        if not self.path.exists():
            return {}
        if not self.persistent:
            raise ValueError('Saved API keys belong to another operating system. Enter them for this session.')
        try:
            rows = json.loads(protect(self.path.read_bytes(), decrypt=True))
            if not isinstance(rows, dict) or not all(isinstance(v, dict) and isinstance(v.get('key'), str) for v in rows.values()):
                raise ValueError()
            return rows
        except (OSError, ValueError):
            raise ValueError('Saved API keys could not be opened. No keys were overwritten.') from None

    def write(self, rows):
        if not self.persistent:
            raise ValueError('Secure persistent storage is unavailable here. Choose this session only.')
        encrypted = protect(json.dumps(rows).encode())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix('.tmp')
        temporary.write_bytes(encrypted)
        temporary.replace(self.path)

    def all(self):
        return {**self.stored(), **self.session}

    def rows(self):
        saved = self.all()
        rows = [{'id': p, 'name': name, 'env': env, 'url': url} for p, name, env, url in PRESETS]
        for ident, record in saved.items():
            if ident not in {p[0] for p in PRESETS}:
                rows.append({k: record[k] for k in ('name', 'env')} | {'id': ident, 'url': ''})
        for row in rows:
            row['category'] = ('models' if row['id'] in MODEL_PROVIDERS else 'tools') if row['id'] in {p[0] for p in PRESETS} else saved.get(row['id'], {}).get('category', 'tools')
            row['status'] = ('This session' if row['id'] in self.session else 'Saved on this computer') if row['id'] in saved else ('Available in environment' if os.environ.get(row['env']) else 'Not added')
            row['saved'] = row['id'] in saved
        return {'items': rows, 'persistent': self.persistent}

    def save(self, ident, key, storage='session', name='', env='', category='tools'):
        preset = next((p for p in PRESETS if p[0] == ident), None)
        if preset:
            _, name, env, _ = preset
        elif ident == 'other':
            if not re.fullmatch(r'[A-Z][A-Z0-9_]{1,70}_(?:API_KEY|TOKEN|SECRET)', env) or not 1 <= len(name.strip()) <= 80:
                raise ValueError('Enter a service name and its documented API key variable, such as SERVICE_API_KEY.')
            ident, name = 'custom-' + env, name.strip()
        else:
            raise ValueError('Choose an API service.')
        if not isinstance(key, str) or not key.strip() or len(key) > 8192 or any(c.isspace() for c in key):
            raise ValueError('Paste the complete API key without spaces or line breaks.')
        if storage not in {'session', 'computer'}:
            raise ValueError('Choose where to keep this key.')
        rows = self.stored()
        if category not in {'models', 'tools'}:
            raise ValueError('Choose a model provider or a tool service.')
        record = {'name': name, 'env': env, 'key': key, 'category': 'models' if ident in MODEL_PROVIDERS else category}
        if storage == 'computer':
            rows[ident] = record
            self.write(rows)
            self.session.pop(ident, None)
        else:
            if ident in rows:
                del rows[ident]
                self.write(rows)
            self.session[ident] = record

    def remove(self, ident):
        rows = self.stored()
        if ident in rows:
            del rows[ident]
            self.write(rows)
        self.session.pop(ident, None)

    def environment(self):
        return {r['env']: r['key'] for r in self.all().values()}

    def guidance(self):
        rows = [r for r in self.rows()['items'] if r['status'] != 'Not added']
        if not rows:
            return ''
        return ('\nAPI credentials available to tools in this process (not verified accounts): ' +
                ', '.join(r['name'] + ' via ' + r['env'] for r in rows) + '. '
                'Use these when helpful through documented provider APIs and your actual tools. '
                'Read secrets from environment variables; never print, echo, quote, persist, or include them in tool arguments or replies. '
                'A saved key does not prove balance, permissions, available models or successful generation.\n')

    def redact(self, text):
        for value in self.environment().values():
            text = text.replace(value, '[API key hidden]')
        return text
