# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from PyQt4 import QtCore, QtGui
from openlp.core.lib import translate

class Ui_TopicsDialog(object):
    def setupUi(self, TopicsDialog):
        TopicsDialog.setObjectName(u'TopicsDialog')
        TopicsDialog.resize(365, 77)
        self.TopicLayout = QtGui.QFormLayout(TopicsDialog)
        self.TopicLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.TopicLayout.setMargin(8)
        self.TopicLayout.setSpacing(8)
        self.TopicLayout.setObjectName(u'TopicLayout')
        self.NameLabel = QtGui.QLabel(TopicsDialog)
        self.NameLabel.setObjectName(u'NameLabel')
        self.TopicLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.NameLabel)
        self.NameEdit = QtGui.QLineEdit(TopicsDialog)
        self.NameEdit.setObjectName(u'NameEdit')
        self.TopicLayout.setWidget(0,
            QtGui.QFormLayout.FieldRole, self.NameEdit)
        self.TopicButtonBox = QtGui.QDialogButtonBox(TopicsDialog)
        self.TopicButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.TopicButtonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Cancel)
        self.TopicButtonBox.setObjectName(u'TopicButtonBox')
        self.TopicLayout.setWidget(1,
            QtGui.QFormLayout.FieldRole, self.TopicButtonBox)

        self.retranslateUi(TopicsDialog)
        QtCore.QObject.connect(self.TopicButtonBox,
            QtCore.SIGNAL(u'accepted()'), TopicsDialog.accept)
        QtCore.QObject.connect(self.TopicButtonBox,
            QtCore.SIGNAL(u'rejected()'), TopicsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TopicsDialog)

    def retranslateUi(self, TopicsDialog):
        TopicsDialog.setWindowTitle(translate('TopicsForm', 'Topic Maintenance'))
        self.NameLabel.setText(translate('TopicsForm', 'Topic name:'))
