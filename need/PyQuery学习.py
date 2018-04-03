# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq


# 参数为字符串的情况
html_str = "<html></html>"

# 参数为网页链接（需带 http：//）
your_url = "http://www.baidu.com"

# 参数为文件
path_to_html_file = "hello123.html"

# 将参数传入pq库之后得到html页面
# d = pq(html_str)
# d = pq(etree.fromstring(html_str))
# d = pq(url=your_url)
# d = pq(url=your_url,
#        opener=lambda url, **kw: urlopen(url).read())
d = pq(filename=path_to_html_file)

# 此时的'd'相当于Jquery的'$',选择器,可以通过标签,id,class等选择元素

# 通过id选择
table = d("#my_table")

# 通过标签选择
head = d("head")

# 通过样式选择,多个样式写一起,使用逗号隔开即可
p = d(".p_font")

# 获取标签内的文本
text = p.text()
print(text)

# 获取标签的属性值
t_class = table.attr('class')
print(t_class)

# 遍历标签内的选项
# 打印表格中的td中的文字
for item in table.items():
    # 这个循环只循环一次,item仍然是pquery的对象
    print(item.text())

for item in table('td'):
    # 这个循环循环多次,item是html的对象
    print(item.text)