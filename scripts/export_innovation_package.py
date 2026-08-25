#!/usr/bin/env python3
from _common import *
from innovation_common import load_package,validate_package,canonical_hash
import argparse,json,zipfile

def export_package(draft_path,output,approved=False):
    if not approved:raise ValueError('Explicit export approval is required; rerun with --approve only after the user approves sharing this package')
    pkg=load_package(draft_path);validate_package(pkg);pkg['privacy']['user_approved_export']=True;pkg['privacy']['approved_at']=now();pkg['integrity']['content_hash']=canonical_hash(pkg);validate_package(pkg,require_export_approval=True);out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
    if out.suffix.lower()=='.zip':
        with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:z.writestr('innovation-package.json',json.dumps(pkg,indent=2)+'\n');z.writestr('README.txt','BusinessOS InnovationPackage. Validate before import; contribution evidence is not automatic proof of effectiveness.\n')
    else:out.write_text(json.dumps(pkg,indent=2)+'\n')
    return pkg,out

def main():
    ap=argparse.ArgumentParser(description='Create an explicitly approved portable InnovationPackage JSON/ZIP. This writes a file; it does not upload it.');ap.add_argument('draft_path');ap.add_argument('--output',required=True);ap.add_argument('--approve',action='store_true');a=ap.parse_args()
    try:pkg,out=export_package(a.draft_path,a.output,a.approve)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps({'package_id':pkg['package_id'],'output':str(out),'approved_for_export':True,'uploaded':False},indent=2))
if __name__=='__main__':main()
