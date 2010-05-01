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

from PyQt4 import QtGui, QtCore

from openlp.core.lib import SettingsTab, Receiver

class DisplayTab(SettingsTab):
    """
    Class documentation goes here.
    """
    def __init__(self, screens):
        """
        Constructor
        """
        self.screens = screens
        SettingsTab.__init__(self, u'Display')

    def setupUi(self):
        self.tabTitleVisible = self.trUtf8('Displays')
        self.layoutWidget = QtGui.QWidget(self)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 40, 241, 79))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CurrentGroupBox = QtGui.QGroupBox(self.layoutWidget)
        self.CurrentGroupBox.setObjectName("CurrentGroupBox")
        self.horizontalLayout = QtGui.QHBoxLayout(self.CurrentGroupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.XLabel = QtGui.QLabel(self.CurrentGroupBox)
        self.XLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.XLabel.setObjectName("XLabel")
        self.verticalLayout_6.addWidget(self.XLabel)
        self.Xpos = QtGui.QLabel(self.CurrentGroupBox)
        self.Xpos.setAlignment(QtCore.Qt.AlignCenter)
        self.Xpos.setObjectName("Xpos")
        self.verticalLayout_6.addWidget(self.Xpos)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.YLabel = QtGui.QLabel(self.CurrentGroupBox)
        self.YLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.YLabel.setObjectName("YLabel")
        self.verticalLayout_7.addWidget(self.YLabel)
        self.Ypos = QtGui.QLabel(self.CurrentGroupBox)
        self.Ypos.setAlignment(QtCore.Qt.AlignCenter)
        self.Ypos.setObjectName("Ypos")
        self.verticalLayout_7.addWidget(self.Ypos)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.HeightLabel = QtGui.QLabel(self.CurrentGroupBox)
        self.HeightLabel.setMaximumSize(QtCore.QSize(100, 16777215))
        self.HeightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.HeightLabel.setObjectName("HeightLabel")
        self.verticalLayout_9.addWidget(self.HeightLabel)
        self.Height = QtGui.QLabel(self.CurrentGroupBox)
        self.Height.setAlignment(QtCore.Qt.AlignCenter)
        self.Height.setObjectName("Height")
        self.verticalLayout_9.addWidget(self.Height)
        self.horizontalLayout.addLayout(self.verticalLayout_9)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.WidthLabel = QtGui.QLabel(self.CurrentGroupBox)
        self.WidthLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.WidthLabel.setObjectName("WidthLabel")
        self.verticalLayout_8.addWidget(self.WidthLabel)
        self.Width = QtGui.QLabel(self.CurrentGroupBox)
        self.Width.setAlignment(QtCore.Qt.AlignCenter)
        self.Width.setObjectName("Width")
        self.verticalLayout_8.addWidget(self.Width)
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        self.verticalLayout.addWidget(self.CurrentGroupBox)
        self.CurrentGroupBox_2 = QtGui.QGroupBox(self)
        self.CurrentGroupBox_2.setGeometry(QtCore.QRect(0, 130, 248, 87))
        self.CurrentGroupBox_2.setMaximumSize(QtCore.QSize(500, 16777215))
        self.CurrentGroupBox_2.setObjectName("CurrentGroupBox_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.CurrentGroupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.XAmendLabel = QtGui.QLabel(self.CurrentGroupBox_2)
        self.XAmendLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.XAmendLabel.setObjectName("XAmendLabel")
        self.verticalLayout_2.addWidget(self.XAmendLabel)
        self.XposEdit = QtGui.QLineEdit(self.CurrentGroupBox_2)
        self.XposEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.XposEdit.setMaxLength(4)
        self.XposEdit.setObjectName("XposEdit")
        self.verticalLayout_2.addWidget(self.XposEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.YAmendLabel = QtGui.QLabel(self.CurrentGroupBox_2)
        self.YAmendLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.YAmendLabel.setObjectName("YAmendLabel")
        self.verticalLayout_3.addWidget(self.YAmendLabel)
        self.YposEdit = QtGui.QLineEdit(self.CurrentGroupBox_2)
        self.YposEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.YposEdit.setMaxLength(4)
        self.YposEdit.setObjectName("YposEdit")
        self.verticalLayout_3.addWidget(self.YposEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.HeightAmendLabel = QtGui.QLabel(self.CurrentGroupBox_2)
        self.HeightAmendLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.HeightAmendLabel.setObjectName("HeightAmendLabel")
        self.verticalLayout_4.addWidget(self.HeightAmendLabel)
        self.HeightEdit = QtGui.QLineEdit(self.CurrentGroupBox_2)
        self.HeightEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.HeightEdit.setMaxLength(4)
        self.HeightEdit.setObjectName("HeightEdit")
        self.verticalLayout_4.addWidget(self.HeightEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.WidthAmendLabel = QtGui.QLabel(self.CurrentGroupBox_2)
        self.WidthAmendLabel.setMaximumSize(QtCore.QSize(100, 16777215))
        self.WidthAmendLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.WidthAmendLabel.setObjectName("WidthAmendLabel")
        self.verticalLayout_5.addWidget(self.WidthAmendLabel)
        self.WidthEdit = QtGui.QLineEdit(self.CurrentGroupBox_2)
        self.WidthEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.WidthEdit.setObjectName("WidthEdit")
        self.verticalLayout_5.addWidget(self.WidthEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.OverrideCheckBox = QtGui.QCheckBox(self)
        self.OverrideCheckBox.setGeometry(QtCore.QRect(0, 10, 191, 23))
        self.OverrideCheckBox.setObjectName("OverrideCheckBox")
        QtCore.QMetaObject.connectSlotsByName(self)
        QtCore.QObject.connect(self.OverrideCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onOverrideCheckBoxChanged)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("self", "Amend Display Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.CurrentGroupBox.setTitle(QtGui.QApplication.translate("self", "Default Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.XLabel.setText(QtGui.QApplication.translate("self", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.Xpos.setText(QtGui.QApplication.translate("self", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.YLabel.setText(QtGui.QApplication.translate("self", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.Ypos.setText(QtGui.QApplication.translate("self", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.HeightLabel.setText(QtGui.QApplication.translate("self", "Height", None, QtGui.QApplication.UnicodeUTF8))
        self.Height.setText(QtGui.QApplication.translate("self", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.WidthLabel.setText(QtGui.QApplication.translate("self", "Width", None, QtGui.QApplication.UnicodeUTF8))
        self.Width.setText(QtGui.QApplication.translate("self", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.CurrentGroupBox_2.setTitle(QtGui.QApplication.translate("self", "Amend Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.XAmendLabel.setText(QtGui.QApplication.translate("self", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.YAmendLabel.setText(QtGui.QApplication.translate("self", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.HeightAmendLabel.setText(QtGui.QApplication.translate("self", "Height", None, QtGui.QApplication.UnicodeUTF8))
        self.WidthAmendLabel.setText(QtGui.QApplication.translate("self", "Width", None, QtGui.QApplication.UnicodeUTF8))
        self.OverrideCheckBox.setText(QtGui.QApplication.translate("self", "Override Output Display", None, QtGui.QApplication.UnicodeUTF8))

    def load(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        self.Xpos.setText(unicode(self.screens.current[u'size'].x()))
        self.Ypos.setText(unicode(self.screens.current[u'size'].y()))
        self.Height.setText(unicode(self.screens.current[u'size'].height()))
        self.Width.setText(unicode(self.screens.current[u'size'].width()))
        xpos = settings.value(u'x position',
            QtCore.QVariant(self.screens.current[u'size'].x())).toString()
        self.XposEdit.setText(xpos)
        ypos = settings.value(u'y position',
            QtCore.QVariant(self.screens.current[u'size'].y())).toString()
        self.YposEdit.setText(ypos)
        height =  settings.value(u'height',
            QtCore.QVariant(self.screens.current[u'size'].height())).toString()
        self.HeightEdit.setText(height)
        width = settings.value(u'width',
            QtCore.QVariant(self.screens.current[u'size'].width())).toString()
        self.WidthEdit.setText(width)
        self.amend_display =  settings.value(u'amend display',
            QtCore.QVariant(False)).toBool()
        self.OverrideCheckBox.setChecked(self.amend_display)
        self.amend_display_start = self.amend_display

    def onOverrideCheckBoxChanged(self, check_state):
        self.amend_display = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.amend_display = True

    def save(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        settings.setValue('x position',
            QtCore.QVariant(self.XposEdit.text()))
        settings.setValue('y position',
            QtCore.QVariant(self.YposEdit.text()))
        settings.setValue('height',
            QtCore.QVariant(self.HeightEdit.text()))
        settings.setValue('width',
            QtCore.QVariant(self.WidthEdit.text()))
        settings.setValue('amend display',
            QtCore.QVariant(self.amend_display))
        self.postSetUp()

    def postSetUp(self):
        self.screens.override[u'size'] = QtCore.QRect(int(self.XposEdit.text()),\
            int(self.YposEdit.text()), int(self.WidthEdit.text()),\
            int(self.HeightEdit.text()))
        if self.amend_display:
            self.screens.set_override_display()
        else:
            self.screens.reset_current_display()
        #only trigger event if data has changed in this edit session
        if self.amend_display_start != self.amend_display:
            self.amend_display_start = self.amend_display
            Receiver.send_message(u'config_screen_changed')