#!/usr/bin/env python
# encoding: utf-8
"""
commonHandler.py

Created by 刘 智勇 on 2013-01-27.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import json

from tornado.web import addslash

from baseHandler import BaseHandler
from huwai2.apps.session import session

class RootHandler(BaseHandler):
    @session
    def get(self):
        self.render("index.html")

class Error404Handler(BaseHandler):
    @addslash
    def get(self):
        self.write(u"从前有个山，\n山里有个庙，\n庙里有个页面，\n现在找不到。")
