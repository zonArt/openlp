# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The :mod:`uistrings` module provides standard strings for OpenLP.
"""
import logging

from openlp.core.lib import translate


log = logging.getLogger(__name__)


class UiStrings(object):
    """
    Provide standard strings for objects to use.
    """
    __instance__ = None

    def __new__(cls):
        """
        Override the default object creation method to return a single instance.
        """
        if not cls.__instance__:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        """
        These strings should need a good reason to be retranslated elsewhere.
        Should some/more/less of these have an &amp; attached?
        """
        self.About = translate('OpenLP.Ui', 'About')
        self.Add = translate('OpenLP.Ui', '&Add')
        self.Advanced = translate('OpenLP.Ui', 'Advanced')
        self.AllFiles = translate('OpenLP.Ui', 'All Files')
        self.Automatic = translate('OpenLP.Ui', 'Automatic')
        self.BackgroundColor = translate('OpenLP.Ui', 'Background Color')
        self.Bottom = translate('OpenLP.Ui', 'Bottom')
        self.Browse = translate('OpenLP.Ui', 'Browse...')
        self.Cancel = translate('OpenLP.Ui', 'Cancel')
        self.CCLINumberLabel = translate('OpenLP.Ui', 'CCLI number:')
        self.CreateService = translate('OpenLP.Ui', 'Create a new service.')
        self.ConfirmDelete = translate('OpenLP.Ui', 'Confirm Delete')
        self.Continuous = translate('OpenLP.Ui', 'Continuous')
        self.Default = translate('OpenLP.Ui', 'Default')
        self.DefaultColor = translate('OpenLP.Ui', 'Default Color:')
        self.DefaultServiceName = translate('OpenLP.Ui', 'Service %Y-%m-%d %H-%M',
            'This may not contain any of the following characters: /\\?*|<>\[\]":+\n'
            'See http://docs.python.org/library/datetime.html#strftime-strptime-behavior for more information.')
        self.Delete = translate('OpenLP.Ui', '&Delete')
        self.DisplayStyle = translate('OpenLP.Ui', 'Display style:')
        self.Duplicate = translate('OpenLP.Ui', 'Duplicate Error')
        self.Edit = translate('OpenLP.Ui', '&Edit')
        self.EmptyField = translate('OpenLP.Ui', 'Empty Field')
        self.Error = translate('OpenLP.Ui', 'Error')
        self.Export = translate('OpenLP.Ui', 'Export')
        self.File = translate('OpenLP.Ui', 'File')
        self.FontSizePtUnit = translate('OpenLP.Ui', 'pt', 'Abbreviated font pointsize unit')
        self.Help = translate('OpenLP.Ui', 'Help')
        self.Hours = translate('OpenLP.Ui', 'h', 'The abbreviated unit for hours')
        self.IFdSs = translate('OpenLP.Ui', 'Invalid Folder Selected', 'Singular')
        self.IFSs = translate('OpenLP.Ui', 'Invalid File Selected', 'Singular')
        self.IFSp = translate('OpenLP.Ui', 'Invalid Files Selected', 'Plural')
        self.Image = translate('OpenLP.Ui', 'Image')
        self.Import = translate('OpenLP.Ui', 'Import')
        self.LayoutStyle = translate('OpenLP.Ui', 'Layout style:')
        self.Live = translate('OpenLP.Ui', 'Live')
        self.LiveBGError = translate('OpenLP.Ui', 'Live Background Error')
        self.LiveToolbar = translate('OpenLP.Ui', 'Live Toolbar')
        self.Load = translate('OpenLP.Ui', 'Load')
        self.Minutes = translate('OpenLP.Ui', 'm', 'The abbreviated unit for minutes')
        self.Middle = translate('OpenLP.Ui', 'Middle')
        self.New = translate('OpenLP.Ui', 'New')
        self.NewService = translate('OpenLP.Ui', 'New Service')
        self.NewTheme = translate('OpenLP.Ui', 'New Theme')
        self.NextTrack = translate('OpenLP.Ui', 'Next Track')
        self.NFdSs = translate('OpenLP.Ui', 'No Folder Selected', 'Singular')
        self.NFSs = translate('OpenLP.Ui', 'No File Selected', 'Singular')
        self.NFSp = translate('OpenLP.Ui', 'No Files Selected', 'Plural')
        self.NISs = translate('OpenLP.Ui', 'No Item Selected', 'Singular')
        self.NISp = translate('OpenLP.Ui', 'No Items Selected', 'Plural')
        self.OLPV1 = translate('OpenLP.Ui', 'openlp.org 1.x')
        self.OLPV2 = translate('OpenLP.Ui', 'OpenLP 2')
        self.OLPV2x = translate('OpenLP.Ui', 'OpenLP 2.1')
        self.OpenLPStart = translate('OpenLP.Ui', 'OpenLP is already running. Do you wish to continue?')
        self.OpenService = translate('OpenLP.Ui', 'Open service.')
        self.PlaySlidesInLoop = translate('OpenLP.Ui', 'Play Slides in Loop')
        self.PlaySlidesToEnd = translate('OpenLP.Ui', 'Play Slides to End')
        self.Preview = translate('OpenLP.Ui', 'Preview')
        self.PrintService = translate('OpenLP.Ui', 'Print Service')
        self.ReplaceBG = translate('OpenLP.Ui', 'Replace Background')
        self.ReplaceLiveBG = translate('OpenLP.Ui', 'Replace live background.')
        self.ResetBG = translate('OpenLP.Ui', 'Reset Background')
        self.ResetLiveBG = translate('OpenLP.Ui', 'Reset live background.')
        self.Seconds = translate('OpenLP.Ui', 's', 'The abbreviated unit for seconds')
        self.SaveAndPreview = translate('OpenLP.Ui', 'Save && Preview')
        self.Search = translate('OpenLP.Ui', 'Search')
        self.SearchThemes = translate('OpenLP.Ui', 'Search Themes...', 'Search bar place holder text ')
        self.SelectDelete = translate('OpenLP.Ui', 'You must select an item to delete.')
        self.SelectEdit = translate('OpenLP.Ui', 'You must select an item to edit.')
        self.Settings = translate('OpenLP.Ui', 'Settings')
        self.SaveService = translate('OpenLP.Ui', 'Save Service')
        self.Service = translate('OpenLP.Ui', 'Service')
        self.Split = translate('OpenLP.Ui', 'Optional &Split')
        self.SplitToolTip = translate('OpenLP.Ui',
            'Split a slide into two only if it does not fit on the screen as one slide.')
        self.StartTimeCode = translate('OpenLP.Ui', 'Start %s')
        self.StopPlaySlidesInLoop = translate('OpenLP.Ui', 'Stop Play Slides in Loop')
        self.StopPlaySlidesToEnd = translate('OpenLP.Ui', 'Stop Play Slides to End')
        self.Theme = translate('OpenLP.Ui', 'Theme', 'Singular')
        self.Themes = translate('OpenLP.Ui', 'Themes', 'Plural')
        self.Tools = translate('OpenLP.Ui', 'Tools')
        self.Top = translate('OpenLP.Ui', 'Top')
        self.UnsupportedFile = translate('OpenLP.Ui', 'Unsupported File')
        self.VersePerSlide = translate('OpenLP.Ui', 'Verse Per Slide')
        self.VersePerLine = translate('OpenLP.Ui', 'Verse Per Line')
        self.Version = translate('OpenLP.Ui', 'Version')
        self.View = translate('OpenLP.Ui', 'View')
        self.ViewMode = translate('OpenLP.Ui', 'View Mode')
