# -*- coding:utf-8 -*-
__author__ = '张全亮'
import cmd
import pdd_status, pdd_receipt
from multiprocessing.dummy import Pool


def main():
    while True:
        try:
            pdd_status.main()
        except:


if __name__ == '__main__':
    main()