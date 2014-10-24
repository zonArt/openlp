from PyQt4 import QtCore, QtGui

from openlp.core.common import translate


class ColorButton(QtGui.QPushButton):
    """
    Subclasses QPushbutton to create a "Color Chooser" button
    """

    colorChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        """
        Initialise the ColorButton
        """
        super(ColorButton, self).__init__()
        self.parent = parent
        self._color = '#ffffff'
        self.setToolTip(translate('OpenLP.ColorButton', 'Click to select a color.'))
        self.clicked.connect(self.on_clicked)

    def change_color(self, color):
        """
        Sets the _color variable and the background color.

        :param color:  String representation of a hexidecimal color
        """
        self._color = color
        self.setStyleSheet('background-color: %s' % color)

    @property
    def color(self):
        """
        Property method to return the color variable

        :return:  String representation of a hexidecimal color
        """
        return self._color

    @color.setter
    def color(self, color):
        """
        Property setter to change the imstamce color

        :param color:  String representation of a hexidecimal color
        """
        self.change_color(color)

    def on_clicked(self):
        """
        Handle the PushButton clicked signal, showing the ColorDialog and validating the input
        """
        new_color = QtGui.QColorDialog.getColor(QtGui.QColor(self._color), self.parent)
        if new_color.isValid() and self._color != new_color.name():
            self.change_color(new_color.name())
            self.colorChanged.emit(new_color.name())
