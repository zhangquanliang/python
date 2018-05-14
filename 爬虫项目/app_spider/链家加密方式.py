# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import hashlib
import base64

"""先md5加密部分数据，未成功"""
S = 'city_id=440300priceRequest=limit_offset=0shequIdRequest=communityRequset=moreRequest=has_recommend=1is_suggestion=0limit_count=20sugQueryStr=comunityIdRequest=areaRequest=is_history=0schoolRequest=condition=roomRequest=isFromMap=falsead_recommend=1'
s = S + "34bad281103e48693406016fa0c947e3"
print(s)
l_md5 = hashlib.md5(s.encode()).hexdigest()
print(l_md5)


"""然后base64加密"""
# psd = '20170324_android:'
# authorization = base64.b64encode(psd.encode())
# print(authorization.decode())
# a = {'city_id': '440300', 'condition': '', 'limit': '10', 'limit_offset': '0', 'order': '', 'query': '', 'sign': ''}
