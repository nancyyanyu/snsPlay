# SNSPlay

This project enables users to scrape, and download large amount of medias from multiple accounts on Twitter, Tumblr and Youtube. 

It integrates a Weibo bot that users could automatically repost recent tweets of some Twitter accounts to Weibo with proper credit, thus users could be able to manage a 'robot' weibo account.

## Getting Started

This project is developed under Python2.7.

```
git clone https://github.com/nancyyanyu/SNSPlay.git
```

### Prerequisites

Python packages:
- youtube_dl: popular package to extract and download Youtube videos
- tweepy: Twitter API wrapper [Document](http://docs.tweepy.org/en/v3.5.0/index.html)
- moviepy: video editing package; in this project, is used to convert video to GIF [Document](https://zulko.github.io/moviepy/)
- urllib2
- binascii
- requests
- rsa
- base64

```
pip install base64,rsa,requests,binascii,urllib2,youtube_dl,tweepy,moviepy
```

### Running the example

Please firstly check [example.py](https://github.com/nancyyanyu/SNSPlay/blob/master/example.py), which demonstrate some basic features and show how to run this project

## Content

- **Download tweets' medias with searching hashtags on Twitter**: [*twitter_search.py*](https://github.com/nancyyanyu/SNSPlay/blob/master/src/twitter/twitter_search.py) enables user download pictures, videos, and words of the latest several tweets with searching hashtags;
- **Download all tweets' medias of specified Twitter accounts**:[*twitter_history.py*](https://github.com/nancyyanyu/SNSPlay/blob/master/src/twitter/twitter_history.py) enables user to download pictures, videos, and words of all tweets of specified list of accounts;
- **Generate report of account status of multiple Twitter accounts**: [*twitter_info.py*](https://github.com/nancyyanyu/SNSPlay/blob/master/src/twitter/twitter_info.py) enables user to generate a report of the number of followers of a large amount of Twitter account. It could be used to track accounts growth;
- **Convert videos to GIF**: as GIF on Twitter would be downloaded in mp4 format, [*twitter_convertGIF.py*](https://github.com/nancyyanyu/SNSPlay/blob/master/src/twitter/twitter_convertGIF.py) enables format transformation from mp4 to gif;
- **Scrape medias of Tumblr posts**: [*tumblr.py*](https://github.com/nancyyanyu/SNSPlay/blob/master/src/tumblr.py) enables user to scrape gif, pictures, videos, and words of posts from specified Tumblr accounts;
- **Download all Youtube videos from a playlist with highest video quality**:[*youtube.py*](https://github.com/nancyyanyu/SNSPlay/blob/master/src/youtube.py)
- **Send weibo**: [*send_weibo.py*](https://github.com/nancyyanyu/SNSPlay/blob/master/src/send_weibo.py) enables users to automatically send Weibo posts with content of specified Twitter accounts' latest posts (with proper credit).





## Authors

* **Yanyu Yan** Email: yy2799@columbia.edu


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details

## Reference

Sending Weibo module of the project was based on the work of Zibin Zhang https://github.com/zhangzibin/sinaWeibo. Thanks to his work!
