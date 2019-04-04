# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 06:45:07 2017

@author: Yanyu
"""


import youtube_dl

def youtube(url):
    """
    Download all best quanlity youtube videos of a playlist
    """
    ydl_opts = {'format': 'best','ignoreerrors':False}
    ydl=youtube_dl.YoutubeDL(ydl_opts)
    ydl.extract_info(url)




