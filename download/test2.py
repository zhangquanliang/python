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
    name = input('请输入想要下载的音乐:')
    # name = 'panama'
    filePath = 'http://songsearch.kugou.com/song_search_v2?keyword=%s&page=1&pagesize=30'

    # VIP音乐URL
    filePath2 = 'http://trackercdn.kugou.com/i/?cmd=4&hash=%s&key=%s&pid=1&forceDown=0&vip=1'

    text = requests.get(filePath % name).text

    jsobj =json.loads(text)
    list = jsobj['data']['lists']
    for l in list:
        file_name = l['FileName']
        hash = l['FileHash']    # 文件下载需要的hash
        album_id = l['AlbumID']   # 文件下载需要的ID
        print(album_id)
        url = 'http://www.kugou.com/song/#hash=%s&album_id=%s' % (hash, album_id)
        print(url)