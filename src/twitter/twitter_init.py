# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 05:53:18 2019

@author: Yan
"""

import tweepy
import os
import datetime
import pandas as pd
from config import *

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




class Twitter(TweetScrape):
        
    def __init__(self,username,count_dates):
        
        """
        This class prepared a list of tweets content with media urls that could be sent to Weibo
        
        :username: (str) twitter account
        :count_dates: (int) how many recent days' you want to look at into
        
        """
        
        super(Twitter,self).__init__()
        self.username=username
        self.count_dates=count_dates
        
        
    def twt_spyder(self):
        tweets=tweepy.Cursor(self.api.user_timeline, id=self.username).items(30)
        media_files = []
        twt_file=[]
        video_files=[]
        id_files=[]
        timepic_file=[]
        timevi_file=[]
        timetwt_file=[]
        for status in tweets:
            try:
                media = status.extended_entities.get('media', [])
                medialen=len(media)
                if(medialen > 0): 
                    twt_file.append(status.text)
                    timetwt_file.append(str(status.created_at))
                    for i in range(medialen):
                        
                        media_files.append(media[i]['media_url']) 
                        timepic_file.append(str(status.created_at))
                        id_files.append(status.id)
                    
                    
                    try:
                        video_files.append(media[0]['video_info']['variants'][0]['url'])
                        timevi_file.append(str(status.created_at))
                    except Exception:
                        pass
            except:
                pass
            
        #put all the media url in a dataframe
        df_twt=pd.DataFrame(zip(twt_file,timetwt_file),columns=['twt','time']).set_index('time')
        df=pd.DataFrame(zip(media_files,timepic_file),columns=['pic_url','time'])
        dfl=list(df.groupby('time'))
        dfl=map(list,dfl)
        for i in dfl:
            if type(df_twt.loc[i[0]].iloc[0])==pd.core.series.Series:
                tp=df_twt.loc[i[0]].iloc[0]['twt']
            else:
                tp=df_twt.loc[i[0]].iloc[0]
            i.append(tp)
            
        #filter tweets that happened in recent countdown days
        countdown=str((datetime.datetime.now()-datetime.timedelta(days=self.count_dates)).date())
        dfl=[i for i in dfl if i[0][:10]>=countdown]
        
        #filter tweets that are reposts
        dfl=[i for i in dfl if i[2][:2]!='RT']
        return dfl
                            