"""

Base Plugin class

"""

class Plugin(Interface):
    "Plugin type"

    def __init__(self, mediaManager, *args, **kwargs):
        "Plugin constructor called with mediaManager argument which allows adding to the 
        mediaManager - generally adding a page to mediaManager.Notebook"
    
    def GetName():
        "Return the plugins name for future plugin manager"

    
        
# vim: autoindent shiftwidth=4 expandtab textwidth=80
