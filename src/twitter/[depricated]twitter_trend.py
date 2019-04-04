# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 21:13:31 2017

@author: Yanyu
"""

import sys
import urllib2
import tweepy
import pandas as pd
import os
import csv
import datetime as dt
from translation import baidu, google, youdao, iciba,bing, ConnectError
from twihistory import videodownload,twtdownload,picdownload
from twitter_init import TweetScrape


class Trend(TweetScrape):
    def __init__(self,hashtags=None,lots=False,vi=True,pic=True,twt=True):
        
        """
        Download historical tweets of a list of accounts
        
        """
        super(Trend,self).__init__(hashtags,lots,vi,pic,twt)
        pass
    



start=dt.datetime.now()







#朴智旻박지민u'\ubc15\uc9c0\ubbfc' 방탄소년단
WOEID=pd.read_csv('C:/Users/Yanyu/Documents/Python Scripts/Twitter/trend/WOEID3.csv')
allid=[1]+list(pd.to_numeric(WOEID['WOEID'],errors='ignore').values)
allplace=['world']+list(WOEID['City'].values)
alltrend={}
for place in range(len(allid)):
    try:
        temp=api.trends_place(allid[place])[0]
    except Exception:
        print '  pass',allplace[place]
    else:
        print allplace[place],'complete!'
        trendsname=[temp['trends'][i]['name'] for i in range(len(temp['trends']))]        
#        trendsurl=[temp['trends'][i]['url'] for i in range(len(temp['trends']))]
        alltrend[allplace[place]]=trendsname

havetrend={}        
for key in alltrend.keys():
    for item in alltrend[key]:
        if (u'\uc9c0\ubbfc' or 'JIMIN' or 'jimin' or 'bts' or 
        'BTS' or u'\ubc29\ud0c4\uc18c\ub144\ub2e8' or 
        u'\u9632\u5f3e\u5c11\u5e74\u56e3' or u'\ubc29\ud0c4') in item:
            havetrend[key]=alltrend[key]
            break
        
for i in range(len(alltrend['Seoul'])):
    print bing(alltrend['Seoul'][i],dst='zh-CHS'),bing(alltrend['Seoul'][i],dst='en'),alltrend['Seoul'][i]


print dt.datetime.now()-start