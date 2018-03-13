from flask import Flask, request
from flask import render_template, send_from_directory
import datetime
import time
import os
import json
import xlwt
from web.export_certificate import export_certificate
app = Flask(__name__)


@app.route('/corporbank/quickCheckVerifyCode.do', methods=['POST'])
def config():
    # return render_template('simple.html',)
    traded_date_s = request.args.get('LOGINNM', '')
    traded_date_s = request.args.get('loginPwd', '')
    traded_date_s = request.args.get('verifyCode', '')
    traded_date_s = request.args.get('EMP_SID', '')
    return "succ"


@app.route('/corporbank/ebill_userLogin.do', methods=['POST', 'GET'])
def config1():
    # return render_template('simple.html',)
    traded_date_s1 = request.args.get('LOGINNM', '')
    traded_date_s2 = request.args.get('loginPwd', '')
    traded_date_s3 = request.args.get('verifyCode', '')
    traded_date_s4 = request.args.get('EMP_SID', '')
    print(traded_date_s1, traded_date_s2, traded_date_s3, traded_date_s4)
    return traded_date_s1+traded_date_s2+traded_date_s3 + traded_date_s4




if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
    )