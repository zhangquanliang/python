# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import re
# re.match是从字符串首字母处匹配
# re.search是遍历整个字符串匹配

str1 = "<abc>aaa</abc>"
a = re.match('>', str1)
print(a)