#!/usr/bin/env python3
"""Keep PreferenceProfile structurally limited to reusable choice customization.

AURA can enforce that permission/authorization namespaces are not PreferenceProfile
fields. It cannot reliably infer from arbitrary prose whether a sentence is a temporary
task constraint, a durable organizational policy/decision, or a genuine preference;
that semantic judgment belongs to the active model/user.
"""
import re

# Reserved structural namespaces that are categorically not preference data. This is a
# storage-type boundary, not a natural-language intent classifier.
FORBIDDEN_KEY_FRAGMENTS={
    'authorization','authorisation','permission','permissions','approval','approvals','consent',
    'allowed_actions','prohibited_actions','authorized_actions','authorised_actions',
    'external_action_boundary','external_action_boundaries','production_action_boundary','production_action_boundaries',
}


def _norm_key(key):return re.sub(r'[^a-z0-9]+','_',str(key).lower()).strip('_')


def forbidden_preference_key(key):
    normalized=_norm_key(key)
    return normalized in FORBIDDEN_KEY_FRAGMENTS or any(
        fragment in normalized for fragment in ('authorization','authorisation','permission','approval')
    )


def preference_semantic_errors(preferences,prefix='preferences'):
    """Validate only the structural preference namespace; do not interpret prose."""
    errors=[]
    def walk(value,path):
        if isinstance(value,dict):
            for key,item in value.items():
                if forbidden_preference_key(key):
                    errors.append(f'{path}.{key}: permission/action-authority namespace is not PreferenceProfile data')
                walk(item,f'{path}.{key}')
        elif isinstance(value,list):
            for i,item in enumerate(value):walk(item,f'{path}[{i}]')
    if not isinstance(preferences,dict):return [f'{prefix}: preferences must be an object']
    walk(preferences,prefix)
    return errors


def validate_preference_semantics(preferences,prefix='preferences'):
    errors=preference_semantic_errors(preferences,prefix)
    if errors:
        raise ValueError(
            '; '.join(errors[:10])+
            '. Keep reusable style/work-method choices in PreferenceProfile. '
            'The active model/user decides whether free-form instructions belong to the current request, a durable organizational decision/policy, or a true reusable preference; AURA does not infer that from prose.'
        )
    return preferences
