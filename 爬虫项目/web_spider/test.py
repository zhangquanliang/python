# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import requests
from bs4 import BeautifulSoup
headers = {
    "Referer": "http://hotels.ctrip.com/hotel/436187.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)" 
                  " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
}
rs = requests.get('http://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID=436187&hotel=436187&NewOpenCount=0&AutoExpiredCount=0&RecordCount=8968&OpenDate=2009-01-01&card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=2&currentPage=2&viewVersion=c&contyped=0&eleven=a879fdeac4f7d70c431eb8e2800bdf4defb4048b7b8fc0e4699eadadf16b4ced&callback=CASYzLutKOxEQiPtH&_=1526017899825', headers=headers)
# rs.text
soup = BeautifulSoup(rs.text, 'html.parser')
t = soup.find_all('div', class_='J_commentDetail')
for i in t:
    print(i)
    print('-'*100)