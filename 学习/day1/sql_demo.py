import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'


def get_data(acc_number):
    conn = cx_Oracle.connect('tcmp/tcmp@192.168.1.7:1521/orcl')  # 连接数据库
    c = conn.cursor()  # 获取cursor
    sql = "select c_bankacco, c_projectcode, c_bankname, c_nameinbank from taccount_bankinfo where c_bankacco='{}'".format(acc_number)
    x = c.execute(sql)  # 使用cursor进行各种操作
    res = x.fetchall()
    c.close()  # 关闭cursor
    conn.close()  # 关闭连接
    return res


def update_data():
    conn = cx_Oracle.connect('system/Legion123@192.168.100.40:1522/LEGIONBOTCER')  # 连接数据库
    c = conn.cursor()  # 获取cursor
    x = c.execute('select "acc_number" from s_t_acc_baseinfo')  # 使用cursor进行各种操作
    acc_number_list = x.fetchall()
    c.close()  # 关闭cursor
    conn.close()  # 关闭连接

    for acc_number_ in acc_number_list:
        conn2 = cx_Oracle.connect('system/Legion123@192.168.100.40:1522/LEGIONBOTCER')  # 连接数据库
        c2 = conn2.cursor()  # 获取cursor
        res = get_data(acc_number_[0])
        if len(res) == 0:
            continue
        sql = """update s_t_acc_baseinfo set "project_id" = '{}', "open_bank"='{}', "acc_open_bank_name"='{}'
         where "acc_number" = '{}'""".format(res[0][1], res[0][2], res[0][3], res[0][0])
        print(sql)
        c2.execute(sql)
        conn2.commit()
        c2.close()  # 关闭cursor
        conn2.close()  # 关闭连接


if __name__ == '__main__':
    update_data()
    # get_data()