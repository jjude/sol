#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
#these pertain to your application
import sol.models
import sol.views
import sol.feeds
import urls
import manage
import settings
#these are django imports
import django.template.loaders.filesystem
import django.template.loaders.app_directories
import django.middleware.common
import django.contrib.sessions.middleware
import django.contrib.auth.middleware
import django.middleware.doc
import django.contrib.auth
import django.contrib.contenttypes
import django.contrib.sessions
import django.contrib.sessions.backends.db
import django.contrib.sites
import django.contrib.admin
import django.core.cache.backends
import django.db.backends.sqlite3.base
import django.db.backends.sqlite3.introspection
import django.db.backends.sqlite3.creation
import django.db.backends.sqlite3.client
import django.template.defaulttags
import django.template.defaultfilters
import django.template.loader_tags

import django.contrib.admin.urls
from django.conf.urls.defaults import *
import django.contrib.admin.views.main
import django.core.context_processors
import django.contrib.auth.views
import django.contrib.auth.backends
import django.views.static
import django.contrib.admin.templatetags.adminmedia
import django.contrib.admin.templatetags.adminapplist
import django.contrib.admin.templatetags.admin_list
import django.contrib.admin.templatetags.admin_modify
import django.contrib.admin.templatetags.log
import django.contrib.admin.views.auth
import django.contrib.admin.views.doc
import django.contrib.admin.views.template
import django.conf.urls.shortcut
import django.views.defaults
import django.contrib.syndication.views

#dont need to import these pkgs
#need to know how to exclude them
import email.mime.audio
import email.mime.base
import email.mime.image
import email.mime.message
import email.mime.multipart
import email.mime.nonmultipart
import email.mime.text
import email.charset
import email.encoders
import email.errors
import email.feedparser
import email.generator
import email.header
import email.iterators
import email.message
import email.parser
import email.utils
import email.base64mime
import email.quoprimime
import django.core.cache.backends.locmem
import django.templatetags.i18n
import django.views.i18n

#let us hook up cherrypy
#is it possible to hook up the dev server itself?
from cherrypy import wsgiserver
import cherrypy
import webbrowser
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler

if __name__ == "__main__":
    import socket
    #gethostbyaddrs returns a tuple in the form of (hostname, aliaslist,ipaddrlist)
    ipaddr = socket.gethostbyaddr(socket.gethostname())[2][0]
    siteaddr = 'http://%s:8000' % ipaddr
    
    print '*****************************************************'
    print 'Demoserver is hosted at: %s' % siteaddr
    print 'Please wait as it opens in the browser'
    print 'To shutdown the server, press ctrl-c in this window'
    print ''
    print 'local user id is: jjude; password is also jjude'
    print 'admin user id is: admin; password is also admin'
    print '*****************************************************'

    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': 'site.log',
                            'log.screen': False})


    try:
        sys.path.insert(0,"..")
        #2nd param to AdminMediaHandler should be absolute path to the admin media files
        cherrypy.tree.graft(AdminMediaHandler(WSGIHandler(),media_dir=os.path.dirname(os.path.abspath(sys.argv[0])) + settings.ADMIN_MEDIA_PREFIX), '/')
        cherrypy.server.socket_port = 8000

        cherrypy.server.quickstart()
        cherrypy.engine.start_with_callback(webbrowser.open, (siteaddr,),)

    except KeyboardInterrupt:
        cherrypy.server.stop()


