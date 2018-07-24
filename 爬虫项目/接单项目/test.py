# -*- coding:utf-8 -*-
"""
author = zhangql
"""
from openpyxl import Workbook
import requests
import re
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
}
book = Workbook()
sheet = book.create_sheet('数据')
sheet.append(['单位', '实验室地址', '电话', '证书编号', '发证日期', '有效期', '批准日期',
              '检测产品/类别', '检测项目/参数', '检测标准（方法）名称及编号', '限制范围或说明'])
data = {"isavailable":"0"}
pool = Pool(processes=20)
for i in range(20):
    url = 'http://app.shzj.gov.cn:443/wzhd/zjcx/rzjgcx/jlrzjg_dataproxy.jsp?startrecord={}&endrecord={}&perpage=8'.format((i*8)+1, (i+1)*8)
    res = requests.post(url, data=data, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    tr_list = soup.find_all('tr')
    for tr in tr_list:
        name = tr.find_all('td')[0].get_text()
        # id = re.findall('id=(.*?)&code', tr.find_all('td')[0].find('a')['href'], re.S | re.I)[0]
        refer_url = 'http://app.shzj.gov.cn:443/wzhd/zjcx/rzjgcx' + tr.find_all('td')[0].find('a')['href'][1:]
        localhost = tr.find_all('td')[1].get_text()
        phone = tr.find_all('td')[2].get_text()
        cer_id = tr.find_all('td')[3].get_text()
        f_date = tr.find_all('td')[4].get_text()
        y_date = tr.find_all('td')[5].get_text()
        p_date = tr.find_all('td')[6].get_text()
        print(name, localhost, phone, cer_id, f_date, y_date, p_date)
        detail_url = 'http://app.shzj.gov.cn:443/wzhd/zjcx/rzjgcx/jlrzjg_dataproxy_xx.jsp?startrecord=1&endrecord=20&perpage=20'
        response = requests.get(refer_url, headers=headers)
        d_id = re.findall("'id':'(.*?)',", response.text, re.I|re.S)[0]
        d_data = {
            "id": d_id
        }

        s = requests.post(detail_url, headers=headers, data=d_data)
        soup2 = BeautifulSoup(s.text, 'html.parser')
        detail_list = soup2.find_all('tr')
        for detail_ in detail_list:
            detail_name = detail_.find_all('td')[0].get_text()
            detail_type = detail_.find_all('td')[1].get_text()
            detail_id = detail_.find_all('td')[2].get_text()
            detail_xy = detail_.find_all('td')[3].get_text()
            sheet.append([name, localhost, phone, cer_id, f_date, y_date, p_date, detail_name, detail_type, detail_id, detail_xy])
    break
pool.close()
pool.join()
book.save('数据.xlsx')