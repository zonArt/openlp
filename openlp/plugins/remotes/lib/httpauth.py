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
import urlparse

SESSION_KEY = '_cp_openlp'


def check_credentials(user_name, password):
    """
    Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure
    """
    # @todo make from config
    print "check_credentials"
    if user_name == 'openlp' and password == 'openlp':
        return None
    else:
        return u"Incorrect username or password."
    # if u.password != md5.new(password).hexdigest():
    #     return u"Incorrect password"


def check_auth(*args, **kwargs):
    """
    A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill
    """
    print "check_auth"
    conditions = cherrypy.request.config.get('auth.require', None)
    print urlparse.urlparse(cherrypy.url()), conditions
    print conditions
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        print username
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                print "c ", condition
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


# Conditions are callables that return True
# if the user fulfills the conditions they define, False otherwise
#
# They can access the current username as cherrypy.request.login
#
# Define those at will however suits the application.

#def member_of(groupname):
#    def check():
#        # replace with actual check if <username> is in <groupname>
#        return cherrypy.request.login == 'joe' and groupname == 'admin'
#    return check


#def name_is(reqd_username):
#    return lambda: reqd_username == cherrypy.request.login

#def any_of(*conditions):
#    """
#    Returns True if any of the conditions match
#    """
#    def check():
#        for c in conditions:
#            if c():
#                return True
#        return False
#    return check

# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
#def all_of(*conditions):
#    """
#    Returns True if all of the conditions match
#    """
#    def check():
#        for c in conditions:
#            if not c():
#                return False
#        return True
#    return check
# Controller to provide login and logout actions


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
        return """<html><body>
            <form method="post" action="/auth/login">
            <input type="hidden" name="from_page" value="%(from_page)s" />
            %(msg)s<br />
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

