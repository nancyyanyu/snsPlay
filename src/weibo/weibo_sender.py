# -*- coding: utf-8 -*-

import time
import re
import json


class Sender(object):

    def __init__(self, session, uid):
        self.session = session
        self.uid = str(uid)
        self.referer = "http://www.weibo.com/u/%s/home?wvr=5" % self.uid


    def send_weibo(self, weibo):
        pids = ''
        if weibo.has_image:
            pids = self.upload_images(weibo.images)
        data = weibo.get_send_data(pids)
        self.session.headers["Referer"] = self.referer
        try:
            r=self.session.post("https://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d"
                              % int(time.time() * 1000),
                              data=data)
            infom=json.loads(r.text)
            print(infom['msg'])
            if infom['code']=='100001':
                return
            else:
                print('Send[%s] success' % str(weibo))
                
        except:
            print('Send[%s] failed' % str(weibo))


    def upload_images(self, images):
        pids = ""
        if len(images) > 9:
            images = images[0: 9]
        for image in images:
            pid = self.upload_image_stream(image)
            if pid:
                pids += " " + pid
            time.sleep(10)
            print('Download pic of %s'%image)
        return pids.strip()


    def upload_image_stream(self, image_url):
        url = "http://picupload.service.weibo.com/interface/pic_upload.php?\
        rotate=0&app=miniblog&s=json&mime=image/jpeg&data=1&wm="

        image_name = image_url
        try:
            f = self.session.get(image_name, timeout=30)
            img = f.content
            resp = self.session.post(url, data=img)
            upload_json = re.search('{.*}}', resp.text).group(0)
            result = json.loads(upload_json)
            code = result["code"]
            if code == "A00006":
                pid = result["data"]["pics"]["pic_1"]["pid"]
                return pid
        except:
            print("Image upload failed：%s" % image_name)








