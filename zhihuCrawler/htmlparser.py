"""Parse HTML and get content, save html files """
# -*- coding: utf-8 -*-
import os
import re


def save_file(data, filename):
    """Save html files """
    pagedir = os.path.dirname(os.path.realpath(__file__)) + "/result/"
    if not os.path.exists(pagedir):
        print('Create new pages directory')
        os.makedirs(pagedir)
    save_path = pagedir + filename + '.html'
    f_obj = open(save_path, 'wb')  # wb 表示打开方式
    f_obj.write(data)
    f_obj.close()


def get_index(s, url):
    """Get index page content"""
    r = s.get("http://www.zhihu.com")
    d = r.content
    save_file(d, "index")


def get_hot_topic(s, url):
    """Get hot topic page content"""
    r = s.get(url)
    d = r.content
    save_file(d, "explore")
    cer = re.compile('(<a class="question_link".*</a>)', flags=0)
    strlist = cer.findall(d.decode("utf-8"))
    for s in strlist:
        print(s)
