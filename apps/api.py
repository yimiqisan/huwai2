#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by 刘 智勇 on 2013-01-26.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import logging
import uuid
from datetime import datetime

from huwai2.config import DB_CON, DB_NAME
from mold import IdDoc

def get_uuid():
    return unicode(uuid.uuid4().hex)

class Added_id(object):
    ''' get autoincrement　id '''
    def __init__(self, idx):
        self.idx = idx
        DB_CON.register([IdDoc])
        self.datastore = DB_CON[DB_NAME]
        self.collection = self.datastore[IdDoc.__collection__]
    
    def incr(self):
        self.collection.update({"_id":self.idx},{"$inc":{"id":1}}, upsert=True)
    
    def decr(self):
        self.collection.update({"_id":self.idx},{"$inc":{"id":-1}}, upsert=True)
    
    def clear(self):
        self.collection.update({"_id":self.idx},{"$set":{"id":0}}, upsert=True)
    
    def count(self):
        try:
            return int(self.collection.one({"_id":self.idx})["id"])
        except:
            return 0
    
    def get(self):
        self.incr()
        return int(self.collection.one({"_id":self.idx})["id"])

class API(object):
    def __init__(self, db_name=DB_NAME, col_name=None, collection=None, doc=None):
        self.datastore = DB_CON[db_name]
        self.col_name = col_name
        self.collection = collection
        self.doc = doc
        self.structure = self.doc.structure
        self.structure.pop('added', None)
        self._fmt = lambda o: o
        
    def _init_doc(self, id):
        try:
            self.doc = self.collection.FileDoc.one({'_id':docid})
        except Exception:
            logging.info(e)
            raise Exception
        
    def create(self, **kwargs):
        self.doc['added'] = {}
        for k, v in kwargs.items():
            try:
                if k in self.structure:
                    if isinstance(self.structure[k], list) and not isinstance(v, list):
                        v = [v]
                    self.doc[k]=v
                else:
                    self.doc['added'][k] = v
            except Exception, e:
                pass
        a = Added_id(self.col_name)
        self.doc['added_id'] = a.get()
        id = get_uuid()
        self.doc['_id'] = id
        self.doc['created'] = datetime.now()
        try:
            self.doc.save(uuid=True, validate=True)
        except Exception, e:
            logging.info(e)
            return (False, unicode(e))
        return (True, id)
        
    def remove(self, id):
        if not id:return False
        return self.collection.remove(id)
        
    def drops(self, **kwargs):
        try:
            self.collection.remove(kwargs)
        except Exception, e:
            logging.info(e)
            return False
        return True
        
    def drop_table(self):
        self.datastore.drop_collection(self.col_name)
        
    def _edit_added(self, id, **addeds):
        r = self.one(_id=id)
        if r[0]:
            addeds_t = r[1].get('added', {})
            addeds_t.update(addeds)
            self.collection.update({"_id":id}, {'$set':{'added': addeds_t}})
    
    def _edit_dict(self, id, key, **dicts):
        r = self.one(_id=id)
        if r[0]:
            dicts.update(r[1].get(key, {}))
            self.collection.update({"_id":id}, {'$set':{key: dicts}})
    
    def edit(self, id, *args, **kwargs):
        items=dict(args)
        items.update(kwargs)
        isOverWrite = items.pop('isOverWrite', False)
        keyl_l = items.keys()
        addeds = {}
        lists = {}
        for k in keyl_l:
            try:
                if k not in self.structure:
                    addeds[k]=items.pop(k)
                elif isinstance([], self.structure[k]) and not isOverWrite:
                    li = items.pop(k, None)
                    if li:lists[k] = {"$each":li} if isinstance(li, list) else li
                elif isinstance({}, self.structure[k]):
                    dicts = items.pop(k)
                    self._edit_dict(id, k, **dicts)
            except Exception, e:
                pass
        try:
            if lists: self.collection.update({"_id":id}, {"$addToSet":lists})
            self.collection.update({"_id":id}, {"$set":items})
            if (len(addeds)>0):self._edit_added(id, **addeds)
        except Exception, e:
            logging.info(e)
            return(False, unicode(e))
        return (True, id)
    
    def _output(self, result=[]):
        now = datetime.now()
        if isinstance(result, dict):
            return self._fmt(result)
        return map(self._fmt, result)
    
    def extend(self, **kwargs):
        cursor = kwargs.pop('cursor', None)
        limit = kwargs.pop('limit', 20)
        order = kwargs.pop('order', -1)
        order_by = kwargs.pop('order_by', 'added_id')
        if cursor and (order < 0):
            kwargs.update({order_by:{'$lt':cursor}})
        elif cursor and (order > 0):
            kwargs.update({order_by:{'$gt':cursor}})
        try:
            objs= self.collection.find(kwargs).sort(order_by, order).limit(limit)
        except:
            return (False, 'search error')
        return (True, objs)
    
    def page(self, **kwargs):
        page = int(kwargs.pop('page', 1))
        pglen = int(kwargs.pop('pglen', 10))
        limit = int(kwargs.pop('limit', 20))
        start = (page-1)*limit
        order_by = kwargs.pop('order_by', 'added_id')
        order = kwargs.pop('order', -1)
        try:
            objs=self.collection.find(kwargs).sort(order_by, order).skip(start).limit(limit)
            cnt=self.collection.find(kwargs).count()
        except Exception, e:
            return (False, e)
        #get page additional infomation
        info = {}
        total_page = cnt/limit
        if (cnt%limit) != 0:total_page+=1
        info['total_page'] = total_page
        info['has_pre'] = (page>1)
        info['start_page'] = 1
        info['pre_page'] = max(1, page-1)
        info['page'] = page
        info['page_list'] = range(max(1, min(page-pglen/2, total_page-pglen+1)), min(max(page+pglen/2, pglen), total_page)+1)
        info['has_eps'] = (total_page>max(page+1+pglen/2, pglen+1)>pglen)
        info['has_next'] = (page<total_page)
        info['next_page'] = min(page+1, total_page)
        info['end_page'] = total_page		
        return (True, objs, info)
    
    def count(self, **kwargs):
        try:
            cnt=self.collection.find(kwargs).count()
        except Exception, e:
            return -1
        return cnt
    
    def one(self, **kwargs):
        try:
            r = self.collection.one(kwargs)
        except Exception, e:
            logging.info(e)
            return (False, e)
        return (True, r)
        
    def find(self, **kwargs):
        lmt = kwargs.pop('limit', None)
        order = kwargs.pop('order', -1)
        order_by = kwargs.pop('order_by', 'added_id')
        try:
            if lmt:
                r = self.collection.find(kwargs).sort(order_by, order).limit(lmt)
            else:
                r = self.collection.find(kwargs).sort(order_by, order)
        except Exception, e:
            logging.info(e)
            return (False, e)
        return (True, r)
    
    def map(self, func, opts, **kwargs):
        if kwargs == {}:
            objs = self.collection.find()
        else:
            ret = self.collection.find(kwargs)
            if not ret[0]:
                return (False, 'error get objects')
            objs = ret[1]
        cnt = objs.count()
        c = True
        for i in xrange(cnt/100+1):
            objr = objs[i*100:(i*100 + 100)]
            for obj in objr:
                r = func(obj, opts)
                if not r:
                    c = False
                    break
            if not c:
                break
        return (True, None)
    
    def exist(self, key, value):
        try:
            return self.collection.one({key:value}) is not None
        except Exception, e:
            logging.info(e)
            raise Exception


