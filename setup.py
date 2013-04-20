#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Edwin Lunando, Joshua Miller, Stevan Pettit,  #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Simon Scudder, Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon      #
# Tibble, Dave Warnock, Frode Woldsund                                        #
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

from setuptools import setup, find_packages
import re

VERSION_FILE = 'openlp/.version'
SPLIT_ALPHA_DIGITS = re.compile(r'(\d+|\D+)')

def try_int(s):
    """
    Convert string s to an integer if possible. Fail silently and return
    the string as-is if it isn't an integer.

    ``s``
    The string to try to convert.
    """
    try:
        return int(s)
    except Exception:
        return s

def natural_sort_key(s):
    """
    Return a tuple by which s is sorted.

    ``s``
        A string value from the list we want to sort.
    """
    return map(try_int, SPLIT_ALPHA_DIGITS.findall(s))

def natural_compare(a, b):
    """
    Compare two strings naturally and return the result.

    ``a``
        A string to compare.

    ``b``
        A string to compare.
    """
    return cmp(natural_sort_key(a), natural_sort_key(b))

def natural_sort(seq, compare=natural_compare):
    """
    Returns a copy of seq, sorted by natural string sort.
    """
    import copy
    temp = copy.copy(seq)
    temp.sort(compare)
    return temp

try:
    # Try to import Bazaar
    from bzrlib.branch import Branch
    b = Branch.open_containing('.')[0]
    b.lock_read()
    try:
        # Get the branch's latest revision number.
        revno = b.revno()
        # Convert said revision number into a bzr revision id.
        revision_id = b.dotted_revno_to_revision_id((revno,))
        # Get a dict of tags, with the revision id as the key.
        tags = b.tags.get_reverse_tag_dict()
        # Check if the latest
        if revision_id in tags:
            version = u'%s' % tags[revision_id][0]
        else:
            version = '%s-bzr%s' % \
                (natural_sort(b.tags.get_tag_dict().keys())[-1], revno)
        ver_file = open(VERSION_FILE, u'w')
        ver_file.write(version)
        ver_file.close()
    finally:
        b.unlock()
except:
    ver_file = open(VERSION_FILE, u'r')
    version = ver_file.read().strip()
    ver_file.close()


setup(
    name='OpenLP',
    version=version,
    description="Open source Church presentation and lyrics projection application.",
    long_description="""\
OpenLP (previously openlp.org) is free church presentation software, or lyrics projection software, used to display slides of songs, Bible verses, videos, images, and even presentations (if PowerPoint is installed) for church worship using a computer and a data projector.""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Religion',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Afrikaans',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Hungarian',
        'Natural Language :: Indonesian',
        'Natural Language :: Japanese',
        'Natural Language :: Norwegian',
        'Natural Language :: Portuguese (Brazilian)',
        'Natural Language :: Russian',
        'Natural Language :: Swedish',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Desktop Environment :: Gnome',
        'Topic :: Desktop Environment :: K Desktop Environment (KDE)',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Video',
        'Topic :: Religion'
    ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='open source church presentation lyrics projection song bible display project',
    author='Raoul Snyman',
    author_email='raoulsnyman@openlp.org',
    url='http://openlp.org/',
    license='GNU General Public License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    scripts=['openlp.py'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """
)
