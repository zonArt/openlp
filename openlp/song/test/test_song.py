"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Carsten Tinggaard

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

import unittest
import os
import sys
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..' ,'..', '..')))

from openlp.song import Song

class SongTest_Init(unittest.TestCase):
    """Class for first initialization check"""
    
    def testCreation(self):
        """Init: Create as empty"""
        s = Song()
        self.assertTrue(True)
        
    def test_str(self):
        """Init: Empty, use __str__ to count attributes"""
        s = Song()
        r = s.__str__()
        l = r.split("\n")
        #print r
        self.assertEqual(len(l), 16)
        
    def test_asString(self):
        """Init: Empty asString"""
        s = Song()
        r = s._get_as_string()
        #print r
        self.assertEqual(len(r), 89)
        
class SongTest_ParseText(unittest.TestCase):
    """Test cases for converting from text format to Song"""
    
    def testSimple(self):
        """Text: Simply return True"""
        self.failUnless(True)
    

if "__main__" == __name__:
    suite1 = unittest.TestLoader().loadTestsFromTestCase(SongTest_ParseText)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(SongTest_Init)
    
    alltests = unittest.TestSuite([suite1, suite2])
    unittest.TextTestRunner(verbosity=2).run(alltests)
    