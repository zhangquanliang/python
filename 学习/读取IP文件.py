# -*- coding: utf-8 -*-
import datetime
import requests
import xlrd


def read_excel():
    ip_list = []
    book = xlrd.open_workbook(r'7500个ip.xlsx')
    sheet = book.sheet_by_index(0)
    nrows = sheet.nrows  # 多少行
    for i in range(1, nrows):
        ip = sheet.row_values(i)[3]
        if ip == '':
            continue
        port = sheet.row_values(i)[4]
        ip_dict = {'ip':ip, 'port':port}
        ip_list.append(ip_dict)
    return ip_list


def check_ip(ip, port):
    url = 'http://www.baidu.com'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"
    headers = {'user-agent': user_agent}
    proxies = {'http': 'http://{}:{}'.format(ip, port)}
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=5)
        if response.status_code == 200 and '百度搜索' in response.text:
            with open(r'有效ip.txt', 'a+', encoding='utf-8') as f:
                f.write(ip + ' ' * 3 + port + '\n')
    except:
        pass



if __name__ == '__main__':
    ip_list = read_excel()
    from multiprocessing.dummy import  Pool
    pool = Pool(processes=10)
    for ip_dict in ip_list:
        pool.apply_async(check_ip, (ip_dict['ip'], ip_dict['port']))
    pool.close()
    pool.join()