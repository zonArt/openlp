# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
Base directory for tests
"""
import sys
from PyQt5 import QtWidgets

if sys.version_info[1] >= 3:
    from unittest.mock import ANY, MagicMock, patch, mock_open, call, PropertyMock
else:
    from mock import ANY, MagicMock, patch, mock_open, call, PropertyMock

# Only one QApplication can be created. Use QtWidgets.QApplication.instance() when you need to "create" a  QApplication.
application = QtWidgets.QApplication([])
application.setApplicationName('OpenLP')

__all__ = ['ANY', 'MagicMock', 'patch', 'mock_open', 'call', 'application', 'PropertyMock']
