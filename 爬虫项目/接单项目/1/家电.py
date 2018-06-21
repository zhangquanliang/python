# encoding:utf-8
# @author: 张思宇
# @time: 2018-6-21 11:14
# 导入相关的模块
import requests
import time
from lxml import etree
import random

# 模仿用户的行为
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
# 伪装成浏览器的头
headers = {
    "User-Agent": random.choice(user_agent_list)
}
# 加上代理IP
proxy = [
    "221.228.17.172:8181",
    "218.241.234.48:8080",
    "221.228.17.172:8181",
    "122.114.31.177:808",
    "113.121.240.235:49911",
    "120.77.13.45:8888",
    "122.246.50.112:8010",
    "122.114.31.177:808",
    "115.153.173.238:61234",
    "110.73.8.51:8123",
    "125.118.148.169:808",
    "14.118.252.224:6666"

]


# 获取起始页的网页源码
def get_page(base_url):
    '''
    :param base_url:
    :return:
    '''
    # 随机睡眠,防止爬取的速度过快
    response = requests.get(url=base_url).text
    # 函数的返回值
    return response


# 获取详情页的链接并解析内容
def detail_page(response):
    '''
    :param response:
    :return:
    '''
    selector = etree.HTML(response)
    urls = selector.xpath('/html/body/div[2]/div/div[2]/div/div[1]/ul/li/h3/a/@href')
    demo_list = []
    for url1 in urls:
        detail_links = requests.get(url=url1).text
        html = etree.HTML(detail_links)
        last_links = html.xpath("/html/body/div[2]/div/div[4]/div[2]/div/ul/li/a/@href")
        for last_link in last_links:
            demo = str(last_link).replace("/p/1347865", '').replace("/p/1347840", '').replace("/p/1347868", '').replace(
                "/p/1347844", '').replace("/p/1347936", '')
            demo_list.append(demo)
            print(demo)
    print('共有{}个demo'.format(len(demo_list)))


# 开始进行函数的整合
def start():
    '''
    :param begin:
    :param end:
    :return:
    '''
    base_url = "http://news.newseed.cn/s553-p2"
    # 调用函数
    page = get_page(base_url)
    detail_page(page)


# 程序入口
if __name__ == '__main__':
    start()
