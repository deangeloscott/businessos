"""Use OS-owned secret storage; never fall back to a plaintext key file."""
import ctypes
import json
import os
import shutil
import subprocess
import sys


class NativeSecrets:
    def __init__(self, service='com.viraltrac.aura.api-keys', keychain=None):
        self.service = service
        self.keychain = keychain

    @property
    def backend(self):
        if sys.platform == 'darwin':
            return 'macOS Keychain'
        if sys.platform.startswith('linux') and os.environ.get('DBUS_SESSION_BUS_ADDRESS') and shutil.which('secret-tool'):
            return 'Linux keyring'
        return ''

    def _mac(self, value=None):
        security = ctypes.CDLL('/System/Library/Frameworks/Security.framework/Security')
        core = ctypes.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
        core.CFRelease.argtypes = [ctypes.c_void_p]
        keychain = ctypes.c_void_p()
        if self.keychain:
            open_keychain = security.SecKeychainOpen
            open_keychain.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
            open_keychain.restype = ctypes.c_int32
            if open_keychain(os.fsencode(self.keychain), ctypes.byref(keychain)):
                raise ValueError('The selected keychain could not be opened.')
        service, account = self.service.encode(), b'aura'
        item, size, data = ctypes.c_void_p(), ctypes.c_uint32(), ctypes.c_void_p()
        find = security.SecKeychainFindGenericPassword
        find.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_uint32,
                         ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p)]
        find.restype = ctypes.c_int32
        code = find(keychain, len(service), service, len(account), account, ctypes.byref(size), ctypes.byref(data), ctypes.byref(item))
        if code not in (0, -25300):
            if keychain:
                core.CFRelease(keychain)
            raise ValueError('macOS Keychain could not be opened. Unlock it or choose this session only.')
        try:
            if value is None:
                return ctypes.string_at(data, size.value).decode('utf-8') if code == 0 else '{}'
            raw = value.encode('utf-8')
            if code == 0:
                change = security.SecKeychainItemModifyAttributesAndData
                change.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_char_p]
                change.restype = ctypes.c_int32
                result = change(item, None, len(raw), raw)
            else:
                add = security.SecKeychainAddGenericPassword
                add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_char_p,
                                ctypes.c_uint32, ctypes.c_char_p, ctypes.c_void_p]
                add.restype = ctypes.c_int32
                result = add(keychain, len(service), service, len(account), account, len(raw), raw, None)
            if result:
                raise ValueError('macOS Keychain could not save this key. Unlock it or choose this session only.')
        finally:
            if data:
                free = security.SecKeychainItemFreeContent
                free.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
                free(None, data)
            if item:
                core.CFRelease(item)
            if keychain:
                core.CFRelease(keychain)

    def _linux(self, value=None):
        args = [shutil.which('secret-tool')]
        args += ['lookup'] if value is None else ['store', '--label=AURA API connections']
        args += ['application', self.service, 'type', 'api-keys']
        try:
            result = subprocess.run(args, input=value, stdin=subprocess.DEVNULL if value is None else None,
                                    capture_output=True, text=True, encoding='utf-8', timeout=25)
        except subprocess.TimeoutExpired:
            raise ValueError('Your keyring did not respond. Unlock it or choose this session only.') from None
        if value is None and result.returncode == 1 and not result.stderr.strip():
            return '{}'
        if result.returncode:
            raise ValueError('Your keyring could not be opened. Unlock it or choose this session only.')
        return result.stdout.strip()

    def load(self):
        if not self.backend:
            return {}
        raw = self._mac() if sys.platform == 'darwin' else self._linux()
        try:
            result = json.loads(raw)
            if not isinstance(result, dict) or not all(isinstance(v, dict) and isinstance(v.get('key'), str) for v in result.values()):
                raise ValueError()
            return result
        except (ValueError, TypeError):
            raise ValueError('Saved API keys could not be opened. No keys were overwritten.') from None

    def save(self, rows):
        if not self.backend:
            raise ValueError('Secure storage is unavailable here. Choose this session only.')
        value = json.dumps(rows)
        self._mac(value) if sys.platform == 'darwin' else self._linux(value)
