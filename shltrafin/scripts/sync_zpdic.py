#!/usr/bin/env python3
"""Download ZpDIC dictionary data on GitHub Actions; never expose the API key."""
import datetime,json,os,time,urllib.error,urllib.parse,urllib.request
from pathlib import Path
key=os.environ.get('ZPDIC_API_KEY')
if not key: raise SystemExit('Missing ZPDIC_API_KEY secret')
words=[];skip=0
while True:
    params=urllib.parse.urlencode({'text':'','mode':'both','type':'prefix','skip':skip,'limit':100})
    url='https://zpdic.ziphil.com/api/v1/dictionary/shltrafin/words?'+params
    req=urllib.request.Request(url,headers={'X-Api-Key':key,'Accept':'application/json','User-Agent':'shltrafin-github-pages-sync/1.0'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req,timeout=30) as resp: data=json.load(resp)
            break
        except urllib.error.HTTPError as exc:
            if exc.code==429 and attempt<3: time.sleep(2**attempt*5);continue
            raise
    batch=data.get('words',[])
    if not isinstance(batch,list): raise RuntimeError('Unexpected response')
    words.extend(batch)
    print('Fetched',len(words),'of',data.get('total','?'))
    if not batch or len(words)>=int(data.get('total',len(words))) or len(batch)<100:break
    skip+=len(batch)
    time.sleep(.3)
# Validate before replacing last known-good data
if not isinstance(words,list):raise RuntimeError('Invalid word list')
out={'updatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'total':len(words),'words':words}
Path('data/words.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
