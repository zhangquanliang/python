# -*-coding:utf-8-*-
import requests
import json
import pytz
import datetime
import time
import urllib3
from pprint import pprint
from requests import Session

urllib3.disable_warnings()
sess = Session()


# 传入session,sid,token,min_price,max_price,time，player_id为球员ID，time为小时，传入小时数量即可，字符串或是整数
def sale_palyer(session,sid,token,min_price,max_price,player_id,hold_time=1):
    sale_url='https://utas.external.s2.fut.ea.com/ut/game/fifa18/auctionhouse?sku_b=FFT18'
    header={
        'Host':'utas.external.s2.fut.ea.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept':'text/plain, */*; q=0.01',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate, br',
        'Content-Type':'application/json',
        'Easw-Session-Data-Nucleus-Id':session,
        'X-UT-SID':sid,
        'X-UT-PHISHING-TOKEN':token,
        'Referer':'https://www.easports.com/fifa/ultimate-team/web-app/',
        'Content-Length':'87',
        'Origin':'https://www.easports.com',
        'Connection':'keep-alive',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache',
    }

    data={"itemData":{"id":int(player_id)},"startingBid":int(min_price),"duration":3600*int(hold_time),
          "buyNowPrice":int(max_price)}

    tz = pytz.timezone('Europe/London')
    # print (datetime.datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z')
    london_time=datetime.datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'    #伦敦时间

    s=requests.post(url=sale_url,headers=header,json=data)
    html=s.text
    time.sleep(1)

    if 'expired session'in html:
        return False

    else:
        dicts = json.loads(html)
        if dicts['id']!=None or dicts['idStr']!='':
            if dicts['id']==int(dicts['idStr']):
                return dicts['idStr']
            return False


'''
tradeId=交易ID
tradeIdStr=交易ID
buyNowPrice=现在买入价
tradeState=状态  active激活
startingBid=BID
expires=买入时限
bidState=是否可买入
'''
# itemData
'''
id=该球员ID
timestamp=查询时刻时间戳
itemType=球员属性 player球员
formation=购买球员的时候用的
'''

def get_html():
    response = requests.get('http://blog.csdn.net/yangwenxue_admin/article/details/51742426')
    return response.text


def buy_player(session, sid, token, min_price, max_price, play_name,quality='special'):
    print(min_price, max_price, play_name, quality)
    sess = Session()
    players_dict = read_json()
    result = {}

    if play_name not in players_dict.keys():
        result['success'] = False
        result['code'] = 1000       # 球员姓名不在球员字典中
        result['error'] = '球员姓名不在球员字典中, 或者球员名有错'
        return result

    player_id = players_dict[play_name]
    print('player id is : %s\n' %  player_id)
    time_arg = str(int(time.time()))
    quality = quality.lower().strip()
    quality_str = '&rare=SP'


    if quality == 'gold':
        quality_str = '&lev=gold'
    elif quality == 'silver':
        quality_str = '&lev=silver'
    elif quality == 'bronze':
        quality_str = '&lev=bronze'
    elif quality == 'all':
        quality_str = ''

    seach_url = 'https://utas.external.s2.fut.ea.com/ut/game/fifa18/transfermarket?start=0&num=36&type=player' + \
                quality_str + '&minb='\
              + str(min_price) + '&maxb=' + str(max_price) + '&_=' + time_arg + "&maskedDefId=" + player_id
    seach_header = {
        'Host':'utas.external.s2.fut.ea.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0)Gecko/20100101 Firefox/56.0',
        'Accept':'text/plain, */*; q=0.01',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate, br',
        'Content-Type':'application/json',
        'Easw-Session-Data-Nucleus-Id':str(session),
        'X-UT-SID':str(sid),
        'X-UT-PHISHING-TOKEN':str(token),
        'Referer':'https://www.easports.com/fifa/ultimate-team/web-app/',
        'Origin':'https://www.easports.com',
        'Connection':'keep-alive',
    }

    seach = sess.get(url=seach_url,headers=seach_header, verify=False)
    html = seach.text
    print("搜到到的html:",html[:100])
    if seach.status_code != 200:
        result['success'] = False
        result['code'] = seach.status_code      # 1002 代表cookie失效, 0 代表搜索结果为空 401代表sid失效 500代表token失效
        if seach.status_code == 401:
            result['error'] = 'sid失效'
        elif seach.status_code == 500:
            result['error'] = 'token失效'
        return result

    if json.loads(html)['auctionInfo'] == []:
        result['success'] = False
        result['code'] = 1001  # 1002 代表cookie失效, 1001 代表搜索结果为空, 0 代表未知
        return result
    else:
        dicts = json.loads(html)
        # pprint((dicts['auctionInfo'][0]['itemData'].keys()))

        # info_dict={}
        # auctionInfo=['tradeId', 'itemData','tradeState', 'buyNowPrice', 'currentBid', 'offers', 'watched', 'bidState', 'startingBid', 'confidenceValue', 'expires', 'sellerName', 'sellerEstablished', 'sellerId', 'tradeOwner', 'tradeIdStr']
        # itemData=['id', 'timestamp', 'formation', 'untradeable', 'assetId', 'rating', 'itemType', 'resourceId', 'owners', 'discardValue', 'itemState', 'cardsubtypeid', 'lastSalePrice', 'morale', 'fitness', 'injuryType', 'injuryGames', 'preferredPosition', 'statsList', 'lifetimeStats', 'training', 'contract', 'suspension', 'attributeList', 'teamid', 'rareflag', 'playStyle', 'leagueId', 'assists', 'lifetimeAssists', 'loyaltyBonus', 'pile', 'nation', 'resourceGameYear']
        # for i in range(0,len(dicts['auctionInfo'])):
        #     print(str(dicts['auctionInfo'][i]['tradeId']),dicts['auctionInfo'][i]['tradeIdStr'])

        player_id = dicts['auctionInfo'][0]['tradeIdStr']
        buyNowPrice = dicts['auctionInfo'][0]['buyNowPrice']
        print('购买价格:%s' % buyNowPrice)
        # time.sleep(0.5)
        buy_url = 'https://utas.external.s2.fut.ea.com/ut/game/fifa18/trade/' + player_id + '/bid?sku_b=FFT18'

        buy_header = {
            'Host':'utas.external.s2.fut.ea.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
            'Accept':'text/plain, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate, br',
            'Content-Type':'application/json',
            'Easw-Session-Data-Nucleus-Id':str(session),
            'X-UT-SID':str(sid),
            'X-UT-PHISHING-TOKEN':str(token),
            'Referer':'https://www.easports.com/fifa/ultimate-team/web-app/',
            'Content-Length':'12',
            'Origin':'https://www.easports.com',
            'Connection':'keep-alive',
        }

        q = {"bid":buyNowPrice}
        buy=sess.put(url=buy_url,headers=buy_header,json=q, verify=False)
        pprint("购买后的返回信息" + buy.text[:100])
        if len(buy.text) != 0 and 'credits' in buy.text:
            buy_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result['success'] = True
            result['name'] = play_name
            result['price'] = buyNowPrice
            result['time'] = buy_time
            result['code'] = buy.status_code
            print('购买成功\n')
            return result
        else:
            result['success'] = False
            result['code'] = 1003  # 1003 代表搜索到结果但是购买失败
            result['error'] = '搜索到结果但是购买时失败'
            print('购买失败\n')
            return result


def read_json():
    path = 'playersDict.json'
    with open(path, 'r') as f:
        json_str = f.read()
        return json.loads(json_str)


def buy_by_multi():
    buy_player(token='6937029332829941513', session='10059583306892', sid='8fbf4c85-079a-4e86-aae0-4588324b5c03212',
               min_price=200, max_price=30000, play_name="Patrick Joosten", quality='gold')

def get_sid(token):
    headers = {
        'Host': 'utas.external.s2.fut.ea.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-UT-PHISHING-TOKEN': str(token),
        'Referer': 'https://www.easports.com/fifa/ultimate-team/web-app/',
        'Content-Length': '263',
        'Origin': 'https://www.easports.com',
        'Connection': 'keep-alive',
    }
    json_dict = {"isReadOnly": False,
         "sku": "FUT18WEB",
         "clientVersion": 1,
         "locale": "en-US",
         "method": "authcode",
         "priorityLevel": 4,
         "identification": {"authCode": "QUOQAOF3ch9lduoas3kxTLAXWD6l2cZZU_nhenm8", "redirectUrl": "nucleus:rest"},
         "nucleusPersonaId": 1899212559,
         "gameSku": "FFA18PCC"},

    json_str = json.dumps(json_dict)
    pprint(json_str)
    url = "https://utas.external.s2.fut.ea.com/ut/auth?sku_b=FFT18&%s" % int(time.time())  #1520778121606
    response = requests.post(url, headers=headers, json=json_str)
    print(response.status_code,response.content)
    print(response.text)


if __name__=='__main__':
    # time.sleep(3)
    from multiprocessing.dummy import Pool
    pool = Pool(processes=2)
    buy_player(token='4313473520044819421', session='1005958330689', sid='8f06759a-8d5c-4cd1-8d98-10d69bd4b6eb',
                   min_price=200, max_price=3000, play_name="Patrick Joosten", quality='all')

    # for i in range(1000):
    #     pool.apply_async(buy_by_multi)
    # pool.close()
    # pool.join()
    # get_sid('6937069332829941513')