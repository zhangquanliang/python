import requests
import xlwt
import re
from bs4 import BeautifulSoup

lie_q = {}
book = xlwt.Workbook()
sheet = book.add_sheet('Sheet')
sheet.write(0, 0, '公司_品牌_车型')
sheet.write(0, 1, '配置ID')
lie = 1
hang = 0
max_lie = [1]


def get_all():
    url = 'http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/201806X.html'
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'gbk'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        list_table = soup.find_all('div', id='divBody')
        for list_ in list_table:
            parser_more(list_)
        book.save('车辆基本信息.xls')


# 一组数据，即一行
def parser_more(list_):
    global lie
    global hang
    hang += 1
    tr = list_.find('tr')
    name = tr.find('td').find('strong').get_text().strip()
    re_match = re.match('\d+', name)
    if not re_match:
        name_t = tr.find('td').find_all('strong')
        name_m = re.findall('<strong>.(\\d+)(.*?)</strong>', str(name_t), re.I | re.S)
        name = name_m[0][0] + name_m[0][1]

    tr_list = tr.find('table', class_='list-table').find_all('tr')
    sheet.write(hang, 0, name)

    for con_tr in tr_list:
        if '车辆基本信息' in con_tr.find('td').get_text().strip():
            cljbxx = ''
            for j in range(len(con_tr.find_all('td'))):
                cljbxx += con_tr.find_all('td')[j].get_text().strip() + '&'
            cljbxx_ = cljbxx.replace('车辆基本信息', '')
            cljbxx = cljbxx_[1:-1]
            sheet.write(hang, 1, cljbxx)
            continue
        lie_n = con_tr.find('th').get_text().strip().replace('\n', '').replace('：', '').replace('（', '').replace('）', '')
        zhi = ''
        for j in range(len(con_tr.find_all('td'))):
            zhi += con_tr.find_all('td')[j].get_text().strip() + "&"
        zhi = zhi[:-1]
        if lie_n not in lie_q.keys():
            lie = max(max_lie) + 1
            max_lie.append(lie)
            lie_q[lie_n] = lie
            sheet.write(0, lie, lie_n)
        else:
            lie = lie_q[lie_n]
        sheet.write(hang, lie, zhi)


if __name__ == '__main__':
    get_all()