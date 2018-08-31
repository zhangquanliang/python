# -*- coding:utf-8 -*-
__author__ = '张全亮'
import re
import random
import urllib3
import requests
import urllib.parse
import time

urllib3.disable_warnings()
req = requests.session()
import pymysql
from logger import Logger
from bs4 import BeautifulSoup

pymysql.install_as_MySQLdb()

# TODO 需要提供goods_url(商品地址), pdduid(拼多多用户ID,可为手机号), accesstoken(websocket加载的token)

"""
goods_url = 商品地址
goods_id = 商品ID
group_id = 分组排序ID
sku_id = 商品的属性ID,如衣服的尺码，颜色
cookie = 需要登陆状态下的Cookie
accesstoken = 支付认证的token
pdduid  = 拼多多用户ID
order_sn = 订单编号
"""

logger = Logger()

headers = {
    'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
}

"""
input = 分组排序ID(group_id), 商品ID(goods_id), 商品属性ID(sku_id), 用户ID(pdduid), 
支付宝登陆成功认证的token(accesstoken), 地址ID(address_id)
output = 付款地址(pay_url)
"""


def pay(alipay, address_id, pdduid, accesstoken, sku_id, group_id, goods_id):
    url = 'https://api.pinduoduo.com/order?pdduid={}'.format(pdduid)
    headers['Referer'] = 'https://mobile.yangkeduo.com/order_checkout.html?sku_id={}&group_id={}&goods_id={}&' \
                         'goods_number=1'.format(sku_id, group_id, goods_id)
    headers['accesstoken'] = accesstoken
    json_str = {
        "address_id": address_id,
        "goods": [{"sku_id": sku_id, "sku_number": 1, "goods_id": goods_id}],
        "group_id": group_id,
        "duoduo_type": 0,
        "biz_type": 0,
        "source_channel": -1,
        "source_type": 0,
        "app_id": 9,
        "is_app": "0",
        "version": 1
    }

    # 循环请求，3次请求仍获取不到，则判断token失效
    order_sn = ''
    for i in range(3):
        time.sleep(random.random())
        res = requests.post(url, headers=headers, json=json_str, verify=False)
        res_json = res.json()
        if 'order_sn' in res_json:
            order_sn = res_json['order_sn']
            break
        elif 'error_code' in res_json and i == 2:
            return False, 'access_token错误, 请更新.'
        else:
            continue

    if alipay:
        logger.log('INFO', '订单: [{}], 支付方式: 支付宝支付'.format(order_sn), 'spider', pdduid)
        url2 = 'https://api.pinduoduo.com/order/prepay?pdduid={}'.format(pdduid)
        t_data = {
            "order_sn": order_sn,
            "app_id": 9,
            "return_url": "https://mobile.yangkeduo.com/alipay_callback.html?order_sn={}".format(order_sn),
            "version": 2,
            "attribute_fields": {"paid_times": 0}
        }
        res2 = requests.post(url2, headers=headers, verify=False, json=t_data)
        xiadan_json = res2.json()
        gateway_url = xiadan_json['gateway_url']
        query = xiadan_json['query']
        a = urllib.parse.urlencode(query)
        dingdan_url = gateway_url + '?' + a
        response = requests.get(dingdan_url, headers=headers, verify=False)
        pay_url = response.url
    else:
        logger.log('INFO', '订单: [{}], 支付方式: 微信支付'.format(order_sn), 'spider', pdduid)
        url2 = 'https://api.pinduoduo.com/order/prepay?pdduid={}'.format(pdduid)
        t_data = {
            "order_sn": order_sn,
            "app_id": 38,
            "pap_pay": 1,
            "version": 1,
            # "attribute_fields": {"paid_times": 0}
        }
        res = requests.post(url2, headers=headers, verify=False, json=t_data)
        xiadan_json = res.json()
        nweb_url = xiadan_json['mweb_url']
        headers['Referer'] = 'https://mobile.yangkeduo.com/wechat_h5_pay_callback.html?order_sn={}'.format(order_sn)
        res2 = requests.get(nweb_url, headers=headers, verify=False)
        pay_url = re.findall('var url="(.*?)";', res2.text, re.I | re.S)[0]
    return order_sn, pay_url


"""
获取需要的地址ID
input = 分组排序ID(group_id), 商品ID(goods_id), 商品的属性ID(sku_id)如衣服的尺码，颜色 购买数量(goods_number)
output = 地址ID(addressId)
"""


def get_address_id(sku_id, group_id, goods_id, amount, goods_number=1):
    url = 'https://mobile.yangkeduo.com/order_checkout.html?sku_id={}&group_id={}&goods_id={}&goods_number={}'.format(
        sku_id, group_id, goods_id, goods_number)
    res = requests.get(url, headers=headers, verify=False)
    if 'window.isUseHttps= false' in res.text or 'window.isUseHttps' not in res.text:
        return '获取地区ID错误, 请更新AccessToken后重试..'
    html = res.text

    addressId = re.findall('"addressId":(.*?),', html)[0]
    soup = BeautifulSoup(html, 'html.parser')
    price = soup.find('span', class_='oc-final-amount').get_text().replace('￥', '').strip()
    if float(price) == float(amount):
        return addressId
    else:
        logger.log('DEBUG', '订单金额不一致, 给定金额:{}，实际支付金额:{}'.format(amount, price), 'spider', pdduid)
        return '订单金额不一致, 给定金额:{}，实际支付金额:{}'.format(amount, price)


"""
获取商品需要的参数
input = 商品地址(goods_url), 登陆状态下的Cookie(cookie)
output = 分组排序ID(group_id), 商品ID(goods_id), 商品的属性ID(sku_id)如衣服的尺码，颜色
"""


def get_goods_id(url, cookie=None):
    res = requests.get(url, headers=headers, verify=False)
    html = res.text
    if cookie is not None:
        headers['Cookie'] = cookie
    # sku_id = random.choice(re.findall('"skuID":(.*?),', html))
    # group_id = random.choice(re.findall('"groupID":(.*?),', html))
    # goods_id = random.choice(re.findall('"goodsID":"(.*?)",', html))
    sku_id = re.findall('"skuID":(.*?),', html)[0]
    group_id = re.findall('"groupID":(.*?),', html)[0]
    goods_id = re.findall('"goodsID":"(.*?)",', html)[0]
    return sku_id, group_id, goods_id


# 获取增加收货地址
def get_shipping_address(pdduid, accesstoken):
    addresses_url = 'https://api.pinduoduo.com/addresses?pdduid={}'.format(pdduid)
    headers['accesstoken'] = accesstoken
    response = requests.get(addresses_url, headers=headers, verify=False)
    if len(response.json()) == 0:
        url = 'https://api.pinduoduo.com/address?pdduid={}'.format(pdduid)
        add_data = {
            "address": "32栋",
            "city_id": 76,
            "district_id": 693,
            "mobile": "15179833221",
            "name": "zs",
            "province_id": 6
        }
        add_response = requests.post(url, headers=headers, json=add_data, verify=False)
        if 'server_time' in add_response.json():
            logger.log('INFO', '新增收货地址成功', 'spider', pdduid)
            return True, '新增收货地址成功'
        else:
            logger.log('ERROR', '新增收货地址失败', 'spider', pdduid)
            return False, '新增收货地址失败'
    else:
        if 'error_code' in response.json():
            logger.log('ERROR', 'access_token错误，请更新.', 'spider', pdduid)
            return False, 'access_token错误，请更新.'
        return True, '已存在收货地址'


"""拼多多下单入口函数"""


def main(pdduid, accesstoken, goods_url, amount, order_number):
    order_number = int(order_number)
    # TODO goods_url, accesstoken, pdduid
    # 是否支付宝支付， True为是
    alipay = False
    cookie = 'pdd_user_id={}; PDDAccessToken={};'.format(pdduid, accesstoken)

    """判断收货地址，没有则增加"""
    is_add, msg = get_shipping_address(pdduid, accesstoken)
    if is_add is False:
        return {'code': 0, 'pay_url': '', 'order_sn': '', 'msg': msg}

    """获取商品信息"""
    sku_id, group_id, goods_id = get_goods_id(goods_url, cookie)

    """获取地区ID"""
    address_id = get_address_id(sku_id, group_id, goods_id, amount, order_number)
    if '错误' not in address_id and '订单金额' not in address_id:
        order_sn, pay_url = pay(alipay, address_id, pdduid, accesstoken, sku_id, group_id, goods_id)
        if '错误' in pay_url:
            return {'code': 0, 'pay_url': '', 'order_sn': '', 'msg': pay_url, 'goods_id': 0}
        logger.log('INFO', '订单编号: [{}],支付链接:{}'.format(order_sn, pay_url), 'spider', pdduid)
        return {'code': 1, 'pay_url': pay_url, 'order_sn': order_sn, 'msg': '', 'goods_id': goods_id}
    elif '订单金额不一致' in address_id:
        return {'code': 0, 'pay_url': '', 'order_sn': '', 'msg': address_id, 'goods_id': 0}
    else:
        logger.log('ERROR', '未获取到地区ID, 更新accesstoken后重试', 'spider', pdduid)
        return {'code': 0, 'pay_url': '', 'order_sn': '', 'msg': address_id, 'goods_id': 0}


if __name__ == '__main__':
    goods_url = 'https://mobile.yangkeduo.com/goods2.html?goods_id=2723075938&page_from=0&share_uin=ZJZOSVZU6NLHPAJCLHXLBNVJ54_GEXDA&_wv=41729&_wvx=10&refer_share_id=1oKRTkcPdybPDQJE0rKgy7B85uMgVuT6&refer_share_uid=3636814957&refer_share_channel=message'
    pdduid = 15179833772
    accesstoken = 'RLNMEXUQAWCNNWY4SK4RNYVGEUUR4N6N4LSW35WNKRU5BGYZ5E2Q101a825'
    amount = 5
    order_number = 1
    main(pdduid, accesstoken, goods_url, amount, order_number)
