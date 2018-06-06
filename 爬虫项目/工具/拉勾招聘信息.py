# -*- coding: utf-8 -*-
"""
Title = 拉钩爬虫及可视化
Date = 2018-03-27
"""
import requests
import urllib3
import json
import re
import random
import time
import datetime
import xlwt
from bs4 import BeautifulSoup
from urllib import parse
urllib3.disable_warnings()
position_job_list = []


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
    headers1 = get_headers('https://www.lagou.com/')
    html = req.get(url=url1, headers=headers1, verify=False).text
    n_cookie = req.cookies.get_dict()['SEARCH_ID']
    req.cookies['SEARCH_ID'] = n_cookie
    soup = BeautifulSoup(html, 'html.parser')
    zhiwei = soup.find('a', id='tab_pos')
    number_html = zhiwei.get_text()
    a = re.search('[1-9]\d*', number_html)
    number = int(a.group(0))    # 得到当前查询职位所在城市的招聘数量
    print('查询城市{}共有{}个相关岗位:'.format(city, number))
    page = int(number/15)

    for i in range(1, page+2):
        query3 = {
            "city": city
        }
        can3 = parse.urlencode(query=query3)

        url2 = 'https://www.lagou.com/jobs/positionAjax.json?px=default&%s' % can3 + '&needAddtionalResult=false&isSchoolJob=0'

        kd = "%s" % job_name
        data = {
            "first": "true",
            "pn": i,
            "kd": kd,
        }
        headers2 = get_headers(url1)
        response = req.post(url=url2, data=data, headers=headers2, verify=False).text

        if json.loads(response)['success'] == True:
            position_list = json.loads(response)['content']['positionResult']['result']
            position_list_size = json.loads(response)['content']['positionResult']['resultSize']
            parser_position(position_list, position_list_size)

        time.sleep(8)
    save_excel(position_job_list)


# 浏览器伪装
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
        "User-Agent": "Mozilla/1.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "X-Anit-Forge-Code": "0",
        "X-Anit-Forge-Token": "None",
        "X-Requested-With": "XMLHttpRequest"
    }
    return headers


# 解析职位信息
def parser_position(position_list, position_list_size):
    for i in range(int(position_list_size)):
        dict_ = {}
        job_list = position_list[i]
        formatCreateTime = job_list['formatCreateTime']  # 发布日期
        positionName = job_list['positionName']  # 职位名称
        workYear = job_list['workYear']   # 工作经验
        salary = job_list['salary']  # 薪资
        education = job_list['education']  # 学历
        jobNature = job_list['jobNature']  # 工作类型
        # city = job_list['city']  # 城市
        companyFullName = job_list['companyFullName']  # 公司名称
        # positionAdvantage = job_list['positionAdvantage']   # 公司诱惑
        # industryField = job_list['industryField']   # 公司领域
        companySize = job_list['companySize']  # 公司规模
        # financeStage = job_list['financeStage']  # 公司现状
        companyLabelList = job_list['companyLabelList']  # 待遇
        # positionLables = job_list['positionLables']  # 公司招聘
        district = job_list['city'] + " " +job_list['district']   # 上班地点

        dict_['formatCreateTime'] = formatCreateTime
        dict_['positionName'] = positionName
        dict_['workYear'] = workYear
        dict_['salary'] = salary
        dict_['education'] = education
        dict_['jobNature'] = jobNature
        dict_['companyFullName'] = companyFullName
        dict_['companySize'] = companySize
        dict_['companyLabelList'] = companyLabelList
        dict_['district'] = district
        position_job_list.append(dict_)


# 将数据保存为Excel
def save_excel(position_job_list):
    t = datetime.datetime.now()
    now_date = t.strftime("%Y-%m-%d")
    book = xlwt.Workbook(encoding='utf-8')  # 实例化Excel对象
    sheet = book.add_sheet("Sheet")  # 添加Excel页签
    sheet.write_merge(0, 0, 0, 10, '{}拉钩网{}岗位招信息详情表'.format(now_date, job_name))
    sheet.write(1, 0, '发布日期')
    sheet.write(1, 1, '职位名称')
    sheet.write(1, 2, '工作经验')
    sheet.write(1, 3, '薪资')
    sheet.write(1, 4, '学历')
    sheet.write(1, 5, '工作类型')
    sheet.write(1, 6, '工作地点')
    sheet.write(1, 7, '公司名称')
    sheet.write(1, 8, '公司规模')
    sheet.write(1, 9, '公司待遇')
    for i in range(len(position_job_list)):
        position_job = position_job_list[i]
        sheet.write(i + 2, 0, position_job['formatCreateTime'])
        sheet.write(i + 2, 1, position_job['positionName'])
        sheet.write(i + 2, 2, position_job['workYear'])
        sheet.write(i + 2, 3, position_job['salary'])
        sheet.write(i + 2, 4, position_job['education'])
        sheet.write(i + 2, 5, position_job['jobNature'])
        sheet.write(i + 2, 6, position_job['district'])
        sheet.write(i + 2, 7, position_job['companyFullName'])
        sheet.write(i + 2, 8, position_job['companySize'])
        sheet.write(i + 2, 9, position_job['companyLabelList'])

    book.save(r'[{}]拉钩网[{}]岗位招聘信息表.xls'.format(str(now_date).replace('-', ''), job_name))


if __name__ == '__main__':
    job_name = input('请输入你想要获取的职位信息 :')
    city = input('请输入你想要工作城市: ')
    go(job_name, city)
