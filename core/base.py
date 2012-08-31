# -*- coding: utf-8 -*-
'''
Created on Feb 13, 2012

@author: Rafael Nunes
'''


import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import db


class BaseHandler(webapp2.RequestHandler):
        @webapp2.cached_property
        def jinja2(self):
            return jinja2.get_jinja2(app=self.app)

        def render(self, filename, **template_args):
            self.response.write(self.jinja2.render_template(filename, **template_args))


class BaseModel(db.Model):
    def to_dict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

    def put_async(self):
        db.put_async(self)
