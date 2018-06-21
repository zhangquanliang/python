#-*- coding:utf-8 -*-

from lxml import etree
import time
import pymysql
import sys
import re
import requests
from random import randint
import json

reload(sys)
sys.setdefaultencoding('utf8')

class Aliexpress3:
    def __init__(self):
        self.conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db="AliExpress",
                                    charset="utf8")
        self.cur = self.conn.cursor()

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'cache-control': 'max-age=0',
            # 'cookie': 'ali_apache_id=10.181.239.78.1481975126111.281811.9; ali_beacon_id=10.181.239.78.1481975126111.281811.9; cna=+e7FEHdr2UYCAd+nId28VVGf; _uab_collina=148276570987506375192855; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932283752585%0932643751757%0932766092845%0932779895390%0932608648527%0932341938991%0932698146494; xman_f=ediproatjhbe5rYO4J6gZANIh/DijKR40Cv8iCvKo+jsmzJYOQGGLJ/I3RtF9zkp4udQoy8HVM1uianCU6Js5S1EiCi+rYVT0mGlcL70ympYdzuPEXEPoQ==; xman_t=cnuWFzNUm5+UlQe0K6V/KXQA6NpWjgL651M9sui4cR7IwmJviYKdqRClgOZOmnof; acs_usuc_t=acs_rt=f05d470772264de1804f5d192c6cf080; _gat=1; xman_us_f=x_l=1&x_locale=en_US; intl_locale=en_US; aep_usuc_f=region=US&site=glo&b_locale=en_US&c_tp=USD; intl_common_forever=AW6kb+KzM/Zfl7d2TJGEoDxfbEkCKmfyx1WLI4oLOaRnGMl7Bd1/ig==; _ga=GA1.2.61760890.1481975162; _umdata=486B7B12C6AA95F207188164B9A28D3D7C199907BA3C192D91D77BD4746EBD235C88FAD75BA09D0A3DC15E17C4438EA38CD014877B99D53B512C3F2AF9AD916FDBEF1174A7B67034D090E53F4BB671679270D79AA5C46F73E9C3BAAA49C6E2A0; JSESSIONID=864F7C0E503B24157E2C2FFA9C12C1B7; ali_apache_track=; ali_apache_tracktmp=; l=ApKSQAWFMP-/-VVRx6U218f2YlJ3QZYq; isg=AtLSiZml3g-ffiLE6eK7WrPSI5h5ddZ9Z-eBX5woHQVnr3CphnIVjPSNabxp',
            'referer': 'https://www.aliexpress.com/1629037',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        }

        # 代理服务器
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = "HCDZH37K7VD6RTED"
        proxyPass = "AF855B8C35306790"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        self.proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

    def Response(self, Url):
        while True:
            try:
                time.sleep(randint(1, 5))
                response = requests.get(Url, proxies=self.proxies, timeout=100, headers=self.headers)
            except Exception as e:
                print e
            else:
                response.encoding = 'utf-8'
                if response:
                    return response.content
                elif response.status_code == 404:
                    print "Page can not be found " + Url
                    response = None
                    return response


    def GetShopId(self, tablename):
        sql = 'SELECT DISTINCT storelink FROM `{}`'.format(tablename)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        if result:
            return result

    def Saveinfo(self, informationItems,tablename):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(informationItems, dict):
            try:
                try:
                    cols = ','.join(informationItems.keys())
                    values = '","'.join(informationItems.values())
                    sql = "INSERT INTO %s (%s) VALUES (%s)" % (tablename, cols, '"' + values + '"')
                except:
                    pass
                else:
                    # print sql
                    '''
                    把下面代码生效就可以插入数据了
                    '''
                    try:
                        result = self.cur.execute(sql)
                        insert_id = self.conn.insert_id()
                        self.conn.commit()
                        # 判断是否执行成功
                        if result:
                            print "插入成功:%s" % insert_id
                        else:
                            print "插入为NULL"
                    except pymysql.Error, e:
                        print e
                        print pymysql.Error
                        # 发生错误时回滚
                        self.conn.rollback()
                        # 主键唯一，无法插入
                        if "key 'PRIMARY'" in e.args[1]:
                            # num += 1
                            print "数据已存在，未插入数据"
                        else:
                            print "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
            except pymysql.Error, e:
                print "数据库错误，原因%d: %s" % (e.args[0], e.args[1])

    def StoreProduct(self, storelink):
        print "New Store " + storelink
        id = storelink.split('store/')[-1]
        categories_url = 'https://www.aliexpress.com/store/{}/search/1.html?spm=2114.12010615.0.0.pEaEEZ&origin=n&SortType=bestmatch_sort'.format(id)
        try:
            resposne = self.Response(categories_url)
        except Exception as e:
            print e
        else:
            if resposne:
                etre = etree.HTML(resposne)
                selectors = etre.xpath('//*[@id="refine-attr-wrap"]/div[@class="cate first-attr"]/div[@class="cate-values"]/ul[@class="category-collapse"]/li')
                for se in selectors:
                    categorie_url = se.xpath('a/@href')
                    categorie_title = se.xpath('a/text()')
                    if categorie_url:
                        categoryId = re.findall('categoryId=(.*?)&SortType=', categorie_url[0])
                        if categoryId:
                            PageNum = 1
                            retime = 0
                            while True:
                                item = []
                                url = 'https://www.aliexpress.com/store/{}/search/{}.html?origin=n&categoryId={}&SortType=new_desc'.format(str(id), str(PageNum), categoryId[0])
                                print "Parsing Page URL " + url
                                try:
                                    resposne = self.Response(url)
                                except Exception as e:
                                    print e
                                else:
                                    if resposne:
                                        a = 1
                                        item.append(a)
                                        etre = etree.HTML(resposne)
                                        selectors = etre.xpath('//ul[@class="items-list util-clearfix"]/li')
                                        rank = 1
                                        for se in selectors:
                                            Dict = {}
                                            if se.xpath('div[@class="detail"]/h3/a/@href'): Dict['productLink'] = \
                                            se.xpath('div[@class="detail"]/h3/a/@href')[0].replace('//','').strip()
                                            if se.xpath('div[@class="detail"]/h3/a/@title'): Dict['productName'] = \
                                            se.xpath('div[@class="detail"]/h3/a/@title')[0].strip()
                                            if se.xpath('div[@class="detail"]/div[@class="cost"]/b/text()'): Dict['productPrice'] = \
                                            se.xpath('div[@class="detail"]/div[@class="cost"]/b/text()')[0].strip()
                                            if se.xpath('div[@class="img"]/div[@class="discount"]/span/text()'): Dict['productDiscount'] = \
                                            se.xpath('div[@class="img"]/div[@class="discount"]/span/text()')[0].strip()
                                            if se.xpath('div[@class="detail"]/div[@class="cost-old"]/del/text()'): Dict['productPriceOld'] = \
                                            se.xpath('div[@class="detail"]/div[@class="cost-old"]/del/text()')[0].strip()
                                            if se.xpath('div[@class="detail"]/div[@class="recent-order"]/text()'): Dict['orders'] = \
                                            se.xpath('div[@class="detail"]/div[@class="recent-order"]/text()')[0].strip()
                                            if se.xpath('div[@class="detail"]/div[@class="cost"]/text()'): Dict['productPriceUnit'] = \
                                            se.xpath('div[@class="detail"]/div[@class="cost"]/text()')[0].strip()
                                            storelink = "www.aliexpress.com/store/" + id
                                            if storelink: Dict['storelink'] = str(storelink)
                                            Dict['category_title'] = str(categorie_title)
                                            Dict['shopId'] = str(id)
                                            Dict['productrank'] = str(rank + (PageNum - 1) * 36).decode('utf-8')
                                            item.append(Dict)
                                            rank += 1
                                            try:
                                                self.Saveinfo(Dict, 'storeproduct')
                                            except Exception, e:
                                                print e
                                    else:
                                        print "Re-try this category"
                                        pass

                                if item:
                                    if len(item) > 1:
                                        if len(selectors) > 30:
                                            PageNum += 1
                                            print "Same Category, Next Page"
                                        else:
                                            print "This Category is Done, Next Category"
                                            break
                                    else:
                                        if PageNum > 1:
                                            print "This Category is Done, Next Category"
                                            break
                                        else:
                                            if retime <= 2:
                                                retime += 1
                                                print "Null for first page: " + str(retime)
                                                pass
                                            else:
                                                print "this category should be null, please double check"
                                                break

if __name__=='__main__':
    A3 = Aliexpress3()
    storelist1 = A3.GetShopId("masterlisting")
    storelist2 = A3.GetShopId("storeproduct")
    results = list(set(storelist1).difference(storelist2))
    # results = A3.GetShopId("masterlisting")
    total = len(results)
    id = 1
    for r in results[]:
        print (str(id) + "/" + str(total))
        try:
            A3.StoreProduct(r[0])
        except Exception, e:
            print e
        id += 1
