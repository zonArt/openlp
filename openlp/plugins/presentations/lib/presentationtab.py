# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

from PyQt4 import Qt, QtCore, QtGui

from openlp.core.lib import SettingsTab, translate

class PresentationTab(SettingsTab):
    """
    PresentationsTab is the Presentations settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, translate(u'PresentationTab', u'Presentation'), u'Presentation')

    def setupUi(self):
        self.setObjectName(u'PresentationTab')
        self.PresentationLayout = QtGui.QHBoxLayout(self)
        self.PresentationLayout.setSpacing(8)
        self.PresentationLayout.setMargin(8)
        self.PresentationLayout.setObjectName(u'PresentationLayout')
        self.PresentationLeftWidget = QtGui.QWidget(self)
        self.PresentationLeftWidget.setObjectName(u'PresentationLeftWidget')
        self.PresentationLeftLayout = QtGui.QVBoxLayout(self.PresentationLeftWidget)
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
        self.PowerpointCheckBox.setObjectName("PowerpointCheckBox")
        self.VerseDisplayLayout.addWidget(self.PowerpointCheckBox, 0, 0, 1, 1)

        self.PowerpointPath = QtGui.QLineEdit(self.VerseDisplayGroupBox)
        self.PowerpointPath.setObjectName("PowerpointPath")
        self.VerseDisplayLayout.addWidget(self.PowerpointPath, 1, 0, 1, 1)

        self.ImpressCheckBox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
        self.ImpressCheckBox.setObjectName("ImpressCheckBox")
        self.VerseDisplayLayout.addWidget(self.ImpressCheckBox, 2, 0, 1, 1)

        self.ImpressPath = QtGui.QLineEdit(self.VerseDisplayGroupBox)
        self.ImpressPath.setObjectName("ImpressPath")
        self.VerseDisplayLayout.addWidget(self.ImpressPath, 3, 0, 1, 1)

        self.PresentationThemeWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.PresentationThemeWidget.setObjectName(u'PresentationThemeWidget')
        self.PresentationThemeLayout = QtGui.QHBoxLayout(self.PresentationThemeWidget)
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
        self.PresentationRightLayout = QtGui.QVBoxLayout(self.PresentationRightWidget)
        self.PresentationRightLayout.setObjectName(u'PresentationRightLayout')
        self.PresentationRightLayout.setSpacing(8)
        self.PresentationRightLayout.setMargin(0)
        self.PresentationRightSpacer = QtGui.QSpacerItem(50, 20,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.PresentationRightLayout.addItem(self.PresentationRightSpacer)
        self.PresentationLayout.addWidget(self.PresentationRightWidget)

        # Signals and slots
        #QtCore.QObject.connect(self.NewChaptersCheckBox,
           # QtCore.SIGNAL("stateChanged(int)"), self.onNewChaptersCheckBoxChanged)

    def retranslateUi(self):
        self.PowerpointCheckBox.setText(translate('PresentationTab', 'Powerpoint available:'))
        self.ImpressCheckBox.setText(translate('PresentationTab', 'Impress available:'))
        self.PowerpointPath.setText(u'powerpoint.exe ')
        self.ImpressPath.setText(u'openoffice.org -nologo -show ')

    def onNewChaptersCheckBoxChanged(self):
        check_state = self.NewChaptersCheckBox.checkState()
        self.show_new_chapters = False
        if check_state == 2: # we have a set value convert to True/False
            self.show_new_chapters = True


    def load(self):
        pass
#        self.paragraph_style = (self.config.get_config(u'paragraph style', u'True'))
#        self.show_new_chapters = (self.config.get_config(u'display new chapter', u"False"))
#        self.display_style = int(self.config.get_config(u'display brackets', u'0'))
#        self.Presentation_theme = int(self.config.get_config(u'Presentation theme', u'0'))
#        self.Presentation_search = (self.config.get_config(u'search as type', u'True'))
#        if self.paragraph_style:
#            self.ParagraphRadioButton.setChecked(True)
#        else:
#            self.VerseRadioButton.setChecked(True)
#        self.NewChaptersCheckBox.setChecked(self.show_new_chapters)
#        self.DisplayStyleComboBox.setCurrentIndex(self.display_style)
#        self.PresentationSearchCheckBox.setChecked(self.Presentation_search)

    def save(self):
        pass
#        self.config.set_config(u'paragraph style', str(self.paragraph_style))
#        self.config.set_config(u'display new chapter', str(self.show_new_chapters))
#        self.config.set_config(u'display brackets', str(self.display_style))
#        self.config.set_config(u'search as type', str(self.Presentation_search))
#        self.config.set_config(u'Presentation theme', str(self.Presentation_theme))
