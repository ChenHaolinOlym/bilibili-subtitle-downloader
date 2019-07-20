import requests
import json

aid = 45936507

url=f"https://api.bilibili.com/x/web-interface/view?aid={aid}"
header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
r=requests.get(url,headers=header)
sdw=r.content.decode('utf-8')
lks=json.loads(sdw)
print(lks)
