# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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
Module implementing BookNameForm.
"""
import logging

from PyQt4.QtGui import QDialog

from openlp.core.lib import translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.plugins.bibles.forms.booknamedialog import \
    Ui_BookNameDialog
from openlp.plugins.bibles.lib.db import BiblesResourcesDB

log = logging.getLogger(__name__)

class BookNameForm(QDialog, Ui_BookNameDialog):
    """
    Class to manage a dialog which help the user to refer a book name a 
    to a english book name
    """
    log.info(u'BookNameForm loaded')
    
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)

    def exec_(self, name):
        items = []
        self.requestComboBox.addItem(u'')
        self.requestLabel.setText(
            translate('BiblesPlugin.BookNameForm', name))
        items = BiblesResourcesDB.get_books()
        for item in items:
            self.requestComboBox.addItem(item[u'name'])
        return QDialog.exec_(self)
    
    def accept(self):
        if self.requestComboBox.currentText() == u'':
            critical_error_message_box(
                message=translate('BiblesPlugin.BookNameForm',
                'You need to choose a book.'))
            self.requestComboBox.setFocus()
            return False
        else:
            return QDialog.accept(self)
