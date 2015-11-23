# -*- coding:utf-8 -*-


def latestNews(s):
    r = s.get("http://news-at.zhihu.com/api/4/news/latest")
    return r.json()


def getNews(s, id):
    r = s.get("http://news-at.zhihu.com/api/4/news/" + str(id))
    return r.json()


def getHistory(s, date):
    r = s.get("http://news.at.zhihu.com/api/4/news/before/" + str(date))
    return r.json()


def getExtraInfo(s, id):
    r = s.get("http://news-at.zhihu.com/api/4/story-extra/#" + str(id))
    return r.json()


def getLongComments(s, id):
    r = s.get("http://news-at.zhihu.com/api/4/story/" + str(id) +
              "/long-comments")
    return r.json()


def getShortComments(s, id):
    r = s.get("http://news-at.zhihu.com/api/4/story/" + str(id) +
              "/short-comments")
    return r.json()


def getTheme(s):
    r = s.get("http://news-at.zhihu.com/api/4/themes")
    return r.json()


def getThemeList(s, id):
    r = s.get("http://news-at.zhihu.com/api/4/theme/" + str(id))
    return r.json()


def getHotNews(s):
    r = s.get("http://news-at.zhihu.com/api/3/news/hot")
    return r.json()


def getSectionList(s):
    r = s.get("http://news-at.zhihu.com/api/3/sections")
    return r.json()


def getSection(s, id):
    r = s.get("http://news-at.zhihu.com/api/3/sections/" + str(id))
    return r.json()
