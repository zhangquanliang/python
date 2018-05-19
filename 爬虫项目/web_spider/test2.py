# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import xlrd
book = xlrd.open_workbook(r'Test.xls')
sheet = book.sheet_by_name('Sheet')  # 通过页签名称
nrows = sheet.nrows  # 获取行数
ncols = sheet.ncols  # 获取列数
zheng_list = []
zheng_dict = {}
for i in range(nrows):
    xingbie = sheet.row_values(i)[0]   # 通过循环行数来获取对应数据
    zhengzhuang_t = sheet.row_values(i)[1]
