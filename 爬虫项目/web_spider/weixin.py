'''
使用代理池抓取搜狗微信文章
并写入mongdb数据库
'''
import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
import pymongo
#mongdb端口
client = pymongo.MongoClient('localhost')
#创建项目名称
db = client['weixin']
#实际操作想要获取更多信息，必须要登陆验证cookie
header = {
    "Host":"weixin.sogou.com",
    "Upgrade-Insecure-Requests":'1',
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}
star_url = "http://weixin.sogou.com/weixin?"
keyword = "青春励志美文"
#代理池的url
proxy_pool_url = "http://127.0.0.1:5000"
#默认代理是空，开始爬取使用本机ip，不能访问后更换ip
proxy = None
#最大请求次数
max_count = 5
def get_proxy():
    '''访问代理池获取代理，如果代理池为空则结束'''
    try:
        res = requests.get(proxy_pool_url)
        if res.status_code ==200:
            return res.text
        return None
    except ConnectionError:
        return None

def get_html(url,count=1):
    '''
    添加代理来获取网页内容
    :param url: 网页地址
    :param count: 次数限制
    :return: 网页内容
    '''
    print("正在爬取得是：",url)
    print("尝试次数：",count)
    global proxy
    if count >= max_count:
        print("请求太多次啦")
        return None
    try:
        if proxy:
            #代理添加格式字典{"http":"http://"+proxy}
            proxies = {
                "http":"http://"+proxy
            }
            #请求添加上代理
            res = requests.get(url,allow_redirects=False,headers=header,proxies=proxies)
        else:
            res = requests.get(url,allow_redirects=False,headers=header)
        if res.status_code == 200:
            return res.text
        if res.status_code ==302:
            print('302')
            proxy = get_proxy()
            if proxy:
                print("正在使用代理：",proxy)
                count+=1
                return get_html(url)
            else:
                print("获取代理失败")
                return None

    except ConnectionError as e:
        print('出错啦：',e.args)
        #递归调用
        proxy = get_proxy()
        count+=1
        return get_html(url,count)

def get_weixin_url(keyword,page):
    '''

    :param keyword: 想要搜索的内容
    :param page: 想要获得内容的页数
    :return: 返回一个函数（get_html(url)）的结果
    '''
    data = {
        "query":keyword,
        "type":'2',
        "page":page
    }
    #将中文转换成字节码
    queries = urlencode(data)
    # print(queries)
    #拼接成实际访问的url
    url = star_url+queries
    # print(url)
    #调用get_html（）函数
    html = get_html(url)
    return html


def parse_html(html):
    '''注意pq的使用方法
    使用pq解析获得的html来得到每页单个信息的url，
    返回一个生成器'''
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    '''访问网页url（微信没有反爬所以不用加header模拟浏览器，添加会出错(没有显示结果)），
    判断是否可以正常访问，并且返回网页内容'''
    try:
        res = requests.get(url)
        if res.status_code ==200:
            return res.text
        return None
    except ConnectionError:
        return None

def pares_detail(html):
    '''使用pq解析html来获得想要的元素信息，并且返回'''
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()#标题
        cent = doc('.rich_media_content').text()#内容文本
        date = doc('#publish_time').text()#发布日期
        ather = doc('#profileBt').text()#作者微信公众号
        return {
            'title':title,
            'cent':cent,
            'date':date,
            'ather':ather
        }
    except XMLSyntaxError:
        return None
def save_to_mongdb(data):
    '''把数据存储到mongdb中，
    使用update（）来去除重复的数据'''
    if db['articles'].update({'title':data['title']},{'$set':data},True):
        print("存储到mongdb成功",data['title'])
    else:
        print("存储失败",data['title'])
def main():
    '''注意判断是否有结果'''
    for page in range(1,11):
        #翻页爬去
        html = get_weixin_url(keyword,page)
        # print(html)
        if html:
            #获取每页单个信息详情的url列表
            art_urls = parse_html(html)
            # print(art_urls)
            #遍历获取带个信息的url
            for art_url in art_urls:
                # print(art_url)
                #解析单个信息的内容，返回想要的详情页内容
                art_html = get_detail(art_url)
                # print(art_html)
                #判断是否获得内容
                if art_html:
                    #解析提取想要获得的提取内容
                    art_data = pares_detail(art_html)
                    print(art_data)
                    #如果获得内容
                    if art_data:
                        #把内容存储到指定的mongdb中
                        save_to_mongdb(art_data)

if __name__ == '__main__':
    main()