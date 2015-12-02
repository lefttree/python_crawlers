import requests
import bs4
import pprint

response = requests.get('http://pyvideo.org/category/50/pycon-us-2014')
# print(response.text)

soup = bs4.BeautifulSoup(response.text, "html.parser")
links = soup.select('div.col-md-6 a[href^=/video]')

pprint.pprint(links)
