import os, os.path
import sys
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..','..')))

from openlp.database.BibleImpl import *

if __name__ == "__main__":
    bi = BibleImpl("TheMessage")
    bi.createTables()
    bi.loadData('biblebooks_msg_short.csv','bibleverses_msg_short.csv')
    bi.Run_Tests()

    b2 = BibleImpl("NIV")
    b2.createTables()
    b2.loadData('biblebooks_niv_short.csv','bibleverses_niv_short.csv')
    b2.Run_Tests()
