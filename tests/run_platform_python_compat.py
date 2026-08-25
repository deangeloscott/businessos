#!/usr/bin/env python3
"""RC10 regression for portable PlatformChange helper syntax and stable identity."""
from pathlib import Path
import importlib.util, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts'/'record_platform_change.py'

def req(c,m):
    if not c: raise AssertionError(m)

def main():
    text=SCRIPT.read_text()
    # Python <=3.11 rejects backslashes inside f-string expression braces.
    req('hashlib.sha256((key+"\\0"+fp).encode())' not in text,
        'record_platform_change.py reintroduced the Python<=3.11-incompatible f-string expression')
    sys.path.insert(0,str(ROOT/'scripts'))
    spec=importlib.util.spec_from_file_location('record_platform_change',SCRIPT)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    key='signalport-developer-platform:events-api-v1-lifecycle'; fp='sha256:abc123'
    expected='plc_relayboard_'+hashlib.sha256((key+'\0'+fp).encode()).hexdigest()[:16]
    req(mod.pid('relayboard',key,fp)==expected,'PlatformChange identity changed while fixing syntax compatibility')
    print('platform helper Python compatibility regression passed')

if __name__=='__main__': main()
