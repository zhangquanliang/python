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
            "Cookie": "cna=R3NTE12xGE0CAXFi8N3jgEXM; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; enc=OE%2FKwf%2BF15Lxhk09Nu4kR6309mOD1PMuP5MMt1WN9sxTYkXP856OGIdc5VhDjkjkOy6CXEfwU06s%2BCJVYdGjsA%3D%3D; miid=7527046761192876951; _m_user_unitinfo_=unit|unsz; _m_unitapi_v_=1508566261407; _m_h5_tk=9d5f9565b1cd7789da38cd3114b182b2_1523864804217; _m_h5_tk_enc=66c112a7ad6f49c32979474c7e9410d6; v=0; _tb_token_=f18e6798e67fe; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; uc1=cookie14=UoTePTwbXKJH7Q%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7p4sj&tag=8&cookie15=URm48syIIVrSKA%3D%3D&pas=0; uc3=nk2=CygKH0Yt%2Fdsg6Q%3D%3D&id2=VW3n%2BXqO%2BA5q&vt3=F8dBz4D93q0ZBZWg1AA%3D&lg2=URm48syIIVrSKA%3D%3D; existShop=MTUyMzkyOTE5MQ%3D%3D; lgc=heidlzzhan; tracknick=heidlzzhan; dnk=heidlzzhan; cookie2=301b86c4cb8125d3ba4d8f4ae2f86054; sg=n6a; csg=c7426ab6; mt=np=&ci=32_1; cookie1=Vq9jIMnWFPq%2FShafHqvp0%2FJjeeUNk8RaCPw0RUA3IxY%3D; unb=620037986; skt=73c295f06a454039; t=d41af883c228e56f94217f4871abf951; _cc_=W5iHLLyFfA%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=heidlzzhan; cookie17=VW3n%2BXqO%2BA5q; isg=BEZGKb20YITcKjR4p9xg9DV5mTzIp4phvO9pwjBviWlEM-dNmjeQcZGBD23_nYJ5; ucn=unsz",
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
