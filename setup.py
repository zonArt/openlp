from setuptools import setupAPP = ['openlp.pyw']OPTIONS = {'argv_emulation': True, 'includes': ['sip', 'PyQt4']}setup(
    name='openlp.org',
    version='1.9.0',
    url='http://www.openlp.org/',    app=APP,    options={'py2app': OPTIONS},    setup_requires=['py2app'],)
