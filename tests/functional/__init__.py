import sip
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QString', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui

# Only one QApplication can be created. Use QtGui.QApplication.instance() when you need to "create" a  QApplication.
application = QtGui.QApplication([])
