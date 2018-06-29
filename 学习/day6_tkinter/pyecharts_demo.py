# -*- coding:utf-8 -*-
"""
author = zhangql
Title = 数据可视化
"""
from pyecharts import Bar, Scatter3D, Line, Overlap
from pyecharts import Page
import random

page = Page()

# 竖行条形图
bar = Bar('阳阳日常分析表','女神阳阳分析表')
bar.use_theme('dark')
# 添加条数据
bar.add('时间',['睡觉','吃饭','化妆','做饭','发呆','看电视'],[10,0.5,1,1,3,4])
# 添加条数据
bar.add('钱',['睡觉','吃饭','化妆','做饭','发呆','看电视'],[0,1,30,1,0,0.5])
page.add(bar)


# 带折线的竖行条形图
bar = Bar('阳阳日常分析表2','女神阳阳分析表')
bar.use_theme('dark')
data1 = [10,0.5,1,1,3,4]
data2 = [0,1,30,1,0,0.5]
data_line1 = [11,1.5,2,3,4,6]
data_line2 = [1,1.5,31,3,4,6]
# 添加条数据
bar.add('时间',['睡觉','吃饭','化妆','做饭','发呆','看电视'],data1)
# 添加条数据
bar.add('钱',['睡觉','吃饭','化妆','做饭','发呆','看电视'],data2)

line = Line()
line.add("时间折线",['睡觉','吃饭','化妆','做饭','发呆','看电视'],data_line1)
line.add("钱折线",['睡觉','吃饭','化妆','做饭','发呆','看电视'],data_line2)
overlap = Overlap()
overlap.add(bar)
overlap.add(line)

page.add(overlap)


# 竖行条形图标记处最大和最小
bar = Bar('阳阳日常分析表3','女神阳阳分析表')
# 添加条数据
bar.add('时间',['睡觉','吃饭','化妆','做饭','发呆','看电视'],[10,0.5,1,1,3,4],mark_point=['max','min'],mark_line='average')
# 添加条数据
bar.add('钱',['睡觉','吃饭','化妆','做饭','发呆','看电视'],[0,1,30,1,0,0.5],mark_point=['max','min'],mark_line='average')
page.add(bar)


# 层叠条形图
attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
v1 = [5, 20, 36, 10, 75, 90]
v2 = [10, 25, 8, 60, 20, 80]
bar = Bar("柱状图数据堆叠示例")
bar.add("商家A", attr, v1, is_stack=True)
bar.add("商家B", attr, v2, is_stack=True)
page.add(bar)

# 空间分布图
data = [[random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)] for _ in range(80)]
range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
               '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
scatter3D = Scatter3D("3D 散点图示例", width=1200, height=600)
scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
page.add(scatter3D)



# 横向条形图
bar = Bar("贵州GDP柱状图", "副标题")
city = ["贵阳市", "遵义市", "六盘水市", "安顺市", "黔东南州"]
data1 = [40, 30, 26, 22, 15]
data2 = [13, 43, 32, 38, 20]
bar.add("2017年GDP", city, data1)
bar.add("2016年GDP", city, data2, is_convert=True)
page.add(bar)

# 动态涟漪图
from pyecharts import EffectScatter
es = EffectScatter("动态散点图各种图形示例")
es.add("警告", [10], [10], symbol_size=20, effect_scale=3.5, effect_period=3, symbol="pin")
es.add("正唱", [20], [20], symbol_size=12, effect_scale=4.5, effect_period=4, symbol="rect")
es.add("注意", [30], [30], symbol_size=30, effect_scale=5.5, effect_period=5, symbol="roundRect")
es.add("揍你", [40], [40], symbol_size=10, effect_scale=6.5, effect_brushtype='fill', symbol="diamond")
es.add("挂挡", [50], [50], symbol_size=16, effect_scale=5.5, effect_period=3, symbol="arrow")
es.add("起飞", [60], [60], symbol_size=6, effect_scale=2.5, effect_period=3, symbol="triangle")

page.add(es)

# 仪表盘
from pyecharts import Gauge
g = Gauge("仪表盘图形","副图标")
g.add("重大项目", "投资占比", 66.66)
page.add(g)


# 水球图
from pyecharts import Liquid
liquid = Liquid("水球图")
liquid.add("Liquid", [0.3])
page.add(liquid)

# 绘制中国地图
from pyecharts import Map
value =[2, 60, 2, 6, 80, 2, 5, 2, 1, 4, 5, 1,
        4, 1, 5, 2, 2, 5, 4, 1, 1, 10, 2]
attr =["安徽", "北京", "福建", "广东", "贵州", "海南", "河北", "河南", "黑龙江",
       "湖北", "湖南", "吉林", "江苏", "辽宁", "山东", "山西", "陕西", "上海",
       "四川", "天津", "云南", "浙江", "重庆"]
map=Map("各省微信好友分布", width=1200, height=600)
map.add("china Map", attr, value, maptype='china', is_visualmap=True,
        visual_text_color='#000')
page.add(map)

# 环形图
from pyecharts import Pie
citys = ["贵阳市", "遵义市", "六盘水市", "安顺市", "黔东南州"]
citys_data1 = [11,33,23,45,34]
citys_data2 = [21,13,26,65,24]
pie = Pie("环形饼图-玫瑰图实例",title_pos = 'left',width = 900)
pie.add("商品A",citys,citys_data1,center=[25,50],is_random=True,radius = [30,75],rosetype='area',is_legend_show=True,is_label_show=False)
pie.add("商品B",citys,citys_data2,center=[75,50],is_random=True,radius = [30,75],rosetype='area',is_legend_show=False,is_label_show=True)


page.add(pie)
# 默认在根据目录输出，可以指定文件路径
page.render()