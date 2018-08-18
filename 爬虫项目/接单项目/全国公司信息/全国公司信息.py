# coding = utf-8
import requests
from bs4 import BeautifulSoup
import json
from openpyxl import Workbook
import city
import pymysql
import datetime
from multiprocessing.dummy import Pool


headers = {
    'Cookie': 'cook_weixin=1; __jsluid=1013f33a49a1ca19b5388bca93560953; qlm_username=13705768550; qlm_password=gmuBRU3fjfEB7fBEEg7ogu7KCpuC883g; rem_login=1; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1516065019; UM_distinctid=163f1c1267b220-096b0392e0cb668-7b155f38-15f900-163f1c1267c1be; gr_user_id=e4f0ca73-4089-489a-bd2a-62125010da89; seo_intime="2018-08-11 15:49:01"; qlmll_his=",89884704,15314730,58057472,57629015,27049073,59185256,60158675,58103724,72989228,75418735,"; Hm_lvt_0a38bdb0467f2ce847386f381ff6c0e8=1532388946,1533952948,1534299656; Hm_lvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1532388946,1533952949,1534299657; seo_refUrl=; seo_curUrl=www.qianlima.com; ant_stream_507d9bc0b72ac=1478016737/2272679883; JSESSIONID=D6CC886361803AF4D440B5A9B67F6AB0.tomcat2; gr_session_id_83e3b26ab9124002bae03256fc549065=bfae9211-ebb7-4108-a29f-443f2c51562d; Hm_lpvt_0a38bdb0467f2ce847386f381ff6c0e8=1534384158;'
              ' Hm_lpvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1534384158; gr_session_id_83e3b26ab9124002bae03256fc549065_bfae9211-ebb7-4108-a29f-443f2c51562d=true',
    'Host':'center.qianlima.com',
    'Referer': 'http://center.qianlima.com/db_qy.jsp?p_area=33',
# Upgrade-Insecure-Requests:1
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5733.400 QQBrowser/10.2.2050.400'
}


def get_city_list():
    # url = 'http://center.qianlima.com/js/select_arr.js'
    city_list = []
    city_list_ = city.city_list
    for x in city_list_:
        if x == 'qg':
            continue
        for j in city_list_[x]:
            city_list.append(j)
    return city_list


def get_city_company(city_url):
    all_shuju_list = []
    url = 'http://center.qianlima.com/db_qy.jsp{}'.format(city_url)
    headers['Referer'] = url
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if '该功能使用次数今日已达上限' in response.text:
            print('该功能使用次数今日已达上限, 请明日继续使用。')
            return all_shuju_list
        parse_html(response.text)
        # TODO 以Excel方式则开启
        # all_shuju_list.append(parse_html(response.text))
        print('获取数据成功，地址为[{}]'.format(url))
    else:
        print('请求异常，请求地址为[{}],响应地址为[{}]'.format(url, response.url))
        return all_shuju_list
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        # return all_shuju_list
        next_url = soup.find('div', class_='center').find_all('a')[-2]['href']
        get_city_company(next_url)
    except:
        print('已经获取到最后一页。')
        return all_shuju_list


def parse_html(html):
    shuju_list = []
    soup = BeautifulSoup(html, 'html.parser')
    table_tr_list = soup.find('table', class_='list').find_all('tr')
    for table_tr in table_tr_list:
        table_td_list = table_tr.find_all('td')
        gsmc = table_td_list[0].get_text().strip()
        if gsmc == '公司名称' or len(table_td_list) < 2:
            continue
        soup2 = BeautifulSoup(str(table_tr), 'html.parser')
        lxr = soup2.find('table', class_='nameList').get_text().strip().replace('\n', '')
        lxdh = soup2.find('table', class_='phoneList').get_text().strip().replace('\n', '')
        dz = table_td_list[-2].get_text().strip().replace('\n', '')
        dq = table_td_list[-1].get_text().strip().replace('\n', '')
        create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into qggs(gsmc,lxr, lxdh, dz, dq, create_date) values ('{}', '{}', '{}', '{}', '{}', '{}')"\
            .format(gsmc, lxr, lxdh, dz, dq, create_date)
        db_insert(sql)
        print('保存信息成功...', gsmc, lxr, lxdh, dz, dq)
        shuju_list.append([gsmc,lxr, lxdh, dz, dq])
    return shuju_list


# 数据库连接入库
def db_insert(sql):
    conn = pymysql.connect(host='localhost', user='root', password='zql9988', database='spider_j', charset='utf8')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as ex:
        print('保存信息失败!!!原因[{}]'.format(ex))
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    city_list = get_city_list()
    for j in city_list:
        shengfen = j['areaName']
        if shengfen != '浙江省':
            continue
        pool = Pool(processes=10)
        for city_ in j['hasCity']:
            city_id = city_['id']
            city_url = '?pg=1&p_area={}'.format(city_id)
            pool.apply_async(get_city_company, [city_url])
            # get_city_company(city_url)
        pool.close()
        pool.join()
        ### 以Excel写入
        """
        book = Workbook()
        city_name = city_['areaName']
        city_id = city_['id']
        excel_name = shengfen + '-' + city_name
        sheet = book.create_sheet(excel_name)
        sheet.append(['公司名称', '联系人', '联系人电话', '地址', '地区'])
        city_url = '?pg=1&p_area={}'.format(city_id)
        all_shuju_list = get_city_company(city_url)
        for shuju_ in all_shuju_list[0]:
            sheet.append(shuju_)
        book.save(excel_name + '.xlsx')
        break
        """
