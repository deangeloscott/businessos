"""One-use replies to live native requests. Nothing here is a saved permission grant."""
import copy
import secrets
import threading
import time


class Requests:
    def __init__(self, changed=lambda rows:None):
        self.lock=threading.RLock();self.rows={};self.changed=changed;self.closed=False

    def snapshot(self):
        with self.lock:
            return [copy.deepcopy({k:v for k,v in row.items() if k not in {'send','validate'}}) for row in self.rows.values()]

    def publish(self):self.changed(self.snapshot())

    def add(self, native_id, title, questions, send, validate, detail='', timeout=None):
        with self.lock:
            if self.closed:raise ValueError('This native request has ended.')
            # A retransmitted native request must not create a second actionable card.
            existing=next((r for r in self.rows.values() if r['native_id']==native_id),None)
            if existing:return existing['id']
            completed=[key for key,row in self.rows.items() if row['status']!='pending']
            for key in completed[:-99]:self.rows.pop(key,None)
            ident=secrets.token_urlsafe(18)
            self.rows[ident]={'id':ident,'native_id':native_id,'title':str(title)[:300],'detail':str(detail)[:12000],
                'questions':copy.deepcopy(questions),'status':'pending','created':time.time(),
                'expires':time.time()+timeout/1000 if isinstance(timeout,(float,int)) and timeout>0 else None,
                'send':send,'validate':validate}
        self.publish();return ident

    def answer(self, ident, answers):
        self.expire()
        failure=None
        with self.lock:
            row=self.rows.get(ident)
            if not row or row['status']!='pending':raise ValueError('This request has already been answered or has expired.')
            payload=row['validate'](answers)
            # Check and native write share the lock with cancellation/expiry.
            try:row['send'](payload)
            except (OSError,ValueError) as exc:
                # A partial native write cannot safely be retried as a new answer.
                row['status']='expired';failure=exc
            else:row.update(status='answered',answered=time.time())
            row.pop('send',None);row.pop('validate',None)
        self.publish()
        if failure:raise ValueError('The native connection ended while sending. Check its chat before continuing.') from None
        return {'id':ident,'status':'answered'}

    def resolve(self, native_id=None):
        with self.lock:
            for row in self.rows.values():
                if row['status']=='pending' and (native_id is None or row['native_id']==native_id):
                    row['status']='expired';row.pop('send',None);row.pop('validate',None)
        self.publish()

    def expire(self):
        changed=False
        with self.lock:
            for row in self.rows.values():
                if row['status']=='pending' and row.get('expires') and row['expires']<=time.time():
                    row['status']='expired';row.pop('send',None);row.pop('validate',None);changed=True
        if changed:self.publish()

    def close(self):
        with self.lock:self.closed=True
        self.resolve()


def answers_for(questions, answers):
    if not isinstance(answers,dict) or set(answers)-{q['id'] for q in questions}:raise ValueError('Answer the questions shown in this request.')
    result={}
    for q in questions:
        values=answers.get(q['id'],[])
        if not values and not q.get('required',True):
            result[q['id']]=[];continue
        if not isinstance(values,list) or not values or any(not isinstance(v,str) or not v.strip() or len(v)>12000 for v in values):
            raise ValueError('Answer each question before submitting.')
        values=list(dict.fromkeys(values))
        if not q.get('multiple') and len(values)!=1:raise ValueError('Choose one answer for this question.')
        allowed={o['value'] for o in q.get('options',[])}
        if allowed and not q.get('allow_text') and any(v not in allowed for v in values):raise ValueError('Choose one of the available answers.')
        result[q['id']]=values
    return result


def question(ident, text, options=(), multiple=False, free=False):
    return {'id':str(ident),'text':str(text),'options':[{'value':str(v),'label':str(v)} for v in options],
            'multiple':bool(multiple),'allow_text':bool(free or not options)}
