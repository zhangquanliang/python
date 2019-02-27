import re
import time
import datetime
import requests
import urllib3

urllib3.disable_warnings()

headers = {
    'User-Agent': 'com.meituan.imeituan/19486 (unknown, iOS 11.4, iPhone, Scale/3.000000)',
    'pragma-os': 'MApi 1.1 (mtscope 9.11.800 appstore; iPhone 11.4 iPhone8,2; a0d0)',
    'pragma-unionid': '000de10f973c4241a5c28749b4a92f100000000000008793149',
    'cookie': '__mta=218928422.1551176675073.1551176699651.1551176745887.7; _lxsdk_cuid=169233792d8c8-0d2ef071714c8-36647105-1aeaa0-169233792d878; uuid=773318c9e026468faf64.1551157684.1.0.0; ci=30; rvct=30%2C10; lat=22.672045; lng=113.821507; IJSESSIONID=slhbbzfgqggt6j1mnfqgvmvf; iuuid=F214FA336BD3BDE69E9607C3DC69E59DD0E572EA971EE5E58694BAE210B516F1; cityname=%E6%B7%B1%E5%9C%B3; _lxsdk=F214FA336BD3BDE69E9607C3DC69E59DD0E572EA971EE5E58694BAE210B516F1; __utma=74597006.1956286438.1551161182.1551161182.1551161182.1; __utmc=74597006; __utmz=74597006.1551161182.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); client-id=53e123ff-2d08-4b97-b77d-e59d4c6e2728; _hc.v=2046d497-5334-661e-91b5-32a37933a8cb.1551161185; ci3=1; backurl=https://i.meituan.com; mtcdn=K; isid=DF4F9D33A566B0A2B050E66B6DEFB891; oops=xPLQWmwF-3i5s8zuybTflv9t9M4AAAAA_QcAAK8_Pnjw9bURNfnfzO7NfsMLOhiOm406sKyqxgHwDrc1yjSPQYsGTAmCnsHquYqQrQ; u=780922927; logintype=normal; latlng=22.550355,113.982923,1551161422936; p_token=xPLQWmwF-3i5s8zuybTflv9t9M4AAAAA_QcAAK8_Pnjw9bURNfnfzO7NfsMLOhiOm406sKyqxgHwDrc1yjSPQYsGTAmCnsHquYqQrQ; i_extend=C_b3E154994617100647057259691967609748530516_e4111529265387623281_a%e4%b8%80%e7%82%b9%e7%82%b9Gimthomepagecategory11H__a; utm_medium=androidweb; utm_source=appshare; utm_term=AandroidBgroupC9.12.401DweiboEpoiG2019022618234813E081094F94E9FDEF7806169392964DC727F5C5D561DB346562651991F42623377; _lx_utm=utm_term%3DAandroidBgroupC9.12.401DweiboEpoiG2019022618234813E081094F94E9FDEF7806169392964DC727F5C5D561DB346562651991F42623377%26utm_source%3Dappshare%26utm_medium%3Dandroidweb; _lxsdk_s=1692955aab9-192-81a-37c%7C%7C21'
}


"""获取一点点商家地址"""


def get_member_address(memberid):
    url = 'http://meishi.meituan.com/i/poi/{}'.format(memberid)
    response = requests.get(url, headers=headers, verify=False)
    html = response.text
    if '验证中心' in html:
        return '访问商家过于频繁'
    try:
        address = re.findall('addr:(.*?)&amp;referer=meituan', html)[0]
    except Exception as ex:
        address = '商家地址错误'
    return address


"""获取美团一点点商家数据"""


def get_member_data():
    # 是否获取商家店铺详细地址，True:是， False:否
    IsAddress = True

    # txt文件名
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = str(now_time) + '_mt.txt'

    url = 'https://apimobile.meituan.com/group/v4/poi/search/30?supportTemplates=default,hotel,block,native,nofilter,cinema&version_name=9.11.800&sort=defaults&limit=200&filterStatus=custom&client=iphone&source=2&supportDisplayTemplates=itemA,itemB,itemC,itemD,itemE,itemF,itemG,itemH,itemI,itemJ,itemK,itemL,itemM,itemN,itemO,itemP,itemQ,itemR,itemS,itemT,itemU,itemV,itemW,itemX,itemDynamic,trainTicket,airplaneTicket,travelIntention&entrance=1&wifi-cur=0&targetCityId=30&card_version=2&__skno=017FF385-C77B-4CFD-B079-70FAFD33DBBE&wifi-mac=fc:7c:02:06:1b:27&q=一点点&utm_medium=iphone&offset=0&__skcy=wcuKprtXpYnbtfwDhVl2A6LdtEc=&wifi-name=C-504&__skua=a91ac6f5f2aba0aa140063108d78b4d7&ci=30&cateId=1&msid=CEE98576-2731-488D-861D-3112F81E04ED2019-02-26-17-35341&__skck=17989db390fc250c67e02d783868197e&specialreq=recommend&queryId=5872592825482293805&utm_content=34F088F43738CC5DE073B2597F20E93044111EBC6A1C5BEFA1C323A759937748&mypos=22.547317,113.987680&__skts=1551173954.739517&utm_campaign=AgroupBgroupD200Ghomepage_searchH0'
    response = requests.get(url, headers=headers, verify=False)
    member_data = response.json()


    # 解析返回的数据
    for i in member_data['data']['searchResult'][0]['items']:
        # 移除没有作用的店铺信息
        if 'id' not in i['business']:
            continue

        memberid = i['business']['id']
        price = i['display']['itemJ']['price']
        name = str(i['display']['itemJ']['title']).replace("'", '"').replace('<font color="#ff6200">', '').replace(
            '</font>', '').replace('<font>', '')
        reviewscore = i['display']['itemJ']['reviewScore']
        if IsAddress:
            address = get_member_address(memberid)
        else:
            address = '-'

        log = '获取到店铺[{}],店铺ID:[{}],人均消费:[{}],评分:[{}],地址:[{}]'.format(name, memberid, price, reviewscore, address)
        with open(file_name, 'a+', encoding='utf8') as f:
            f.write(log + '\n')
        print(log)
        print('-' * 100)


"""获取秒级的时间戳"""
def get_localhost_second(tssl):
    timeArray = time.strptime(str(tssl), "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def mt_main():
    get_member_data()


if __name__ == '__main__':
    mt_main()
