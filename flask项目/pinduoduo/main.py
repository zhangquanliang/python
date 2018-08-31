# -*- coding:utf-8 -*-
__author__ = '张全亮'
import cmd
import time
import pdd_status, pdd_receipt
import threading
from logger import Logger
logger = Logger()

def main():
    while True:
        try:
            current_thread = threading.current_thread()
            print('main: ', current_thread)
            thread_list = threading.enumerate()
            status_thread = threading.Thread(target=pdd_status.main)
            receipt_thread = threading.Thread(target=pdd_receipt.main)
            thread_list = threading.enumerate()
            status_thread.start()
            receipt_thread.start()
            thread_list = threading.enumerate()
            active_count = threading.active_count()
        except Exception as ex:
            logger.log('ERROR', '主线程异常: {}'.format(ex), 'Main', 'Admin')
        time.sleep(30)


if __name__ == '__main__':
    main()