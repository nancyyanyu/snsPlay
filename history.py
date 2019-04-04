# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 15:47:15 2017

@author: Yanyu
"""
import urllib2
import tweepy
import os
import pandas as pd
auth = tweepy.OAuthHandler('LgmCVQcE7YiNlHdoil6xCugPt', 'uGoIJQtFgoHmpcWLBPffi0sGFgXGQmU1qIqvsAiiBOP4NnDhrs')
auth.set_access_token('837607037404078080-8nvbEm9osOl13XU49FvhBvdd2JUwdd5', 'p93OtbOs3RhKngSpNYjnHjQbx2BdLFdfaUSXTSPb3N3pW')
api = tweepy.API(auth)

def mainHistory(accounts,vi,pic,twt,lots=False):
    returninfo={}
    for username in accounts:
        newpath='C:/Users/Yan/Documents/Python Scripts/Twitter/getHistoryFlexible/%s'%username
        try:
            os.makedirs(newpath)
        except WindowsError:
            pass
        print
        print (username,'start!'  )   
        historylist=os.listdir(newpath)
        if lots==False:
            num=api.get_user(username).statuses_count              
        else:
            num=lots
            
        tweets=tweepy.Cursor(api.user_timeline, id=username).items(num)
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
                                print 'tweets still have: ',count     
                    except Exception:
                        pass
            print username,'get all history tweets!'   
            pd.DataFrame([media_files,timepic_file,id_files]).transpose().rename(columns={0:'pic',1:'timepic',2:'id'}).to_csv(newpath+'/pic.csv',encoding='utf-8')
            pd.DataFrame([twt_file,timetwt_file,id_files]).transpose().rename(columns={0:'twt',1:'timetwt',2:'id'}).to_csv(newpath+'/twt.csv',encoding='utf-8')
            pd.DataFrame([video_files,timevi_file,id_files]).transpose().rename(columns={0:'video',1:'timevi',2:'id'}).to_csv(newpath+'/video.csv',encoding='utf-8')

            if twt==True:
                for i in range(len(twt_file)):
                    file_name = newpath+'/%s_%i'%(timetwt_file[i][:10],list(set(id_files))[i])+'.txt'
                    f = open(file_name, 'w')
                    f.write(twt_file[i].encode('utf-8'))
                    f.close()               
            if pic==True:
                medialen=len(media_files)
                for i in range(medialen):    
                    medialen=medialen-1
                    if medialen%100==0:
                        print username,'pic',medialen
                    file_basic=newpath+'/%s_%i_%s'%(timepic_file[i][:10],id_files[i],media_files[i][-9:-4])
                    if media_files[i][-3:]=='jpg':              
                        file_name = file_basic+'.jpg'
                    elif media_files[i][-3:]=='png':              
                        file_name = file_basic+'.png'
                    if file_name[-39:] not in historylist:
                        try:
                            rsp = urllib2.urlopen(media_files[i])
                        except Exception:
                            print 'cant download'
                        else:
                            with open(file_name,'wb') as f:
                                f.write(rsp.read())
#                    else:
                        
                        #print id_files[i],'pass'
                print username,"pics download!"
                
            if vi==True:
                videolen=len(video_files)            
                for i in range(videolen):
                    videolen=videolen-1
                    if videolen%10==0:
                        print username,'video',videolen
                    if video_files[i]!=0:
                        if video_files[i][-3:]=='mp4':                   
                            file_name = newpath+'/%s_%i'%(timevi_file[i][:10],id_files[i])+'.mp4'
                            if file_name[-33:] not in historylist:
                                try:
                                    rsp = urllib2.urlopen(video_files[i])
                                except Exception:
                                    print 'cant download'
                                else:
                                    with open(file_name,'wb') as f:
                                        f.write(rsp.read())
                        else:
                            print 'pass',file_name[-33:]
                    
                print username,"video download!"            
            else:
                print 'video blah!'
            

      
            print username,'download complete!!'  
            print
        except Exception:
            pass
    returninfo['pic']=media_files
    returninfo['twt']=twt_file
    returninfo['video']=video_files
    returninfo['id']=id_files
    returninfo['timepic']=timepic_file
    returninfo['timevi']=timevi_file
    returninfo['timetwt']=timetwt_file

    return returninfo
    
    


def picdownload(fileall,name):
    
    media_files=fileall['pic']
    timepic_file=fileall['timepic']
    id_files=fileall['id']
    username=name
    newpath='C:/Users/Yan/Documents/Python Scripts/Twitter/getHistoryFlexible/%s'%username
    historylist=os.listdir(newpath)
    medialen=len(media_files)
    for i in range(medialen):    
        medialen=medialen-1
        if medialen%100==0:
            print username,'pic',medialen
        file_basic=newpath+'/%s_%i_%s'%(timepic_file[i][:10],id_files[i],media_files[i][-9:-4])
        if media_files[i][-3:]=='jpg':              
            file_name = file_basic+'.jpg'
        elif media_files[i][-3:]=='png':              
            file_name = file_basic+'.png'
        if file_name[-39:] not in historylist:
            
            try:
                rsp = urllib2.urlopen(media_files[i])
                with open(file_name,'wb') as f:
                    f.write(rsp.read())                
            except Exception:
                print 'pic failed'


        else:
            print 'pass',file_name[-39:]
    
    

def videodownload(fileall,name):
    video_files=fileall['video']
    id_files=fileall['id']
    timevi_file=fileall['timevi']
    username=name
    newpath='C:/Users/Yan/Documents/Python Scripts/Twitter/getHistoryFlexible/%s'%username
    historylist=os.listdir(newpath)
    videolen=len(video_files)            
    for i in range(videolen):
        videolen=videolen-1
        if videolen%10==0:
            print username,'video',videolen
        if video_files[i]!=0:
            try:
                if video_files[i][-3:]=='mp4':                   
                    file_name = newpath+'/%s_%i'%(timevi_file[i][:10],id_files[i])+'.mp4'
                    if file_name[-33:] not in historylist:
                        try:
                            rsp = urllib2.urlopen(video_files[i])
                        except Exception:
                            print ' cant mp4 urlopen'
                        else:
                            with open(file_name,'wb') as f:
                                f.write(rsp.read())
                    else:
                        print 'pass',file_name[-39:]
                elif video_files[i][-4:]=='m3u8':
                    pass
                '''
                    file_name = newpath+'/%s_%i'%(timevi_file[i][:10],id_files[i])+'.m3u8'
                    if file_name[-33:] not in historylist:
                        try:
                            rsp = urllib2.urlopen(video_files[i])
                        except Exception:
                            print ' cant m3u8 urlopen'
                        else:
                            with open(file_name,'wb') as f:
                                f.write(rsp.read())
                    else:
                        print 'pass',file_name[-39:]
                '''
            except Exception:
                print 'video failed'
    print username,"video download!"     

def twtdownload(fileall,name):
    username=name
    twt_file=fileall['twt']
    id_files=fileall['id']
    timetwt_file=fileall['timetwt']
    newpath='C:/Users/Yan/Documents/Python Scripts/Twitter/getHistoryFlexible/%s'%username
    for i in range(len(twt_file)):
        file_name = newpath+'/%s_%i'%(timetwt_file[i][:10],list(set(id_files))[i])+'.txt'
        f = open(file_name, 'w')
        f.write(twt_file[i].encode('utf-8'))
        f.close()   
    
    
    
    
    
    

if __name__=="__main__":
        
    WantHistory=['MingleMangle_JM','kookmin9795','kookminzip','MinKook9597','moovin_','OnlyForJIKOOK','JiminBase']
    RecentKookmin=['9597pics', 'bestofjikook','enemy9597_th', 'JIKOOKDAILY','JikookLove', 'kookmin9795', 'kookminlove', 'kookminzip', 'onetopkj','OnlyForJIKOOK', 'sonsofbusan9597',
    '_Kookmin_']
    Jiminsite=[u'parkjamjam_kr', u'miningfulmoment', u'mighty_jimin', u'ILIKEIT_JM',
       u'scene_stealer_', u'honeywater_jm', u'951013SOME', u'creamsoda1013',
       u'TODAY_PJM', u'The_luMINary95', u'JIMIN_house', u'heartthrob_jm',
       u'BTS_LOVEONTOP', u'JSWD_JM', u'BTS_JIMINI95', u'LittleBlossomJM',
       u'SD_jimin', u'poco_jimin', u'19951013_JM', u'miracle_1013',
       u'cottoncandy__jm', u'JIMINIMOUTH', u'ranunculus1013', u'lookatmin1013',
       u'HOMMEFATAL1013', u'PJMerlion', u'AphetaMINe1013', u'adelio_bts',
       u'MINToYou_1013', u'SWEETPILL_JM', u'SNIPERJIMIN', u'JIMint_p',
       u'TheBestJm_95', u'starlight_chim', u'BurningPoint_JM', u'byallmeans95',
       u'951013_jimin', u'foreverjimin_', u'tensionup_1013', u'BABYITSU1013',
       u'piecesofmind_jm', u'myloverjimin', u'JIMINHOME_1013', u'AJEONG_JM',
       u'appeal_box', u'Jet_streaM95', u'JMumbrella', u'ArbRe_JM',
       u'ORANGEMIN1013', u'FABULOUSBOY_JM', u'newseason1013', u'Fairy_jimin',
       u'MERRYWHITE_JM', u'PrinceOfBusanJM', u'jimrain1013', u'SUNSHINEonJM',
       u'arabesque951013', u'Warmtowards1013', u'LoveInOctober_', u'PP951013',
       u'PJM_1013', u'Lovebeat_jm', u'opallios_JM', u'sunnyday1013',
       u'goodday_1013', u'wildyouth_jm', u'FallInLove_JM', u'Lisianthus_JM95',
       u'swetemptaion_jm', u'951013__JM', u'be_JIMIN951013', u'LoveMINsU_JM',
       u'Dream_JM1013', u'happymoment1013', u'pinkyJM1013', u'peach_jelly1013',
       u'PEISley_jm', u'placeboeffect_j', u'sweetfever1013', u'mydearJM_1013',
       u'TINYPEA_1013', u'amoureuxjm', u'sonorous_JM', u'JMsourire',
       u'Watchout1013', u'1llusion_jimin', u'moment0613', u'berryMIN_',
       u'peachbasket_JM', u'_951013_jm', u'moveslikejimin', u'_Twinkle_BabY_',
       u'fuwachim', u'Octoberboy1013', u'mozzimin']    
    JMedit=['MingleMangle_JM','comely_jimin','JiminBase','GetOnSwag','Rgrey613']    
    JJKedit=['LikeaRabbit97']  
    
    #mainHistory(['parkjamjam_kr'],lots=False,vi=True,pic=True,twt=False)



  