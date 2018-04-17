
# -*- coding: utf-8 -*-
import requests
import os
import urllib3
urllib3.disable_warnings()
"""
Title = 王者荣耀盒子App(英雄皮肤) + 掌上英雄联盟App(英雄皮肤)
Date = 2018-03-27
"""


class Wzry:
    """王者荣耀英雄"""

    def __init__(self):
        self.headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.1; vivo X20Plus UD Build/NMF26X)"
        }
        self.url = "http://gamehelper.gm825.com/wzry/hero/list?channel_id=90028a&app_id=h9044j&game_id=7622"

    # 王者荣耀英雄
    def wzry_hero(self):
        rs = requests.get(self.url, headers=self.headers, verify=False)

        for hero_list in rs.json()['list']:
            name = hero_list['name']
            image_url = hero_list['cover']
            response = requests.get(image_url, headers=self.headers, verify=False)
            hero = response.content
            save_hero(hero=hero, name=name)


class LoL:
    """英雄联盟"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.1; vivo X20Plus UD Build/NMF26X)"
        }
        self.url = 'http://apps.game.qq.com/daoju/go/zmgoods/cat?plat=android&version=9774'

    def lol_hero(self):
        rs = requests.get(self.url, self.headers, verify=False)
        for hero_type_list in rs.json()['list']:
            for hero_type_scat in hero_type_list['scat']:
                scat = hero_type_scat['id']
                hero_type = hero_type_scat['name']
                if scat == 0 or scat == '0':
                    continue
                self.get_hero(scat=int(scat), hero_type=hero_type)
            break

    def get_hero(self, scat, hero_type=None):
        for page in range(10):
            hero_list_url = 'http://apps.game.qq.com/daoju/go/zmgoods/list?cat=16&orderby=dtBegin&scat=%s' % scat + \
                            '&filter=&page=%s&plat=android&version=9774' % page
            rs = requests.get(hero_list_url, self.headers, verify=False)
            a = rs.json()['data']['goods']
            if a is None or a == "null" or a == "":
                continue

            for hero_list in rs.json()['data']['goods']:
                name = hero_list['sGoodsName']
                image_url = hero_list['sGoodsPic']
                response = requests.get(image_url, headers=self.headers, verify=False)
                hero = response.content
                save_hero(hero=hero, name=name, hero_type=hero_type)


# 用于保存英雄图片
def save_hero(hero, name, hero_type=None):
    if hero_type is None:
        isTrue = os.path.exists('heros')
        if isTrue:
            pass
        else:
            os.mkdir('heros')
    else:
        isTrue = os.path.exists('heros/{}'.format(hero_type))
        if isTrue:
            pass
        else:
            os.mkdir('heros/{}'.format(hero_type))

    hero_png_path = r'heros/{}/'.format(hero_type) + name + '.png'
    f = open(hero_png_path, 'wb')
    f.write(hero)
    f.close()


if __name__ == '__main__':
    # wzry = Wzry()      # 王者荣耀
    # wzry.wzry_hero()   # 王者荣耀
    lol = LoL()
    lol.lol_hero()