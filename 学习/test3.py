# -*- coding:utf-8 -*-
"""
author = zhangql
"""
lst = ["'HONDA', 'Accord', '1993', '2003', 'CBHO-26', 'CC7/CE8,CE5,CE9...','Left/Right Lower              '"]
a = lst[0].replace("'", '')
d = a.split(',')
c = d[-4:-1]
x = str(c).replace('"', '').replace("'", '').replace('[', '').replace(']', '')
d.remove('CE5')
d.remove('CE9...')
d.remove(' CC7/CE8')
d.insert(-1, x)
print(d)