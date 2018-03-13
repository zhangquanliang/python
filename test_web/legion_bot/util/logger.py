# -*- coding: utf-8 -*-

import datetime


class Logger(object):
    """
    预留可拓展logger:

    content 日志内容 ，需简明扼要
    bank_type 银行名 ，如cib,jsb
    log_type 日志类型(1:流水采集,2:登录,3:余额采集4:账户持仓采集5:其他)
    server_ip 运行机器IP(开发时不用填)
    creat_time 创建时间
    """
    # msg = "info:content[bank_type][acc_number][log_type][ip][time]"
    msg = "[{}][{}]:【{}】[{}][{}][{}][{}]"

    @staticmethod
    def time_stamp():
        # return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return datetime.datetime.now().strftime("%H:%M:%S")

    def printer(self, log_lever, content, bank_type, log_type, acc_number, server_ip, creat_time):
        print(self.msg.format(creat_time, log_lever, content, bank_type, log_type, acc_number, server_ip))

    def debug(self, content, bank_type, log_type, acc_number="", server_ip="dev", creat_time=None, *args, **kwargs):
        log_lever = "DEBUG"
        if not creat_time:
            creat_time = self.time_stamp()
        self.printer(log_lever, content, bank_type, log_type, acc_number, server_ip, creat_time)

    def info(self, content, bank_type, log_type, acc_number="", server_ip="dev", creat_time=None, *args, **kwargs):
        log_lever = "INFO"
        if not creat_time:
            creat_time = self.time_stamp()
        self.printer(log_lever, content, bank_type, log_type, acc_number, server_ip, creat_time)

    def warn(self, content, bank_type, log_type, acc_number="", server_ip="dev", creat_time=None, *args, **kwargs):
        log_lever = "WARN"
        if not creat_time:
            creat_time = self.time_stamp()
            self.printer(log_lever, content, bank_type, log_type, acc_number, server_ip, creat_time)

    def error(self, content, bank_type, log_type, acc_number="", server_ip="dev", creat_time=None, *args, **kwargs):
        log_lever = "ERROR"
        if not creat_time:
            creat_time = self.time_stamp()
            self.printer(log_lever, content, bank_type, log_type, acc_number, server_ip, creat_time)


if __name__ == '__main__':
    l = Logger()
    l.info('no content', '属羊银行', 'test', '账号8888')
    l.error('no content', '属羊银行', 'test')
