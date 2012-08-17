# -*- coding: utf-8 -*-
'''
Created on Feb 13, 2012

@author: Rafael Nunes
'''
import os
from webapp2_extras import jinja2
from google.appengine.api import users
from webapp2 import redirect

def template(name, values):
    path = os.path.join(os.path.dirname(__file__), name)
    return template.render(path, values)
