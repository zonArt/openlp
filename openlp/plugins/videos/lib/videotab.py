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

from PyQt4 import QtCore, QtGui

from openlp.core import translate
from openlp.core.lib import SettingsTab
from openlp.core.resources import *

class VideoTab(SettingsTab):
    """
    VideoTab is the video settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, u'Video')

    def setupUi(self):
        self.setObjectName(u'VideoTab')

        self.VideoLayout = QtGui.QFormLayout(self)
        self.VideoLayout.setObjectName("VideoLayout")

        self.VideoModeGroupBox = QtGui.QGroupBox(self)
        self.VideoModeGroupBox.setObjectName("VideoModeGroupBox")
        self.VideoModeLayout = QtGui.QVBoxLayout(self.VideoModeGroupBox)
        self.VideoModeLayout.setSpacing(8)
        self.VideoModeLayout.setMargin(8)
        self.VideoModeLayout.setObjectName("VideoModeLayout")
        self.UseVMRCheckBox = QtGui.QCheckBox(self.VideoModeGroupBox)
        self.UseVMRCheckBox.setObjectName("UseVMRCheckBox")
        self.VideoModeLayout.addWidget(self.UseVMRCheckBox)
        self.UseVMRLabel = QtGui.QLabel(self.VideoModeGroupBox)
        self.UseVMRLabel.setObjectName("UseVMRLabel")
        self.VideoModeLayout.addWidget(self.UseVMRLabel)
        
        self.VideoLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.VideoModeGroupBox)
        
        QtCore.QObject.connect(self.UseVMRCheckBox,\
                               QtCore.SIGNAL("stateChanged(int)"), self.onVMRCheckBoxchanged)             
        
    def retranslateUi(self):
        self.VideoModeGroupBox.setTitle(translate("SettingsForm", "Video Mode"))
        self.UseVMRCheckBox.setText(translate("SettingsForm", "Use Video Mode Rendering"))
        self.UseVMRLabel.setText(translate("SettingsForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">No video preview available with VMR enabled</span></p></body></html>"))

    def onVMRCheckBoxchanged(self):
        mode_layout = self.UseVMRCheckBox.checkState()
        self.mode_layout = False
        if mode_layout == 2: # we have a set value convert to True/False
            self.mode_layout = True
    
    def load(self):
        mode_layout = self.config.get_config("use mode layout",u"0" )
        self.mode_layout = True
        # used for first time initialisation
        # mode_layout will be a string with True/False so need to fix and make boolean
        if mode_layout == '0'or mode_layout == "False":   
            self.mode_layout = False
        else:
            self.UseVMRCheckBox.setChecked(True)
        
    def save(self):
        self.config.set_config("use mode layout", str(self.mode_layout))        
