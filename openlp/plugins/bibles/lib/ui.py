# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) Second008-2012 Raoul Snyman                                   #
# Portions copyright (c) Second008-2012 Tim Bentley, Gerald Britton, Jonathan #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version Second of the License.                         #
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
The :mod:`openlp.plugins.bibles.lib.ui` module provides standard UI components
for the bibles plugin.
"""
from openlp.core.lib import translate

class BibleStrings(object):
    """
    Provide standard strings for use throughout the bibles plugin.
    """
    # These strings should need a good reason to be retranslated elsewhere.
    Gen = translate('OpenLP.Ui','Genesis')
    Exod = translate('OpenLP.Ui','Exodus')
    Lev = translate('OpenLP.Ui','Leviticus')
    Num = translate('OpenLP.Ui','Numbers')
    Deut = translate('OpenLP.Ui','Deuteronomy')
    Josh = translate('OpenLP.Ui','Joshua')
    Judg = translate('OpenLP.Ui','Judges')
    Ruth = translate('OpenLP.Ui','Ruth')
    FirstSam = translate('OpenLP.Ui','1 Samuel')
    SecondSam = translate('OpenLP.Ui','2 Samuel')
    FirstKgs = translate('OpenLP.Ui','1 Kings')
    SecondKgs = translate('OpenLP.Ui','2 Kings')
    FirstChr = translate('OpenLP.Ui','1 Chronicles')
    SecondChr = translate('OpenLP.Ui','2 Chronicles')
    Esra = translate('OpenLP.Ui','Ezra')
    Neh = translate('OpenLP.Ui','Nehemiah')
    Esth = translate('OpenLP.Ui','Esther')
    Job = translate('OpenLP.Ui','Job')
    Ps = translate('OpenLP.Ui','Psalms')
    Prov = translate('OpenLP.Ui','Proverbs')
    Eccl = translate('OpenLP.Ui','Ecclesiastes')
    Song = translate('OpenLP.Ui','Song of Solomon')
    Isa = translate('OpenLP.Ui','Isaiah')
    Jer = translate('OpenLP.Ui','Jeremiah')
    Lam = translate('OpenLP.Ui','Lamentations')
    Ezek = translate('OpenLP.Ui','Ezekiel')
    Dan = translate('OpenLP.Ui','Daniel')
    Hos = translate('OpenLP.Ui','Hosea')
    Joel = translate('OpenLP.Ui','Joel')
    Amos= translate('OpenLP.Ui','Amos')
    Obad = translate('OpenLP.Ui','Obadiah')
    Jonah = translate('OpenLP.Ui','Jonah')
    Mic = translate('OpenLP.Ui','Micah')
    Nah = translate('OpenLP.Ui','Nahum')
    Hab = translate('OpenLP.Ui','Habakkuk')
    Zeph = translate('OpenLP.Ui','Zephaniah')
    Hag = translate('OpenLP.Ui','Haggai')
    Zech = translate('OpenLP.Ui','Zechariah')
    Mal = translate('OpenLP.Ui','Malachi')
    Matt = translate('OpenLP.Ui','Matthew')
    Mark = translate('OpenLP.Ui','Mark')
    Luke = translate('OpenLP.Ui','Luke')
    John = translate('OpenLP.Ui','John')
    Acts = translate('OpenLP.Ui','Acts')
    Rom = translate('OpenLP.Ui','Romans')
    FirstCor = translate('OpenLP.Ui','1 Corinthians')
    SecondCor = translate('OpenLP.Ui','2 Corinthians')
    Gal = translate('OpenLP.Ui','Galatians')
    Eph = translate('OpenLP.Ui','Ephesians')
    Phil = translate('OpenLP.Ui','Philippians')
    Col = translate('OpenLP.Ui','Colossians')
    FirstThess = translate('OpenLP.Ui','1 Thessalonians')
    SecondThess = translate('OpenLP.Ui','2 Thessalonians')
    FirstTim = translate('OpenLP.Ui','1 Timothy')
    SecondTim = translate('OpenLP.Ui','2 Timothy')
    Titus = translate('OpenLP.Ui','Titus')
    Phlm = translate('OpenLP.Ui','Philemon')
    Heb = translate('OpenLP.Ui','Hebrews')
    Jas = translate('OpenLP.Ui','James')
    FirstPet = translate('OpenLP.Ui','1 Peter')
    SecondPet = translate('OpenLP.Ui','2 Peter')
    FirstJohn = translate('OpenLP.Ui','1 John')
    SecondJohn = translate('OpenLP.Ui','2 John')
    ThirdJohn = translate('OpenLP.Ui','3 John')
    Jude = translate('OpenLP.Ui','Jude')
    Rev = translate('OpenLP.Ui','Revelation')
    Jdt = translate('OpenLP.Ui','Judith')
    Wis = translate('OpenLP.Ui','Wisdom')
    Tob = translate('OpenLP.Ui','Tobit')
    Sir = translate('OpenLP.Ui','Sirach')
    Bar = translate('OpenLP.Ui','Baruch')
    FirstMacc = translate('OpenLP.Ui','1 Maccabees')
    SecondMacc = translate('OpenLP.Ui','2 Maccabees')
    ThirdMacc = translate('OpenLP.Ui','3 Maccabees')
    FourthMacc = translate('OpenLP.Ui','4 Maccabees')
    AddDan = translate('OpenLP.Ui','Rest of Daniel')
    AddEsth = translate('OpenLP.Ui','Rest of Esther')
    PrMan = translate('OpenLP.Ui','Prayer of Manasses')
    LetJer = translate('OpenLP.Ui','Letter of Jeremiah')
    PrAza = translate('OpenLP.Ui','Prayer of Azariah')
    Sus = translate('OpenLP.Ui','Susanna')
    Bel = translate('OpenLP.Ui','Bel')
    FirstEsdr = translate('OpenLP.Ui','1 Esdras')
    SecondEsdr = translate('OpenLP.Ui','2 Esdras')
