"""Validate exact settings reported by a native connection, without a second catalog."""


def options(rows):
    for row in rows:
        if 'options' in row:yield from options(row['options'])
        elif 'value' in row:yield row


def selections(rows,values):
    if not isinstance(values,dict):raise ValueError('Choose valid native settings.')
    found={r['id']:r for r in rows if isinstance(r,dict) and r.get('id')}
    for ident,value in values.items():
        row=found.get(ident)
        if not row or row.get('type','select')!='select' or row.get('category') in {'model','mode','thought_level'}:
            raise ValueError('This native setting changed. Reopen the model picker.')
        if value not in [r['value'] for r in options(row.get('options',[]))]:
            raise ValueError('Choose an available value for '+str(row.get('name') or ident)+'.')
    return dict(values)
