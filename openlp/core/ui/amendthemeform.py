# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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
import logging

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QColor, QFont
from openlp.core.lib import ThemeXML
from openlp.core import Renderer

from amendthemedialog import Ui_AmendThemeDialog

log = logging.getLogger(u'AmendThemeForm')

class AmendThemeForm(QtGui.QDialog,  Ui_AmendThemeDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def loadTheme(self, theme):
        if theme == None:
            theme = self.baseTheme()
        else:
            pass
        self.generateImage(theme)

    def baseTheme(self):
        log.debug(u'base Theme')
        newtheme = ThemeXML()
        newtheme.new_document(u'New Theme')
        newtheme.add_background_solid(str(u'#000000'))
        newtheme.add_font(str(QFont().family()), str(u'#FFFFFF'), str(30), u'False')
        newtheme.add_font(str(QFont().family()), str(u'#FFFFFF'), str(12), u'False', u'footer')
        newtheme.add_display(str(False), str(u'#FFFFFF'), str(False), str(u'#FFFFFF'),
            str(0), str(0), str(0))
        return newtheme.extract_xml()

    def generateImage(self, theme_xml):
        log.debug(u'generateImage %s ',  theme_xml)
        theme = ThemeXML()
        theme.parse(theme_xml)
        #print theme
        size=QtCore.QSize(800,600)
        frame=TstFrame(size)
        frame=frame
        paintdest=frame.GetPixmap()
        r=Renderer()
        r.set_paint_dest(paintdest)

        r.set_theme(theme) # set default theme
        r._render_background()
        r.set_text_rectangle(QtCore.QRect(0,0, size.width()-1, size.height()-1), QtCore.QRect(10,560, size.width()-1, size.height()-1))

        lines=[]
        lines.append(u'Amazing Grace!')
        lines.append(u'How sweet the sound')
        lines.append(u'To save a wretch like me;')
        lines.append(u'I once was lost but now am found,')
        lines.append(u'Was blind, but now I see.')
        lines1=[]
        lines1.append(u'Amazing Grace (John Newton)' )
        lines1.append(u'CCLI xxx (c)Openlp.org')

        answer=r._render_lines(lines, lines1)

        self.ThemePreview.setPixmap(frame.GetPixmap())

class TstFrame:
    def __init__(self, size):
        """Create the DemoPanel."""
        self.width=size.width();
        self.height=size.height();
        # create something to be painted into
        self._Buffer = QtGui.QPixmap(self.width, self.height)
    def GetPixmap(self):
        return self._Buffer
