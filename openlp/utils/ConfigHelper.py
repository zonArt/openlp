import os

# Utility Helper to allow classes to find directories in a standard manner

def get_registry_value(reg, key, value_name):
	k = _winreg.OpenKey(reg, key)
	value = _winreg.QueryValueEx(k, value_name)[0]
	_winreg.CloseKey(k)
	return value

def getConfigPath():
    if os.name == 'nt':
        import _winreg
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        path = get_registry_value(reg, key, "Common AppData")
    elif os.name == 'posix':
        path = os.path.join(os.getenv('HOME'), ".openlp.org")
        if os.path.exists(path) == False : 
            raise Exception ('Configuration Directory does not Exist ')
    return path

def getSongsFile():
    path = getConfigPath()
    songfile = os.path.join(path, ".openlp.org", "Data", "songs.olp")
    if os.path.exists(songfile):
        filename.set_filename(songfile)
    print songfile

def getBiblePath():
    return os.path.join(getConfigPath(), 'Bibles')
   
