# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 23:09:17 2017

@author: Yanyu
"""
import sys
import urllib2
import tweepy
import pandas as pd
from convertGIF import GIFconvertMain,GIFConvertsearch
from history import videodownload,twtdownload,picdownload


returninfo={}
media_files = []
twt_file=[]
video_files=[]
id_files=[]
timepic_file=[]
timevi_file=[]
timetwt_file=[]
        
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
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
        except Exception:
            pass                    
                    
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream
one='jimin'
streamingAPI = tweepy.streaming.Stream(auth, MyStreamListener())
streamingAPI.filter(track=[one])
'''
returninfo['pic']=media_files
returninfo['twt']=twt_file
returninfo['video']=video_files
returninfo['id']=id_files
returninfo['timepic']=timepic_file
returninfo['timevi']=timevi_file
returninfo['timetwt']=timetwt_file

twtdownload(returninfo,one)
picdownload(returninfo,one)
videodownload(returninfo,one)
GIFconvertMain([one])

'''


