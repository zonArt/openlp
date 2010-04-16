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

import logging

from PyQt4 import QtCore, QtGui
import os
from openlp.core.utils import AppLocation, ConfigHelper
#from openlp.core.ui import MainWindow
#import i18n_rc

class LanguageManager(object):
    """
        Helper for Language selection
    """
    __qmList__ = None
    __AutoLanguage__ = None
    
    @staticmethod
    def getTranslator(language):
        if LanguageManager.__AutoLanguage__ is True:
            language = QtCore.QLocale.system().name()
        lang_Path = AppLocation.get_directory(AppLocation.AppDir)
        lang_Path = os.path.join(lang_Path, u'resources', u'i18n')
        appTranslator = QtCore.QTranslator()
        if appTranslator.load("openlp_" + language, lang_Path):
            return appTranslator

    @staticmethod
    def findQmFiles():
        trans_dir = AppLocation.get_directory(AppLocation.AppDir)
        trans_dir = QtCore.QDir(os.path.join(trans_dir, u'resources', u'i18n'))
        fileNames = trans_dir.entryList(QtCore.QStringList("*.qm"),
                QtCore.QDir.Files, QtCore.QDir.Name)
        for i in fileNames:
            fileNames.replaceInStrings(i, trans_dir.filePath(i))
        return fileNames

    @staticmethod
    def languageName(qmFile):
        translator = QtCore.QTranslator() 
        translator.load(qmFile)

        return translator.translate(u'MainWindow', u'English')

    @staticmethod
    def getLanguage():
        language = ConfigHelper.get_registry().get_value(u'general', u'language', u'[en]')
        print "getLanguage %s" % language
        regEx = QtCore.QRegExp("^\[(.*)\]")
        if regEx.exactMatch(language):
            LanguageManager.__AutoLanguage__ = True
            language = regEx.cap(1)
        return language

    @staticmethod
    def setLanguage(action):
        actionName = u'%s' % action.objectName()
        qmList = LanguageManager.getQmList()
        if LanguageManager.__AutoLanguage__ == True:
            language = u'[%s]' % qmList[actionName]
        else:
            language = u'%s' % qmList[actionName]
        print "setLanguage: %s" % language
        ConfigHelper.set_config(u'general', u'language', language)
        QtGui.QMessageBox.information(None, 
                    u'Language', u'After restart new Language settings will be used.')

    @staticmethod
    def initQmList():
        LanguageManager.__qmList__ = {}
        qmFiles = LanguageManager.findQmFiles()
        for i, qmf in enumerate(qmFiles):
            regEx = QtCore.QRegExp("^.*openlp_(.*).qm")
            if regEx.exactMatch(qmf):
                langName = regEx.cap(1)
                LanguageManager.__qmList__[u'%i %s' % (i, LanguageManager.languageName(qmf))] = langName 

    @staticmethod
    def getQmList():
        if LanguageManager.__qmList__ == None:
            LanguageManager.initQmList()
        return LanguageManager.__qmList__

