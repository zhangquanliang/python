# -*- coding:utf-8 -*-
"""
author = zhangql
"""
from openpyxl import Workbook


book = Workbook()
sheet = book.create_sheet('test')
sheet.append(['1', '2', '3'])
book.save('123.xlsx')