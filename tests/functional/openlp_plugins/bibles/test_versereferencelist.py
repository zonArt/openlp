"""
This module contains tests for the versereferencelist submodule of the Bibles plugin.
"""

from unittest import TestCase
from openlp.plugins.bibles.lib.versereferencelist import VerseReferenceList

class TestVerseReferenceList(TestCase):
    def setUp(self):
        self.reference_list = VerseReferenceList()
        
    def add_test(self):
        """
        Test the addition of verses to the list
        """
        
        #GIVEN: book, chapter, verse and version
        book = u'testBook'
        chapter = 1
        verse = 1
        version = u'testVersion'
        copyright = u'testCopyright'
        permission = u'testPermision'
        
        #WHEN: We add it to the verse list
        self.reference_list.add(book, chapter, verse, version, copyright, permission)
        
        #THEN: The entries should be in the first entry of the list
        self.assertEqual(self.reference_list.current_index, 0, u'The current index should be 0')
        self.assertEqual(self.reference_list.verse_list[0][u'book'], book, u'The book in first entry should be %s' %book)
        self.assertEqual(self.reference_list.verse_list[0][u'chapter'], chapter, u'The chapter in first entry should be %u' %chapter)
        self.assertEqual(self.reference_list.verse_list[0][u'start'], verse, u'The start in first entry should be %u' %verse)
        self.assertEqual(self.reference_list.verse_list[0][u'version'], version, u'The version in first entry should be %s' %version)
        self.assertEqual(self.reference_list.verse_list[0][u'end'], verse, u'The end in first entry should be %u' %verse)
        
        #GIVEN: next verse
        verse = 2

        #WHEN: We add it to the verse list
        self.reference_list.add(book, chapter, verse, version, copyright, permission)
        
        #THEN: The current index should be 0 and the end pointer of the entry should be '2'
        self.assertEqual(self.reference_list.current_index, 0, u'The current index should be 0')
        self.assertEqual(self.reference_list.verse_list[0][u'end'], verse, u'The end in first entry should be %u' %verse)

        #GIVEN: a verse in another book
        book = u'testBook2'
        chapter = 2
        verse = 5

        #WHEN: We add it to the verse list
        self.reference_list.add(book, chapter, verse, version, copyright, permission)
        
        #THEN: the current index should be 1
        self.assertEqual(self.reference_list.current_index, 1, u'The current index should be 1')

    def add_version_test(self):
        """
        Test the addition of versions to the list
        """
        #GIVEN: version, copyright and permission
        version = u'testVersion'
        copyright = u'testCopyright'
        permission = u'testPermision'


        #WHEN: a not existing version will be added
        self.reference_list.add_version(version, copyright, permission)
        
        #THEN: the data will be appended to the list
        self.assertEqual(self.reference_list.version_list[0], {u'version': version, u'copyright': copyright, u'permission': permission},
                         u'The version data should be appended')
        

        #GIVEN: old length of the array
        oldLen = self.reference_list.version_list.__len__()
        
        #WHEN: an existing version will be added
        self.reference_list.add_version(version, copyright, permission)
        
        #THEN: the data will not be appended to the list
        self.assertEqual(self.reference_list.version_list.__len__(), oldLen, u'The version data should not be appended')
        

