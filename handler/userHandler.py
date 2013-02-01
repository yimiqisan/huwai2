#!/usr/bin/env python
# encoding: utf-8
"""
userHandler.py

Created by 刘 智勇 on 2013-01-30.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import json

from tornado.web import addslash

from baseHandler import BaseHandler
from huwai2.apps.user import User
from huwai2.apps.session import session


class RegHandler(BaseHandler):
    def get(self):
        self.render("reg.html")
    
    @session
    def post(self):
        icode = self.get_argument('icode')
        tel = self.get_argument('name')
        password = self.get_argument('password')
        nick = self.get_argument('nick')
        user = User()
        r = user.reg(tel, password, nick=nick)
        if r[0]:
            self.SESSION['uid']=user._id
            self.SESSION['nick']=user.nick
            ref = self.request.headers.get('Referer', '').split('/')[-1]
            if ref == 'reg':ref='/'
            return self.redirect('/'+ref)
        else:
            return self.redirect('/reg/')

class QQRegAjax(BaseHandler):
    @session
    def post(self):
        icode = self.get_argument('icode')
        openid = self.get_argument('openid')
        token = self.get_argument('token')
        nick = self.get_argument('nick')
        user = User()
        r = user.qqreg(openid, token, nick=nick)
        if r[0]:
            self.SESSION['uid']=user._id
            self.SESSION['nick']=user.nick
        else:
            print r

class RegCheck(BaseHandler):
    def get(self):
        key = self.get_argument('key')
        val = self.get_argument('val')
        d = {}
        if key == 'name':
            if not User.exist('tel', val):
                d['ok'] = '未被注册号码，可用'
            else:
                d['error'] = '该号码已被注册'
        elif key == 'icode':
            d['ok'] = '有效的邀请码'
        return self.write(json.dumps(d))

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    
    @session
    def post(self):
        name = self.get_argument('name')
        password = self.get_argument('password')
        user = User(name=name)
        if user.check_password(password):
            self.SESSION['uid']=user._id
            self.SESSION['nick']=user.nick
            ref = self.request.headers.get('Referer', '').split('/')[-1]
            if ref == 'login':ref='/'
            return self.redirect('/'+ref)
        else:
            print '密码不正确'
            return self.redirect('/login/')

class QQLoginAjax(BaseHandler):
    @session
    def post(self):
        openid = self.get_argument('openid')
        user = User()
        user.whois('qq', openid)
        self.SESSION['uid']=user._id
        self.SESSION['nick']=user.nick

class LoginCheck(BaseHandler):
    def get(self):
        key = self.get_argument('key')
        val = self.get_argument('val')
        d = {}
        if key == 'name':
            if User.exist('tel', val):
                d['ok'] = '有效的电话号码'
            else:
                d['error'] = '不存在此电话号码'
        elif key == 'qq':
            if User.exist('qq', val):
                d['ok'] = '可登陆QQ号'
            else:
                d['error'] = '尚未绑定，不可用'
        return self.write(json.dumps(d))

class LoginAjax(BaseHandler):
    @session
    def post(self):
        name = self.get_argument('name')
        password = self.get_argument('password')
        user = User(name=name)
        if user.check_password(password):
            self.SESSION['uid']=user._id
            self.SESSION['nick']=user.nick
            self.write({'ok':user._id})
        else:
            self.write({'error':'登陆失败'})

class LoginOAuth(BaseHandler):
    @session
    def get(self):
        self.render("user/qqlogin.html")

class LogoutHandler(BaseHandler):
    @addslash
    @session
    def get(self):
        del self.SESSION['uid'], self.SESSION['nick']
        return self.redirect(self.request.headers.get('Referer', '/'))


