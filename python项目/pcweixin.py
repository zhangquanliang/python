# -*- coding: utf-8 -*-
"""
Title = 搜狗微信公众号
Date = 2018-02-02
"""
import pdfkit
import requests
import re
import json
import fake_useragent


class SGGZH:

    def __init__(self):
        self.r = requests.session()
        self.ua = fake_useragent.UserAgent()
        self.timeout = 5
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Cache-Control": "no-cache",
            "User-Agent": self.ua.random,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer":"http://weixin.sogou.com/weixin?type=1&query=python&ie=utf8&_sug_=y"
        }

    def article(self):  # 微信历史文章
        search_html = self.get_search_result_by_keywords()
        reg = re.findall('<a target="_blank" uigs="account_name_0" href="(.*?)">', search_html)

        # 公众号地址
        url = reg[0].replace('amp;', '')
        response = self.r.get(url, headers=self.headers, timeout=self.timeout)

        article_list_html = response.text
        if article_list_html.find('验证码') > -1:
            url = 'http://mp.weixin.qq.com/mp/verifycode?cert=1521712933277.6548'
            response = self.r.get(url)
            f = open('a.png', 'wb')
            f.write(response.content)
            f.close()

        article_list = re.findall('"list":(.*?)};', article_list_html)
        reg = re.findall('content_url":"(.*?)",', article_list[0])
        for i in reg:
            url_ = "http://mp.weixin.qq.com" + i.replace('amp;', '')
            res = self.r.get(url_)
            print(res.text)
            break

    # 搜索入口地址，以公众为关键字搜索该公众号
    def get_search_result_by_keywords(self):
        url = 'http://weixin.sogou.com/weixin?type=1&query=python&ie=utf8&_sug_=y'
        response = self.r.get(url, headers=self.headers, timeout=self.timeout)
        return response.text

    def str_to_json(self, string):
        json_obj = json.dumps(string)   # 转化成json对象
        json_dict = json.loads(json_obj)    # 转化成json字典
        return json_dict


if __name__ == '__main__':
    gzh = SGGZH()
    gzh.article()