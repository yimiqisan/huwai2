#!/usr/bin/env python
# encoding: utf-8
"""
baseHandler.py

Created by 刘 智勇 on 2013-01-27.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

from tornado.web import RequestHandler
from huwai2.config import DB_CON
from huwai2.apps.session import session

class BaseHandler(RequestHandler):
    @property
    def db(self):
        return DB_CON
    
    @session
    def get_current_user(self):
        return self.SESSION['nick']
    
    @session
    def render(self, template_name, **kwargs):
        kwargs['uid'] = self.SESSION['uid']
        kwargs['warning'] = kwargs.get('warning', None)
        kwargs['page_title'] = kwargs.get('page_title', None)
        kwargs['meta_kws'] = kwargs.get('meta_kws', None)
        kwargs['meta_desp'] = kwargs.get('meta_desp', None)
        super(BaseHandler, self).render(template_name, **kwargs)

