from flask import Flask, request
from flask import render_template, send_from_directory
from model.sqlalchemy_models import AccBalance, AccTraded, AccBaseInfo
from model.sqlalchemy_models import session
import datetime
import time
import os
import json
import xlwt
from web.export_certificate import export_certificate
app = Flask(__name__)


def query():
    acc_number = request.args.get('acc_number', '')

    traded_date_s = request.args.get('acc_traded_date_s', '')
    traded_date_e = request.args.get('acc_traded_date_e', '')
    bank_type = request.args.get('bank_type', '')
    if not bank_type:
        bank_type = "CMBE"

    if not traded_date_s:
        traded_date_s = datetime.datetime.now().strftime("%Y-%m-%d")
    if not traded_date_e:
        traded_date_e = datetime.datetime.now().strftime("%Y-%m-%d")
    traded_date_s = datetime.datetime.strptime(traded_date_s, "%Y-%m-%d")
    traded_date_e = datetime.datetime.strptime(traded_date_e, "%Y-%m-%d") + datetime.timedelta(days=1)

    acc_list = session.query(AccBaseInfo).order_by(AccBaseInfo.acc_number).filter_by(bank_type=bank_type)
    if not acc_number:
        balance = session.query(AccBalance).filter_by(acc_number=acc_number).one()

        traded_list = session.query(AccTraded).order_by(AccTraded.id.desc()) \
            .filter_by(acc_number=acc_number)\
            .filter(AccTraded.acc_transaction_date.between(traded_date_s, traded_date_e))\
            .all()
    else:
        balance = AccBalance(acc_number='')
        traded_list = []

    return balance, traded_list, traded_date_s, traded_date_e, bank_type, acc_list


@app.route('/')
def spider_data_page():
    balance, traded_list, traded_date_s, traded_date_e, bank_type, acc_list = query()
    for traded in traded_list:
        if not traded.acc_drawee_money:
            traded.acc_drawee_money = 0.00
        if not traded.acc_credit_money:
            traded.acc_credit_money = 0.00
        if not traded.acc_balance:
            traded.acc_balance = 0.00
        traded.transaction_date = traded.acc_transaction_date.strftime("%Y-%m-%d")

    return render_template('simple.html', balance=balance, treded_list=traded_list, traded_date_s=traded_date_s,
                           traded_date_e=traded_date_e, bank_type=bank_type, acc_list=acc_list)


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
        balance, traded_list, traded_date_s, traded_date_e = query()

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Sheet')
        ws.write_merge(0, 0, 0, 7, '账户流水明细(31000188000145586)({})'.format(datetime.datetime.now()))
        ws.write(1, 0, "序号")
        ws.write(1, 1, "交易日期")
        ws.write(1, 2, "对方账号")
        ws.write(1, 3, "对方户名")
        ws.write(1, 4, "收入")
        ws.write(1, 5, "支出")
        ws.write(1, 6, "余额")
        for j in range(7):
            ws.col(j).width = 0x0d00 + j*500
        i = 2
        traded_list = list(reversed(traded_list))
        for traded in traded_list:
            ws.write(i, 0, str(i-1))
            ws.write(i, 1, str(traded.acc_transaction_date).replace("-", ""))
            ws.write(i, 2, traded.acc_opposite_number)
            ws.write(i, 3, traded.acc_opposite_name)
            ws.write(i, 4, traded.acc_credit_money)
            ws.write(i, 5, traded.acc_drawee_money)
            ws.write(i, 6, traded.acc_balance)
            i = i+1
        filename = 'account-flow-{}.xls'.format(int(time.time()))
        wb.save("files/{}".format(filename))
        print(filename)

    return send_from_directory("files", filename, as_attachment=True)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
    )
