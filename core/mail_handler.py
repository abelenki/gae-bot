# -*- coding: utf-8 -*-
'''
Created on Feb 29, 2012

@author: Rafael Nunes
'''


import logging

from core.base import BaseHandler
from google.appengine.api import mail
from core.models import Listener
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

log = logging


class IncomingMail(BaseHandler):
    def post(self):
        pass


class MuteMail(InboundMailHandler):
    def receive(self, mail_message):
        log.warn("Receiving mail " + mail_message.sender)
        sender = ''
        if '<' in mail_message.sender:
            init = mail_message.sender.index('<')
            end = mail_message.sender.index('>')
            sender = mail_message.sender[init + 1:end]
        else:
            sender = mail_message.sender

        usu = Listener.all().filter("mail", sender).fetch(1)[0]
        if not usu is None:
            acao = mail_message.subject
            if acao == 'enable':
                usu.mute = 1
            elif acao == 'disable':
                usu.mute = 0
            usu.put()
