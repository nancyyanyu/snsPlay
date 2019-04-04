# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 05:53:18 2019

@author: Yan
"""


import time
import numpy as np
import random
from twitter.twitter_init import Twitter
from weibo.weibo_login import weibo_login
from weibo.weibo_sender import Sender
from weibo.weibo_message import Message



def send_weibo(username_list):
    
    sent_list=list(np.load('./sent.npy'))
    (wei_session, uid) =weibo_login()
    wei_session.get('http://weibo.com/')
    send=Sender(wei_session, uid)
    
    
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

    #send weibo
    for i in dfl:
        if i[0]+i[-1] not in sent_list:
            mess=i[2]+'      cr.'+i[-1]
            mess=mess.encode('utf8')
            img=list(i[1]['pic_url'].values)
            weibo=Message(mess,img)
            send.send_weibo(weibo)
            sent_list.append(i[0]+i[-1])
            np.save('./sent.npy',np.array(sent_list))
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
    
            
                
if __name__ == '__main__':
    username_list=['JMoment_bts','JKasBunny','kittenjm','kookpics','BTSorbit','kooklq',
                   'btscberry','pjmarchv','247jimin','jiminhqpics','parkjiminpics','jiminxpictures','AllJiminPark',
                   'kookpiics','jjkarchives','dou_xfine']
    
    send_weibo(username_list)
