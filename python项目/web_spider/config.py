# -*- coding: utf-8 -*-
import pymysql
import os
import sys
import json
import dateutil.parser
import datetime
pymysql.install_as_MySQLdb()


# 配置数据库连接
def mysql_tools():
    connect = pymysql.connect(
    host="localhost",   # IP地址，本机为localhost
    db="dianshang",     # 数据库
    user="root",        # 用户名
    passwd="zql9988",   # 密码
    charset='utf8',     # 默认连接编码
    use_unicode=True)
    return connect.cursor(), connect


# 脚本程序设置运行时间
crawl_time = {
    "running_time": "10:10-10:12;15:20-15:21"
}


# 定时启动任务
def run_time():
    now_time = datetime.datetime.now()
    for running_time in crawl_time["running_time"].split(";"):
        start_time, end_time = map(dateutil.parser.parse, running_time.split("-"))
        if (now_time > start_time) and (now_time < end_time):
            return True
    return False
