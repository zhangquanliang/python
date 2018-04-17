# -*- coding: utf-8 -*-
import requests

class HuaRun:
    def __init__(self):
        self.login_url = 'http://172.31.3.83/webAuth/index.htm?www.people.com.cn/'
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
            "Referer":"http://172.31.3.83/webAuth/index.htm?www.people.com.cn/",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
        }

    def sw(self):
        data = {
            "username":"lz_cs01",
            "password":"lz_cs01@123",
            "pwd":"lz_cs01@123",
            "secret":"true"
        }
        rq = requests.session()
        response = rq.post(self.login_url, data=data)
        response.encoding='utf-8'
        html = response.text
        if '该IP已登录，请先注销' in html:
            print('已经连接，可以使用网络!')
        else:
            print('认证成功，可以使用网络!')


if __name__ == '__main__':
    huarun = HuaRun()
    huarun.sw()