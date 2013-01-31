#!/usr/bin/env python
# encoding: utf-8
"""
eventHandler.py

Created by 刘 智勇 on 2013-01-27.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

from baseHandler import BaseHandler
from huwai2.apps.event import Event
from tornado.web import addslash

class EventHandler(BaseHandler):
    @addslash
    def get(self):
        self.render("event/list.html")    

class EventItemHandler(BaseHandler):
    @addslash
    def get(self, id):
        self.render("event/item.html")

class EventNewHandler(BaseHandler):
    @addslash
    def get(self):
        self.render("event/new.html")
