# -*- coding:utf-8 -*-
"""
Title = 抖音用户小视频
author = zhangql
"""
import requests

class DouYin:
    def __init__(self):
        pass

    # 获取附近的抖音视频
    def get_fj_movie(self):
        pass


    def save_movie(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Proxy-Connection": "keep-alive",
            "Range": "bytes=0-",
            "Accept": "*/*",
            "Accept-Encoding": "identity;q=1, *;q=0"
        }
        # url = 'https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200f190000bbvb9nignbh5ubla0go0&line=0'
        res = requests.get(url, verify=False, headers=headers, allow_redirects=False)
        s_url = res.headers['Location']
        headers["Referer"] = s_url
        res2 = requests.get(s_url, headers=headers, verify=False)
        with open('video.mp4', 'wb') as f:
            f.write(res2.content)



if __name__ == '__main__':
    douyin = DouYin()
    douyin.get_fj_movie()