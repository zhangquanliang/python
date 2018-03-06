# encoding=utf8
import sys, os
from multiprocessing import Pool
import json
import hashlib
import requests
import urllib.request

def getMd5(src):
    m2 = hashlib.md5(src.encode('utf-8')).hexdigest()
    return m2

def start_pool(filename, download_url):
    urllib.request.urlretrieve(download_url, 'F:\\download\\' + filename + '.mp3')


if __name__ == '__main__':
    name=input('请输入音乐：')
    # name = 'panama'
    filePath = 'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=%s&page=1&pagesize=30'

    # VIP音乐URL
    filePath2 = 'http://trackercdn.kugou.com/i/?cmd=4&hash=%s&key=%s&pid=1&forceDown=0&vip=1'

    response = requests.get(filePath % name)
    text = response.text
    jsobj =json.loads(text)
    list = jsobj['data']['info']
    for l in list:
        filename = l['filename']
        sqhash =l['sqhash']
        #所需hash值
        # sqhash='3ff53ce866608179f53e226796ae525d'
        if sqhash!='':
            key = getMd5(l['sqhash'] + "kgcloud")
            # if固定hash值
            # key = getMd5(sqhash + "kgcloud")
            filePath3 = filePath2%(sqhash, key)
            print('歌名: %s' % filename)
            #取URL-filePath3 的内容(url)
            req=requests.get(filePath3)
            url_text = req.text
            print(filePath3)
            print(url_text)
            dictinfo = json.loads(url_text)
            print('下载地址： %s' % (dictinfo["url"]))
            download_url = dictinfo["url"]
            # pool = Pool(processes=4)
            # pool.apply_async(start_pool, (filename, download_url))
            # pool.close()
            # pool.join()

    # print('\n' * 1)
    # input('\n---------------------按任意键退出---------------------')