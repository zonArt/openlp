# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
import datetime
import mutagen
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import save_cancel_button_box


class PrintServiceOrderForm(QtGui.QDialog):
    def __init__(self, parent=None):
        """
        Constructor
        """
        self.serviceManager = parent
        QtGui.QDialog.__init__(self, parent)
        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        self.dialogLayout = QtGui.QHBoxLayout(self)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.serviceTitleLayout = QtGui.QHBoxLayout()
        self.serviceTitleLayout.setObjectName(u'serviceTitleLayout')
        self.serviceTitleLabel = QtGui.QLabel(self)
        self.serviceTitleLabel.setObjectName(u'serviceTitleLabel')
        self.serviceTitleLayout.addWidget(self.serviceTitleLabel)
        self.serviceTitleLineEdit = QtGui.QLineEdit(self)
        self.serviceTitleLineEdit.setObjectName(u'serviceTitleLineEdit')
        self.serviceTitleLayout.addWidget(self.serviceTitleLineEdit)
        self.verticalLayout.addLayout(self.serviceTitleLayout)
        self.printSlideTextCheckBox = QtGui.QCheckBox(self)
        self.printSlideTextCheckBox.setObjectName(u'printSlideTextCheckBox')
        self.verticalLayout.addWidget(self.printSlideTextCheckBox)
        self.printNotesCheckBox = QtGui.QCheckBox(self)
        self.printNotesCheckBox.setObjectName(u'printNotesCheckBox')
        self.verticalLayout.addWidget(self.printNotesCheckBox)
        self.metaDataCheckBox = QtGui.QCheckBox(self)
        self.metaDataCheckBox.setObjectName(u'metaDataCheckBox')
        self.verticalLayout.addWidget(self.metaDataCheckBox)
        self.verticalLayout.addWidget(save_cancel_button_box(self))
        self.dialogLayout.addLayout(self.verticalLayout)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(
            translate('OpenLP.PrintServiceOrderForm', 'Print Service Order'))
        self.printSlideTextCheckBox.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Include slide text if avaialbe'))
        self.printNotesCheckBox.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Include service item notes'))
        self.metaDataCheckBox.setText(translate('OpenLP.PrintServiceOrderForm',
            'Include play lenght of media items'))
        self.serviceTitleLabel.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Service Order Title'))

    def serviceOrderText(self):
        """
        """
        if self.serviceTitleLineEdit.text():
            text = u'<h2>%s</h2>' % unicode(self.serviceTitleLineEdit.text())
        else:
            text = u'<h2>%s</h2>' % translate('OpenLP.ServiceManager',
                'Service Order Sheet')
        for item in self.serviceManager.serviceItems:
            item = item[u'service_item']
            # Add the title of the service item.
            text += u'<h4><img src="%s" /> %s</h4>' % (item.icon,
                item.get_display_title())
            # Add slide text of the service item.
            if self.printSlideTextCheckBox.isChecked():
                if item.is_text():
                    # Add the text of the service item.
                    for slide in item.get_frames():
                        text += u'<p>' + slide[u'text'] + u'</p>'
                elif item.is_image():
                    # Add the image names of the service item.
                    text += u'<ol>'
                    for slide in range(len(item.get_frames())):
                        text += u'<li><p>%s</p></li>' % \
                            item.get_frame_title(slide)
                    text += u'</ol>'
                if item.foot_text:
                    # add footer
                    text += u'<p>%s</p>' % item.foot_text
            # Add service items' notes.
            if self.printNotesCheckBox.isChecked():
                if item.notes:
                    text += u'<p><b>%s</b> %s</p>' % (translate(
                        'OpenLP.ServiceManager', 'Notes:'), item.notes)
            # Add play length of media files.
            if item.is_media() and self.metaDataCheckBox.isChecked():
                path = os.path.join(item.get_frames()[0][u'path'],
                    item.get_frames()[0][u'title'])
                if not os.path.isfile(path):
                    continue
                file = mutagen.File(path)
                if file is not None:
                    length = int(file.info.length)
                    text += u'<p><b>%s</b> %s</p>' % (translate(
                        'OpenLP.ServiceManager', u'Playing time:'),
                        unicode(datetime.timedelta(seconds=length)))
        return text
    
    
