# -*- coding: utf-8 -*-
import requests
import re
"""
Title = 知乎关注粉丝
Date = 2018-03-27
"""


class ZhiHu:
    """获取知乎粉丝信息"""

    def __init__(self):
        self.url = 'https://zhuanlan.zhihu.com/wajuejiprince'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
        }

    # 知乎粉丝信息
    def zh_fans(self):
        r = requests.session()
        response = r.get(self.url, headers=self.headers)

        # 查找共有多少人关注
        reg = re.findall('target="_blank">(.*?)人关注</a>', response.text)
        fans_number = int(reg[0].strip())
        num = int(fans_number/20)  # 共有44页

        f = open('fans_list.txt', 'a', encoding='utf-8')
        for i in range(num+1):
            if i == 0:
                fans_url = 'https://zhuanlan.zhihu.com/api/columns/wajuejiprince/followers?limit=20'
            else:
                offset = i*20
                fans_url = 'https://zhuanlan.zhihu.com/api/columns/wajuejiprince/followers?limit=20&offset={}'\
                    .format(offset)
            response = r.get(fans_url, headers=self.headers)
            for fans_list in response.json():
                job_name = fans_list['bio']
                name = fans_list['name']
                uid = str(fans_list['uid'])
                if job_name is None:
                    job_name = ""
                f.write(name)
                f.write('  ')
                f.write(job_name)
                f.write('  ')
                f.write(uid)
                f.write('\n')
                f.flush()

        f.close()


if __name__ == '__main__':
    zhihu = ZhiHu()
    zhihu.zh_fans()