
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import str_to_bool, Receiver
from openlp.core.lib import SettingsTab

class AlertManager(self):
    """
    BiblesTab is the Bibles settings tab in the settings dialog.
    """
    global log
    log = logging.getLogger(u'AlertManager')
    log.info(u'Alert Manager loaded')

    def __init__(self):
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'alert_text'), self.displayAlert)

    def displayAlert(self, text=u''):
        """
        Called from the Alert Tab to display an alert

        ``text``
            display text
        """
        log.debug(u'display alert called %s' % text)
        self.parent.StatusBar.showMessage(self.trUtf8(u''))
        self.alertList.append(text)
        if self.timer_id != 0 or self.mediaLoaded:
            self.parent.StatusBar.showMessage(\
                    self.trUtf8(u'Alert message created and delayed'))
            return
        self.generateAlert()

    def generateAlert(self):
        log.debug(u'Generate Alert called')
        if len(self.alertList) == 0:
            return
        text = self.alertList.pop(0)
        alertTab = self.parent.settingsForm.AlertsTab
        alertframe = \
            QtGui.QPixmap(self.screen[u'size'].width(), self.alertHeight)
        alertframe.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(alertframe)
        painter.fillRect(alertframe.rect(), QtCore.Qt.transparent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(
            QtCore.QRect(
                0, 0, alertframe.rect().width(),
                alertframe.rect().height()),
            QtGui.QColor(alertTab.bg_color))
        font = QtGui.QFont()
        font.setFamily(alertTab.font_face)
        font.setBold(True)
        font.setPointSize(alertTab.font_size)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(alertTab.font_color))
        x, y = (0, 0)
        metrics = QtGui.QFontMetrics(font)
        painter.drawText(
            x, y + metrics.height() - metrics.descent() - 1, text)
        painter.end()
        self.display_alert.setPixmap(alertframe)
        # check to see if we have a timer running
        if self.timer_id == 0:
            self.timer_id = self.startTimer(int(alertTab.timeout) * 1000)

    def timerEvent(self, event):
        if event.timerId() == self.timer_id:
            self.display_alert.setPixmap(self.transparent)
        self.killTimer(self.timer_id)
        self.timer_id = 0
        self.generateAlert()
