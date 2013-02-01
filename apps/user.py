#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by 刘 智勇 on 2013-01-26.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime
from md5 import md5

from huwai2.config import DB_CON, DB_NAME
from mold import UserDoc
from api import API

class User(object):
    def __init__(self, name=None, api=None):
        self._api = api if api else UserAPI()
        if name:self.whois('tel', name)
    
    def __getattr__(self, key):
        if hasattr(self, 'info') and self.info and (key in self.info):
            return self.info[key]
        else:
            return None
    
    @classmethod
    def exist(self, k, v):
        if not hasattr(self, '_api'):self._api = UserAPI()
        return self._api.exist(k, v)
    
    def whois(self, k, v):
        c = self._api.one(**{k:v})
        if c[0] and c[1]:
            self.info = c[1]
            self.uid = self.info['_id']
        else:
            self.uid = self.info = None
    
    def check_password(self, pwd):
        return self.password == unicode(md5(pwd).hexdigest())
    
    def reg(self, tel, password, **info):
        if self._api.exist('tel', tel):
            return (False, '已存在此电话号码')
        info.update({'tel':tel, 'password':unicode(md5(password).hexdigest())})
        c = self._api.create(**info)
        self.info = info if c[0] else None
        return c
    
    def qq(self, openid, token, **info):
        if self._api.exist('qq', openid):
            return (False, '此号码已注册')
        info.update({'qq':openid, 'qq_token':token})
        c = self._api.create(**info)
        self.info = info if c[0] else None
        return c

class UserAPI(API):
    def __init__(self):
        DB_CON.register([UserDoc])
        datastore = DB_CON[DB_NAME]
        col_name = UserDoc.__collection__
        collection = datastore[col_name]
        doc = collection.UserDoc()
        API.__init__(self, col_name=col_name, collection=collection, doc=doc)
    
    def is_nick_exist(self, nick):
        return self.exist("nick", nick)
    
    def is_email_exist(self, email):
        return self.exist("email", email)
    
    def is_nick(self, nick):
        try:
            nick.encode('utf8')
        except UnicodeEncodeError:
            return True
        if len(nick)==32:
            return False
        return True
    
    def change_pwd(self, id, o, n, c):
        self.edit(id, password=n)
    
    def check_email(self):
        pass
    
    def nick2id(self, nick):
        if self.is_nick(nick):
            r = self.one(nick=nick)
            if r[0] and r[1]:
                return r[1]['_id']
            return None
        return nick
