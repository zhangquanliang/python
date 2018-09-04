# -*- coding: utf-8 -*-
import pymysql

from twisted.enterprise import adbapi
from twisted.internet import reactor
import dateutil.parser
import datetime
pymysql.install_as_MySQLdb()

db_setting = {
    'host': 'localhost',   # IP地址，本机为localhost
    'db': 'dianshang',     # 数据库
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


# 异步插入
def mysql_synchronous(sql):
    try:
        # 生成连接池
        db_conn = adbapi.ConnectionPool('pymysql', db_setting)
        # 通过连接池执行具体的sql操作，返回一个对象
        query = db_conn.runInteraction(go_insert, sql)
        # 对错误信息进行提示处理
        query.addCallbacks(handle_error)
    except Exception as e:
        print(e)
    # 定时，给4秒时间让twisted异步框架完成数据库插入异步操作，没有定时什么都不会做
    reactor.callLater(4, reactor.stop)
    reactor.run()


def go_insert(cursor, sql):
    # 对数据库进行插入操作，并不需要commit，twisted会自动帮我commit
    try:
        for i in range(10):
            data = str(i)
            cursor.execute(sql, data)
    except Exception as e:
        print(e)


def handle_error(failure):
    # 打印错误
    if failure:
        print(failure)


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