# Crawler for zhihu

## Todo 

- use `requests` and `beautifusoup` library
- "热门圆桌", "热门话题"， "热门收藏" ...
- "今日最热"， "本月最热" ...

- database to save results

## Current process

- get _xsrf from "http://www.zhihu.com" response
- try login without captcha, post to "http://www.zhihu.com/login/email"
- if failed, get captcha, let user enter captcha, then try again

## Reference 

- [零基础自学python3网络爬虫](https://jecvay.com/category/smtech/python3-webbug)
- [手把手教你用python模拟登录知乎](http://knarfeh.github.io/2015/04/04/%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E4%BD%A0%E7%94%A8Python%E6%A8%A1%E6%8B%9F%E7%99%BB%E9%99%86%E7%9F%A5%E4%B9%8E/)
- [zhihuSpider](https://github.com/lining0806/ZhihuSpider/blob/master/ZhihuSpider.py)
- [zhihu unofficial api library](https://github.com/7sDream/zhihu-py3)
- [Handling Cookies in Python](http://www.voidspace.org.uk/python/articles/cookielib.shtml#cookies)
