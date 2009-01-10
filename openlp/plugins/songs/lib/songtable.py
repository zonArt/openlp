"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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
class Author(object):
    def __init__(self, authorname, first_name, last_name):
        self.authorname =authorname
        self.first_name =first_name
        self.last_name =last_name                
        
    def __repr__(self):
        return "<authormeta(%r,%r,%r)>"  %(self.authorname, self.first_name, self.last_name)
        
    def get_author(self):
        return self.authorname, self.first_name, self.last_name
        
    def get_author_name(self):
        return self.authorname
