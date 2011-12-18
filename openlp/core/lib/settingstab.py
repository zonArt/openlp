# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

class SettingsTab(QtGui.QWidget):
    """
    SettingsTab is a helper widget for plugins to define Tabs for the settings
    dialog.
    """
    def __init__(self, parent, title, visible_title=None, icon_path=None):
        """
        Constructor to create the Settings tab item.

        ``title``
            The title of the tab, which is used internally for the tab handling.

        ``visible_title``
            The title of the tab, which is usually displayed on the tab.
        """
        QtGui.QWidget.__init__(self, parent)
        self.tabTitle = title
        self.tabTitleVisible = visible_title
        self.settingsSection = self.tabTitle.lower()
        if icon_path:
            self.icon_path = icon_path
        self.setupUi()
        self.retranslateUi()
        self.initialise()
        self.load()

    def setupUi(self):
        """
        Setup the tab's interface.
        """
        self.tabLayout = QtGui.QHBoxLayout(self)
        self.tabLayout.setObjectName(u'tabLayout')
        self.leftColumn = QtGui.QWidget(self)
        self.leftColumn.setObjectName(u'leftColumn')
        self.leftLayout = QtGui.QVBoxLayout(self.leftColumn)
        self.leftLayout.setMargin(0)
        self.leftLayout.setObjectName(u'leftLayout')
        self.tabLayout.addWidget(self.leftColumn)
        self.rightColumn = QtGui.QWidget(self)
        self.rightColumn.setObjectName(u'rightColumn')
        self.rightLayout = QtGui.QVBoxLayout(self.rightColumn)
        self.rightLayout.setMargin(0)
        self.rightLayout.setObjectName(u'rightLayout')
        self.tabLayout.addWidget(self.rightColumn)

    def resizeEvent(self, event=None):
        """
        Resize the sides in two equal halves if the layout allows this.
        """
        if event:
            QtGui.QWidget.resizeEvent(self, event)
        width = self.width() - self.tabLayout.spacing() - \
            self.tabLayout.contentsMargins().left() - \
            self.tabLayout.contentsMargins().right()
        left_width = min(width - self.rightColumn.minimumSizeHint().width(),
            width / 2)
        left_width = max(left_width, self.leftColumn.minimumSizeHint().width())
        self.leftColumn.setFixedWidth(left_width)

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        pass

    def initialise(self):
        """
        Do any extra initialisation here.
        """
        pass

    def load(self):
        """
        Load settings from disk.
        """
        pass

    def save(self):
        """
        Save settings to disk.
        """
        pass

    def cancel(self):
        """
        Reset any settings if cancel pressed
        """
        self.load()

    def postSetUp(self, postUpdate=False):
        """
        Changes which need to be made after setup of application

        ``postUpdate``
            Indicates if called before or after updates.

        """
        pass

    def tabVisible(self):
        """
        Tab has just been made visible to the user
        """
        pass
