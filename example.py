# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 15:24:45 2017

@author: Yanyu
"""


from src.tumblr import Tumblr
from src.youtube import youtube
from src.twitter.twitter_info import Info
from src.twitter.twitter_search import Search
from src.twitter.twitter_history import History
from src.twitter.twitter_convertGIF import GIFconvert
from src.twitter.logger import *



#try search keywords and post the latest tweets to weibo (with credit source!)           
hashtag=['jimin','jungkook','kookmin'] 
obj1=Search(hashtag,lots=20,vi=True,pic=True,twt=True)
obj1.search_download()  


#try download all historical tweets of a list of accounts
accounts=['realDonaldTrump']
obj2=History(accounts,lots=20,vi=True,pic=True,twt=True)
obj2.history_download()


#convert mp4 to gif
GIFconvert(hashtag)

#report a summary of a large amount of accounts
obj3=Info(usernamesjimin,'jimin') #check usernamesjimin in logger.py
obj3.getinfo()


#download all medias of all tumblr posts of an account
obj4=Tumblr('sweaterpawsjimin',50)
posts=obj4.get_post()
obj4.download(posts,video=False)


#download all videos of a playlist with best quanlity
url='https://www.youtube.com/watch?v=b_I-B7NjhXo'
youtube(url)



