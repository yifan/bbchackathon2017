# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 09:42:08 2017

@author: Owner
"""

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

'''
class Args(object):
    debug = False
    min_articles = 3
    term = "brexit"
args = Args()

'''
args = parser.parse_args()

from textblob import TextBlob

flag_debug = args.debug # True
rejected = False

def check(input_text="UK news, London news, EU, EU news, Brexit, Brexit"):
    #input_text = "UK news, London news, EU, EU news, Brexit, Brexit"
    text_object = TextBlob(input_text)
    text_parsed_list = text_object.words
    
    unique_words_list= set(text_parsed_list)
    if flag_debug : print("\nOriginal Input Text:\n",input_text)
    
    #print("\nUnique words: ", unique_words_list,"\n")
    mynewlist = list(unique_words_list)
    mynewstring=str()
    for num,i in enumerate(mynewlist):
        if num>0:
            mynewstring += " "+ i
        if num<=0:
            mynewstring += i
    if flag_debug : print("Unique words:\n", mynewstring,"\n")
    
    list2=[]; num=0
    for word in mynewlist:
        #print(word)
        list2.append([word,text_parsed_list.count(word),num])
        num += 1
    
    if flag_debug : print("List of unique words,count,number_ID:\n",list2)
    
    
    #rejection algorithm:
    
    # basic algo: if count of "news" > 2, then reject text1
    # harsh algo: if word duplicated (count is 2 or more) then reject text
    
    rejected = False
    
    for i in text_parsed_list:
        # only reject if word exceeds 3 letters length 
        if len(i)>3:
            # only reject if word is duplicated i.e. count exceeds 1
            if text_parsed_list.count(i)>1:
                rejected = True
                if flag_debug: print("rejected word:",i,"count:",text_parsed_list.count(i))
            if i=="chunk": 
                rejected = True
    
    if args.debug: 
        if rejected: 
            print('\nOne storyline rejected!')
            print(input_text)
        else: 
            print('\nStoryline accepted!')
        
    # Summary
    if flag_debug : 
        print("\nOriginal Input Text:\n",input_text)
        print("\nUnique words:\n", mynewstring,"\n")
        print("List of unique words,count,number_ID:\n",list2)
    
        #Tags for words in input text
        '''
        for word, pos in text_object.tags:
            print(word, pos)
            
        print("")
        '''
        #Nouns
        text_object2 = TextBlob(input_text)
        
        list3=[]
        for word, pos in text_object2.tags:
            if pos=="NNP":
                list3.append(word)
        if flag_debug : 
            print("")
            print("NNP words: ",list3)
            print('Noun phrases: ', text_object2.noun_phrases)
        
        #print("Nouns: ", text_object.tags(POS="NN"))
        
    return rejected






# MAIN

client = Elasticsearch([{'host': 'summadb2.summa-project.eu', 'port': 80}])

s = Search(using=client, index='stories')\
  .query('match', summary=args.term)

res = s.execute()

for j, hit in enumerate(res['hits']['hits']):
    rejected = False
    story = hit['_source']
    items = [ item for item in story['mediaItems'] if 'sourceItemType' in item and item['sourceItemType'] == 'Article']

    if len(items) < args.min_articles:
        continue

    if story['summary'] == "":
        continue

    # check the storyline text, to evaluate if it is good enough 
    rejected = check(story['title'])
    
    if not rejected: 
        if args.debug: print('=' * 40)
        print(story['title'])
        if args.debug: print ('-'*4)
        if args.debug: print (story['summary'])
        if args.debug: print ('-'*20)
    
        if not args.debug:
            continue
    
        for i,mediaItem in enumerate(items):
            print(i)
            print(mediaItem['sourceItemType'])
            print(mediaItem['title'])

#res2 = res.count(index ='stories')
#print(res2)
#
#sys.exit(0)
