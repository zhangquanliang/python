from requestium import Session, Keys
import urllib3
urllib3.disable_warnings()


s = Session(webdriver_path=r'D:\git\zhangql\util_zql\chromedriver(zql).exe', browser='chrome')
# a = s.get('http://www.baidu.com')
# c = a.decode('gbk')
a = s.request('get', 'http://www.baidu.com', verify=False)
print(a.text)