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
Provide Error Handling and login Services
"""
import logging
import inspect

from openlp.core.common import trace_error_handler
DO_NOT_TRACE_EVENTS = ['timerEvent', 'paintEvent']


class OpenLPMixin(object):
    """
    Base Calling object for OpenLP classes.
    """
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__module__)
        for name, m in inspect.getmembers(self, inspect.ismethod):
            if name not in DO_NOT_TRACE_EVENTS:
                if not name.startswith("_") and not name.startswith("log_"):
                    setattr(self, name, self.logging_wrapper(m, self))

    def logging_wrapper(self, func, parent):
        """
        Code to added debug wrapper to work on called functions within a decorated class.
        """
        def wrapped(*args, **kwargs):
            if parent.logger.getEffectiveLevel() == logging.DEBUG:
                parent.logger.debug("Entering %s" % func.__name__)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if parent.logger.getEffectiveLevel() <= logging.ERROR:
                    parent.logger.error('Exception in %s : %s' % (func.__name__, e))
                raise e
        return wrapped

    def log_debug(self, message):
        """
        Common log debug handler which prints the calling path
        """
        self.logger.debug(message)

    def log_info(self, message):
        """
        Common log info handler which prints the calling path
        """
        self.logger.info(message)

    def log_error(self, message):
        """
        Common log error handler which prints the calling path
        """
        trace_error_handler(self.logger)
        self.logger.error(message)

    def log_exception(self, message):
        """
        Common log exception handler which prints the calling path
        """
        trace_error_handler(self.logger)
        self.logger.exception(message)