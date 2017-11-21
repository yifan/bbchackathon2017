import sys
from urlparse import urlparse, urlunparse
from bs4 import BeautifulSoup
import requests
import codecs

class Event(object):
  def __init__(self, topic):
    self.topic = topic
    self.source = []
    self.text = []
    self.media = []
    self.links = []

  def __str__(self):
    return "\n".join([str(self.source), str(self.media), str(self.links)])

  def add_source(self, source):
    self.source.append(source)
    for a in source.find_all('a'):
      if a.attrs['href'].startswith('http://www.aljazeera.com/news'):
        self.add_link(a.attrs['href'])

  def add_media(self, media):
    self.media.append(media)

  def add_link(self, link):
    self.links.append(link)
    r = requests.get(link)
    o = urlparse(link)
    # if 
    s = BeautifulSoup(r.text, 'html.parser')
    body = s.find('div', class_='main-article-body')
    for img in body.select('.main-article-media-img'):
      imgurl = urlunparse([o.scheme, o.netloc, img.attrs['data-src'], '', '', ''])
      self.add_media(imgurl)

URL = 'http://www.aljazeera.com/news/2017/06/qatar-diplomatic-crisis-latest-updates-170605105550769.html'

r = requests.get(URL)
content = r.text

soup = BeautifulSoup(content, 'html.parser')
article = soup.find('div', class_='article-p-wrapper')
events = []
for item in article.children:
  if item.name == 'h2':
    event = Event(item.text)
    events.append(event)
  elif events and item.name == 'ul':
    events[-1].add_source(item)

o = codecs.getwriter('utf-8')(sys.stdout)
for event in events:
  print >>o, event.topic, "\t", event.media[0] if event.media else ""
