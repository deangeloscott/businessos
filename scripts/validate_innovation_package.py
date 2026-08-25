#!/usr/bin/env python3
from innovation_common import load_package,validate_package
import argparse,json

def main():
    ap=argparse.ArgumentParser(description='Validate an InnovationPackage JSON/ZIP, privacy boundary, and integrity hash.');ap.add_argument('package_path');ap.add_argument('--require-export-approval',action='store_true');a=ap.parse_args()
    try:pkg=load_package(a.package_path);validate_package(pkg,a.require_export_approval)
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))
    print(json.dumps({'valid':True,'package_id':pkg['package_id'],'detail_level':pkg['detail_level'],'identity_level':pkg['identity_level'],'approved_for_export':pkg['privacy']['user_approved_export']},indent=2))
if __name__=='__main__':main()
