# -*- coding: utf-8 -*-
import urllib.request
import hashlib
src ='123'
import requests
a = requests.get('http://www.kugou.com/yy/index.php?r=play/getdata&hash=2688ADB1CA449448388270987BDCE6E8&album_id=960327&_=1516759561406')
print(a.json())