#!/usr/bin/python
# -*- coding: utf-8 -*-
import re,os,random,json,os.path,scrapy,urllib,subprocess



class Wrtrhj(scrapy.Spider):
    name = "wrtrhj"
    start_urls = ['http://']


    #处理登录参数
    def start_login(self, response):
        print response
        imgUrl ="http//xxxxxxxx"  #验证码图片地址
        print u'进入首页获取登录验证码图片'
        yield scrapy.Request(imgUrl,
                             callback=self.parse_validator,
                             meta={'oldResponse': response},
                             dont_filter=True,)

    def parse(self, response):
        return self.start_login(response)

    def parse_validator(self, response):
        oldResponse = response.meta['oldResponse']
        filename = 'validate.gif'
        with open(filename, 'wb') as f:
            f.write(response.body)

        with open(os.devnull, "w") as fnull:
            cmd = self.settings['PRE_PROCESS_EXE'] + ' validate.gif validate.jpg'
            process = subprocess.Popen(cmd, shell=True, stdout=fnull, stderr=fnull)
            print u'预处理验证码图片'
            process.wait()

        with open(os.devnull, "w") as fnull:
            cmd = self.settings['TESSERACT_EXE'] + ' validate.jpg validate -psm 7'
            process = subprocess.Popen(cmd, shell=True, stdout=fnull, stderr=fnull)
            print u'解析验证码图片'
            process.wait()

        with open('validate.txt', 'r') as pData:
            validateText = unicode(re.sub("[^0123456789()+-x÷]", "", pData.readline()), "UTF-8")
            try:
                insignia = str(validateText[1])
            except:
                print u""
            IvalidateText= 1
            try:
                print insignia
            except:
                insignia="+"
            if ( validateText[0]==None and validateText[2]==None ) :
                self.start_login
            else:
                try:
                    if ( insignia == 'x' or insignia == 'X' ):
                        IvalidateText=int(validateText[0]) * int(validateText[2])
                    elif (insignia == '+'):
                        IvalidateText=int(validateText[0]) + int(validateText[2])
                    elif (insignia == '-'):
                        IvalidateText = int(validateText[0]) - int(validateText[2])
                    else:
                        IvalidateText = int(validateText[0]) / int(validateText[2])
                except:
                       self.start_login(response)

                print str(IvalidateText)
                self.logger.info('validate: ' + validateText)
                print u'开始登陆'
                return scrapy.FormRequest(
                    url='http://xxxxx',
                    method='POST',
                    headers={
                           'Accept': '*/*',
                           'Accept-Encoding': 'gzip, deflate',
                           'Accept-Language': 'zh-CN,zh;q=0.8',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36 ',
                           'X-Requested-With': 'XMLHttpRequest',
                           'Origin': 'http://114.251.10.109',
                           'Connection': 'keep-alive',
                           'Referer': 'http://114.251.10.109/wrdkpfmis/admin/shareuserlogin.jsp',
                           'Host': '114.251.10.109',
                    },
                    formdata={
                        'user_id': self.settings['LOGIN_NAME'],
                        'passwd': self.settings['PASSWORD'],
                        'validcode': str(IvalidateText),
                    },
                    callback=self.after_login,
                    dont_filter=True,
                )

    def after_login(self, response):
        with open('html\\after_login.html', 'wb') as f:
            f.write(response.body)
        if '错误' in response.body:#我这边的验证，如果登不上的话会返回错误
            # 验证不成功，重新来一遍
            print u'登录失败，重新登陆'
            yield scrapy.Request(self.start_urls[0], callback=self.start_login,dont_filter=True)
        else:
            print u'登陆成功'
