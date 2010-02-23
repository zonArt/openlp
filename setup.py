#!/usr/bin/env python

from setuptools import setup, find_packages
import sys, os

VERSION_FILE = 'openlp/.version'

try:
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
            version = '%s-bzr%s' % (sorted(b.tags.get_tag_dict().keys())[-1], revno)
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
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='open source church presentation lyrics projection song bible display project',
    author='Raoul Snyman',
    author_email='raoulsnyman@openlp.org',
    url='http://openlp.org/',
    license='GNU General Public License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    scripts=['openlp.pyw', 'scripts/openlp-1to2-converter.py', 'scripts/bible-1to2-converter.py'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """
)
