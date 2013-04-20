# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
The actual print service dialog
"""
import cgi
import datetime
import os

from PyQt4 import QtCore, QtGui
from lxml import html

from openlp.core.lib import Settings, UiStrings, Registry, translate, get_text_file_string
from openlp.core.ui.printservicedialog import Ui_PrintServiceDialog, ZoomSize
from openlp.core.utils import AppLocation

DEFAULT_CSS = """/*
Edit this file to customize the service order print. Note, that not all CSS
properties are supported. See:
http://doc.trolltech.com/4.7/richtext-html-subset.html#css-properties
*/

.serviceTitle {
   font-weight: 600;
   font-size: x-large;
   color: black;
}

.item {
   color: black;
}

.itemTitle {
   font-weight: 600;
   font-size: large;
}

.itemText {
   margin-top: 10px;
}

.itemFooter {
   font-size: 8px;
}

.itemNotes {}

.itemNotesTitle {
   font-weight: bold;
   font-size: 12px;
}

.itemNotesText {
   font-size: 11px;
}

.media {}

.mediaTitle {
    font-weight: bold;
    font-size: 11px;
}

.mediaText {}

.imageList {}

.customNotes {
   margin-top: 10px;
}

.customNotesTitle {
   font-weight: bold;
   font-size: 11px;
}

.customNotesText {
   font-size: 11px;
}

.newPage {
    page-break-before: always;
}
"""


class PrintServiceForm(QtGui.QDialog, Ui_PrintServiceDialog):
    """
    The :class:`~openlp.core.ui.printserviceform.PrintServiceForm` class displays a dialog for printing the service.
    """
    def __init__(self):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, self.main_window)
        self.printer = QtGui.QPrinter()
        self.print_dialog = QtGui.QPrintDialog(self.printer, self)
        self.document = QtGui.QTextDocument()
        self.zoom = 0
        self.setupUi(self)
        # Load the settings for the dialog.
        settings = Settings()
        settings.beginGroup(u'advanced')
        self.slide_text_check_box.setChecked(settings.value(u'print slide text'))
        self.page_break_after_text.setChecked(settings.value(u'add page break'))
        if not self.slide_text_check_box.isChecked():
            self.page_break_after_text.setDisabled(True)
        self.meta_data_check_box.setChecked(settings.value(u'print file meta data'))
        self.notes_check_box.setChecked(settings.value(u'print notes'))
        self.zoom_combo_box.setCurrentIndex(settings.value(u'display size'))
        settings.endGroup()
        # Signals
        self.print_button.triggered.connect(self.print_service_order)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_original_button.clicked.connect(self.zoom_original)
        self.preview_widget.paintRequested.connect(self.paint_requested)
        self.zoom_combo_box.currentIndexChanged.connect(self.display_size_changed)
        self.plain_copy.triggered.connect(self.copy_text)
        self.html_copy.triggered.connect(self.copy_html_text)
        self.slide_text_check_box.stateChanged.connect(self.on_slide_text_check_box_changed)
        self.update_preview_text()

    def toggle_options(self, checked):
        """
        Toggle various options
        """
        self.options_widget.setVisible(checked)
        if checked:
            left = self.options_button.pos().x()
            top = self.toolbar.height()
            self.options_widget.move(left, top)
            self.title_line_edit.setFocus()
        else:
            self.save_options()
        self.update_preview_text()

    def update_preview_text(self):
        """
        Creates the html text and updates the html of *self.document*.
        """
        html_data = self._add_element(u'html')
        self._add_element(u'head', parent=html_data)
        self._add_element(u'title', self.title_line_edit.text(), html_data.head)
        css_path = os.path.join(AppLocation.get_data_path(), u'service_print.css')
        custom_css = get_text_file_string(css_path)
        if not custom_css:
            custom_css = DEFAULT_CSS
        self._add_element(u'style', custom_css, html_data.head, attribute=(u'type', u'text/css'))
        self._add_element(u'body', parent=html_data)
        self._add_element(u'h1', cgi.escape(self.title_line_edit.text()), html_data.body, classId=u'serviceTitle')
        for index, item in enumerate(self.service_manager.service_items):
            self._add_preview_item(html_data.body, item[u'service_item'], index)
        # Add the custom service notes:
        if self.footer_text_edit.toPlainText():
            div = self._add_element(u'div', parent=html_data.body, classId=u'customNotes')
            self._add_element(
                u'span', translate('OpenLP.ServiceManager', 'Custom Service Notes: '), div, classId=u'customNotesTitle')
            self._add_element(u'span', cgi.escape(self.footer_text_edit.toPlainText()), div, classId=u'customNotesText')
        self.document.setHtml(html.tostring(html_data))
        self.preview_widget.updatePreview()

    def _add_preview_item(self, body, item, index):
        """
        Add a preview item
        """
        div = self._add_element(u'div', classId=u'item', parent=body)
        # Add the title of the service item.
        item_title = self._add_element(u'h2', parent=div, classId=u'itemTitle')
        self._add_element(u'img', parent=item_title, attribute=(u'src', item.icon))
        self._add_element(u'span', u'&nbsp;' + cgi.escape(item.get_display_title()), item_title)
        if self.slide_text_check_box.isChecked():
            # Add the text of the service item.
            if item.is_text():
                verse_def = None
                for slide in item.get_frames():
                    if not verse_def or verse_def != slide[u'verseTag']:
                        text_div = self._add_element(u'div', parent=div, classId=u'itemText')
                    else:
                        self._add_element(u'br', parent=text_div)
                    self._add_element(u'span', slide[u'html'], text_div)
                    verse_def = slide[u'verseTag']
                # Break the page before the div element.
                if index != 0 and self.page_break_after_text.isChecked():
                    div.set(u'class', u'item newPage')
            # Add the image names of the service item.
            elif item.is_image():
                ol = self._add_element(u'ol', parent=div, classId=u'imageList')
                for slide in range(len(item.get_frames())):
                    self._add_element(u'li', item.get_frame_title(slide), ol)
            # add footer
            foot_text = item.foot_text
            foot_text = foot_text.partition(u'<br>')[2]
            if foot_text:
                foot_text = cgi.escape(foot_text.replace(u'<br>', u'\n'))
                self._add_element(u'div', foot_text.replace(u'\n', u'<br>'), parent=div, classId=u'itemFooter')
        # Add service items' notes.
        if self.notes_check_box.isChecked():
            if item.notes:
                p = self._add_element(u'div', classId=u'itemNotes', parent=div)
                self._add_element(u'span', translate('OpenLP.ServiceManager', 'Notes: '), p, classId=u'itemNotesTitle')
                self._add_element(u'span', cgi.escape(item.notes).replace(u'\n', u'<br>'), p, classId=u'itemNotesText')
        # Add play length of media files.
        if item.is_media() and self.meta_data_check_box.isChecked():
            tme = item.media_length
            if item.end_time > 0:
                tme = item.end_time - item.start_time
            title = self._add_element(u'div', classId=u'media', parent=div)
            self._add_element(
                u'span', translate('OpenLP.ServiceManager', 'Playing time: '), title, classId=u'mediaTitle')
            self._add_element(u'span', unicode(datetime.timedelta(seconds=tme)), title, classId=u'mediaText')

    def _add_element(self, tag, text=None, parent=None, classId=None, attribute=None):
        """
        Creates a html element. If ``text`` is given, the element's text will
        set and if a ``parent`` is given, the element is appended.

        ``tag``
            The html tag, e. g. ``u'span'``. Defaults to ``None``.

        ``text``
            The text for the tag. Defaults to ``None``.

        ``parent``
            The parent element. Defaults to ``None``.

        ``classId``
            Value for the class attribute

        ``attribute``
            Tuple name/value pair to add as an optional attribute
        """
        if text is not None:
            element = html.fragment_fromstring(unicode(text), create_parent=tag)
        else:
            element = html.Element(tag)
        if parent is not None:
            parent.append(element)
        if classId is not None:
            element.set(u'class', classId)
        if attribute is not None:
            element.set(attribute[0], attribute[1])
        return element

    def paint_requested(self, printer):
        """
        Paint the preview of the *self.document*.

        ``printer``
            A *QPrinter* object.
        """
        self.document.print_(printer)

    def display_size_changed(self, display):
        """
        The Zoom Combo box has changed so set up the size.
        """
        if display == ZoomSize.Page:
            self.preview_widget.fitInView()
        elif display == ZoomSize.Width:
            self.preview_widget.fitToWidth()
        elif display == ZoomSize.OneHundred:
            self.preview_widget.fitToWidth()
            self.preview_widget.zoomIn(1)
        elif display == ZoomSize.SeventyFive:
            self.preview_widget.fitToWidth()
            self.preview_widget.zoomIn(0.75)
        elif display == ZoomSize.Fifty:
            self.preview_widget.fitToWidth()
            self.preview_widget.zoomIn(0.5)
        elif display == ZoomSize.TwentyFive:
            self.preview_widget.fitToWidth()
            self.preview_widget.zoomIn(0.25)
        settings = Settings()
        settings.beginGroup(u'advanced')
        settings.setValue(u'display size', display)
        settings.endGroup()

    def copy_text(self):
        """
        Copies the display text to the clipboard as plain text
        """
        self.update_song_usage()
        cursor = QtGui.QTextCursor(self.document)
        cursor.select(QtGui.QTextCursor.Document)
        clipboard_text = cursor.selectedText()
        # We now have the unprocessed unicode service text in the cursor
        # So we replace u2028 with \n and u2029 with \n\n and a few others
        clipboard_text = clipboard_text.replace(u'\u2028', u'\n')
        clipboard_text = clipboard_text.replace(u'\u2029', u'\n\n')
        clipboard_text = clipboard_text.replace(u'\u2018', u'\'')
        clipboard_text = clipboard_text.replace(u'\u2019', u'\'')
        clipboard_text = clipboard_text.replace(u'\u201c', u'"')
        clipboard_text = clipboard_text.replace(u'\u201d', u'"')
        clipboard_text = clipboard_text.replace(u'\u2026', u'...')
        clipboard_text = clipboard_text.replace(u'\u2013', u'-')
        clipboard_text = clipboard_text.replace(u'\u2014', u'-')
        # remove the icon from the text
        clipboard_text = clipboard_text.replace(u'\ufffc\xa0', u'')
        # and put it all on the clipboard
        self.main_window.clipboard.setText(clipboard_text)

    def copy_html_text(self):
        """
        Copies the display text to the clipboard as Html
        """
        self.update_song_usage()
        self.main_window.clipboard.setText(self.document.toHtml())

    def print_service_order(self):
        """
        Called, when the *print_button* is clicked. Opens the *print_dialog*.
        """
        if not self.print_dialog.exec_():
            return
        self.update_song_usage()
        # Print the document.
        self.document.print_(self.printer)

    def zoom_in(self):
        """
        Called when *zoom_in_button* is clicked.
        """
        self.preview_widget.zoomIn()
        self.zoom -= 0.1

    def zoom_out(self):
        """
        Called when *zoom_out_button* is clicked.
        """
        self.preview_widget.zoomOut()
        self.zoom += 0.1

    def zoom_original(self):
        """
        Called when *zoom_out_button* is clicked.
        """
        self.preview_widget.zoomIn(1 + self.zoom)
        self.zoom = 0

    def update_text_format(self, value):
        """
        Called when html copy check box is selected.
        """
        if value == QtCore.Qt.Checked:
            self.copyTextButton.setText(UiStrings().CopyToHtml)
        else:
            self.copyTextButton.setText(UiStrings().CopyToText)

    def on_slide_text_check_box_changed(self, state):
        """
        Disable or enable the ``page_break_after_text`` checkbox  as it should only
        be enabled, when the ``slide_text_check_box`` is enabled.
        """
        self.page_break_after_text.setDisabled(state == QtCore.Qt.Unchecked)

    def save_options(self):
        """
        Save the settings and close the dialog.
        """
        # Save the settings for this dialog.
        settings = Settings()
        settings.beginGroup(u'advanced')
        settings.setValue(u'print slide text', self.slide_text_check_box.isChecked())
        settings.setValue(u'add page break', self.page_break_after_text.isChecked())
        settings.setValue(u'print file meta data', self.meta_data_check_box.isChecked())
        settings.setValue(u'print notes', self.notes_check_box.isChecked())
        settings.endGroup()

    def update_song_usage(self):
        """
        Update the song usage
        """
        # Only continue when we include the song's text.
        if not self.slide_text_check_box.isChecked():
            return
        for item in self.service_manager.service_items:
            # Trigger Audit requests
            Registry().register_function(u'print_service_started', [item[u'service_item']])

    def _get_service_manager(self):
        """
        Adds the service manager to the class dynamically
        """
        if not hasattr(self, u'_service_manager'):
            self._service_manager = Registry().get(u'service_manager')
        return self._service_manager

    service_manager = property(_get_service_manager)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)
