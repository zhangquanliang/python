# -*- coding: utf-8 -*-
"""
Title = 财联社24小时电报
Date = 20180424
"""
import requests

url = 'https://www.cailianpress.com/index'
response = requests.get(url)
print(response.text)