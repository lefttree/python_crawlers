import requests
import json

def get_latest_news():
    url = "http://news-at.zhihu.com/api/4/news/latest"
    r = requests.get(url)
    objects = r.json()
    json.dump(objects, os.path.dirname(os.path.realpath(__file__)) + "/result/latest_news")
    print(objects)


def get_news_info(news_id):
    url = "http://news-at.zhihu.com/api/4/news/{}".format(news_id)
    r = requests.get(url)
    objects = r.json()
    # json.dump(objects, os.path.dirname(os.path.realpath(__file__)) + "/result/latest_news")
    print(objects)


def get_date_news(date):
    """
    date shold be after 20130520
    """
    url = "http://news.at.zhihu.com/api/4/news/before/{}".format(date)
    r = requests.get(url)
    objects = r.json()
    # json.dump(objects, os.path.dirname(os.path.realpath(__file__)) + "/result/latest_news")
    print(objects)


def get_extra_news_info(news_id):
    """
    # long comments
    # popularity
    # short comments
    # comments
    """
    url = "http://news-at.zhihu.com/api/4/story-extra/{}".format(news_id)
    r = requests.get(url)
    objects = r.json()
    # json.dump(objects, os.path.dirname(os.path.realpath(__file__)) + "/result/latest_news")
    print(objects)


def get_news_long_comments(news_id):
    url = "http://news-at.zhihu.com/api/4/story/{}/long-comments".format(news_id)
    r = requests.get(url)
    objects = r.json()
    # json.dump(objects, os.path.dirname(os.path.realpath(__file__)) + "/result/latest_news")
    print(objects)


def get_news_long_comments(news_id):
    url = "http://news-at.zhihu.com/api/4/story/{}/short-comments".format(news_id)
    r = requests.get(url)
    objects = r.json()
    # json.dump(objects, os.path.dirname(os.path.realpath(__file__)) + "/result/latest_news")
    print(objects)


def get_themes():
    url = "http://news-at.zhihu.com/api/4/themes"
    r = requests.get(url)
    objects = r.json()
    # json.dump(objects, os.path.dirname(os.path.realpath(__file__)) + "/result/latest_news")
    print(objects)


def get_theme_content(theme_id):
    url = "http://news-at.zhihu.com/api/4/theme/{}".format(theme_id)
    r = requests.get(url)
    objects = r.json()
    # json.dump(objects, os.path.dirname(os.path.realpath(__file__)) + "/result/latest_news")
    print(objects)


def get_hot_news():
    url = "http://news-at.zhihu.com/api/3/news/hot"
    r = requests.get(url)
    objects = r.json()
    # json.dump(objects, os.path.dirname(os.path.realpath(__file__)) + "/result/latest_news")
    print(objects)

