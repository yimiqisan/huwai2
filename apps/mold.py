#!/usr/bin/env python
# encoding: utf-8
"""
mold.py

Created by 刘 智勇 on 2013-01-26.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

from datetime import datetime
import uuid

from mongokit import Document, IS, INDEX_GEO2D

from huwai2.config import DB_NAME

class IdDoc(Document):
    __collection__ = 'ids'
    __database__ = DB_NAME
    
    structure = {
            '_id':unicode,
            'id':int,
    }
    use_schemaless = True
    use_dot_notation=True

class UserDoc(Document):
    __collection__ = 'people'
    __database__ = DB_NAME
    
    structure = {
            '_id':      unicode,
            'tel':      unicode,
            'qq':       unicode,
            'nick':     unicode,
            'password': unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
    }
    
    indexes = [
        {
            'fields':['_id', 'tel'],
            'unique':True,
        },
    ]
    
    required_fields = ['_id', 'created']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True


class EventDoc(Document):
    __collection__ = 'event'
    __database__ = DB_NAME
        
    structure = {
            '_id':      unicode,
            'owner':    unicode,
            'created':  datetime,
            'added':    dict,
            'added_id': int,
            'logo':     unicode,
            'title':    unicode,
            'members':  dict,
            'tags':     list,
            'club':     unicode,
            'is_merc':  bool,
            'level':    float,
            'route':    unicode,
            'date':     datetime,
            'day':      int,
            'place':    unicode,
            
            'schedule_tl':  unicode,
            'spend_tl':     unicode,
            'equip':        list,
            'declare_tl':   unicode,
            'attention_tl': unicode,
            
            'deadline': datetime,
            'fr':       int,
            'to':       int,
            'when':     datetime,
            'where':    unicode,
            
            'check':    bool,
    }
    required_fields = ['_id', 'owner', 'created', 'title', 'tags', 'date']
    default_values = {'_id':uuid.uuid4().hex, 'created':datetime.now(), 'fr':0, 'to':30, 'date':datetime.now(), 'deadline':datetime.now(), 'when':datetime.now()}
    
    use_schemaless = True
    use_dot_notation=True
