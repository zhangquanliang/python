# -*- coding:utf-8 -*-
__author__ = '张全亮'
import requests
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup
from openpyxl import Workbook
book = Workbook()
sheet = book.create_sheet('专利')
sheet.append(['专利地址', '非专利地址'])
req = requests.session()
headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, sdch",
        "accept-language": "zh-CN,zh;q=0.8",
        "cache-control": "max-age=0",
        "user-agent": "Mozilla/1.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    }


def get_zhuanli(url):
    response = req.get(url, headers=headers, verify=False)
    if response.url == url and response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        shop_list = soup.find_all('a', class_='title-link')
        for shop_ in shop_list:
            detail_url = shop_['href']
            get_detail(detail_url)
        try:
            next_url = soup.find('a', class_='next')['href']
            print('下一页的地址为:[{}]'.format(next_url))
            get_zhuanli(next_url)
        except:
            print('已查询到最后一页。程序结束!')
            return
    else:
        print('异常请求，地址:[{}]'.format(response.url))
    book.save('1688店铺专利.xlsx')


def get_detail(url):
    response = req.get(url, headers=headers, verify=False)
    if response.url == url and response.status_code == 200:
        if '专利' in response.text:
            sheet.append([url, ''])
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            data_tfs_url = soup.find('div', class_='desc-lazyload-container')['data-tfs-url']
            response2 = req.get(data_tfs_url, headers=headers, verify=False)
            if '专利' in response2.text:
                print('此商品有专利，地址如下[{}]...'.format(url))
                sheet.append([url, ''])
                return
            else:
                print('此商品无专利，地址如下[{}]'.format(url))
                sheet.append(['', url])
                return
        except:
            print('获取专利异常，请确认!')
    else:
        print('异常请求，地址:[{}]'.format(response.url))


if __name__ == '__main__':
    url = 'https://shop1435078361771.1688.com/page/offerlist.htm?spm=a2615.2177701.0.0.2798766eZbIGHI'
    get_zhuanli(url)