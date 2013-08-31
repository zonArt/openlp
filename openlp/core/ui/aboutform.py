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
The About dialog.
"""

from PyQt4 import QtCore, QtGui

from .aboutdialog import Ui_AboutDialog
from openlp.core.lib import translate
from openlp.core.utils import get_application_version


class AboutForm(QtGui.QDialog, Ui_AboutDialog):
    """
    The About dialog
    """

    def __init__(self, parent):
        """
        Do some initialisation stuff
        """
        super(AboutForm, self).__init__(parent)
        application_version = get_application_version()
        self.setupUi(self)
        about_text = self.about_text_edit.toPlainText()
        about_text = about_text.replace('<version>', application_version['version'])
        if application_version['build']:
            build_text = translate('OpenLP.AboutForm', ' build %s') % application_version['build']
        else:
            build_text = ''
        about_text = about_text.replace('<revision>', build_text)
        self.about_text_edit.setPlainText(about_text)
        self.volunteer_button.clicked.connect(self.on_volunteer_button_clicked)

    def on_volunteer_button_clicked(self):
        """
        Launch a web browser and go to the contribute page on the site.
        """
        import webbrowser
        webbrowser.open_new('http://openlp.org/en/contribute')
