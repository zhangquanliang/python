# -*- coding: utf-8 -*-
"""
Title = 深圳通发票查询下载
Date = 20180329
"""
import urllib3
urllib3.disable_warnings()
import requests
import re
import time
import os


class SZTSpider:
    """深圳通爬虫，下载查询到的pdf发票"""
    def __init__(self, cardnum=None, date=None):
        self.headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Cache-Control":"no-cache",
            "Connection":"keep-alive",
            "Host":"www.shenzhentong.com",
            "Pragma":"no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        }
        self.url = 'https://www.shenzhentong.com/service/invoice_101007009.html'
        self.yzm_url = 'https://www.shenzhentong.com/ajax/WaterMark.ashx?s=0.6806041122839781'
        self.check_yzm_url = 'https://www.shenzhentong.com/Ajax/ElectronicInvoiceAjax.aspx'
        if cardnum is None:
            cardnum = "688152326"
        self.cardnum = cardnum
        self.req = requests.session()
        self.date = date

    # 深圳通发票
    def sztfp(self):
        self.req.get(self.url, headers=self.headers, verify=False)

        response = self.req.get(self.yzm_url, headers=self.headers, verify=False)
        f = open('szt.png', 'wb')
        f.write(response.content)
        f.close()
        yzm = input('验证码: ')
        data = {
            "tp": 1,
            "yzm": yzm,
            "cardnum": self.cardnum
        }
        res = self.req.post(self.check_yzm_url, headers=self.headers, data=data, verify=False)  # 100

        if res.json()['state'] == 100 or res.json()['state'] == "100":
            url = 'https://www.shenzhentong.com/service/fplist_101007009_{}_{}.html'.format(self.cardnum, self.date)
            response = self.req.get(url, headers=self.headers, verify=False)
            html = response.text

            if len(re.findall('<tr class="odd_body"(.*?)>', html)) > 0:
                pass
            else:
                print(u'查询深圳通用户[{}], 日期[{}],当前无发票可下载。'.format(self.cardnum, self.date))
                return False

            try:
                self.save_pdf(html)
            except:
                reg = re.findall('<tr class="odd_body" lsh="(.*?)" zdh="(.*?)" kh="(.*?)" rq="(.*?)" sj="(.*?)">', html)
                self.download_fp_pdf(reg, url)
        else:
            print(res.text)

    # 发送下载pdf请求
    def download_fp_pdf(self, reg, select_url):
        lsh = reg[0][0]
        zdh = reg[0][1]
        kh = reg[0][2]
        rq = reg[0][3]
        sj = reg[0][4]
        data = {
            "tp":"3",
            "jlsh": lsh,
            "jzdh": zdh,
            "jkh": kh,
            "jrq": rq,
            "jsj": sj,
            "jfirmfpmc": "深圳市览众科技股份有限公司",
            "jfirmsbh": "914403007619892204",
            "jfirmaddre": "深圳市南山区中山园路1001号TCL科学园E4栋11楼B1",
            "jfirmtel": "0755-26470041",
            "jfirmyh": "招商银行车公庙支行",
            "jfirmyhzh": "813887672310001",
            "jfirmphone": "15179833772"
        }
        url = 'https://www.shenzhentong.com/Ajax/ElectronicInvoiceAjax.aspx '
        self.req.post(url, data=data, headers=self.headers, verify=False)
        time.sleep(3)
        response = self.req.get(select_url, headers=self.headers, verify=False)
        html = response.text
        self.save_pdf(html)

    # 保存发票pdf文件
    def save_pdf(self, html):
        reg = re.findall('<a target="_blank" href="(.*?)"', html)
        response1 = self.req.get(reg[0], headers=self.headers, verify=False)
        if os.path.exists('sztfp'):
            pass
        else:
            os.mkdir('sztfp')
        path = r'sztfp/' + self.cardnum + "_" + date + ".pdf"
        with open(path, 'wb') as f:
            f.write(response1.content)
            f.close()
        print(u'查询深圳通用户[{}], 日期[{}]发票下载成功。'.format(self.cardnum, self.date))


if __name__ == '__main__':
    # date = input('请输入想要打印的发票日期: ')
    cardnum = '18299536448'
    date = '20180318'
    szt = SZTSpider(date=date)
    szt.sztfp()