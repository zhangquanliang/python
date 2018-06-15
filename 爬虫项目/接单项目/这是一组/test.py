# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import pandas as pd
import xlwt
import re

book = xlwt.Workbook(encoding='utf-8')  # 实例化Excel对象
sheet = book.add_sheet("Sheet")     # 添加Excel页签
# sheet.write_merge(0, 0, 0, 7, 'python专属')
# w = 2
# sheet.write(1, 0, '章节')
# sheet.write(1, 1, '内容')

with open('14.txt', 'r', encoding='utf8') as f:
    f_data = f.read()

# reg = re.findall('(.*?)\n', str(f_data), re.S | re.I)
# for i in reg:
#     print(i)
reg = re.findall('第(.)章', str(f_data), re.S | re.I)
for i in range(len(reg)):
    if i <= 4:
        reg1 = re.findall('第{}章(.*?)第{}章'.format(reg[i], reg[i+1]), str(f_data), re.S | re.I)[0]
        reg2 = re.findall('(.*?)\n―、', str(reg1).replace('"', ''), re.S | re.I)
        print(reg2)
    else:
        reg1 = re.findall('第{}章(.*?)见于恶核等'.format(reg[i]), str(f_data), re.S | re.I)
        reg2 = re.findall('(.*?)\n―、', str(reg1).replace('"', ''), re.S | re.I)
    # print(reg1)
    # print(len(reg2))
    # print(reg2)
    # print(reg2)
    # break
    # sheet.write(w, 0, '第{}章'.format(reg[i]))
    # sheet.write(w, 1, reg1)
    # w += 1

# path = r'文件.xls'
# book.save(path)

