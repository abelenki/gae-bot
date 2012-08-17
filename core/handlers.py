# -*- coding: utf-8 -*-
''' 
Created on Feb 13, 2012

@author: Rafael Nunes
'''
import logging

from core.base import BaseHandler
from google.appengine.api import taskqueue, xmpp, memcache, mail
from django.utils import simplejson
from core.models import Listener
from sets import Set
from webapp2_extras import json
import urllib

log = logging

class SendNotificacao(BaseHandler):
    def post(self):
        out = self.response.write
        try:
            param = self.request.get('json')
            json = simplejson.loads(param)
            user = json['user']
            sender = Listener.all().filter("mail", json['from']).get()
            msg = urllib.unquote(json['message'])
            if '@' in user:
                taskqueue.add(url='/notify', params = {'from':sender.mail,'user':user, 'message':msg},queue_name='notify')
            else:
                users = Listener.all().filter("groups", user.upper()).fetch(limit=None)
                for u in users:
                    if sender.mute == 0 and u.mail != sender.mail:
                        taskqueue.add(url='/notify', params = {'from':sender.mail,'user':u.talk, 'message':msg},queue_name='notify')
            out('{"success":true}')
        except Exception, e:
            out('{"success": false, "msg":"' + str(e)+'"}')

class CreateListener(BaseHandler):
    def post(self):
        out = self.response.write
        try:
            param = self.request.get('json')
            json = simplejson.loads(param)
            for user in json['notify']:
                exists = Listener.all().filter("mail", user['mail']).get()
                if exists is None:
                    listener = Listener(mail=user['mail'], talk=user.get('talk', user['mail']), groups=user['groups'], mute=0)
                    listener.put()
                    taskqueue.add(url='/invite', params = {'mail':user['mail']}, queue_name='invite')
        except Exception, e:
            out('Erro no gae ' + str(e))
            
class AddGroups(BaseHandler):
    def post(self):
        param = self.request.get('json', '{"mail":"None"}')
        json = simplejson.loads(param)
        user = Listener.all().filter("mail", json['mail']).get()
        if not user is None:
            user.groups=json['grupos']
            user.put()
            
class AddGroup(BaseHandler):
    def post(self):
        param = self.request.get('json', '{"mail":"None"}')
        json = simplejson.loads(param)
        user = Listener.all().filter("mail", json['mail']).get()
        if not user is None:
            user.groups= user.groups + json['grupos']
            user.put()

        
class ListGroups(BaseHandler):
    def get(self):
        out = self.response.write
        users = Listener.all().fetch(limit=None)
        grupos = Set([])
        for u in users:
            for g in u.groups:
                grupos.add(g)
        resp = {'mail':'nunes@q10.com.br'} 
        resp['grupos'] = list(grupos)
        out(json.encode(resp))
        
class AlertaUser(BaseHandler):
    def post(self):
        user = self.request.get('user')
        message = self.request.get('message')
        remetente = self.request.get('from')
        tipo = self.request.get('tipo', 'talk')
        self.notify(remetente, user,tipo,message)
    
    def notify(self, sender,user, tipo, message):
        if tipo == 'talk':
            xmpp.send_message(user, 'From: ' + sender + ' - ' + message)
        elif tipo == 'mail':
            mail.send_mail(user, user, 'GAE Notify', 'From: ' + sender + ' - ' + message)    
        
class InviteUser(BaseHandler):
    def post(self):
        try:
            mail = self.request.get('mail')
            xmpp.send_invite(mail)
        except:
            log.error('NÃ£o foi possÃ­vel enviar o convite para ' + mail)            
