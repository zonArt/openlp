# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from PyQt4 import QtGui

from openlp.core.lib import SettingsTab, translate

class PresentationTab(SettingsTab):
    """
    PresentationsTab is the Presentations settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self,
            translate(u'PresentationTab', u'Presentation'), u'Presentations')

    def setupUi(self):
        self.setObjectName(u'PresentationTab')
        self.PresentationLayout = QtGui.QHBoxLayout(self)
        self.PresentationLayout.setSpacing(8)
        self.PresentationLayout.setMargin(8)
        self.PresentationLayout.setObjectName(u'PresentationLayout')
        self.PresentationLeftWidget = QtGui.QWidget(self)
        self.PresentationLeftWidget.setObjectName(u'PresentationLeftWidget')
        self.PresentationLeftLayout = QtGui.QVBoxLayout(
            self.PresentationLeftWidget)
        self.PresentationLeftLayout.setObjectName(u'PresentationLeftLayout')
        self.PresentationLeftLayout.setSpacing(8)
        self.PresentationLeftLayout.setMargin(0)
        self.VerseDisplayGroupBox = QtGui.QGroupBox(self)
        self.VerseDisplayGroupBox.setObjectName(u'VerseDisplayGroupBox')
        self.VerseDisplayLayout = QtGui.QGridLayout(self.VerseDisplayGroupBox)
        self.VerseDisplayLayout.setMargin(8)
        self.VerseDisplayLayout.setObjectName(u'VerseDisplayLayout')
        self.VerseTypeWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.VerseTypeWidget.setObjectName(u'VerseTypeWidget')
        self.VerseTypeLayout = QtGui.QHBoxLayout(self.VerseTypeWidget)
        self.VerseTypeLayout.setSpacing(8)
        self.VerseTypeLayout.setMargin(0)
        self.VerseTypeLayout.setObjectName(u'VerseTypeLayout')
        self.PowerpointCheckBox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
        self.PowerpointCheckBox.setTristate(False)
        self.PowerpointCheckBox.setObjectName(u'PowerpointCheckBox')
        self.VerseDisplayLayout.addWidget(self.PowerpointCheckBox, 0, 0, 1, 1)
        self.PowerpointViewerCheckBox = QtGui.QCheckBox(
            self.VerseDisplayGroupBox)
        self.PowerpointViewerCheckBox.setTristate(False)
        self.PowerpointViewerCheckBox.setObjectName(u'PowerpointViewerCheckBox')
        self.VerseDisplayLayout.addWidget(
            self.PowerpointViewerCheckBox, 1, 0, 1, 1)
        self.ImpressCheckBox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
        self.ImpressCheckBox.setTristate(False)
        self.ImpressCheckBox.setObjectName(u'ImpressCheckBox')
        self.VerseDisplayLayout.addWidget(self.ImpressCheckBox, 2, 0, 1, 1)
        self.PresentationThemeWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.PresentationThemeWidget.setObjectName(u'PresentationThemeWidget')
        self.PresentationThemeLayout = QtGui.QHBoxLayout(
            self.PresentationThemeWidget)
        self.PresentationThemeLayout.setSpacing(8)
        self.PresentationThemeLayout.setMargin(0)
        self.PresentationThemeLayout.setObjectName(u'PresentationThemeLayout')
        self.PresentationLeftLayout.addWidget(self.VerseDisplayGroupBox)
        self.PresentationLeftSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.PresentationLeftLayout.addItem(self.PresentationLeftSpacer)
        self.PresentationLayout.addWidget(self.PresentationLeftWidget)
        self.PresentationRightWidget = QtGui.QWidget(self)
        self.PresentationRightWidget.setObjectName(u'PresentationRightWidget')
        self.PresentationRightLayout = QtGui.QVBoxLayout(
            self.PresentationRightWidget)
        self.PresentationRightLayout.setObjectName(u'PresentationRightLayout')
        self.PresentationRightLayout.setSpacing(8)
        self.PresentationRightLayout.setMargin(0)
        self.PresentationRightSpacer = QtGui.QSpacerItem(50, 20,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.PresentationRightLayout.addItem(self.PresentationRightSpacer)
        self.PresentationLayout.addWidget(self.PresentationRightWidget)

    def retranslateUi(self):
        self.PowerpointCheckBox.setText(
            translate(u'PresentationTab', 'Powerpoint available:'))
        self.PowerpointViewerCheckBox.setText(
            translate(u'PresentationTab', 'PowerpointViewer available:'))
        self.ImpressCheckBox.setText(
            translate(u'PresentationTab', 'Impress available:'))

    def load(self):
        self.PowerpointCheckBox.setChecked(
            int(self.config.get_config(u'Powerpoint', 0)))
        self.PowerpointViewerCheckBox.setChecked(
            int(self.config.get_config(u'Powerpoint Viewer', 0)))
        self.ImpressCheckBox.setChecked(
            int(self.config.get_config(u'Impress', 0)))

    def save(self):
        self.config.set_config(
            u'Powerpoint', unicode(self.PowerpointCheckBox.checkState()))
        self.config.set_config(
            u'Powerpoint Viewer',
            unicode(self.PowerpointViewerCheckBox.checkState()))
        self.config.set_config(
            u'Impress', unicode(self.ImpressCheckBox.checkState()))
