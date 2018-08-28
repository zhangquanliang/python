# -*- coding:utf-8 -*-
__author__ = '张全亮'

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

import re
import random
import urllib3
import requests
import urllib.parse
urllib3.disable_warnings()
req = requests.session()

headers = {
    'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
}


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
    sku_id = random.choice(re.findall('"skuID":(.*?),', html))
    group_id = random.choice(re.findall('"groupID":(.*?),', html))
    goods_id = random.choice(re.findall('"goodsID":"(.*?)",', html))
    return sku_id, group_id, goods_id


"""
获取需要的地址ID
input = 分组排序ID(group_id), 商品ID(goods_id), 商品的属性ID(sku_id)如衣服的尺码，颜色 购买数量(goods_number)
output = 地址ID(addressId)
"""
def get_localhost(sku_id, group_id, goods_id, goods_number=1):
    url = 'https://mobile.yangkeduo.com/order_checkout.html?sku_id={}&group_id={}&goods_id={}&goods_number={}'.format(sku_id, group_id, goods_id, goods_number)
    res = requests.get(url, headers=headers, verify=False)
    if 'window.isUseHttps= false' in res.text or 'window.isUseHttps' not in res.text:
        print('获取地区ID错误, 请更新AccessToken后重试..')
        return False
    html = res.text
    addressId = re.findall('"addressId":(.*?),', html)[0]
    return addressId


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
        "goods": [{"sku_id": sku_id, "sku_number":1,"goods_id": goods_id}],
        "group_id": group_id,
        "duoduo_type": 0,
        "biz_type": 0,
        "source_channel": -1,
        "source_type": 0,
        "app_id": 9,
        "is_app": "0",
        "version": 1
    }

    res = requests.post(url, headers=headers, json=json_str, verify=False)
    res_json = res.json()
    if 'error_code' in res_json:
        response = requests.get('https://api.pinduoduo.com/addresses?pdduid={}'.format(pdduid), headers=headers,
                                verify=False)
        if len(response.json()) == 0:
            print('未检测到收货地址，请填写后重试..')
        else:
            print('当前accesstoken无效，请更新accesstoken后重试.')
        # print('获取订单编号错误,请填写完收货地址后,更新accesstoken.')
        return ''
    order_sn = res_json['order_sn']
    print('订单编号: {}'.format(order_sn))

    if alipay:
        print('支付宝支付...')
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
        print('微信支付...')
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
        pay_url = re.findall('var url="(.*?)";', res2.text, re.I|re.S)[0]
    return pay_url


def check_pay_state(url):
    if url is None:
        return
    headers['Cookie'] = 'JSESSIONID=RZ13wHrCb1mgcFL0RExO8SzqetcOhvmobileclientgwRZ13; cna=R3NTE12xGE0CAXFi8N3jgEXM; isg=AsrKoR5EpPrHrChWM3LqRKbnFbBmjmrPoDsVvlQDFp2oB2rBPEueJRB1Y2w_; mobileSendTime=-1; credibleMobileSendTime=-1; ctuMobileSendTime=-1; riskMobileBankSendTime=-1; riskMobileAccoutSendTime=-1; riskMobileCreditSendTime=-1; riskCredibleMobileSendTime=-1; riskOriginalAccountMobileSendTime=-1; rtk=lnXY1h447OU0k/Q4xn89+AcmJpsd5yPcl6mA1ZRc1mC45yiIn0E; _uab_collina=153473501160675278696592; ALIPAY_WAP_CASHIER_COOKIE=0573CE726FA3E9C57B6FE5F31BF1EEA4CBBD18D64128246BDC4A80A1C999577F; awid=RZ13wHrCb1mgcFL0RExO8SzqetcOhvmobileclientgwRZ13; JSESSIONID=11CDC7C263428A01B0BD18720A407DDD; zone=RZ13B; ssl_upgrade=0; spanner=4U9quWeo+RIS47CbgHLOtRdVvK/n4dcu'
    response = requests.get(url, headers=headers, verify=False)
    if '订单信息' in response.text:
        print('支付宝现处于已登陆状态.可直接打开网页付款。')
    else:
        print('支付宝未登录, 请登录后重新打开网页付款, 或复制链接进支付宝App付款。')


def main(pdduid, accesstoken, goods_url):
    # TODO goods_url, accesstoken, pdduid
    # 是否支付宝支付， True为是
    alipay = False
    cookie = 'pdd_user_id={}; PDDAccessToken={};'.format(pdduid, accesstoken)
    sku_id, group_id, goods_id = get_goods_id(goods_url, cookie)
    # sku_id, group_id, goods_id = get_goods_id(goods_url)
    address_id = get_localhost(sku_id, group_id, goods_id)
    if address_id is not False:
        pay_url = pay(alipay, address_id, pdduid, accesstoken, sku_id, group_id, goods_id)
        print('付款链接: {}'.format(pay_url))
        # check_pay_state(pay_url)
    else:
        print('程序结束, 未获取到地区ID, 无付款链接...')


if __name__ == '__main__':
    goods_url = 'http://mobile.yangkeduo.com/goods.html?goods_id=9962830&is_spike=0&page_el_sn=99862&refer_page_name=index&refer_page_id=10002_1534904453632_CTDgPWCMNe&refer_page_sn=10002&refer_page_el_sn=99862'
    pdduid = 15179833772
    accesstoken = '4KVF5U4NUNLVDNAPUGZH4WNA5QAEXUYOUGEOQ7MWKBWZWRLYZWMQ101a825'
    main(pdduid, accesstoken, goods_url)