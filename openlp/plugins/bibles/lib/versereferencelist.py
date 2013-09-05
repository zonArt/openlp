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

class VerseReferenceList(object):
    """
    The VerseReferenceList class encapsulates a list of verse references, but maintains the order in which they were
    added.
    """

    def __init__(self):
        self.verse_list = []
        self.version_list = []
        self.current_index = -1

    def add(self, book, chapter, verse, version, copyright, permission):
        self.add_version(version, copyright, permission)
        if not self.verse_list or self.verse_list[self.current_index]['book'] != book:
            self.verse_list.append({'version': version, 'book': book,
                'chapter': chapter, 'start': verse, 'end': verse})
            self.current_index += 1
        elif self.verse_list[self.current_index]['chapter'] != chapter:
            self.verse_list.append({'version': version, 'book': book,
                'chapter': chapter, 'start': verse, 'end': verse})
            self.current_index += 1
        elif (self.verse_list[self.current_index]['end'] + 1) == verse:
            self.verse_list[self.current_index]['end'] = verse
        else:
            self.verse_list.append({'version': version, 'book': book,
                'chapter': chapter, 'start': verse, 'end': verse})
            self.current_index += 1

    def add_version(self, version, copyright, permission):
        for bible_version in self.version_list:
            if bible_version['version'] == version:
                return
        self.version_list.append({'version': version, 'copyright': copyright, 'permission': permission})

    def format_verses(self):
        result = ''
        for index, verse in enumerate(self.verse_list):
            if index == 0:
                result = '%s %s:%s' % (verse['book'], verse['chapter'], verse['start'])
                if verse['start'] != verse['end']:
                    result = '%s-%s' % (result, verse['end'])
                continue
            prev = index - 1
            if self.verse_list[prev]['version'] != verse['version']:
                result = '%s (%s)' % (result, self.verse_list[prev]['version'])
            result += ', '
            if self.verse_list[prev]['book'] != verse['book']:
                result = '%s%s %s:' % (result, verse['book'], verse['chapter'])
            elif self.verse_list[prev]['chapter'] != verse['chapter']:
                result = '%s%s:' % (result, verse['chapter'])
            result += str(verse['start'])
            if verse['start'] != verse['end']:
                result = '%s-%s' % (result, verse['end'])
        if len(self.version_list) > 1:
            result = '%s (%s)' % (result, verse['version'])
        return result

    def format_versions(self):
        result = ''
        for index, version in enumerate(self.version_list):
            if index > 0:
                if result[-1] not in [';', ',', '.']:
                    result += ';'
                result += ' '
            result = '%s%s, %s' % (result, version['version'], version['copyright'])
            if version['permission'].strip():
                result = result + ', ' + version['permission']
        result = result.rstrip()
        if result.endswith(','):
            return result[:len(result)-1]
        return result
