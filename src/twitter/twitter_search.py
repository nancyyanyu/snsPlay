# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 03:59:37 2017

@author: Yanyu
"""

import urllib2
import tweepy
import os
from twitter_init import TweetScrape

class Search(TweetScrape):
    def __init__(self,hashtags=None,lots=False,vi=True,pic=True,twt=True):
            
        """
        
        Search on the latest tweets on twitter about a list of hashtags, download pictures, videos, and tweets in folder under each hashtag
        
        """

        super(Search,self).__init__(hashtags,lots,vi,pic,twt)
        pass
            
            
    def search_download_single(self,h):
        download_path=self.twt_start(h)
        
        historylist=os.listdir(download_path)
        tweets=tweepy.Cursor(self.api.search, q=h).items(self.lots)   
        
        media_files = []
        video_files= []
        id_files= []
        timepic_file=[]
        timevi_file=[]
        
        #extract information from status                
        for status in tweets:
            
            #filter any tweets that are retweet of @BTS_twt because there are too many duplicates.
            if '%s_%i.mp4'%(str(status.created_at),status.id) not in historylist and status.text[:11]!='RT @BTS_twt':
                try:
                    media = status.extended_entities.get('media', [])
                    medialen=len(media)
                    if(medialen > 0):
                        file_name = download_path+'/%s_%i'%(str(status.created_at)[:10],status.id)+'.txt'
                        f = open(file_name, 'w')
                        f.write(status.text.encode('utf8'))
                        f.close()   
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
        
        #download pictures if pic is True
        if self.pic==True:
            medialen=len(media_files)
            for i in range(medialen):   
                medialen=medialen-1
                #if medialen%10==0:
                #    print medialen
                file_basic=download_path+'/%s_%i_%s'%(timepic_file[i][:10],id_files[i],media_files[i][-9:-4])
                if media_files[i][-3:]=='jpg':              
                    file_name = file_basic+'.jpg'
                elif media_files[i][-3:]=='png':              
                    file_name = file_basic+'.png'
                try:
                    rsp = urllib2.urlopen(media_files[i])
                except Exception:
                    pass
                else:
                    with open(file_name,'wb') as f:
                        f.write(rsp.read())
            print ("Pics download:{0:s}".format(h))

        #download videos if vid is True
        if self.vi==True:           
            videolen=len(video_files)            
            for i in range(videolen):
                videolen=videolen-1
                #if videolen%100==0:
                #    print videolen
                if video_files[i]!=0:
                    if video_files[i][-3:]=='mp4':                   
                        file_name = download_path+'/%s_%i'%(timevi_file[i][:10],id_files[i])+'.mp4'
                        try:
                            rsp = urllib2.urlopen(video_files[i])
                        except Exception:
                            pass
                        else:
                            with open(file_name,'wb') as f:
                                f.write(rsp.read())
            print ("Videos download:{0:s}".format(h))

        print ("{0:s} download complete!".format(h))



    def search_download(self):
        
        for h in self.hashtags:
            self.search_download_single(h)
        
        
        

    
    