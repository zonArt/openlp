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

from openlp.core.lib import SettingsTab,  str_to_bool,  translate

class MediaTab(SettingsTab):
    """
    mediaTab is the media settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, translate(u'MediaTab', u'Media'), u'Media')

    def setupUi(self):
        self.setObjectName(u'MediaTab')
        self.MediaLayout = QtGui.QFormLayout(self)
        self.MediaLayout.setObjectName(u'MediaLayout')
        self.MediaModeGroupBox = QtGui.QGroupBox(self)
        self.MediaModeGroupBox.setObjectName(u'MediaModeGroupBox')
        self.MediaModeLayout = QtGui.QVBoxLayout(self.MediaModeGroupBox)
        self.MediaModeLayout.setSpacing(8)
        self.MediaModeLayout.setMargin(8)
        self.MediaModeLayout.setObjectName(u'MediaModeLayout')
        self.UseVMRCheckBox = QtGui.QCheckBox(self.MediaModeGroupBox)
        self.UseVMRCheckBox.setObjectName(u'UseVMRCheckBox')
        self.MediaModeLayout.addWidget(self.UseVMRCheckBox)
        self.UseVMRLabel = QtGui.QLabel(self.MediaModeGroupBox)
        self.UseVMRLabel.setObjectName(u'UseVMRLabel')
        self.MediaModeLayout.addWidget(self.UseVMRLabel)

        self.MediaLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.MediaModeGroupBox)
        # Signals and slots
        QtCore.QObject.connect(self.UseVMRCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onVMRCheckBoxChanged)

    def retranslateUi(self):
        self.MediaModeGroupBox.setTitle(translate(u'MediaTab', u'Media Mode'))
        self.UseVMRCheckBox.setText(translate(u'MediaTab', u'Use Video Mode Rendering'))
        self.UseVMRLabel.setText(translate(u'MediaTab', u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            u'<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            u'p, li { white-space: pre-wrap; }\n'
            u'</style></head><body style="font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;">\n'
            u'<p style="margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-style:italic;">No video preview available with VMR enabled</span></p></body></html>'))

    def onVMRCheckBoxChanged(self):
        use_vmr_mode = self.UseVMRCheckBox.checkState()
        self.use_vmr_mode = False
        if use_vmr_mode == 2:
            # we have a set value convert to True/False
            self.use_vmr_mode = True

    def load(self):
        self.use_vmr_mode = str_to_bool(self.config.get_config(u'use mode layout', u'False'))
        if self.use_vmr_mode :
            self.UseVMRCheckBox.setChecked(True)

    def save(self):
        self.config.set_config(u'use mode layout', unicode(self.use_vmr_mode))