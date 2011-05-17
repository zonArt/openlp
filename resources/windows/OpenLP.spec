# -*- mode: python -*-
a = Analysis([
    os.path.join(HOMEPATH, 'support\\_mountzlib.py'),
    os.path.join(HOMEPATH, 'support\\useUnicode.py'),
    os.path.abspath('openlp.pyw')],
    pathex=[os.path.abspath('.')])
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, exclude_binaries=1,
    name=os.path.abspath(os.path.join('build', 'pyi.win32', 'OpenLP',
        'OpenLP.exe')),
    debug=False, strip=False, upx=True, console=False,
    icon=os.path.abspath(os.path.join('resources', 'images', 'OpenLP.ico')))
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True,
    name=os.path.abspath(os.path.join('dist', 'OpenLP')))
