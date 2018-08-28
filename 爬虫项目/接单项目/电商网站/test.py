import requests
import urllib3
urllib3.disable_warnings()
pdduid = 15179833772
accesstoken = '4KVF5U4NUNLVDNAPUGZH4WNA5QAEXUYOUGEOQ7MWKBWZWRLYZWMQ101a825'

headers = {
    'Cookie': 'pdd_user_id={}; PDDAccessToken={};'.format(pdduid, accesstoken),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
}
# url = 'https://mobile.yangkeduo.com/addresses.html'
# res = requests.get(url, headers=headers, verify=False)
headers['AccessToken'] = accesstoken
# requests.options('https://api.pinduoduo.com/addresses?pdduid=4336079679912', headers=headers, verify=False)
rest = requests.get('https://api.pinduoduo.com/addresses?pdduid={}'.format(pdduid), headers=headers, verify=False)
print(rest.text)