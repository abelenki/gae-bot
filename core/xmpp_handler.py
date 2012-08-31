# -*- coding: utf-8 -*-
'''
Created on Feb 29, 2012

@author: Rafael Nunes
'''


import logging

from core.base import BaseHandler
from google.appengine.api import xmpp, mail
from core.models import Listener

log = logging


class IncomingMessage(BaseHandler):
    def post(self):
        msg = xmpp.Message(self.request.POST)
        fields = msg.body.split(';')
        try:
            if len(fields) < 2:
                xmpp.send_message(msg.sender,
                                  'Invalid message. Syntax: \
                                  <dest - user or group>;\
                                  <talk or mail(ignore for talk)>;\
                                  <message>')
            else:
                sender = msg.sender.split('/')[0]
                self.parse_message(fields, sender)
        except Exception, e:
            xmpp.send_message(msg.sender, 'Error sending message - ' + str(e))

    def parse_message(self, fields, sender):
        if '@' in fields[0]:
            usu = Listener.all().filter("mail", fields[0]).fetch(1)[0]
            if len(fields) == 3:
                self.notify(sender, usu, fields[1], fields[2])
            else:
                self.notify(sender, usu, 'talk', fields[1])
        else:
            users = Listener.all().filter("groups",
                                          fields[0].upper()).fetch(limit=None)
            for user in users:
                if user.talk != sender:
                    if len(fields) == 3:
                        self.notify(sender, user, fields[1],
                                    '[' + fields[0].upper() + '] ' + fields[2])
                    else:
                        self.notify(sender, user, 'talk',
                                    '[' + fields[0].upper() + ']' + fields[1])

    def notify(self, sender, user, tipo, message):
        if tipo == 'talk':
            xmpp.send_message(user.talk, 'From: ' + sender + ' - ' + message)
        elif tipo == 'mail':
            mail.send_mail(user.mail,
                           user.mail, 'GAE Notify',
                           'From: ' + sender + ' - ' + message)
