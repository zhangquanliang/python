# -*- coding: utf-8 -*-
"""模拟用户UA"""
import fake_useragent
ua = fake_useragent.UserAgent()
print(ua.random)


"""URL加密"""
import requests
payload = {'wd': '张亚楠', 'rn': '100'}
r = requests.get("http://www.baidu.com/s", params=payload)
print(r.url)


"""重定向"""
import requests
requests.get('http://www.baidu.com',  allow_redirects=False)


"""IP代理"""
import requests
proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}
requests.get("http://www.zhidaow.com", proxies=proxies)
