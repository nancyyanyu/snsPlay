# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 05:53:18 2019

@author: Yan
"""


import re
import json
import base64
import binascii
import rsa
import requests
from config import WBCLIENT, USER_AGENT,USER_NAME, PASSWD


def _password(password, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    return binascii.b2a_hex(passwd)

def weibo_login():
    session = requests.session()
    session.headers['User-Agent'] = USER_AGENT

    username = USER_NAME
    password = PASSWD
    resp = session.get(
        'http://login.sina.com.cn/sso/prelogin.php?'
        'entry=weibo&callback=sinaSSOController.preloginCallBack&'
        'su=%s&rsakt=mod&checkpin=1&client=%s' %
        (base64.b64encode(username.encode('utf-8')), WBCLIENT)
    )

    pre_login_str = re.match(r'[^{]+({.+?})', resp.text).group(1)
    pre_login = json.loads(pre_login_str)
    data = {
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'userticket': 1,
        'ssosimplelogin': 1,
        'su': base64.b64encode(requests.utils.quote(username).encode('utf-8')),
        'service': 'miniblog',
        'servertime': pre_login['servertime'],
        'nonce': pre_login['nonce'],
        'vsnf': 1,
        'vsnval': '',
        'pwencode': 'rsa2',
        'sp': _password(password, pre_login['pubkey'],
                             pre_login['servertime'], pre_login['nonce']),
        'rsakv': pre_login['rsakv'],
        'encoding': 'UTF-8',
        'prelt': '53',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
               'naSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }

    login_url_list = 'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT
    resp = session.post(login_url_list, data=data)
    match_obj = re.search('replace\\(\'([^\']+)\'\\)', resp.text)
    if match_obj is None:
        print('Login failed')
        return (session, None)

    login_url = match_obj.group(1)
    resp = session.get(login_url)
    login_str = login_str = re.search('\((\{.*\})\)', resp.text).group(1)
    login_info = json.loads(login_str)
    print("login success：[%s]" % str(login_info))
    uniqueid = login_info["userinfo"]["uniqueid"]
    return (session, uniqueid)


