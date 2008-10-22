import os, os.path
import sys
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..')))

from openlp.utils import ConfigHelper

class BibleManager:
    def __init__(self): # bible, type, path, user, password): # , type='sqlite'
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection information
        Throws Exception if no Bibles are found.
    
        Init confirms the bible exists and stores the database path.   
        """
        #if bible != "niv" and bible !="message":
        #    raise Exception('Unsupported bible requested ' + bible)
        self.biblePath = ConfigHelper.getBiblePath()
        print self.biblePath
        
        
    def getBibles(self):
        """
        Returns a list of Books of the bible
        """
        print "get Bibles"
        return ["NIV","The_Message"]

    def getBibleBooks(self,bible):
        """
        Returns a list of the books of the bible
        """
        return ["Gen","Exd","Matt","Mark"]
        
    def getBookVerseCount(self, bible, book, chapter):
        """
        Returns all the number of verses for a given 
        book and chapter
        """
        return 28
        
    def getVerseText(self, bible,book,  chapter, sverse, everse):       
        """
        Returns a list of verses for a given Book, Chapter and ranges of verses.
        If the end verse(everse) is less then the start verse(sverse)
        then only one verse is returned
        """

        if everse < sverse:
            print "adjusted end verse"
            everse = sverse
        return ["In the Beginning was the Word","God made the world as saw it was good"]


bm = BibleManager()
