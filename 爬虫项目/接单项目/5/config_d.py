# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import pymysql
import cx_Oracle

db_setting = {
    'host': 'localhost',   # IP地址，本机为localhost
    'db': 'spider_j',     # 数据库
    'user': 'root',        # 用户名
    'passwd': 'zql9988',   # 密码
    'charset': 'utf8',     # 默认连接编码
    'use_unicode': True
}


# 配置数据库连接（普通插入）
def mysql_tools():
    connect = pymysql.connect(
    host=db_setting['host'],   # IP地址，本机为localhost
    db=db_setting['db'],     # 数据库
    user=db_setting['user'],        # 用户名
    passwd=db_setting['passwd'],   # 密码
    charset=db_setting['charset'],     # 默认连接编码
    use_unicode=db_setting['use_unicode'])
    return connect.cursor(), connect


def oracle_tools():
    connect = cx_Oracle.connect('tcmp/tcmp@192.168.1.7:1521/orcl')  # 连接数据库
    # c = connect.cursor()  # 获取cursor
    # x = c.execute(sql)  # 使用cursor进行各种操作
    # res = x.fetchall()
    # c.close()  # 关闭cursor
    # conn.close()  # 关闭连接
    return connect.corsor(), connect


# 用户代理池
headers_list = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
    'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'
]
