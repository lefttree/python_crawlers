"""
Simple python scraper
"""
import argparse
import requests # made for human api!
import bs4 # html parser
import pprint
import re
from multiprocessing import Pool

root_url = 'http://pyvideo.org'
index_url = root_url + '/category/50/pycon-us-2014'


def get_video_page_urls():
    """
    Get video page urls
    """
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser') # get an soup object, specify html parser
    return [a.attrs.get('href') for a in
            soup.select('div.col-md-6 a[href^=/video]')] # css selector

# pprint.pprint(get_video_page_urls())


def get_video_data(video_page_url):
    """
    Get video page details for each page
    - title
    - speaks
    - youtube address
    - views
    - likes
    - dislikes
    Return:
        dictionary contains all the info
    """
    video_data = {}
    try:
        # urls from index page are relative
        response = requests.get(root_url + video_page_url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # should use inspector to get all these css classes
        # select() returns a list
        video_data['title'] = soup.select('div#videobox h3')[0].get_text()
        video_data['speakers'] = [a.get_text().decode('utf-8') for a in
                                  soup.select('div#sidebar a[href^=/speaker]')]
        video_data['youtube_url'] = soup.select(
            'div#sidebar a[href^=http://www.youtube.com]')[0].get_text()

        # get info from youtube page
        response = requests.get(video_data['youtube_url'])
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        video_data['views'] = int(re.sub('[^0-9]', '',
                                         soup.select('.watch-view-count')
                                         [0].get_text().split()[0]))
        video_data['likes'] = soup.select('.like-button-renderer-like-button\
                                          .yt-uix-button-content')[0].get_text()
        video_data['dislikes'] = soup.select('.like-button-renderer-dislike-button\
                                              .yt-uix-button-content')[0].get_text()

        return video_data
    except Exception:
        pass


def show_video_stats(options):
    # parallel processing
    pool = Pool(options.workers)
    # get all the video pages' url
    video_page_urls = get_video_page_urls()
    results = sorted(pool.map(get_video_data, video_page_urls), key=lambda video: video[options.sort] if video else -1,
                     reverse=True)
    max = options.max
    if max is None or max > len(results):
        max = len(results)
    if options.csv:
        print('"title", "speakers", "views", "likes", "dislikes"')
    else:
        print('View +1 -1 Title (Speakers)')

    for i in range(max):
        if options.csv:
            print('"{0}","{1}",{2},{3},{4}'.format(
                  results[i]['title'], ', '.join(results[i]['speakers']),
                  results[i]['views'], results[i]['likes'],
                  results[i]['dislikes']))
        else:
            print('{0} {1} {2} {3} ({4})'.format(
                results[i]['views'], results[i]['likes'],
                results[i]['dislikes'], results[i]['title'],
                ', '.join(results[i]['speakers'])))
#     for i in range(max):
        # pprint.pprint(results[i])


def parse_args():
    parser = argparse.ArgumentParser(description="Show Pycon 2014 video statistics.")
    parser.add_argument('--sort', metavar='FIELD', choices=['views', 'likes',
                        'dislikes'], default='views',
                        help='sort by the specified field. Options are views, likes and dislikes')
    parser.add_argument('--max', metavar='MAX', type=int, help='show the top MAX entries only.')
    parser.add_argument('--csv', action='store_true', default=False,
                        help='output the data in CSV format.')
    parser.add_argument('--workers', type=int, default=8,
                        help='number of workers to use, 8 by default.')
    return parser.parse_args()

if __name__ == "__main__":
    show_video_stats(parse_args())
