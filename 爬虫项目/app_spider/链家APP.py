# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import requests
import urllib3
urllib3.disable_warnings()

url = 'https://app.api.lianjia.com/house/ershoufang/searchv4?city_id=440300&priceRequest=&limit_offset=20&shequIdRequest=&communityRequset=&moreRequest=&has_recommend=1&is_suggestion=0&limit_count=20&sugQueryStr=&comunityIdRequest=&areaRequest=&is_history=0&schoolRequest=&condition=&roomRequest=&isFromMap=false&ad_recommend=1'
headers = {
    "Page-Schema":  "ershou/homepage",
    "Referer": "homepage?cityId=440300&position=app_index",
    "Authorization": "MjAxNzAzMjRfYW5kcm9pZDoyM2JhOWY3OGExZmQ0N2Y3Zjk4NzY5NmM3MDgxMTQ1ZjM2Yzc4YzFk",
    "User-Agent": "HomeLink8.4.9;vivo vivo+X20Plus+UD; Android 7.1.1"
}
req = requests.session()
response = req.get(url, verify=False, headers=headers, timeout=5)
json_str = response.json()
print(json_str)
print(json_str['data']['return_count'])

house_list = json_str['data']['list']
print(len(house_list))
for house in house_list:
    print(house['house_code'], house['title'])