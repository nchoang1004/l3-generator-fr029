from pathlib import Path
import json,os,tomllib,sys,urllib.request,time
sys.path.insert(0,str(Path('slice').resolve()))
from l3slice.docagent import OpenAICompatProvider,Budget,ProviderError
from l3slice.docpipeline import run_documents
root=Path('ket-qua-chay/api-budget-050-20261011-r2');root.mkdir(exist_ok=True)
key=tomllib.loads(Path('C:/Users/dell/.codeboarding/config.toml').read_text(encoding='utf-8-sig'))['provider']['openai_api_key']
os.environ['L3_TEST_KEY']=key
provider=OpenAICompatProvider('https://api.openai.com/v1','gpt-4.1-mini-2025-04-14','L3_TEST_KEY',max_output_tokens=4000,prices=(.4,.1,1.6),timeout=60)
provider.WAITS=0;provider.NET_RETRIES=0
original=urllib.request.urlopen
ledger=[];reserved=0.0221356
def guarded(req,*a,**kw):
 global reserved
 reserved=0.0221356+provider.cost_usd
 if not isinstance(req,urllib.request.Request) or req.full_url!='https://api.openai.com/v1/chat/completions':raise ProviderError('UNEXPECTED_ENDPOINT',False)
 payload=json.loads(req.data)
 upper=((len(req.data)+10000)*.4+payload['max_completion_tokens']*1.6)/1e6
 if reserved+upper>.45:raise ProviderError('LOCAL_BUDGET_RESERVATION_STOP',False)
 reserved+=upper
 ledger.append({'request':len(ledger)+1,'reserved_upper_usd':upper,'total_reserved_usd':reserved})
 (root/'budget.json').write_text(json.dumps(ledger,indent=2))
 print('request',len(ledger),'reserved',round(reserved,5),flush=True)
 return original(req,*a,**kw)
urllib.request.urlopen=guarded
try:
 data=run_documents(Path('D:/VSF/l3-generator-quote-evidence/sample-repos/teamhide_fastapi-boilerplate-df4e6d4'),root/'output',Path('ket-qua-chay/fr029-20261002/teamhide-existing.membership.json'),'teamhide',provider,budget=Budget(max_turns=120,max_tokens=1500000,max_seconds=600,retries=0,max_cost_usd=.45),run_id='run_paid_teamhide_20261011')
 print('OUTPUT',list(data),flush=True)
except Exception as e:
 print('ERROR_TYPE',type(e).__name__,flush=True)
finally:
 (root/'cost.json').write_text(json.dumps({'model':provider.model,'usage_based_cost_usd':provider.cost_usd,'reserved_upper_usd':reserved,'requests':len(ledger),'budget_usd':.5,'prior_run_cost_usd':.0221356,'combined_usage_cost_usd':.0221356+provider.cost_usd},indent=2))
 print('COST',provider.cost_usd,flush=True)
