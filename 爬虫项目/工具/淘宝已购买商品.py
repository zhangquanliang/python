# -*- coding: utf-8 -*-
"""
Title = 淘宝已购买信息
Date = 20180416
"""
import requests
import re
import json


class TaoBao:
    """淘宝已购买数据"""
    def __init__(self):
        self.headers = {
            "Cookie": "thw=cn; miid=7527046761192876951; enc=5uJ32OyvFoHJG6LElX2uw92uKWY%2ByZnbtjIhQmGXhFUAk8XcUVueiO%2B4b6%2BZv85o6tIvi3GmuEH52CONZnuN6g%3D%3D; UM_distinctid=163873d82dd1a3-04d73ded4ac9d5-4d015463-100200-163873d82dece; hng=CN%7Czh-CN%7CCNY%7C156; cna=R3NTE12xGE0CAXFi8N3jgEXM; ali_ab=113.98.240.221.1528876668966.1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _m_h5_tk=9f6e1f657f96218d3bf4e7da1b6e4730_1531736236123; _m_h5_tk_enc=df9e54e9134e9fea7dd4a74949eb9216; v=0; _tb_token_=5b418bd7b693e; unb=620037986; uc1=cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=U%2BGCWk%2F7p4sj&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTfKjysnZt%2F8Q%3D%3D&tag=8&lng=zh_CN; sg=n6a; t=d41af883c228e56f94217f4871abf951; _l_g_=Ug%3D%3D; skt=76bfa4ceee8772c6; cookie2=3bb3680f4200945d015746a31af8ac35; cookie1=Vq9jIMnWFPq%2FShafHqvp0%2FJjeeUNk8RaCPw0RUA3IxY%3D; csg=66be77b6; uc3=vt3=F8dBzrhCnD5yVbyquzM%3D&id2=VW3n%2BXqO%2BA5q&nk2=CygKH0Yt%2Fdsg6Q%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; existShop=MTUzMTgxNzI3Mg%3D%3D; tracknick=heidlzzhan; lgc=heidlzzhan; _cc_=U%2BGCWk%2F7og%3D%3D; dnk=heidlzzhan; _nk_=heidlzzhan; cookie17=VW3n%2BXqO%2BA5q; tg=0; mt=ci=41_1&np=; isg=BBgYs1iL97YjFdqyxfoW7vcH50aqAXyLPmGHCFIJu9MG7bnX-xEZG-yPIWf4RjRj; ucn=unsz",
            "user-agent": "Mozilla/1.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a1z02.1.a2109.d1000368.ac22782dMZVXzl&nekot=1470211439694"
            }
        self.money = 0

    def parser_json(self, json_list, type):
        for buy_ in json_list['mainOrders']:
            buy_id = buy_['id']  # 订单号
            buy_time = buy_['orderInfo']['createDay']  # 日期
            buy_money = buy_['payInfo']['actualFee']  # 金额
            self.money += float(buy_money)
            if type == 1 or type == '1':
                buy_name = buy_['subOrders'][0]['itemInfo']['title'].replace('u', '\\u').encode('utf-8').decode(
                    'unicode_escape')
                try:
                    user_name = buy_['seller']['shopName'].replace('u', '\\u').encode('utf-8').decode(
                        'unicode_escape')  # 店铺名称
                except:
                    user_name = ''
            else:
                buy_name = buy_['subOrders'][0]['itemInfo']['title']
                try:
                    user_name = buy_['seller']['shopName']
                except:
                    user_name = ''
            print('订单号:{} 日期:{} 金额:{} 商品:{} 店铺:{}'.format(buy_id, buy_time, buy_money, buy_name, user_name))

    # 第一页淘宝已购买数据
    def first_page(self):
        url = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a1z02.1.a2109.d1000368.ac22782dMZVXzl&nekot=1470211439694'
        response = requests.get(url, headers=self.headers)
        html = response.text.replace('\\', '')
        reg = re.findall('{"error":(.*?)"type":"t3"}', html, re.S | re.I)
        list_buy = '{"error":' + reg[0] + '"type":"t3"}]}'
        json_list = json.loads(list_buy)
        self.parser_json(json_list, 1)
        return json_list['page']['totalPage']

    # 下一页淘宝已购买数据
    def next_page(self, page):
        for i in range(1, page+1):
            url = 'https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&_input_charset=utf8'
            data = {
                "queryOrder": "desc",
                "pageSize": "15",
                "prePageNo": i,
                "pageNum": i+1
            }
            response = requests.post(url, data=data, headers=self.headers)
            self.parser_json(json.loads(response.text), i+1)
        print(u'共消费金额: {}'.format(self.money))


if __name__ == '__main__':
    taobao = TaoBao()
    page = taobao.first_page()
    taobao.next_page(int(page))
