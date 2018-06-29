# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq

# doc = pq(filename='hello.html')
# li = doc('li')
# print(type(li))
# print(li.text())

"""属性操作"""
# p1 = pq('<p id="hello1" value="张三"></p>')
# p2 = pq('<p id="hello1" class="hello2" value="张三"></p>')('p')
# print(p.attr('value'))
# print(p.attr('id', '321'))   # 后面321不传为取id的值
# print(p1.add_class('beaturl'))  # 添加class，有就追加class
# print(p1.remove_class('beaturl'))  # 删除class
# print(p1.css('font-size', '20px'))  # 增加样式
# print(p1.css('background-color', 'red'))  # 增加样式


"""DOM操作"""
# p = pq('<p id="hello" class="hello"></p>')
# print(p.append('check out <a href="http://reddit.com/r/python"><span>reddit</span></a>'))
# print(p.prepend('Oh yes!'))
# d = pq('<div class="wrap"><div id="test"><a href="http://cuiqingcai.com">Germy</a></div></div>')
# print(d.empty())


"""遍历"""
# doc = pq(filename='hello.html')
# lis = doc('li')
# print(lis.eq(5).text())
# for li in lis.items():
#     f = pq(li).eq(0).text()
#     print(f)

"""网页请求"""
# print(pq('http://cuiqingcai.com/', headers={'user-agent': 'pyquery'}))  # get请求
# print(pq('http://httpbin.org/post', data={'foo': 'bar'}, method='post', verify=True))  # post请求
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
# }
# doc = pq('http://www.yuncaijing.com/data/lhb/main.html', headers=headers, verify=False)
# print(doc)
url = 'https://ebank.95559.com.cn/CEBS/aq/cb0121_enterpriseAuthAccQry.do'
headers = {
            "Cookie": ";JSESSIONID=0000Yc003O1Fv7TI7H2bQDowcUn:-1;com.bocom.cebs.base.resolver.CEBSSmartLocaleResolver.LOCALE=zh_CN",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; HCTE; InfoPath.3)"
        }
data = {
    # "accName": acc_name,
    "accNo": "443066467011803011021",
    "beginDate": "20180626",
    "endDate": "20180626",
    "step": "_ql"
}
doc = pq(url=url, headers=headers, data=data)
with open('shuju.html', 'a+', encoding='utf-8') as f:
    f.write(doc.html())