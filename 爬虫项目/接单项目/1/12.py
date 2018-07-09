# encoding:utf-8
import requests
from lxml import etree
from bs4 import BeautifulSoup

headers = {
    "Cookie": "website_cityid=1; website_qiehuan_cityid=1; website_cityname=%e6%b2%88%e9%98%b3; Hm_cv_1f8e83330039496a701d7ae44836ed10=1*userType*visitor; UM_distinctid=16472e91520117-0f8fe9b737bb46-47e1f32-100200-16472e915227b1; BPC=fe2e1e558cca25dcab5efb6cc9ac8014; safedog-flow-item=6C36E765; ASP.NET_SessionId=cwg2fssxih5lcsxu4sgqnips; Hm_lvt_1f8e83330039496a701d7ae44836ed10=1530932334,1531053154,1531057823; Hm_lpvt_1f8e83330039496a701d7ae44836ed10=1531057823",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"

}


def get_page(base_url):
    response = requests.get(url=base_url, headers=headers).content
    print(response.decode())
    return response


def detail_page(response):
    html = etree.HTML(response)
    detail_links = html.xpath('//*[@class="details"]/h3/a/@href')
    for detail_link in detail_links:
        detail_link1 = "http://www.517.cn" + str(detail_link)
        print(detail_link1)
        source_code = requests.get(url=detail_link1, headers=headers).text
        soup = BeautifulSoup(source_code, 'lxml')
        html1 = etree.HTML(source_code)
        address = str(html1.xpath("//*[@id='form1']/div[3]/div[1]/a[3]/text()")[0]).replace("二手房", '')
        print(address)
        address1 = str(html1.xpath("//*[@id='form1']/div[3]/div[1]/a[4]/text()")[0]).replace("二手房", '')
        print(address1)
        titles = soup.find("span", class_="t-h-title").text
        print(titles)
        house_source = str(html1.xpath("//*[@class='t-h-tags']/i/text()")[0]).replace("房源编号：", '').strip()
        print(house_source)


def start():
    base_url = "http://www.517.cn/ershoufang/pgq1?ckattempt=1"
    page = get_page(base_url)
    detail_page(page)


if __name__ == '__main__':
    start()
