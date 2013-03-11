# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

"""
The :mod:`http` module manages the HTTP authorisation logic.  This code originates from
http://tools.cherrypy.org/wiki/AuthenticationAndAccessRestrictions

"""

import cherrypy
import logging

from openlp.core.lib import Settings

SESSION_KEY = '_cp_openlp'

log = logging.getLogger(__name__)


def check_credentials(user_name, password):
    """
    Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure
    """
    if user_name == Settings().value(u'remotes/user id') and password == Settings().value(u'remotes/password'):
        return None
    else:
        return u"Incorrect username or password."


def check_auth(*args, **kwargs):
    """
    A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill
    """
    conditions = cherrypy.request.config.get('auth.require', None)
    if not Settings().value(u'remotes/authentication enabled'):
        return None
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/auth/login")
        else:
            raise cherrypy.HTTPRedirect("/auth/login")

cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)


def require_auth(*conditions):
    """
    A decorator that appends conditions to the auth.require config variable.
    """
    def decorate(f):
        """
        Lets process a decoration.
        """
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate


class AuthController(object):

    def on_login(self, username):
        """
        Called on successful login
        """

    def on_logout(self, username):
        """
        Called on logout
        """

    def get_loginform(self, username, msg="Enter login information", from_page="/"):
        """
        Provides a login form
        """
        return """<html>
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, minimum-scale=1, maximum-scale=1" />
                <title>User Login</title>
                <link rel="stylesheet" href="/files/jquery.mobile.css" />
                <link rel="stylesheet" href="/files/openlp.css" />
                <link rel="shortcut icon" type="image/x-icon" href="/files/images/favicon.ico">
                <script type="text/javascript" src="/files/jquery.js"></script>
                <script type="text/javascript" src="/files/openlp.js"></script>
                <script type="text/javascript" src="/files/jquery.mobile.js"></script>
            </head>
            <body>
                <form method="post" action="/auth/login">
                <input type="hidden" name="from_page" value="%(from_page)s" />
                %(msg)s<br/>
                Username: <input type="text" name="username" value="%(username)s" /><br />
                Password: <input type="password" name="password" /><br />
                <input type="submit" value="Log in" />
            </body></html>""" % locals()

    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):
        """
        Provides the actual login control
        """
        if username is None or password is None:
            return self.get_loginform("", from_page=from_page)

        error_msg = check_credentials(username, password)
        if error_msg:
            return self.get_loginform(username, error_msg, from_page)
        else:
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or "/")

    @cherrypy.expose
    def logout(self, from_page="/"):
        """
        Provides the actual logout functions
        """
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or "/")

