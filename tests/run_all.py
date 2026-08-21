#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'tests'))
from validate_distribution import validate_distribution
from routing_acceptance import run as routing_acceptance

validate_distribution()
routing_acceptance()
print('full test suite passed')
