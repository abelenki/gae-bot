# -*- coding: utf-8 -*-
'''
Created on Aug 03, 2012

@author: Rafael Nunes
'''


import logging
from google.appengine.api import users, taskqueue

from core.base import BaseHandler
from core.models import Listener

from sets import Set


log = logging


class MainPage(BaseHandler):
    def get(self):
        self.redirect('/adm/index')


def buscar_grupos():
    users = Listener.all().fetch(limit=None)
    grupos = Set([])
    for u in users:
        for g in u.groups:
            grupos.add(g)
    return grupos


class IndexPage(BaseHandler):
    def get(self):
        usuario = users.get_current_user().email()
        user = Listener.all().filter("mail", usuario).get()
        if user is None:
            user = Listener(mail=usuario, talk=usuario, groups=[], mute=0)
            user.put()
            taskqueue.add(url='/invite',
                          params={'mail': usuario},
                          queue_name='invite')
        todos = list(buscar_grupos().difference(user.groups))
        self.render('index.html',
                    usuario=usuario,
                    user_groups=user.groups,
                    all_groups=todos)


class HandleUsers(BaseHandler):
    def get(self):
        users = Listener.all().fetch(limit=None)
        self.render('usuarios.html', usuarios=users)


class HandleMensagem(BaseHandler):
    def get(self):
        usuario = users.get_current_user().email()
        self.render('mensagem.html', user=usuario)

    def post(self):
        print 'ok'


class HandleGroups(BaseHandler):
    def get(self):
        self.render('grupos.html')
