from setuptools import setup, find_packages
import sys, os

VERSION_FILE = 'openlp/.version'

try:
    from bzrlib.branch import Branch
    b = Branch.open_containing('.')[0]
    b.lock_read()
    try:
        revno = b.revno()
        # Add the latest tag in here too
        verno = b.tags.get_tag_dict().keys()[0]
    finally:
        b.unlock()
except:
    revno = 0

version = '1.9.1-bzr%s' % revno

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
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """
)
