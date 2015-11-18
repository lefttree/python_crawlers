# -*- coding: utf-8 -*-
# ######################################################
# File Name   :    ideatest.py
# Description :    模拟知乎登陆
# Author      :    Frank
# Date        :    2014.04.04
# ######################################################

import cookielib
import urllib2
import urllib
import zlib
import json
import re
import time
import socket


cookieJarInMemory = cookielib.LWPCookieJar()

def main_start():
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJarInMemory))
    urllib2.install_opener(opener)

    print u'现在开始登陆，请根据提示输入您的账号密码'
    print u'请输入用户名（知乎注册邮箱），回车确认'
    account, password = get_account_password()
    print "account:", account
    print "password:", password
    captcha = ''
    while not send_message(account, password, captcha):
        print u'啊哦，登录失败了'
        print u'或者猛击回车进入获取验证码的流程'
        confirm = raw_input()
        captcha = get_captcha()
    return


def send_message(account, password, captcha=''):
    xsrf = getXsrf(get_http_content('http://www.zhihu.com'))
    if xsrf == '':
        print u'知乎网页打开失败'
        print u'回车重新发送登陆请求'
        return False
    _xsrf = xsrf.split('=')[1]
    # add xsrf as cookie into cookieJar,
    xsrfCookie = make_cookie(name='_xsrf', value=_xsrf, domain='www.zhihu.com')
    cookieJarInMemory.set_cookie(xsrfCookie)
    if captcha == '':    # 如果没有验证码
        loginData = '{0}&email={1}&password={2}'.format(xsrf, account, password, ) + '&rememberme=y'
    else:
        loginData = '{0}&email={1}&password={2}&captcha={3}'.format(xsrf, account, password, captcha) + '&rememberme=y'
    loginData = urllib.quote(loginData, safe='=&')     # 表示不要对=&编码
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',    # 主要属性，有此项，知乎认为来源非脚本
        'Accept-Language': 'zh,zh-CN;q=0.8,en-GB;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/34.0.1847.116 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    header['Origin'] = 'http://www.zhihu.com'
    header['Referer'] = 'http://www.zhihu.com/'

    request = urllib2.Request(url='http://www.zhihu.com/login/email', data=loginData)

    for headerKey in header.keys():
        request.add_header(headerKey, header[headerKey])

    try:
        result = urllib2.urlopen(request)
        jsonData = zlib.decompress(result.read(), 16 + zlib.MAX_WBITS)
        result = json.loads(jsonData)
        print "输出result:", result
    except Exception as error:
        print error
        return False

    if result['r'] == 0:
        print u'登陆成功!'
        print u'登陆的账号为：', account
        return True
    else:
        print u'登陆失败!'
        return False

def get_account_password():
    account = raw_input()
    while re.search(r'\w+@[\w\.]{3,}', account) is None:   # 匹配邮箱的正则表达式，可以更完善
        print u'抱歉，输入的账号不规范...\n请输入正确的知乎登录邮箱\n'
        print u'账号要求：1.必须是正确格式的邮箱\n2.邮箱用户名只能由数字、字母和下划线_构成\n3.@后面必须要有.而且长度至少为3位'
        print u'请重新输入账号，回车确认'
        account = raw_input()
    print u'OK,验证通过\n请输入密码，回车确认'
    password = raw_input()
    while len(password) < 6:
        print u'密码至少6位起~'
        print u'请重新输入密码，回车确认'
        password = raw_input()
    return account, password

def getXsrf(content=''):
    u"""
    提取xsrf信息
    """
    xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
    if xsrf == None:
        return ''
    else:
        return '_xsrf=' + xsrf.group(0)

def get_http_content(url='', extraHeader={} , data=None, timeout=5):
    u"""获取网页内容

    获取网页内容, 打开网页超过设定的超时时间则报错

    参数:
        url         一个字符串,待打开的网址
        extraHeader 一个简单字典,需要添加的http头信息
        data        需传输的数据,默认为空
        timeout     int格式的秒数，打开网页超过这个时间将直接退出，停止等待
    返回:
        pageContent 打开成功时返回页面内容，字符串或二进制数据|失败则返回空字符串
    报错:
        IOError     当解压缩页面失败时报错
    """
    if data == None:
        request = urllib2.Request(url=url)
    else:
        request = urllib2.Request(url=url, data=data)
    for headerKey in extraHeader.keys():
        request.add_header(headerKey, extraHeader[headerKey])
    try:
        raw_page_data = urllib2.urlopen(request, timeout=timeout)
    except urllib2.HTTPError as error:
        print u'网页打开失败'
        print u'错误页面:' + url
        if hasattr(error, 'code'):
            print u'失败代码:' + str(error.code)
        if hasattr(error, 'reason'):
            print u'错误原因:' + error.reason
    except urllib2.URLError as error:
        print u'网络连接异常'
        print u'错误页面:' + url
        print u'错误原因:'
        print error.reason
    except socket.timeout as error:
        print u'打开网页超时'
        print u'超时页面' + url
    else:
        return decodeGZip(raw_page_data)
    return ''

def decodeGZip(rawPageData):
    u"""返回处理后的正常网页内容

    判断网页内容是否被压缩，无则直接返回，若被压缩则使用zlip解压后返回

    参数:
        rawPageData   urlopen()传回的fileLike object
    返回:
        pageContent   页面内容，字符串或二进制数据|解压缩失败时则返回空字符串
    报错:
        无
    """
    if rawPageData.info().get(u"Content-Encoding") == "gzip":
        try:
            page_content = zlib.decompress(rawPageData.read(), 16 + zlib.MAX_WBITS)
        except zlib.error as ziperror:
            print u'解压出错'
            print u'出错解压页面:' + rawPageData.geturl()
            print u'错误信息：'
            print zlib.error
            return ''
    else:
        page_content = rawPageData.read()
        return page_content

def get_captcha():
    buf = urllib2.urlopen(u'http://www.zhihu.com/captcha.gif')     # 获得验证码的图片
    f = open(u'验证码.gif', 'wb')
    f.write(buf.read())
    f.close()
    print u'验证码在程序运行的文件夹中，请输入验证码'
    captcha_str = raw_input()
    return captcha_str

def make_cookie(name, value, domain):
    cookie = cookielib.Cookie(
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

if __name__ == "__main__":
    main_start()
