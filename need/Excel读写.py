# -*- coding: utf-8 -*-
import xlwt
import datetime
"""
Title = Excel创建
Date = 2018/03/27
"""
book = xlwt.Workbook(encoding='utf-8')  # 实例化Excel对象
sheet = book.add_sheet("Sheet")     # 添加Excel页签
sheet.write_merge(0, 0, 0, 7, 'TEst')
sheet.write(1, 0, '年龄')
sheet.write(1, 1, '地址')
for i in range(2, 10):
    sheet.write(i, 0, '张三')
    sheet.write(i, 1, '20')
    sheet.write(i, 2, '深圳')
t = datetime.datetime.now()
a = t.strftime("%Y-%m-%d")
path = r'Test%s' % str(a).replace('-', '') + '.xls'
book.save(path)


"""
Title = Excel读写
Date = 2018/03/27
"""
import xlrd
book = xlrd.open_workbook(r'Test.xls')
sheet = book.sheet_by_name('Sheet')  # 通过页签名称
nrows = sheet.nrows  # 获取行数
ncols = sheet.ncols  # 获取列数
for i in range(nrows):
    name = sheet.row_values(i)[0]   # 通过循环行数来获取对应数据
    age = sheet.row_values(i)[1]
    dizhi = sheet.row_values(i)[2]
    print(name, age, dizhi)