# -*- coding: utf-8 -*-
'''
Created on Feb 14, 2012

@author: Rafael Nunes
'''

from google.appengine.ext import db
from core.base import BaseModel
    
class Listener(BaseModel):
    mail = db.StringProperty()
    talk = db.StringProperty()
    groups = db.StringListProperty()
    mute = db.IntegerProperty()

    
