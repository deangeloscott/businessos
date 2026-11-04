#!/usr/bin/env python3
from _common import *
import json
p=ROOT/'PUBLISHER.json'
print(json.dumps(json.loads(p.read_text(encoding='utf-8')),indent=2))
