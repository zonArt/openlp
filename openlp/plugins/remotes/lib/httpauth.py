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
import os

from mako.template import Template

from openlp.core.lib import Settings
from openlp.core.utils import AppLocation, translate

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
        return translate('RemotePlugin.Mobile', 'Incorrect username or password.')


def check_authentication(*args, **kwargs):
    """
    A tool that looks in config for 'auth.require'. If found and it is not None, a login is required and the entry is
    evaluated as a list of conditions that the user must fulfill
    """
    conditions = cherrypy.request.config.get('auth.require', None)
    a = cherrypy.request
    print a
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

cherrypy.tools.auth = cherrypy.Tool('before_handler', check_authentication)


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
        pass

    def on_logout(self, username):
        """
        Called on logout
        """
        pass

    def get_login_form(self, username, message=None, from_page="/"):
        """
        Provides a login form
        """
        if not message:
            message = translate('RemotePlugin.Mobile', 'Enter login information')
        variables = {
            'title': translate('RemotePlugin.Mobile', 'OpenLP 2.1 User Login'),
            'from_page': from_page,
            'message': message,
            'username': username
        }
        directory = os.path.join(AppLocation.get_directory(AppLocation.PluginsDir), u'remotes', u'html')
        login_html = os.path.normpath(os.path.join(directory, u'login.html'))
        html = Template(filename=login_html, input_encoding=u'utf-8', output_encoding=u'utf-8').render(**variables)
        cherrypy.response.headers['Content-Type'] = u'text/html'
        cherrypy.response.status = 200
        return html

    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):
        """
        Provides the actual login control
        """
        if username is None or password is None:
            return self.get_login_form("", from_page=from_page)
        error_msg = check_credentials(username, password)
        if error_msg:
            return self.get_login_form(username, from_page, error_msg,)
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

