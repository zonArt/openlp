from PyQt4 import QtCore, QtGui

class ColorButton(QtGui.QPushButton):
    """
    Subclasses QPushbutton to create a "Color Chooser" button
    """

    colorChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(ColorButton, self).__init__()
        self._color = '#ffffff'
        self.parent = parent
        self.clicked.connect(self.on_clicked)

    def change_color(self, color):
        self._color = color
        self.setStyleSheet('background-color: %s' % color)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self.change_color(color)

    def on_clicked(self):
        new_color = QtGui.QColorDialog.getColor(QtGui.QColor(self._color), self.parent)
        if new_color.isValid() and self._color != new_color.name():
            self.change_color(new_color.name())
            print("changed")
            self.colorChanged.emit(new_color.name())