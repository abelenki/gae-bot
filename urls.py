# -*- coding: utf-8 -*-
'''
Created on Feb 13, 2012

@author: Rafael Nunes
'''
import webapp2

from core.handlers import *
from core.page_handlers import *
from core.xmpp_handler import IncomingMessage

routes = [('/', MainPage),
          ('/core/user/add', CreateListener),
          ('/notify/mensagem', SendNotificacao),
          ('/invite', InviteUser),
          ('/notify', AlertaUser),
          
          
          #Admin
          ('/adm/index', IndexPage),
          ('/adm/usuarios', HandleUsers),
          ('/adm/grupos', HandleGroups),
          ('/adm/mensagem', HandleMensagem),
          ('/adm/mensagem/send', SendNotificacao),
          ('/adm/grupos/add', AddGroups),
          ('/adm/grupo/add', AddGroup),
          ('/adm/grupos/listar', ListGroups),
          
          #XMPP
          ('/_ah/xmpp/message/chat/', IncomingMessage),
          
         ]
          
app = webapp2.WSGIApplication(routes, debug=True)





