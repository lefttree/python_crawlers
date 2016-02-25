# urllib, urllib2 & requests

>python3 urllib和urllib2已经合并成urllib

he urllib module has been split into parts and renamed in Python 3 to
urllib.request, urllib.parse, and urllib.error. The 2to3 tool will automatically
adapt imports when converting your sources to Python 3.
Also note that the urllib.urlopen() function has been removed in Python 3 in
favor of urllib2.urlopen().

Python的urllib和urllib2模块都做与请求URL相关的操作，但他们提供不同的功能。他们两个最显着的差异如下：

- urllib2可以接受一个Request对象，并以此可以来设置一个URL的headers，但是urllib\
只接收一个URL。这意味着，你不能伪装你的用户代理字符串等。
- urllib模块可以提供进行urlencode的方法，该方法用于GET查询字符串的生成，urllib2
的不具有这样的功能。这就是urllib与urllib2经常在一起使用的原因。

## urllib & urllib2 -> urllib in python3

in python3, is split into 

- `urllib.request` for opening and reading URLs
- `urllib.error`
- `urllib.parse` for parsing URLs
- `urllib.robotparser` for parsing `robots.txt` files

```python
import urllib.request
with urllib.request.urlopen('http://python.org/') as response:
   html = response.read()

# download the files
local_filename, headers = urllib.request.urlretrieve('http://python.org/')
html = open(local_filename)

# Request
req = urllib.request.Request('http://www.voidspace.org.uk')
with urllib.request.urlopen(req) as response:
   the_page = response.read()
```

In python3, all in `urllib`

```python
import urllib.request  
weburl = "http://www.douban.com/"  
webheader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}   
req = urllib.request.Request(url=weburl, headers=webheader)    
webPage=urllib.request.urlopen(req)  
data = webPage.read()  
data = data.decode('UTF-8')  
print(data)  
print(type(webPage))  
print(webPage.geturl())  
print(webPage.info())  
print(webPage.getcode())
```

## Request Class

Request

- URL
- data
- headers
- cookies
- ...

[Request class](https://cloud.google.com/appengine/docs/python/tools/webapp/requestclass)

## opener

- `installopener(opener)`
- `buildopener([handler,...])`

blablab

## requests module

requests use urllib3, inherited from urllib2

[requests doc](http://cn.python-requests.org/zh_CN/latest/)

## References

- [urllib与urllib2总结](http://www.cnblogs.com/wly923/archive/2013/05/07/3057122.html)
- [urllib, urllib2](http://hustcalm.me/blog/2013/11/14/httplib-httplib2-urllib-urllib2-whats-the-difference/)
- [python3.x爬虫教程](http://blog.csdn.net/evankaka/article/details/46849095)
- [深入理解urllib, urllib2, requests](http://www.codefrom.com/paper/%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3urllib%E3%80%81urllib2%E5%8F%8Arequests)
