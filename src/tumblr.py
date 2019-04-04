# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 01:56:37 2017

@author: Yanyu
"""

import urllib2
import json
import os
import numpy as np


class Tumblr(object):
    def __init__(self,username,num):
        self.username=username
        self.num=num


    def get_url(self,username,start,end):
        url='http://'+username+'.tumblr.com/api/read/json?start=%i&num=%i'%(start,end)
        data=urllib2.urlopen(url).read()    
        return data


    def get_resource(self,url):
        postList=[]
    
        data=json.loads(url[22:-2])
        for i in range(0,len(data["posts"])):
            onepost={}
            onepost['videoList']=[]
            onepost['imageList']=[]
            onepost['slugList']=[]        
            onepost['date-gmt']=data["posts"][i]['date-gmt']    
            onepost['caption']=''    
            if data["posts"][i]["type"]=="regular":
                onepost['caption']=data["posts"][i]['regular-body']  
            if data["posts"][i]["type"]=="video":
                videoSourceCode = data["posts"][i]["video-player-500"]
                onepost['videoList'].append(videoSourceCode)
                onepost['caption']=data["posts"][i]['video-caption']  
            if data['posts'][i]['slug']!=None:
                onepost['slugList'].append(data['posts'][i]['slug'])
            if data["posts"][i]["type"]=="photo":
                onepost['caption']=data["posts"][i]['photo-caption']  
                if data["posts"][i]["photos"]!= None:
                    for j in range(0,len(data["posts"][i]["photos"])):
                        onepost['imageList'].append(data["posts"][i]["photos"][j]["photo-url-1280"])
    
            postList.append(onepost)
        return postList   
        
    
    def download(self,posts,video=False):
        download_path='./tbr_resource/'
            
        file_name=download_path+self.username+'/'      
        
        if not os.path.isdir(file_name):
            os.makedirs(file_name)

        allfile=os.listdir(file_name)
        if video==False:
            for po in posts:        
                mediacount=len(po['imageList'])
                for media in po['imageList']:
                    media_name=po['slugList'][0]+'_%i'%mediacount+'_'+po['date-gmt'][:10]+media[-4:]
                    mediacount=mediacount-1
               
                    if media_name.encode('utf-8') not in allfile:
                        rsp=urllib2.urlopen(media)
                        with open(file_name+media_name,'wb') as fi:
                            fi.write(rsp.read())
                        print (media_name)
                    else:
                        print (' pass',media_name)
                txt_name=po['slugList'][0]+'_'+po['date-gmt'][:10]+'.txt'
                if txt_name.encode('utf-8') not in allfile:
                    with open(file_name+txt_name,'wb') as fi:
                        fi.write(po['caption'].encode('utf-8'))    
                        
        if video==True:
            for po in posts:        
                if po['videoList']!=[]:
                    video=po['videoList'][0]
                    video_name=po['slugList'][0]+'_'+po['date-gmt'][:10]+'.mp4'
                    if (video_name.encode('utf-8') not in allfile):
                        if 'tweet' not in video_name:
                            
                            try:
                                video_url='https://vtt.tumblr.com/'+video.split('"')[-4].split('/')[6]+'.mp4'
                                rsp=urllib2.urlopen(video_url)
                                
                                with open(r'%s'%file_name+video_name,'wb') as fi:
                                    fi.write(rsp.read())
                            except Exception:
                                print ('  ERROR',video_name)
                                print 
                                print
                            else:
                                print (video_name)
                    else:
                        print (' pass',video_name   )
                        
                txt_name=po['slugList'][0]+'_'+po['date-gmt'][:10]+'_.txt'
                if txt_name.encode('utf-8') not in allfile:
                    with open(file_name+txt_name,'wb') as fi:
                        fi.write(po['caption'].encode('utf-8'))      
        print (self.username,'complete!!')
        print
    
    
    def get_post(self):
        posts=[]
        if self.num>50:                
            for i in np.arange(0,self.num,50):
                onepost=self.get_resource(self.get_url(self.username,i,i+50))
                if len(onepost)!=0:                
                    posts=posts+onepost
                elif len(onepost)==0: 
                    break
                
        else:
            posts=self.get_resource(self.get_url(self.username,0,self.num))    
        return posts
        





