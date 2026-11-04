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
    'antigravity': [('review','Require approval','request-review'),
                    ('accept-edits','Allow file edits','accept-edits'),
                    ('auto','Auto review','auto'),
                    ('plan','Plan only','plan'),
                    ('full','Full access','--dangerously-skip-permissions')],
}
FULL_ACCESS_MODES = ('full', 'bypassPermissions', 'yolo')
DESCRIPTIONS = {
    'native':'Use the permission settings already configured in your AI app.',
    'read-only':'Read files and ask before actions that need approval.',
    'workspace-write':'Allow changes in this workspace; ask before broader access.',
    'full':'Allow actions without asking for approval.',
    'default':'Ask before actions that need approval.',
    'review':'Ask before edits, commands, and web actions.',
    'acceptEdits':'Allow file edits; keep other approval checks.',
    'accept-edits':'Allow workspace file edits; keep other approval checks.',
    'auto':'Let the app review actions automatically where supported. Otherwise it uses its default approval mode.',
    'plan':'Investigate and plan before making changes.',
    'dontAsk':'Decline actions that would require approval.',
    'bypassPermissions':'Allow actions without asking for approval.',
    'always-ask':'Ask before tool actions.',
    'always-ask-cached':'Ask and remember approvals supported by the app.',
    'write':'Allow file edits; keep other approval checks.',
    'yolo':'Allow actions without asking for approval.',
}


def choices(kind):
    return [dict(id=ident,name=name,native=native,description=DESCRIPTIONS[ident],unrestricted=ident in FULL_ACCESS_MODES)
            for ident,name,native in [('native','Use AI app settings','No permission override'),*MODES.get(kind,[])]]


def validate(kind, mode):
    if mode not in {row['id'] for row in choices(kind)}:
        raise ValueError('This AI app does not support that permission choice in Aura.')
    return mode


def describe(kind, mode='native'):
    validate(kind,mode)
    return {'app':kind,'mode':mode,'choices':choices(kind),'scope':'New requests launched through Aura on this computer',
            'native':next(row['native'] for row in choices(kind) if row['id']==mode),
            'interactive':kind in {'codex','claude','pi','omp'},
            'unrestricted':mode in FULL_ACCESS_MODES,
            'note':('Pi has no built-in permission mode to change here. Approval extensions keep their own settings.' if kind=='pi' else
                    'Applies to the next request in Aura. This Antigravity connection declines actions needing an interactive approval; it cannot show those prompts here.' if kind=='antigravity' else
                    'Applies to the next request in Aura. An already running request keeps its current permissions.')}


def arguments(kind, mode):
    validate(kind,mode)
    if mode=='native' or kind=='codex':return []
    if kind=='claude':return ['--permission-mode',mode]
    if kind=='omp':return ['--approval-mode',mode]
    if kind=='hermes':return ['--yolo']
    if kind=='antigravity':
        if mode=='full':return ['--dangerously-skip-permissions']
        if mode=='review':return ['--settings',json.dumps({'agentMode':'','toolPermission':'request-review'},separators=(',',':'))]
        return ['--mode',mode]
    return []


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app',required=True);parser.add_argument('--mode',default='native');parser.add_argument('--json',action='store_true')
    action=parser.add_mutually_exclusive_group();action.add_argument('--current',action='store_true');action.add_argument('--save',action='store_true')
    parser.add_argument('--business-id');parser.add_argument('--chat');parser.add_argument('--url',default='http://127.0.0.1:4187')
    parser.add_argument('--workspace')
    args=parser.parse_args()
    if args.current or args.save:
        if not args.business_id:parser.error('--current and --save need --business-id')
        from _common import workspace_root,workspace_scope
        from workspace_goals import live_change
        from urllib.parse import urlencode
        with workspace_scope(args.workspace or workspace_root()):
            payload={'kind':args.app,**({'chat_id':args.chat} if args.chat else {})}
            result=live_change(args.url,args.business_id,{**payload,'mode':args.mode},'/api/permissions') if args.save else live_change(args.url,args.business_id,None,'/api/permissions?'+urlencode({'business':args.business_id,**payload}))
    else:result=describe(args.app,args.mode)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    import sys
    from urllib.error import HTTPError,URLError
    try:main()
    except HTTPError as error:
        try:message=json.load(error).get('error','Aura could not complete this action.')
        except (ValueError,OSError):message='Aura could not complete this action.'
        print('Error: '+str(message),file=sys.stderr);sys.exit(1)
    except URLError:
        print('Error: Aura is not reachable. Start the local Aura service and check --url.',file=sys.stderr);sys.exit(1)
    except (OSError,ValueError) as error:
        print('Error: '+str(error),file=sys.stderr);sys.exit(1)
