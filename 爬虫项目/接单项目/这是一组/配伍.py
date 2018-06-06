# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 17:09
# @Author  : 张思宇
# @Email   : zsy9426x@163.com
# @File    : 配伍.py
# @IDE: PyCharm
import csv
import re

import re
import pandas as pd


# with open('D:/1/中医临床常用对药配伍（已校对）.txt', 'r', encoding='utf8') as txtfile:
with open(r'13.txt', 'r', encoding='utf8') as txtfile:
    lines = txtfile.readlines()
    dy_list = []
    for line in lines:
        if not re.search(r'一 \d+ 一', line):

            obj = re.search(r'[(（].+对药.(.+)', line)

            if obj:
                dym = obj.group(1)
                dy_dict = {'对药': dym}
            else:
                obj2 = re.search(r'^(功用|主治|按语|常用量).(.+)*', line)
                # print(obj2)
    # #
                if obj2:
                    bt = obj2.group(1)
                    content = obj2.group(2)
                    # print(content)
                    if not content:
                        content = ''
                    dy_dict = {bt: content}
                else:
                    dy_dict = {'': line}

            dy_list.append(dy_dict)

    print(dy_list)
    # #
    # # #
    dy_list2 = []
    key_list = []
    for i, temp in enumerate(dy_list):
        # print(temp)
        for key, value in temp.items():
            if key:
                dy_list2.append(temp)
                key_list.append(key)
            else:
                # print(dy_list2)
                dy_old = dy_list2[-1:][0]
                # print(dy_old)
                dy_old[key_list[-1:][0]] += value.strip()
                dy_list2.pop()
                dy_list2.append(dy_old)
                # print(dy_old)
    #
    tmp2 = dict()
    tmp2_list = []
    #
    for i, tmp in enumerate(dy_list2):
        for key1 in tmp:
            if key1 == '对药':
                tmp2 = tmp
            else:
                tmp2 = {**tmp2, **tmp}
        tmp2_list.append(tmp2)
    #
    #
    tt2_list = []
    for i, tt in enumerate(tmp2_list):
        dy_name = tt['对药']
        tt2 = tt
        if i < len(tmp2_list)-2:
            if dy_name == tmp2_list[i+1]['对药']:
                tt2 = tmp2_list[i+1]
            else:
                tt2_list.append(tt2)
                # print(tt2)
    df = pd.DataFrame(tt2_list)
    print(df)

    df.to_csv('a3.csv', index=False, sep=',')








