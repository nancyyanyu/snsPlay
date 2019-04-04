# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 05:53:18 2019

@author: Yan
"""

import urllib2
import tweepy
import os
from logger import *

class TweetScrape(object):
    #get OAuth Token
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    auth.set_access_token(KEY,SECRET)
    api = tweepy.API(auth)
    
    def __init__(self,hashtags=None,lots=0,vi=True,pic=True,twt=True):
        
        """
        :hashtags:(list) a list of hashtags, maybe hot topics
        :lots:(int) how many new tweets to download
        :vi:(boolean) whether download videos
        :pic:(boolean) whether download pictures
        :twt:(boolean) whether download tweets
        
        """
        
        if hashtags!=None:           
            self.hashtags=hashtags
        else: 
            self.hashtags=['jimin','jungkook','kookmin']         
        
        self.lots=lots
        self.vi=vi
        self.pic=pic
        self.twt=twt
        
        if self.lots>200:
            raise Warning("Search too many content!")
        
    
    def twt_start(self,h):
        download_path='./twt_resource/%s'%h
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
            
        print("Start to download (search): %s"%h)
        return download_path

            