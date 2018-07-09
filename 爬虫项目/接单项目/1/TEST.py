# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import requests
# import execjs
headers = {
    "Connection":"keep-alive",
    "Host":"www.517.cn",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Cookie": "website_cityid=1; website_qiehuan_cityid=1; website_cityname=%e6%b2%88%e9%98%b3; safedog-flow-item=6C36E765; Hm_cv_1f8e83330039496a701d7ae44836ed10=1*userType*visitor; ASP.NET_SessionId=nf0loiv30mqtylfbut1k4tdz; Hm_lvt_1f8e83330039496a701d7ae44836ed10=1531053184,1531059950; BPC=3febd9c962bb1f84d42ffba4df6b5274; Hm_lpvt_1f8e83330039496a701d7ae44836ed10=1531061541",
}


req = requests.session()
res = req.get('http://www.517.cn/website/Ashx/HouseHandler.ashx?action=ershoufang&pagename=houselist&url=www.517.cn%2Fershoufang%2Fpgq1%253Fckattempt%253D1%2Fpg1%2F&radius=3000&pageIndex=1&pageSize=20', headers=headers)
res.encoding = 'utf-8'
# res2 = req.get('http://www.517.cn/ershoufang/pgq1?ckattempt=1')
# execjs.eval("https://g.517cdn.com/www517cn/js/aes.min.js")
# res2.encoding = 'utf-8'
print(res.text)