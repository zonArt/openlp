# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
Provide Registry Services
"""
from openlp.core.common import Registry, de_hump


class RegistryMixin(object):
    """
    This adds registry components to classes to use at run time.
    """
    def __init__(self, parent):
        """
        Register the class and bootstrap hooks.
        """
        print("RegistryMixin - before super ", self.__class__.__name__)
        try:
            super(RegistryMixin, self).__init__(parent)
        except TypeError:
            super(RegistryMixin, self).__init__()
        print("RegistryMixin - after super")
        Registry().register(de_hump(self.__class__.__name__), self)
        Registry().register_function('bootstrap_initialise', self.bootstrap_initialise)
        Registry().register_function('bootstrap_post_set_up', self.bootstrap_post_set_up)

    def bootstrap_initialise(self):
        """
        Dummy method to be overridden
        """
        pass

    def bootstrap_post_set_up(self):
        """
        Dummy method to be overridden
        """
        pass
