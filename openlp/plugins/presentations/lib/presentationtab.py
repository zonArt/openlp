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
    BiblesTab is the Bibles settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, u'Presentation')

    def setupUi(self):
        self.setObjectName(u'BiblesTab')
        self.BibleLayout = QtGui.QHBoxLayout(self)
        self.BibleLayout.setSpacing(8)
        self.BibleLayout.setMargin(8)
        self.BibleLayout.setObjectName(u'BibleLayout')
        self.BibleLeftWidget = QtGui.QWidget(self)
        self.BibleLeftWidget.setObjectName(u'BibleLeftWidget')
        self.BibleLeftLayout = QtGui.QVBoxLayout(self.BibleLeftWidget)
        self.BibleLeftLayout.setObjectName(u'BibleLeftLayout')
        self.BibleLeftLayout.setSpacing(8)
        self.BibleLeftLayout.setMargin(0)

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

        self.BibleThemeWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.BibleThemeWidget.setObjectName(u'BibleThemeWidget')
        self.BibleThemeLayout = QtGui.QHBoxLayout(self.BibleThemeWidget)
        self.BibleThemeLayout.setSpacing(8)
        self.BibleThemeLayout.setMargin(0)
        self.BibleThemeLayout.setObjectName(u'BibleThemeLayout')

        self.BibleLeftLayout.addWidget(self.VerseDisplayGroupBox)
        self.BibleLeftSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.BibleLeftLayout.addItem(self.BibleLeftSpacer)
        self.BibleLayout.addWidget(self.BibleLeftWidget)

        self.BibleRightWidget = QtGui.QWidget(self)
        self.BibleRightWidget.setObjectName(u'BibleRightWidget')
        self.BibleRightLayout = QtGui.QVBoxLayout(self.BibleRightWidget)
        self.BibleRightLayout.setObjectName(u'BibleRightLayout')
        self.BibleRightLayout.setSpacing(8)
        self.BibleRightLayout.setMargin(0)
        self.BibleRightSpacer = QtGui.QSpacerItem(50, 20,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.BibleRightLayout.addItem(self.BibleRightSpacer)
        self.BibleLayout.addWidget(self.BibleRightWidget)

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
#        self.bible_theme = int(self.config.get_config(u'bible theme', u'0'))
#        self.bible_search = (self.config.get_config(u'search as type', u'True'))
#        if self.paragraph_style:
#            self.ParagraphRadioButton.setChecked(True)
#        else:
#            self.VerseRadioButton.setChecked(True)
#        self.NewChaptersCheckBox.setChecked(self.show_new_chapters)
#        self.DisplayStyleComboBox.setCurrentIndex(self.display_style)
#        self.BibleSearchCheckBox.setChecked(self.bible_search)

    def save(self):
        pass
#        self.config.set_config(u'paragraph style', str(self.paragraph_style))
#        self.config.set_config(u'display new chapter', str(self.show_new_chapters))
#        self.config.set_config(u'display brackets', str(self.display_style))
#        self.config.set_config(u'search as type', str(self.bible_search))
#        self.config.set_config(u'bible theme', str(self.bible_theme))
