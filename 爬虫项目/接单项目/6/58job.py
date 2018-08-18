# -*- coding:utf-8 -*-
__author__ = '张全亮'
import requests
req = requests.session()


def get_jianli(job_name):
    url = 'http://qd.58.com/job/pn1/?key={}&final=1&jump=1'.format(job_name)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    response = req.get(url, headers=headers)


if __name__ == '__main__':
    job_name = '服务员'
    get_jianli(job_name)