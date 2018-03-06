# encoding=utf-8
import requests
import json
import time


def export_certificate(json_param):
    build_url = "https://wit-custody.jsbchina.cn:9070/plutussearch/plutus/search/account/exportCertificate"
    download_url = "https://wit-custody.jsbchina.cn:9070/plutussearch/search/yx/file/downloadByUrl?url="
    headers = {
        "Host": "wit-custody.jsbchina.cn:9070",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://wit-custody.jsbchina.cn:9070/plutussearch/goframe/p/plutus.search.account.account_list?_t=332093",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    }
    r = requests.post(build_url, json=json_param, headers=headers)
    result_json = r.json()
    print(result_json)
    if result_json["status"]:
        result_url = result_json["data"]
        _download_url = download_url + result_url
        print(_download_url)
        r = requests.get(_download_url)
        disposition = r.headers.get("Content-Disposition")
        print(disposition)
        filename = str(disposition).split("=")[1]
        with open("files/"+filename, "wb") as code:
            code.write(r.content)
            code.flush()
            code.close()
        return filename


def main():
    export_certificate([{"accountName":"江苏省国际信托有限责任公司","accountNo":"31000188000145586","balance":4390408.75,"expense":50000000,"flowId":"999967000048","income":0,"jdFlag":"0","money":50000000,"oppositeAccountName":"广发基金管理有限公司直销专户","oppositeAccountNo":"3602000129838383823","payDate":"2018-01-16","payTime":"20180116null","_id":46,"_uid":46}])


def test():
    pass
    from model.sqlalchemy_models import AccTraded
    import datetime
    AccTraded = AccTraded(acc_transaction_date=datetime.datetime.now())
    AccTraded.date = AccTraded.acc_transaction_date.strftime("%Y-%m-%d")
    print(AccTraded.date)

if __name__ == '__main__':
    # main()
    test()
