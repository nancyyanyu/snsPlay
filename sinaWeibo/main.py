# -*- coding: utf-8 -*-

from weibo.weibo_login import wblogin
from weibo.weibo_sender import WeiboSender
from weibo.weibo_message import WeiboMessage
import urllib2
import tweepy
import time
import unicodedata
import os
import numpy as np
import datetime
import pandas as pd
import random
auth = tweepy.OAuthHandler('LgmCVQcE7YiNlHdoil6xCugPt', 'uGoIJQtFgoHmpcWLBPffi0sGFgXGQmU1qIqvsAiiBOP4NnDhrs')
auth.set_access_token('837607037404078080-8nvbEm9osOl13XU49FvhBvdd2JUwdd5', 'p93OtbOs3RhKngSpNYjnHjQbx2BdLFdfaUSXTSPb3N3pW')
api = tweepy.API(auth)

class Twitter(object):
    def __init__(self,username,count_dates):
        self.username=username
        self.count_dates=count_dates
        
    def twt_spyder(self):
        tweets=tweepy.Cursor(api.user_timeline, id=self.username).items(30)
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
        countdown=str((datetime.datetime.now()-datetime.timedelta(days=self.count_dates)).date())
        dfl=[i for i in dfl if i[0][:10]>=countdown]
        dfl=[i for i in dfl if i[2][:2]!='RT']
        return dfl
                
                
if __name__ == '__main__':
    sent=list(np.load('./sent.npy'))
    (wei_session, uid) = wblogin()
    wei_session.get('http://weibo.com/')
    send=WeiboSender(wei_session, uid)
    
    username_list=['JMoment_bts','JKasBunny','kittenjm','kookpics','BTSorbit','kooklq',
                   'btscberry','pjmarchv','247jimin','jiminhqpics','parkjiminpics','jiminxpictures','AllJiminPark',
                   'kookpiics','jjkarchives','dou_xfine']
    
    #download data
    dfl=[]
    for username in username_list:
        
        twt=Twitter(username,1)
        ad=twt.twt_spyder()
        if len(ad)>10:
            ad=ad[-10:]
        for i in ad:
            i.append(username)
        dfl=dfl+ad
        print(username)
    random.shuffle(dfl)

    #
    for i in dfl:
        if i[0]+i[-1] not in sent:
            mess=i[2]+'      cr.'+i[-1]
            mess=mess.encode('utf8')
            img=list(i[1]['pic_url'].values)
            weibo=WeiboMessage(mess,img)
            send.send_weibo(weibo)
            sent.append(i[0]+i[-1])
            np.save('./sent.npy',np.array(sent))
            print("Sleep 3 mins")
            print
            time.sleep(180)
            
            
            if (dfl.index(i)+1)%3==0:
                print("Sleep 10 mins")
                print
                time.sleep(600)
            if (dfl.index(i)+1)%6==0:
                print("Sleep 15 mins")
                print
                time.sleep(900)
            if (dfl.index(i)+1)%8==0:
                print("Sleep 20 mins")
                print
                time.sleep(1800)
    
            
