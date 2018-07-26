# -*- coding:utf-8 -*-
import datetime
__author__ = '张全亮'

# 字典推导式
x = {k: str(k) for k in range(1, 4)}
print(x)

# 得到的是一个lambda对象
res = [lambda x: x*i for i in range(3)]
for i in res:
    print(i(2))

# 输入年月日，判断是当年的第几天
targetDay = datetime.date(2017, 12, 13)  #将输入的日期格式化成标准的日期
dayCount = targetDay - datetime.date(targetDay.year - 1, 12, 31)  #减去上一年最后一天
print('%s是%s年的第%s天。'% (targetDay, 2017, dayCount.days))


