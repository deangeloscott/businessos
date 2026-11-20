"""What AI use cost and how much of each plan it used, from what the apps already report; estimates only when asked."""
import os,sys,tempfile,time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))


def main():
    with tempfile.TemporaryDirectory(prefix='aura-costs-') as t,patch.dict(os.environ,{'AURA_STATE_DIR':str(Path(t)/'state')}):
        import workspace_usage as usage,workspace_prices as prices,workspace_world as world

        # A request's share of the plan: the level just before it and the last level it reported, in the same window.
        job={'created':1000.0}
        before={'checked_at':900.0,'windows':[{'bucket':'Codex','name':'Weekly limit','used_percent':40,'resets_at':5000}]}
        usage.plan_mark(job,before,[{'bucket':'Codex','name':'Weekly limit','used_percent':41,'resets_at':5000}])
        usage.plan_mark(job,{},[{'bucket':'Codex','name':'Weekly limit','used_percent':43.5,'resets_at':5000}])
        assert usage.plan_share(job)==([{'window':'Weekly limit','used':3.5}],True),usage.plan_share(job)
        stale={'created':1000.0};usage.plan_mark(stale,{**before,'checked_at':0},[{'bucket':'Codex','name':'Weekly limit','used_percent':43,'resets_at':5000}])
        assert usage.plan_share(stale)==([],False),'an old level is not a fair starting point, so nothing is claimed'
        busy={'created':1000.0};usage.plan_mark(busy,before,[{'bucket':'Codex','name':'Weekly limit','used_percent':44,'resets_at':5000}],shared=True)
        assert usage.plan_share(busy)[1] is False,'two requests on one plan at once can only be split approximately'

        # Prices: only changes are kept, each request uses the price of its day, and an unknown model is not guessed.
        listing=lambda price:{'data':[{'id':'openai/gpt-x','pricing':{'prompt':str(price),'completion':str(price*4)}},{'id':'reseller/gpt-x','pricing':{'prompt':'9','completion':'9'}},
                                       {'id':'openai/gpt-x:free','pricing':{'prompt':'0','completion':'0'}}]}
        assert prices.refresh(force=True,fetch=lambda:listing(1e-6))==1
        assert prices.refresh(force=True,fetch=lambda:listing(1e-6))==0,'an unchanged price adds nothing'
        assert prices.refresh(fetch=lambda:listing(5e-6)) is None,'at most weekly unless asked'
        first=prices.load()['models']['gptx'][0][0]
        time.sleep(.01);assert prices.refresh(force=True,fetch=lambda:listing(2e-6))==1
        assert abs(prices.estimate('GPT-X',1000,100,first+.001)-(1000*1e-6+100*4e-6))<1e-12,'a request is estimated at the price of its day'
        assert abs(prices.estimate('gpt-x',1000,100,time.time())-(1000*2e-6+100*8e-6))<1e-12
        assert prices.estimate('another-model',1000,100,time.time()) is None
        prices.refresh(force=True,fetch=lambda:{'data':[{'id':'anthropic/model-y','pricing':{'prompt':'1e-6','completion':'5e-6','input_cache_read':'1e-7'}}]})
        assert abs(prices.estimate('model-y-20251001',1000,0,time.time(),cached_tokens=900)-(100*1e-6+900*1e-7))<1e-12,'cached input at its own price; a dated release is the same model'

        # Each conversation's share of its app's current plan: measured where seen, otherwise split by tokens and marked.
        now=time.time()
        app=type('App',(),{})();app.usage_accounts={'codex-events':[{'checked_at':now,'windows':[{'name':'Weekly limit','used_percent':30,'resets_at':now+86400}]}]}
        app.preferences={'usage_receipts':[{'business_id':'b','agent':'Codex','chat_id':'c1','at':now-60,'input_tokens':100,'output_tokens':0,'plan':[{'window':'Weekly limit','used':2.0}],'plan_measured':True},
                                           {'business_id':'b','agent':'Codex','chat_id':'c2','at':now-30,'input_tokens':300,'output_tokens':0},
                                           {'business_id':'b','agent':'Codex','chat_id':'old','at':now-9*86400,'input_tokens':999,'output_tokens':0}]}
        plans,shares=world._plans('b',app)
        assert plans==[{'app':'Codex','window':'Weekly limit','used_percent':30,'resets_at':now+86400}]
        assert shares['c1']=={'used':2.0,'approx':False,'window':'Weekly limit','app':'Codex'} and shares['c2']['approx'] and shares['c2']['used']==22.5 and 'old' not in shares,shares
    print('Workspace costs passed: plan shares around requests, price history kept by change, estimates at the day\'s price, plan shares by conversation.')


if __name__=='__main__':main()
