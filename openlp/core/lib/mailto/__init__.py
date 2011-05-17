# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# Utilities for opening files or URLs in the registered default application   #
# and for sending e-mail using the user's preferred composer.                 #
# --------------------------------------------------------------------------- #
# Copyright (c) 2007 Antonio Valentino                                        #
# All rights reserved.                                                        #
# --------------------------------------------------------------------------- #
# This program offered under the PSF License as published by the Python       #
# Software Foundation.                                                        #
#                                                                             #
# The license text can be found at http://docs.python.org/license.html        #
#                                                                             #
# This code is taken from: http://code.activestate.com/recipes/511443         #
# Modified for use in OpenLP                                                  #
###############################################################################

__version__ = u'1.1'
__all__ = [u'open', u'mailto']

import os
import sys
import webbrowser
import subprocess

from email.Utils import encode_rfc2231

_controllers = {}
_open = None


class BaseController(object):
    """
    Base class for open program controllers.
    """

    def __init__(self, name):
        self.name = name

    def open(self, filename):
        raise NotImplementedError


class Controller(BaseController):
    """
    Controller for a generic open program.
    """

    def __init__(self, *args):
        super(Controller, self).__init__(os.path.basename(args[0]))
        self.args = list(args)

    def _invoke(self, cmdline):
        if sys.platform[:3] == u'win':
            closefds = False
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            closefds = True
            startupinfo = None

        if (os.environ.get(u'DISPLAY') or sys.platform[:3] == u'win' or \
                sys.platform == u'darwin'):
            inout = file(os.devnull, u'r+')
        else:
            # for TTY programs, we need stdin/out
            inout = None

        # if possible, put the child precess in separate process group,
        # so keyboard interrupts don't affect child precess as well as
        # Python
        setsid = getattr(os, u'setsid', None)
        if not setsid:
            setsid = getattr(os, u'setpgrp', None)

        pipe = subprocess.Popen(cmdline, stdin=inout, stdout=inout,
            stderr=inout, close_fds=closefds, preexec_fn=setsid,
            startupinfo=startupinfo)

        # It is assumed that this kind of tools (gnome-open, kfmclient,
        # exo-open, xdg-open and open for OSX) immediately exit after lauching
        # the specific application
        returncode = pipe.wait()
        if hasattr(self, u'fixreturncode'):
            returncode = self.fixreturncode(returncode)
        return not returncode

    def open(self, filename):
        if isinstance(filename, basestring):
            cmdline = self.args + [filename]
        else:
            # assume it is a sequence
            cmdline = self.args + filename
        try:
            return self._invoke(cmdline)
        except OSError:
            return False


# Platform support for Windows
if sys.platform[:3] == u'win':

    class Start(BaseController):
        """
        Controller for the win32 start progam through os.startfile.
        """

        def open(self, filename):
            try:
                os.startfile(filename)
            except WindowsError:
                # [Error 22] No application is associated with the specified
                # file for this operation: '<URL>'
                return False
            else:
                return True

    _controllers[u'windows-default'] = Start(u'start')
    _open = _controllers[u'windows-default'].open


# Platform support for MacOS
elif sys.platform == u'darwin':
    _controllers[u'open'] = Controller(u'open')
    _open = _controllers[u'open'].open


# Platform support for Unix
else:

    import commands

    # @WARNING: use the private API of the webbrowser module
    from webbrowser import _iscommand

    class KfmClient(Controller):
        """
        Controller for the KDE kfmclient program.
        """

        def __init__(self, kfmclient=u'kfmclient'):
            super(KfmClient, self).__init__(kfmclient, u'exec')
            self.kde_version = self.detect_kde_version()

        def detect_kde_version(self):
            kde_version = None
            try:
                info = commands.getoutput(u'kfmclient --version')

                for line in info.splitlines():
                    if line.startswith(u'KDE'):
                        kde_version = line.split(u':')[-1].strip()
                        break
            except (OSError, RuntimeError):
                pass

            return kde_version

        def fixreturncode(self, returncode):
            if returncode is not None and self.kde_version > u'3.5.4':
                return returncode
            else:
                return os.EX_OK

    def detect_desktop_environment():
        """
        Checks for known desktop environments

        Return the desktop environments name, lowercase (kde, gnome, xfce)
        or "generic"
        """

        desktop_environment = u'generic'

        if os.environ.get(u'KDE_FULL_SESSION') == u'true':
            desktop_environment = u'kde'
        elif os.environ.get(u'GNOME_DESKTOP_SESSION_ID'):
            desktop_environment = u'gnome'
        else:
            try:
                info = commands.getoutput(u'xprop -root _DT_SAVE_MODE')
                if u' = "xfce4"' in info:
                    desktop_environment = u'xfce'
            except (OSError, RuntimeError):
                pass

        return desktop_environment


    def register_X_controllers():
        if _iscommand(u'kfmclient'):
            _controllers[u'kde-open'] = KfmClient()

        for command in (u'gnome-open', u'exo-open', u'xdg-open'):
            if _iscommand(command):
                _controllers[command] = Controller(command)


    def get():
        controllers_map = {
            u'gnome': u'gnome-open',
            u'kde': u'kde-open',
            u'xfce': u'exo-open',
        }

        desktop_environment = detect_desktop_environment()

        try:
            controller_name = controllers_map[desktop_environment]
            return _controllers[controller_name].open

        except KeyError:
            if _controllers.has_key(u'xdg-open'):
                return _controllers[u'xdg-open'].open
            else:
                return webbrowser.open

    if os.environ.get(u'DISPLAY'):
        register_X_controllers()
    _open = get()


def open(filename):
    """
    Open a file or an URL in the registered default application.
    """

    return _open(filename)


def _fix_addresses(**kwargs):
    for headername in (u'address', u'to', u'cc', u'bcc'):
        try:
            headervalue = kwargs[headername]
            if not headervalue:
                del kwargs[headername]
                continue
            elif not isinstance(headervalue, basestring):
                # assume it is a sequence
                headervalue = u','.join(headervalue)
        except KeyError:
            pass
        except TypeError:
            raise TypeError(u'string or sequence expected for "%s", %s '
                u'found' % (headername, type(headervalue).__name__))
        else:
            translation_map = {u'%': u'%25', u'&': u'%26', u'?': u'%3F'}
            for char, replacement in translation_map.items():
                headervalue = headervalue.replace(char, replacement)
            kwargs[headername] = headervalue

    return kwargs


def mailto_format(**kwargs):
    """
    Compile mailto string from call parameters
    """
    # @TODO: implement utf8 option

    kwargs = _fix_addresses(**kwargs)
    parts = []
    for headername in (u'to', u'cc', u'bcc', u'subject', u'body', u'attach'):
        if kwargs.has_key(headername):
            headervalue = kwargs[headername]
            if not headervalue:
                continue
            if headername in (u'address', u'to', u'cc', u'bcc'):
                parts.append(u'%s=%s' % (headername, headervalue))
            else:
                headervalue = encode_rfc2231(headervalue) # @TODO: check
                parts.append(u'%s=%s' % (headername, headervalue))

    mailto_string = u'mailto:%s' % kwargs.get(u'address', '')
    if parts:
        mailto_string = u'%s?%s' % (mailto_string, u'&'.join(parts))

    return mailto_string


def mailto(address, to=None, cc=None, bcc=None, subject=None, body=None,
           attach=None):
    """
    Send an e-mail using the user's preferred composer.

    Open the user's preferred e-mail composer in order to send a mail to
    address(es) that must follow the syntax of RFC822. Multiple addresses
    may be provided (for address, cc and bcc parameters) as separate
    arguments.

    All parameters provided are used to prefill corresponding fields in
    the user's e-mail composer. The user will have the opportunity to
    change any of this information before actually sending the e-mail.

    ``address``
        specify the destination recipient

    ``cc``
        specify a recipient to be copied on the e-mail

    ``bcc``
        specify a recipient to be blindly copied on the e-mail

    ``subject``
        specify a subject for the e-mail

    ``body``
        specify a body for the e-mail. Since the user will be able to make
        changes before actually sending the e-mail, this can be used to provide
        the user with a template for the e-mail text may contain linebreaks

    ``attach``
        specify an attachment for the e-mail. file must point to an existing
        file
    """

    mailto_string = mailto_format(**locals())
    return open(mailto_string)

