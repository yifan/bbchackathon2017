import sys
import json
import requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

import argparse
parser = argparse.ArgumentParser(prog="getStory.py",
                                     usage="%(prog)s [options] [arguments]")

parser.add_argument("--debug", type=bool, default=False,
                    help="print debug information")
parser.add_argument("--min-articles", type=int, default=3, 
                    help="minimal number of articles required for a story")
parser.add_argument("term", type=str, help='term to be used in search')
args = parser.parse_args()

client = Elasticsearch([{'host': 'summadb2.summa-project.eu', 'port': 80}])

s = Search(using=client, index='stories')\
  .query('match', summary=args.term)

res = s.execute()

for j, hit in enumerate(res['hits']['hits']):
  story = hit['_source']
  items = [ item for item in story['mediaItems'] if 'sourceItemType' in item and item['sourceItemType'] == 'Article']

  if len(items) < args.min_articles:
    continue

  if story['summary'] == "":
    continue

  if args.debug: print '=' * 40
  print story['title']
  if args.debug: print '-'*4
  if args.debug: print story['summary']
  if args.debug: print '-'*20

  if not args.debug:
    continue

  for i,mediaItem in enumerate(items):
    print i
    print mediaItem['sourceItemType']
    print mediaItem['title']

#res = es.count(index ='stories')
#print res
#
#sys.exit(0)

