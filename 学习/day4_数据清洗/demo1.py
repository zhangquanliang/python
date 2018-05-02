# -*- coding: utf-8 -*-

from pandas import Series,DataFrame, np
from numpy import nan as NA

# is(not)null，这一对方法对对象做出元素级的应用，然后返回一个布尔型数组，一般可用于布尔型索引。
# Series_data = Series(['abc', 'efgh', 'ijkl', 'mnop'])
# print(Series_data)  # 对数据清洗
# print('-' * 20)
# Series_data[0] = NA
# print(Series_data.isnull())

# dropna，对于一个Series，dropna返回一个仅含非空数据和索引值的Series。
# Series_data = Series(['abc', None, NA, 'mnop'])
# print(Series_data.dropna())  # dropna返回一个仅含非空数据和索引值的Series。


# 过滤DataFrame行的问题涉及问题序列数据
data = DataFrame(np.random.randn(7, 3))
data.ix[:4, 1] = NA
data.ix[:2, 2] = NA
print(data)
print("...........")
# print(data.dropna(thresh=2))  # dropna清除部分数据
print(data.fillna(0))   # fillna不清除数据