# -*- coding: utf-8 -*-

import urllib.request
import urllib
import http.cookiejar
import gzip
import re
import os
import json
import getpass


def saveFile(data):
    save_path = './response'
    f_obj = open(save_path, 'wb')  # wb 表示打开方式
    f_obj.write(data)
    f_obj.close()


def getXSRF(data):
    cer = re.compile('name="_xsrf" value="(.*)"', flags=0)
    strlist = cer.findall(data)
    return strlist[0]


def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data


def get_captcha():
    buf = urllib.request.urlopen(u'http://www.zhihu.com/captcha.gif')
    f = open(u'验证码.gif', 'wb')
    f.write(buf.read())
    f.close()
    print('验证码在程序运行的文件夹中，请输入验证码')
    os.system("gnome-open ./验证码.gif")
    captcha_str = input()
    print("输入的验证码为: " + captcha_str)
    return captcha_str


def getOpener(head):
    # deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


def get_account_password():
    account = input()
    while re.search(r'\w+@[\w\.]{3,}', account) is None:   # 匹配邮箱的正则表达式，可以更完善
        print('抱歉，输入的账号不规范...\n请输入正确的知乎登录邮箱\n')
        print('账号要求：1.必须是正确格式的邮箱\n2.邮箱用户名只能由数字、字母和下划线_构成\n3.@后面必须要有.而且长度至少为3位')
        print('请重新输入账号，回车确认')
        account = input()
    print('OK,验证通过\n请输入密码，回车确认')
    # password = input()
    password = getpass.getpass()
    while len(password) < 6:
        print('密码至少6位起~')
        print('请重新输入密码，回车确认')
        password = raw_input()
    return account, password


def generateMessage(account, password, _xsrf, captcha=''):
    postDict = {
        '_xsrf': _xsrf,
        'email': account,
        'password': password,
        'rememberme': 'y',
        'captcha': captcha
    }

    postData = urllib.parse.urlencode(postDict).encode()
    print(postData)
    return postData
    

def main_start():
    head = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Encoding': 'gzip,deflate',  # 主要属性，有此项，知乎认为来源非脚本
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    head['Origin'] = 'http://www.zhihu.com'
    head['Referer'] = 'http://www.zhihu.com'

    url = "http://www.zhihu.com"
    url_login = "http://www.zhihu.com/login/email"
    opener = getOpener(head)
    
    captcha = get_captcha()

    op = opener.open(url, timeout=1000)
    data = ungzip(op.read())
    _xsrf = getXSRF(data.decode("utf-8"))
    print("_xsrf: %s" % (_xsrf, ))
    print("验证码: %s" % (captcha, ))

    print("现在开始登陆，请根据提示输入您的账号密码")
    print('请输入用户名（知乎注册邮箱），回车确认')
    account, password = get_account_password()
    print("account: %s" % (account, ))
    # print "password:", password

    print("获取验证码图片，请准备输入验证码:")
    

    msg = generateMessage(account, password, _xsrf, captcha)
    op = opener.open(url_login, msg)
    data = ungzip(op.read())

    print(data.decode('utf-8'))

if __name__ == "__main__":
    # opener = makeMyOpener()
    main_start()
    # uop = opener.open('http://www.zhihu.com/', timeout=1000)
    # data = ungzip(uop.read())
    # saveFile(data)
    # # xsrf = getXSRF(data.decode('utf-8'))
    # get_captcha()
