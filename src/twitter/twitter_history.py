# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 15:47:15 2017

@author: Yanyu
"""
import urllib2
import tweepy
import os
import pandas as pd
from twitter_init import TweetScrape
from logger import *

class History(TweetScrape):
    def __init__(self,hashtags=None,lots=False,vi=True,pic=True,twt=True):
        
        """
        Download historical tweets of a list of accounts
        
        """
        super(History,self).__init__(hashtags,lots,vi,pic,twt)
        pass
    
    
    def history_download_single(self,username):    
        download_path=self.twt_start(username)
        
        historylist=os.listdir(download_path)
        if self.lots==False:
            num=self.api.get_user(username).statuses_count              
        else:
            num=self.lots
            
        tweets=tweepy.Cursor(self.api.user_timeline, id=username).items(num)
        media_files = []
        twt_file=[]
        video_files=[]
        id_files=[]
        timepic_file=[]
        timevi_file=[]
        timetwt_file=[]
        
        count=num
        try:
            for status in tweets:
                count=count-1
                if status.text[:11]!='RT @BTS_twt':
#                if '%s_%i.mp4'%(str(status.created_at)[:10],status.id) not in historylist and status.text[:11]!='RT @BTS_twt':
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

                            if count%100==0:
                                print ('tweets still have: ',count     )
                    except Exception:
                        pass
            print (username,'get all history tweets!'   )
            pd.DataFrame([media_files,timepic_file,id_files]).transpose().rename(columns={0:'pic',1:'timepic',2:'id'}).to_csv(download_path+'/pic.csv',encoding='utf-8')
            pd.DataFrame([twt_file,timetwt_file,id_files]).transpose().rename(columns={0:'twt',1:'timetwt',2:'id'}).to_csv(download_path+'/twt.csv',encoding='utf-8')
            pd.DataFrame([video_files,timevi_file,id_files]).transpose().rename(columns={0:'video',1:'timevi',2:'id'}).to_csv(download_path+'/video.csv',encoding='utf-8')

            if self.twt==True:
                for i in range(len(twt_file)):
                    file_name = download_path+'/%s_%i'%(timetwt_file[i][:10],list(set(id_files))[i])+'.txt'
                    f = open(file_name, 'w')
                    f.write(twt_file[i].encode('utf-8'))
                    f.close()               
            if self.pic==True:
                medialen=len(media_files)
                for i in range(medialen):    
                    medialen=medialen-1
                    file_basic=download_path+'/%s_%i_%s'%(timepic_file[i][:10],id_files[i],media_files[i][-9:-4])
                    if media_files[i][-3:]=='jpg':              
                        file_name = file_basic+'.jpg'
                    elif media_files[i][-3:]=='png':              
                        file_name = file_basic+'.png'
                    if file_name[-39:] not in historylist:
                        try:
                            rsp = urllib2.urlopen(media_files[i])
                        except Exception:
                            print ("Can't download")
                        else:
                            with open(file_name,'wb') as f:
                                f.write(rsp.read())

                print (username,"pics download!")
                
            if self.vi==True:
                videolen=len(video_files)            
                for i in range(videolen):
                    videolen=videolen-1
                    if video_files[i]!=0:
                        if video_files[i][-3:]=='mp4':                   
                            file_name =download_path+'/%s_%i'%(timevi_file[i][:10],id_files[i])+'.mp4'
                            if file_name[-33:] not in historylist:
                                try:
                                    rsp = urllib2.urlopen(video_files[i])
                                except Exception:
                                    print ('cant download')
                                else:
                                    with open(file_name,'wb') as f:
                                        f.write(rsp.read())
                        else:
                            print ('pass',file_name[-33:])
                    
                print (username,"video download!"      )      

      
            print (username,'download complete!!' ) 
            
        except Exception:
            pass


    def history_download(self):
        
        for h in self.hashtags:
            self.history_download_single(h)
        
        
    