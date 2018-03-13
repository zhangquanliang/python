from flask import Flask, request
from flask import render_template, send_from_directory
from model.models import AccBalance, AccTraded, AccBaseInfo, LoginAcc
from model.model_manager import session
from util import data_interface
from model.model_manager import LoginAccManager
import datetime
import time
import os
import json
import xlwt
app = Flask(__name__)
from export_certificate import export_certificate


def query():
    acc_number = request.args.get('acc_number', '')
    traded_date_s = request.args.get('acc_traded_date_s', '')
    traded_date_e = request.args.get('acc_traded_date_e', '')
    bank_type = request.args.get('bank_type', '')
    if not bank_type:
        bank_type = "HXB"
    # if not acc_number:
    #     if bank_type == "CMBU":
    #         acc_number = "110902536410100"
    #     elif bank_type == "CMBE":
    #         acc_number = "110902536410116"

    if not traded_date_s:
        # traded_date_s = datetime.datetime.now().strftime("%Y-%m-%d")
        traded_date_s = "2017-01-01"
    if not traded_date_e:
        traded_date_e = datetime.datetime.now().strftime("%Y-%m-%d")
    traded_date_s_ = datetime.datetime.strptime(traded_date_s, "%Y-%m-%d")
    traded_date_e_ = datetime.datetime.strptime(traded_date_e, "%Y-%m-%d") + datetime.timedelta(days=1)

    acc_list = session.query(AccBaseInfo).order_by(AccBaseInfo.acc_number).filter_by(bank_type=bank_type)
    print(acc_number, bank_type, traded_date_s_, traded_date_e_, acc_list)
    balance = None
    traded_list = None
    if acc_number:
        try:
            balance = session.query(AccBalance).filter_by(acc_number=acc_number).first()

            traded_list = session.query(AccTraded).order_by(AccTraded.acc_transaction_time.desc()) \
                .filter_by(acc_number=acc_number)\
                .filter(AccTraded.acc_transaction_date.between(traded_date_s_, traded_date_e_))\
                .all()
        except:
            print("Query Exception!")

    if balance is None:
        balance = AccBalance(acc_number='', acc_balance=0.00, acc_name='', created_at='')
    if traded_list is None:
        traded_list = []

    print(balance, traded_list, traded_date_s, traded_date_e, bank_type, acc_list)
    return balance, traded_list, traded_date_s, traded_date_e, bank_type, acc_list, acc_number


@app.route('/')
def spider_data_page():
    balance, traded_list, traded_date_s, traded_date_e, bank_type, acc_list, acc_number = query()
    for traded in traded_list:
        if not traded.acc_drawee_money:
            traded.acc_drawee_money = 0.00
        if not traded.acc_credit_money:
            traded.acc_credit_money = 0.00
        if not traded.acc_balance:
            traded.acc_balance = 0.00
        traded.transaction_date = traded.acc_transaction_date.strftime("%Y-%m-%d")
        if not traded.acc_abstract:
            traded.acc_abstract = ""
        if not traded.acc_opposite_name:
            traded.acc_opposite_name = ""
        if not traded.acc_opposite_number:
            traded.acc_opposite_number = ""
        if not traded.acc_opposite_open_name:
            traded.acc_opposite_open_name = ""
        if not traded.acc_remarks:
            traded.acc_remarks = ""

    return render_template('simple.html', balance=balance, treded_list=traded_list, traded_date_s=traded_date_s,
                           traded_date_e=traded_date_e, bank_type=bank_type, acc_list=acc_list, acc_number=acc_number)


@app.route('/download', methods=['POST', 'GET'])
def download_file():
    pass
    exp_type = request.args.get('exp_type', '')
    if exp_type == 'certificate':
        data_list = request.values.getlist("data_check")
        post_list = []
        for data in data_list:
            _data = str(data).split("|")
            jd_flag = "1"
            income = _data[3]
            money = _data[3]
            account_name = "江苏省国际信托有限责任公司"
            account_no = "31000188000145586"
            from_acc_name = account_name
            from_acc_no = account_no
            to_acc_name = _data[2]
            to_acc_no = _data[1]

            if _data[4] != "0.00":
                jd_flag = "0"
                income = 0
                money = _data[4]
                from_acc_name = _data[2]
                from_acc_no = _data[1]
                to_acc_name = account_name
                to_acc_no = account_no

            param_dict = {
                "accountName": from_acc_name,
                "accountNo": from_acc_no,
                "balance": _data[5],
                "expense": 0,
                "flowId": _data[6],
                "income": income,
                "jd_flag": jd_flag,
                "money": money,
                "oppositeAccountName": to_acc_name,
                "oppositeAccountNo": to_acc_no,
                "payDate": _data[0],
                "payTime": _data[0],
                "_id": 2,
                "_uid": 2
            }
            post_list.append(param_dict)

        filename = export_certificate(post_list)

    if exp_type == 'flow':
        balance, traded_list, traded_date_s, traded_date_e,bank_type, acc_list, acc_number = query()

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Sheet')
        ws.write_merge(0, 0, 0, 7, '账户流水明细({})({})'.format(acc_number,datetime.datetime.now()))
        ws.write(1, 0, "序号")
        ws.write(1, 1, "交易日期")
        ws.write(1, 2, "对方账号")
        ws.write(1, 3, "对方户名")
        ws.write(1, 4, "对方银行")
        ws.write(1, 5, "收入")
        ws.write(1, 6, "支出")
        ws.write(1, 7, "余额")
        ws.write(1, 8, "摘要")
        ws.write(1, 9, "附言")

        for j in range(10):
            ws.col(j).width = 0x0d00 + j*500
        i = 2
        traded_list = list(reversed(traded_list))
        for traded in traded_list:
            ws.write(i, 0, str(i-1))
            ws.write(i, 1, str(traded.acc_transaction_date).replace("-", ""))
            ws.write(i, 2, traded.acc_opposite_number)
            ws.write(i, 3, traded.acc_opposite_name)
            ws.write(i, 4, traded.acc_opposite_open_name)
            ws.write(i, 5, traded.acc_credit_money)
            ws.write(i, 6, traded.acc_drawee_money)
            ws.write(i, 7, traded.acc_balance)
            ws.write(i, 8, traded.acc_abstract)
            ws.write(i, 9, traded.acc_remarks)
            i = i+1
        filename = 'account-flow-{}.xls'.format(int(time.time()))
        wb.save("D:\\{}".format(filename))
        print(filename)

    return send_from_directory("D:", filename, as_attachment=True)


@app.route('/login_info')
def config():
    return render_template('config.html',)


@app.route('/login_info_save', methods=['POST'])
def config_save():

    login_user = request.form['login_user']
    login_password = request.form['login_password']
    bank_type = request.form['bank_type']
    login_extend1 = request.form['login_extend1']

    login_user = LoginAcc(bank_type=bank_type, login_user=login_user, login_password=login_password, login_extend1=login_extend1)
    result = LoginAccManager.create_obj(login_user)
    if result:
        return "success"
    else:
        return "error"


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80, debug=True
    )
