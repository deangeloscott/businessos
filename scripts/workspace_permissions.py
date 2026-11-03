"""Session-scoped native permission choices; never portable permission grants."""
import argparse
import json

# Values are the native app's own modes. Similar names do not imply equal isolation.
MODES = {
    'codex': [('read-only','Read only','read-only · on-request'),
              ('workspace-write','Workspace access','workspace-write · on-request'),
              ('full','Full access','danger-full-access · never')],
    'claude': [('default','Ask for approval','default'),('acceptEdits','Allow file edits','acceptEdits'),
               ('plan','Plan only','plan'),('dontAsk','Deny when approval is needed','dontAsk'),
               ('bypassPermissions','Full access','bypassPermissions')],
    'omp': [('always-ask','Ask for approval','always-ask'),('always-ask-cached','Ask and remember','always-ask-cached'),
            ('write','Allow file edits','write'),('yolo','Full access','yolo')],
    'hermes': [('yolo','Full access','--yolo')],
}


def choices(kind):
    return [{'id':'native','name':'Use harness settings','native':'No permission override'},
            *[{'id':ident,'name':name,'native':native} for ident,name,native in MODES.get(kind,[])]]


def validate(kind, mode):
    if mode not in {row['id'] for row in choices(kind)}:
        raise ValueError('This AI app does not support that permission choice in Aura.')
    return mode


def describe(kind, mode='native'):
    validate(kind,mode)
    return {'app':kind,'mode':mode,'choices':choices(kind),'scope':'New requests launched through Aura on this computer',
            'native':next(row['native'] for row in choices(kind) if row['id']==mode),
            'interactive':kind in {'codex','claude','pi','omp'}}


def arguments(kind, mode):
    validate(kind,mode)
    if mode=='native' or kind=='codex':return []
    if kind=='claude':return ['--permission-mode',mode]
    if kind=='omp':return ['--approval-mode',mode]
    if kind=='hermes':return ['--yolo']
    return []


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app',required=True);parser.add_argument('--mode',default='native');parser.add_argument('--json',action='store_true')
    args=parser.parse_args();print(json.dumps(describe(args.app,args.mode)))


if __name__=='__main__':main()
