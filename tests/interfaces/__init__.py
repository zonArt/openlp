import sip
sip.setapi(u'QDate', 2)
sip.setapi(u'QDateTime', 2)
sip.setapi(u'QString', 2)
sip.setapi(u'QTextStream', 2)
sip.setapi(u'QTime', 2)
sip.setapi(u'QUrl', 2)
sip.setapi(u'QVariant', 2)

#from PyQt4 import QtGui

# Only one QApplication can be created. Use QtGui.QApplication.instance() when you need to "create" an QApplication.
#application = QtGui.QApplication([])
