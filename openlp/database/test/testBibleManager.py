import os, os.path
import sys
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..','..')))

from openlp.database.BibleManager import *

bm = BibleManager()
print bm
print bm.getBibles()
b = bm.getBibles()
for b1 in b:
    print b1
print bm.getBibleBooks("NIV")
c = bm.getBibleBooks("NIV")
for c1 in c:
    print c1
print bm.getBookVerseCount("NIV", "GEN", 1)
print bm.getVerseText("NIV", "GEN",1,1,1)
c = bm.getVerseText("NIV","GEN",1,2,1)
for c1 in c:
    print c1
