# -*- coding: utf-8 -*-
"""
拉钩网招聘信息
"""
import requests
import urllib3
import json
import re
import time
import fake_useragent
from bs4 import BeautifulSoup
from urllib import parse
urllib3.disable_warnings()
ua = fake_useragent.UserAgent()
ip_temp_list = []   # 用于接收西刺上的HTTPS IP


def go(job_name, city):
    query2 = {
        "list_": job_name
    }
    can2 = parse.urlencode(query=query2).replace('=', '')

    query = {
        "city": city,
        "cl": "false",
        "fromSearch": "true",
        "labelWords": "",
        "suginput": ""
    }
    can1 = parse.urlencode(query=query)
    url1 = 'https://www.lagou.com/jobs/%s?%s' % (can2, can1)

    req = requests.session()
    req.get('https://www.lagou.com/')
    headers1 = get_headers('https://www.lagou.com/')
    html = req.get(url=url1, headers=headers1, verify=False).text

    soup = BeautifulSoup(html, 'html.parser')
    zhiwei = soup.find('a', id='tab_pos')
    number_html = zhiwei.get_text()
    a = re.search('[1-9]\d*', number_html)
    number = int(a.group(0))    # 得到当前查询职位所在城市的招聘数量
    print(number)
    page = int(number/15)
    for i in range(1, page+2):
        print(i)
        try:
            user_agent = ua.random  # 使用随机USER_AGENT
        except:
            user_agent = ua.random
        query3 = {
            "city": city
        }
        can3 = parse.urlencode(query=query3)
        for j in range(3):
            url2 = 'https://www.lagou.com/jobs/positionAjax.json?px=default&%s' % can3 + '&needAddtionalResult=false&isSchoolJob=0'

            kd = "%s" % job_name
            data = {
                "first": "true",
                "pn": i,
                "kd": kd,
            }
            headers2 = get_headers(url1)
            response = req.post(url=url2, data=data, headers=headers2, verify=False).text
            print(response)
            try:
                if json.loads(response)['success'] == True:
                    position_list = json.loads(response)['content']['positionResult']['result']
                    position_list_size = json.loads(response)['content']['positionResult']['resultSize']
                    parser_position(position_list, position_list_size)
                    break
                else:
                    continue
            except Exception as e:
                print(e)
            time.sleep(2)


def get_headers(url):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.lagou.com",
        "Referer": url,
        "Origin": "https://www.lagou.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "X-Anit-Forge-Code": "0",
        "X-Anit-Forge-Token": "None",
        "X-Requested-With": "XMLHttpRequest"
    }
    return headers


# IP集合
def ip_list():
    req = requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    a = req.get(url='http://www.xicidaili.com/nn/', headers=headers)
    htm = (a.text)
    soup = BeautifulSoup(htm, 'html.parser')
    ip_list = soup.find('table', id='ip_list')
    ip_list_tr = ip_list.find_all('tr')
    file = open('ip.txt', 'w+')
    for x in range(1, len(ip_list_tr)):
        ip = ip_list_tr[x]
        tds = ip.findAll("td")
        ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
        https = tds[5].contents[0]
        if https == 'HTTP':
            continue
        ip_temp_list.append(ip_temp)


# 解析职位信息
def parser_position(position_list, position_list_size):
    # print(position_list['resultSize'])
    for i in range(int(position_list_size)):
        job_list = position_list[i]
        formatCreateTime = job_list['formatCreateTime']  # 发布日期
        positionName = job_list['positionName']  # 职位名称
        workYear = job_list['workYear']   # 工作经验
        salary = job_list['salary']  # 薪资
        education = job_list['education']  # 学历
        jobNature = job_list['jobNature']  # 工作类型
        city = job_list['city']  # 城市
        companyFullName = job_list['companyFullName']  # 公司名称
        positionAdvantage = job_list['positionAdvantage']   # 公司诱惑
        industryField = job_list['industryField']   # 公司领域
        companySize = job_list['companySize']  # 公司规模
        financeStage = job_list['financeStage']  # 公司现状
        companyLabelList = job_list['companyLabelList']  # 待遇
        positionLables = job_list['positionLables']  # 公司招聘
        district = job_list['city'] + " " +job_list['district']   # 上班地点
        print('职位名称:%s 工作经验:%s 薪资:%s 学历:%s 上班地点:%s 公司名称:%s 公司规模:%s 公司现状:%s 待遇:%s'
              % (positionName, workYear, salary, education, district, companyFullName, companySize, financeStage, companyLabelList))


if __name__ == '__main__':
    job_name = input('请输入你想要获取的职位信息 :')
    city = input('请输入你想要工作城市: ')
    # ip_list()
    go(job_name, city)

