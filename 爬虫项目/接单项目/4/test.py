# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import requests
res = requests.get('http://www.4756.co/qzbzsg/searchShiFu.php?uid=oVSYq1ILccv7mOkPteE78qe87r-E&lat=39.910924&lng=116.413387')
print(res.text)