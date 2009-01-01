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
from openlp.core.utils import ConfigHelper

class MigrateFiles():
    def __init__(self, display):
        self.display = display

    def process(self):
        self.display.output("Files process started");
        self._initial_setup()
        self.display.output("Files process finished");        
        
    def _initial_setup(self):
        self.display.output("Initial Setup started");
        ConfigHelper.get_data_path()
        self.display.sub_output("Config created");        
        ConfigHelper.get_config("bible", "data path")
        self.display.sub_output("Config created");        
        ConfigHelper.get_config("videos", "data path") 
        self.display.sub_output("videos created");                
        ConfigHelper.get_config("images", "data path") 
        self.display.sub_output("images created");                
        ConfigHelper.get_config("presentations", "data path") 
        self.display.sub_output("presentations created");                
        self.display.output("Initial Setup finished");        
