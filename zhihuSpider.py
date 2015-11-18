# -*- coding: utf-8 -*-

import urllib.request
import urllib
import http.cookiejar
import gzip
import re
import os
import json
import getpass
import time
from sys import platform as _platform

cj = http.cookiejar.CookieJar()


def saveFile(data):
    save_path = './response.html'
    f_obj = open(save_path, 'wb')  # wb 表示打开方式
    f_obj.write(data)
    f_obj.close()


def getXSRF(data):
    cer = re.compile('name="_xsrf" value="(.*)"', flags=0)
    strlist = cer.findall(data)
    return strlist[0]

def make_cookie(name, value, domain):
    cookie = http.cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=time.time() + 300000000,
        discard=False,
        comment=None,
        comment_url=None,
        rest={}
    )
    return cookie


def ungzip(data):
    try:        # 尝试解压
        # print('正在解压.....')
        data = gzip.decompress(data)
        # print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data


def get_captcha(opener):
    buf = opener.open(u'http://www.zhihu.com/captcha.gif')
    f = open(u'验证码.gif', 'wb')
    f.write(buf.read())
    f.close()
    print('验证码在程序运行的文件夹中，请输入验证码')
    if _platform == "linux" or _platform == "linux2":
        os.system("gnome-open ./验证码.gif")
    elif _platform == "darwin":
        os.system("open ./验证码.gif")
    elif _platform == "win32":
        os.system("验证码.gif")
    captcha_str = input()
    print("输入的验证码为: " + captcha_str)
    return captcha_str


def getOpener(head):
    # deal with the Cookies
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    # urllib.request.install_opener(opener)
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
    
    if captcha != '':
        print("使用验证码登录")
        postDict['captcha'] = captcha

    postData = urllib.parse.urlencode(postDict).encode()
    return postData
    

def send_message(opener, account, password, captcha):
    url = "http://www.zhihu.com"
    url_login = "http://www.zhihu.com/login/email"

    op = opener.open(url, timeout=5)
    data = ungzip(op.read())
    _xsrf = getXSRF(data.decode("utf-8"))
    print("_xsrf: ", _xsrf)
    xsrfCookie = make_cookie(name='_xsrf', value=_xsrf, domain='www.zhihu.com')
    cj.set_cookie(xsrfCookie)

    postDict = {
        '_xsrf': _xsrf,
        'email': account,
        'password': password,
        'rememberme': 'true'
    }

    msg = generateMessage(account, password, _xsrf, captcha)

    try:
        op = opener.open(url_login, msg)
        data = ungzip(op.read())
        result = json.loads(data.decode("utf-8"))
        print("result: " + str(result))
    except  Exception as error:
        print(error)
        return False

    if result['r'] == 0:
        print('登陆成功!')
        print('登陆的账号为：', account)
        return True
    else:
        print('登陆失败!')
        return False

def main_start():

    head = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Encoding': 'gzip,deflate',  # 主要属性，有此项，知乎认为来源非脚本
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    head['Origin'] = 'http://www.zhihu.com'
    head['Referer'] = 'http://www.zhihu.com'

    
    opener = getOpener(head)
    
    print("现在开始登陆，请根据提示输入您的账号密码")
    print('请输入用户名（知乎注册邮箱），回车确认')
    account, password = get_account_password()
    print("account: %s" % (account, ))
    # print "password:", password

    captcha = ''
    while not send_message(opener, account, password, captcha):
        print("登录失败了")
        print("回车进入获取验证码的流程")
        confirm = input()
        captcha = get_captcha(opener)

    index = opener.open("http://www.zhihu.com")
    d = ungzip(index.read())
    saveFile(d)

    # msg = generateMessage(account, password, _xsrf, captcha)
    

if __name__ == "__main__":
    # opener = makeMyOpener()
    main_start()
