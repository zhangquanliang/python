# -*- coding: utf-8 -*-

import datetime
import os
import json

import dateutil.parser


# 控制台输入处理函数：将控制台的入参格式化为json参数返回
def console_param_handle(argv):
    json_param = {}
    if len(argv) > 1:
        try:
            # 将字符串，转成json格式
            json_param = eval(argv[1])
        except Exception as ex:
            print("参数转换异常！", ex)
    return json_param


# 控制台输出处理函数：将数据统一处理，输出控制台
def console_result_handle(result):
    # if result['success']:
    #     result['success'] = 'true'
    # else:
    #     result['success'] = 'false'
    return result


# 返回今日日期 如 "2018-01-21"
def today_str():
    return str(datetime.date.today())


# 返回昨日日期 如 "2018-01-21"
def pre_n_day_str(n=1):
    # 昨日日期字符串
    today = datetime.date.today()
    n_days = datetime.timedelta(days=n)
    yesterday = today - n_days
    return str(yesterday)


# 读配置文件，检验是否运行时间
def is_crawl_time(bank_type):
    real_path = os.path.dirname(os.path.realpath(__file__))
    real_path = "/".join(real_path.split("\\")) + "/"
    with open(real_path + "../config/crawl_time.json") as f:
        data = json.loads(f.read())
    now_time = datetime.datetime.now()
    for running_time in data[bank_type]["running_time"].split(";"):
        start_time, end_time = map(dateutil.parser.parse, running_time.split("-"))
        if (now_time > start_time) and (now_time < end_time):
            return True
    return False


if __name__ == '__main__':
    print(is_crawl_time('jsb'))
