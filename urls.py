#!/usr/bin/env python
# encoding: utf-8
"""
urls.py

Created by 刘 智勇 on 2013-01-26.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

from handler import *

handlers = [(r"/", RootHandler),
            
            (r"/reg/", RegHandler),
            (r"/c/reg/", RegCheck),
            (r"/qq/reg/", QQRegAjax),
            
            (r"/login/", LoginHandler),
            (r"/a/login/", LoginAjax),
            (r"/c/login/", LoginCheck),
            (r"/o/login/", LoginOAuth),
            
            (r"/logout/", LogoutHandler),
            
            (r"/event/", EventHandler),
            (r"/event/(.{32})/", EventItemHandler),
            (r"/event/new/", EventNewHandler),
            
            (r".*", Error404Handler),
            ]