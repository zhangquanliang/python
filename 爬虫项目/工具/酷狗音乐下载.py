# encoding=utf8
"""
Title = 酷狗音乐歌曲下载
Date = 2018-03-12
"""
from multiprocessing import Pool
import json
import hashlib
import requests
import urllib.request


def start_pool(filename, download_url):
    urllib.request.urlretrieve(download_url, 'F:\\music\\' + filename + '.mp3')


if __name__ == '__main__':
    name = input('欢迎来到音乐下载系统, 请输入想要下载的音乐:')
    # 搜索歌曲地址
    filePath = 'http://songsearch.kugou.com/song_search_v2?keyword=%s&page=1&pagesize=30'

    text = requests.get(filePath % name).text

    jsobj =json.loads(text)
    list = jsobj['data']['lists']
    for i in list:
        filename = i['FileName']    # 歌曲名
        filehash = i['FileHash']    # 歌曲hash
        print(u'已搜索到音乐 %s' % filename)
        url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash=2688ADB1CA449448388270987BDCE6E8&album_id=960327'
        page = requests.get(url).text
        page_json = json.loads(page)
        down_url = page_json['data']['play_url']
        pool = Pool(processes=4)
        print(u'正在为你下载音乐: [%s] ' % filename)
        print(u'音乐下载地址为 ', down_url)
        pool.apply_async(start_pool, (filename, down_url))
        pool.close()
        pool.join()