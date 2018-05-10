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
from util_zql.tools import Tools


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
        yzm = Tools.ocr_verify_code('szt.png')
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

            if self.save_pdf(html):
                reg = re.findall('<tr class="odd_body" lsh="(.*?)" zdh="(.*?)" kh="(.*?)" rq="(.*?)" sj="(.*?)">', html)
                self.download_fp_pdf(reg, url)
        else:
            return self.sztfp()

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
            # "jfirmphone": "15179833772"
            "jfirmphone": "15779557620"
        }
        url1 = 'https://www.shenzhentong.com/Ajax/ElectronicInvoiceAjax.aspx'
        response1 = self.req.post(url1, data=data, headers=self.headers, verify=False)
        try:
           pid = response1.json()['strs']
        except:
            print(response1.text)
        url2 = 'https://www.shenzhentong.com/service/fpdetail.aspx?nodecode=101007009&pid=%s' % pid
        self.req.get(url2, headers=self.headers, verify=False)

        time.sleep(1)
        response3 = self.req.get(select_url, headers=self.headers, verify=False)
        html = response3.text
        self.save_pdf(html)

    # 保存发票pdf文件
    def save_pdf(self, html):
        reg = re.findall('<a target="_blank" href="(.*?)"', html)
        if len(reg) < 2:
            return True
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
    cardnum = '689220671'

    # for i in range(1, 31):
    #     if i < 10:
    #         date = '2018040%s' % i
    #     elif i >= 10 and i <20:
    #         date = '201804%s' % i
    #     else:
    #         date = '201804%s' % i
    date = '2018429'
    szt = SZTSpider(date=date)
    szt.sztfp()