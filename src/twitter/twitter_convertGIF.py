# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:48:00 2017

@author: Yanyu
"""
import os
from moviepy.editor import VideoFileClip

def GIFconvert_single(gifsource):

    print (gifsource,'start!')
    try:
        rootpath='./twt_resource/'
        sourcepath=rootpath+gifsource            
        generatepath=rootpath+gifsource    

        searchlist=os.listdir(sourcepath)
        allMP4=[i for i in searchlist if i[-3:]=='mp4']    
        
        if not os.path.isdir(generatepath):
            os.makedirs(generatepath)
        
        allGIF=os.listdir(generatepath)
        
        num=len(allMP4)
        print ('all mp4 count:',num)
        for vi in allMP4:
            num=num-1
            if vi[:-4]+'.gif' not in allGIF:
                try:
                    clip = (VideoFileClip(sourcepath+'/'+vi))
                    x=clip.fps * clip.duration
                    if x<200:
                        clip.write_gif(generatepath+"/%s.gif"%vi[:-4])  

                        if x<120:
                            clip.write_gif(generatepath+"/%s.gif"%vi[:-4])  
                            
                            
                        elif 120<x<170:
                            y=-0.5/50.*(x-120)+1.
                            #y=1.
                            clip = (VideoFileClip(sourcepath+'/'+vi).resize(y))
                            clip.write_gif(generatepath+"/%s.gif"%vi[:-4])    

                        elif 170<x<200:
                            y=-0.2/30.*(x-170)+0.5
                            clip = (VideoFileClip(sourcepath+'/'+vi).resize(y))
                            clip.write_gif(generatepath+"/%s.gif"%vi[:-4]) 
                    else:
                        print ("not a gif")
                        pass

                            
                    print (num)
                except Exception:
                    pass
                
            else:
                print ('pass')
    except Exception:
        pass


def GIFconvert(hashtags):
    for gifsource in hashtags:
        GIFconvert_single(gifsource)
        
                
                
                
                
                
                