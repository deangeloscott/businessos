#!/usr/bin/env python3
from _common import *
from innovation_common import load_package,validate_package,canonical_hash
import argparse,json,zipfile


def export_package(draft_path,output,approved=False):
    if not approved:raise ValueError('Explicit export approval is required; rerun with --approve only after the user approves sharing this package')
    package=load_package(draft_path);validate_package(package);package['privacy']['user_approved_export']=True;package['privacy']['approved_at']=now();package['integrity']['content_hash']=canonical_hash(package);validate_package(package,require_export_approval=True);out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
    if out.suffix.lower()=='.zip':
        with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('innovation-package.json',json.dumps(package,indent=2)+'\n')
            archive.writestr('README.txt','ViralTrac AURA InnovationPackage. Validate before import; contribution evidence is not automatic proof of effectiveness.\n')
    else:out.write_text(json.dumps(package,indent=2)+'\n')
    return package,out


def main():
    parser=argparse.ArgumentParser(description='Create an explicitly approved portable AURA InnovationPackage JSON/ZIP. This writes a file; it does not upload it.');parser.add_argument('draft_path');parser.add_argument('--output',required=True);parser.add_argument('--approve',action='store_true');args=parser.parse_args()
    try:package,out=export_package(args.draft_path,args.output,args.approve)
    except ValueError as exc:raise SystemExit(str(exc))
    print(json.dumps({'package_id':package['package_id'],'output':str(out),'approved_for_export':True,'uploaded':False},indent=2))

if __name__=='__main__':main()
