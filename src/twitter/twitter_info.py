# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:25:33 2017

@author: Yanyu
"""

import urllib2
import tweepy
import pandas as pd
import datetime as dt
from twitter_init import TweetScrape


class Info(TweetScrape):
    def __init__(self,usernames,flag):
        
        """
        Summary the basic info, like followers_count, created_at, etc., and generate an excel report.
        This class could be used to track and report the followers growth of a large amount of accounts.
        
        :usernames: (list) find in logger.py, choose betweeen usernamesv, usernamessuga,usernamesjjk, usernamesjimin
        :flag: (str) choose betwwen 'jimin','jungkook','v'
        
        """
        
        super(Info,self).__init__()
        self.usernames=usernames
        self.flag=flag
    

    def getinfo(self):
        count=len(self.usernames)
        all_info={}
        for username in self.usernames:
            count=count-1
            try:
                tweets=self.api.get_user(username)
            except Exception:
                try:
                    tweets=self.api.get_user(username)
                except Exception:
                    print (username,'wrong')
            else:
                info={}
                info['followers_count']=tweets.followers_count
                info['created_at']=tweets.created_at            
                info['statuses_count']=tweets.statuses_count
                info['description']=tweets.description

                all_info[username]=info
                print (count,' ; ',username)
                                
        all_data=pd.DataFrame.from_dict(all_info).transpose()
        if self.flag=='jimin':
            all_data.to_csv('jiminFanBase_info%s.txt'%str(dt.datetime.now())[:10],encoding='utf-8')
            part_data=all_data[['followers_count','statuses_count','created_at']].sort(['followers_count'],ascending=False)
            
            writer = pd.ExcelWriter('jiminFanBase_info_%s.xlsx'%str(dt.datetime.now())[:10]) 
            part_data.to_excel(writer,sheet_name=dt.datetime.now().strftime("%Y-%m-%d"))
            writer.save()

        elif self.flag=='jungkook':
            all_data.to_csv('jjkFanBase_info%s.txt'%str(dt.datetime.now())[:10],encoding='utf-8')
            part_data=all_data[['followers_count','statuses_count','created_at']].sort(['followers_count'],ascending=False)
            
            writer = pd.ExcelWriter('jjkFanBase_info%s.xlsx'%str(dt.datetime.now())[:10]) 
            part_data.to_excel(writer,sheet_name=dt.datetime.now().strftime("%Y-%m-%d"))
            writer.save()

        elif self.flag=='v':
            all_data.to_csv('vFanBase_info%s.txt'%str(dt.datetime.now())[:10],encoding='utf-8')
            part_data=all_data[['followers_count','statuses_count','created_at']].sort(['followers_count'],ascending=False)
            
            writer = pd.ExcelWriter('vFanBase_info%s.xlsx'%str(dt.datetime.now())[:10]) 
            part_data.to_excel(writer,sheet_name=dt.datetime.now().strftime("%Y-%m-%d"))
            writer.save()    
    
        print (all_data[['followers_count','statuses_count','created_at']].sort(['followers_count'],ascending=False))
        return part_data

