import re
import urllib
import urllib.request

from collections import deque

queue = deque()
visited = set()

url = "http://news.dbanotes.net"

queue.append(url)
cnt = 0

while queue:
    url = queue.popleft()
    visited |= {url}

    print('Crawled: ' + str(cnt))
    print('Crawling <--- ' + url)
    cnt += 1
    urlop = urllib.request.urlopen(url)
    if 'html' not in urlop.getheader('Content-Type'):
        continue

    try:
        data = urlop.read().decode('utf-8')
    except:
        continue

    linkre = re.compile('href="(.+?)"')
    for x in linkre.findall(data):
        if 'http' in x and x not in visited:
            queue.append(x)
            print('Add to queue ---> ' + x)
