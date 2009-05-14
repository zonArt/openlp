"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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
import types
from PyQt4 import QtCore, QtGui

__all__ = ['convertStringToBoolean','buildIcon',]

def convertStringToBoolean(stringvalue):
    return stringvalue.strip().lower() in (u'true', u'yes', u'y')

def buildIcon(icon):
    ButtonIcon = None
    if type(icon) is QtGui.QIcon:
        ButtonIcon = icon
    elif type(icon) is types.StringType or type(icon) is types.UnicodeType:
        ButtonIcon = QtGui.QIcon()
        if icon.startswith(u':/'):
            ButtonIcon.addPixmap(QtGui.QPixmap(icon), QtGui.QIcon.Normal,
                QtGui.QIcon.Off)
        else:
            ButtonIcon.addPixmap(QtGui.QPixmap.fromImage(QImage(icon)),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return ButtonIcon
