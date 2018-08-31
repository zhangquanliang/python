# -*- coding: utf-8 -*-

import datetime
import os
import time
import random
import logging


class Logger(object):

    def __init__(self):
        self.logger = logging.getLogger()  # 生成一个日志对象，（）内为日志对象的名字，可以不带，名字不给定就是root，一般给定名字，否则会把其他的日志输出也会打印到你的文件里。
        handler = logging.FileHandler("Log.txt")  # 生成一个handler（处理器），
        # formatter 下面代码指定日志的输出格式
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)  # 实例化formatter
        handler.setFormatter(formatter)  # 为handler添加formatter
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.NOTSET)  # 设置日志输出信息的级别

    """
    预留可拓展logger:

    content 日志内容 ，需简明扼要
    log_type 日志类型(1:spider, 2:status, 3:其他)
    creat_time 创建时间
    """
    # msg = "info:content[log_type][pdduid][time]"
    msg = "[{}][{}]:【{}】【{}】[{}]"
    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)).split('logger')[0], 'log')

    @staticmethod
    def time_stamp():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # return datetime.datetime.now().strftime("%H:%M:%S")

    def printer(self, log_lever, content, log_type, pdduid, create_time):
        print(self.msg.format(create_time, log_lever, content, log_type, pdduid))

    def log(self, log_lever, content, log_type, pdduid, creat_time=None):
        if not creat_time:
            creat_time = self.time_stamp()
        self.printer(log_lever, content, log_type, pdduid, creat_time)
        self.__save(log_lever, content, log_type, pdduid, creat_time)

    def __save(self, log_lever, content, log_type, pdduid, creat_time):
        try:
            create_data = datetime.datetime.now().strftime("%Y%m%d")
            if not os.path.exists(os.path.join(self.save_dir, create_data)):
                os.makedirs(os.path.join(self.save_dir, create_data))
            path = os.path.join(self.save_dir, create_data)
            if not os.path.exists(os.path.join(path, log_type)):
                os.makedirs(os.path.join(path, log_type))
            save_time = datetime.datetime.now().strftime("%Y%m%d %H%M%S")
            with open(os.path.join(path, log_type + '\\' + save_time + '.log'), 'a', encoding='utf-8') as f:
                f.write(self.msg.format(log_lever, content, log_type, pdduid, creat_time) + '\n')
        except Exception as ex:
            print(ex)
            print('log save error!')


if __name__ == '__main__':
    l = Logger()
    l.log('INFO', 'Test', 'spider', '123')
