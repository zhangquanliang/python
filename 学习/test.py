# -*- coding: utf-8 -*-
import pandas

import requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Proxy-Connection":"keep-alive",
    "Range":"bytes=0-",
    "Accept":"*/*",
    "Accept-Encoding":"identity;q=1, *;q=0"
}
url = 'https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200f190000bbvb9nignbh5ubla0go0&line=0'
res = requests.get(url, verify=False, headers=headers, allow_redirects=False)
print(res.headers)
url1 = res.headers['Location']
headers["Referer"] = url1
res2 = requests.get(url1, headers=headers, verify=False)
print(res2.status_code)
with open('video.mp4', 'wb') as f:
    f.write(res2.content)

