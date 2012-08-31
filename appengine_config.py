# -*- coding: utf-8 -*-
'''
Created on Feb 15, 2012

@author: Rafael Nunes
'''


def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = recording.appstats_wsgi_middleware(app)
    return app
