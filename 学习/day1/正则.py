# -*- coding: utf-8 -*-

import re
str = "<h1><src href='http://www.baidu.com'>这是一个百度标题</h1>"
reg1 = re.search('<H1><src.href=.(.*?).>', str, re.I)     # search 寻找从前往后找，找到返回一个match对象
reg2 = re.findall('abc', str, re.S | re.I)    # findall找到所有的abc，返回  re.S可换行匹配 re.I忽视大小写
reg3 = re.match('.h1', str)      # .可以匹配任意一个字符，不包括换行符
reg4 = re.match('a*', str)       # *  代表它前面的自表达式任意次(多次),匹配最多次 贪婪匹配
reg5 = re.match('aa*?', str)     # *? 按最少的情况匹配 只能匹配到一个a 非贪婪匹配
reg6 = re.match('aa*?', str,)     # () 代表字表达式，会把匹配到的内容放进缓存，返回
print(reg1.group(1))
print(reg4)
