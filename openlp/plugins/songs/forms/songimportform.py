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
The song import functions for OpenLP.
"""
import codecs
import logging
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Settings, UiStrings, translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.wizard import OpenLPWizard, WizardStrings
from openlp.plugins.songs.lib.importer import SongFormat, SongFormatSelect

log = logging.getLogger(__name__)


class SongImportForm(OpenLPWizard):
    """
    This is the Song Import Wizard, which allows easy importing of Songs
    into OpenLP from other formats like OpenLyrics, OpenSong and CCLI.
    """
    log.info(u'SongImportForm loaded')

    def __init__(self, parent, plugin):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.

        ``plugin``
            The songs plugin.
        """
        self.clipboard = self.main_window.clipboard
        OpenLPWizard.__init__(self, parent, plugin, u'songImportWizard', u':/wizards/wizard_importsong.bmp')

    def setupUi(self, image):
        """
        Set up the song wizard UI.
        """
        self.formatWidgets = dict([(format, {}) for format in SongFormat.get_format_list()])
        OpenLPWizard.setupUi(self, image)
        self.currentFormat = SongFormat.OpenLyrics
        self.formatStack.setCurrentIndex(self.currentFormat)
        QtCore.QObject.connect(self.formatComboBox, QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onCurrentIndexChanged)

    def onCurrentIndexChanged(self, index):
        """
        Called when the format combo box's index changed.
        """
        self.currentFormat = index
        self.formatStack.setCurrentIndex(index)
        self.sourcePage.emit(QtCore.SIGNAL(u'completeChanged()'))

    def customInit(self):
        """
        Song wizard specific initialisation.
        """
        for format in SongFormat.get_format_list():
            if not SongFormat.get(format, u'availability'):
                self.formatWidgets[format][u'disabledWidget'].setVisible(True)
                self.formatWidgets[format][u'importWidget'].setVisible(False)

    def customSignals(self):
        """
        Song wizard specific signals.
        """
        for format in SongFormat.get_format_list():
            select_mode = SongFormat.get(format, u'selectMode')
            if select_mode == SongFormatSelect.MultipleFiles:
                QtCore.QObject.connect(self.formatWidgets[format][u'addButton'],
                    QtCore.SIGNAL(u'clicked()'), self.onAddButtonClicked)
                QtCore.QObject.connect(self.formatWidgets[format][u'removeButton'],
                    QtCore.SIGNAL(u'clicked()'), self.onRemoveButtonClicked)
            else:
                QtCore.QObject.connect(self.formatWidgets[format][u'browseButton'],
                    QtCore.SIGNAL(u'clicked()'), self.onBrowseButtonClicked)
                QtCore.QObject.connect(self.formatWidgets[format][u'filepathEdit'],
                    QtCore.SIGNAL(u'textChanged (const QString&)'), self.onFilepathEditTextChanged)

    def addCustomPages(self):
        """
        Add song wizard specific pages.
        """
        # Source Page
        self.sourcePage = SongImportSourcePage()
        self.sourcePage.setObjectName(u'SourcePage')
        self.sourceLayout = QtGui.QVBoxLayout(self.sourcePage)
        self.sourceLayout.setObjectName(u'SourceLayout')
        self.formatLayout = QtGui.QFormLayout()
        self.formatLayout.setObjectName(u'FormatLayout')
        self.formatLabel = QtGui.QLabel(self.sourcePage)
        self.formatLabel.setObjectName(u'FormatLabel')
        self.formatComboBox = QtGui.QComboBox(self.sourcePage)
        self.formatComboBox.setObjectName(u'FormatComboBox')
        self.formatLayout.addRow(self.formatLabel, self.formatComboBox)
        self.formatSpacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.formatLayout.setItem(1, QtGui.QFormLayout.LabelRole, self.formatSpacer)
        self.sourceLayout.addLayout(self.formatLayout)
        self.formatHSpacing = self.formatLayout.horizontalSpacing()
        self.formatVSpacing = self.formatLayout.verticalSpacing()
        self.formatLayout.setVerticalSpacing(0)
        self.stackSpacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.formatStack = QtGui.QStackedLayout()
        self.formatStack.setObjectName(u'FormatStack')
        self.disablableFormats = []
        for self.currentFormat in SongFormat.get_format_list():
            self.addFileSelectItem()
        self.sourceLayout.addLayout(self.formatStack)
        self.addPage(self.sourcePage)

    def retranslateUi(self):
        """
        Song wizard localisation.
        """
        self.setWindowTitle(translate('SongsPlugin.ImportWizardForm', 'Song Import Wizard'))
        self.titleLabel.setText(WizardStrings.HeaderStyle % translate('OpenLP.Ui', 'Welcome to the Song Import Wizard'))
        self.informationLabel.setText(translate('SongsPlugin.ImportWizardForm',
            'This wizard will help you to import songs from a variety of '
            'formats. Click the next button below to start the process by selecting a format to import from.'))
        self.sourcePage.setTitle(WizardStrings.ImportSelect)
        self.sourcePage.setSubTitle(WizardStrings.ImportSelectLong)
        self.formatLabel.setText(WizardStrings.FormatLabel)
        for format in SongFormat.get_format_list():
            format_name, custom_combo_text, description_text, select_mode = \
                SongFormat.get(format, u'name', u'comboBoxText', u'descriptionText', u'selectMode')
            combo_box_text = (custom_combo_text if custom_combo_text else format_name)
            self.formatComboBox.setItemText(format, combo_box_text)
            if description_text is not None:
                self.formatWidgets[format][u'descriptionLabel'].setText(description_text)
            if select_mode == SongFormatSelect.MultipleFiles:
                self.formatWidgets[format][u'addButton'].setText(
                    translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
                self.formatWidgets[format][u'removeButton'].setText(
                    translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
            else:
                self.formatWidgets[format][u'browseButton'].setText(UiStrings().Browse)
                f_label = 'Filename:'
                if select_mode == SongFormatSelect.SingleFolder:
                    f_label = 'Folder:'
                self.formatWidgets[format][u'filepathLabel'].setText(translate('SongsPlugin.ImportWizardForm', f_label))
        for format in self.disablableFormats:
            self.formatWidgets[format][u'disabledLabel'].setText(SongFormat.get(format, u'disabledLabelText'))
        self.progressPage.setTitle(WizardStrings.Importing)
        self.progressPage.setSubTitle(
            translate('SongsPlugin.ImportWizardForm', 'Please wait while your songs are imported.'))
        self.progressLabel.setText(WizardStrings.Ready)
        self.progressBar.setFormat(WizardStrings.PercentSymbolFormat)
        self.errorCopyToButton.setText(translate('SongsPlugin.ImportWizardForm', 'Copy'))
        self.errorSaveToButton.setText(translate('SongsPlugin.ImportWizardForm', 'Save to File'))
        # Align all QFormLayouts towards each other.
        formats = filter(lambda f: u'filepathLabel' in self.formatWidgets[f], SongFormat.get_format_list())
        labels = [self.formatWidgets[f][u'filepathLabel'] for f in formats]
        # Get max width of all labels
        max_label_width = max(self.formatLabel.minimumSizeHint().width(),
            max([label.minimumSizeHint().width() for label in labels]))
        self.formatSpacer.changeSize(max_label_width, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        spacers = [self.formatWidgets[f][u'filepathSpacer'] for f in formats]
        for index, spacer in enumerate(spacers):
            spacer.changeSize(
                max_label_width - labels[index].minimumSizeHint().width(), 0,
                QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        # Align descriptionLabels with rest of layout
        for format in SongFormat.get_format_list():
            if SongFormat.get(format, u'descriptionText') is not None:
                self.formatWidgets[format][u'descriptionSpacer'].changeSize(
                    max_label_width + self.formatHSpacing, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

    def customPageChanged(self, pageId):
        """
        Called when changing to a page other than the progress page.
        """
        if self.page(pageId) == self.sourcePage:
            self.onCurrentIndexChanged(self.formatStack.currentIndex())

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        Provide each song format class with a chance to validate its input by
        overriding isValidSource().
        """
        if self.currentPage() == self.welcomePage:
            return True
        elif self.currentPage() == self.sourcePage:
            this_format = self.currentFormat
            Settings().setValue(u'songs/last import type', this_format)
            select_mode, class_, error_msg = SongFormat.get(this_format, u'selectMode', u'class', u'invalidSourceMsg')
            if select_mode == SongFormatSelect.MultipleFiles:
                import_source = self.getListOfFiles(self.formatWidgets[this_format][u'fileListWidget'])
                error_title = UiStrings().IFSp
                focus_button = self.formatWidgets[this_format][u'addButton']
            else:
                import_source = self.formatWidgets[this_format][u'filepathEdit'].text()
                error_title = (UiStrings().IFSs if select_mode == SongFormatSelect.SingleFile else UiStrings().IFdSs)
                focus_button = self.formatWidgets[this_format][u'browseButton']
            if not class_.isValidSource(import_source):
                critical_error_message_box(error_title, error_msg)
                focus_button.setFocus()
                return False
            return True
        elif self.currentPage() == self.progressPage:
            return True

    def getFiles(self, title, listbox, filters=u''):
        """
        Opens a QFileDialog and writes the filenames to the given listbox.

        ``title``
            The title of the dialog (unicode).

        ``listbox``
            A listbox (QListWidget).

        ``filters``
            The file extension filters. It should contain the file descriptions
            as well as the file extensions. For example::

                u'SongBeamer Files (*.sng)'
        """
        if filters:
            filters += u';;'
        filters += u'%s (*)' % UiStrings().AllFiles
        filenames = QtGui.QFileDialog.getOpenFileNames(self, title,
            Settings().value(self.plugin.settingsSection + u'/last directory import'), filters)
        if filenames:
            listbox.addItems(filenames)
            Settings().setValue(self.plugin.settingsSection + u'/last directory import',
                os.path.split(unicode(filenames[0]))[0])

    def getListOfFiles(self, listbox):
        """
        Return a list of file from the listbox
        """
        return [listbox.item(i).text() for i in range(listbox.count())]

    def removeSelectedItems(self, listbox):
        """
        Remove selected listbox items
        """
        for item in listbox.selectedItems():
            item = listbox.takeItem(listbox.row(item))
            del item

    def onBrowseButtonClicked(self):
        """
        Browse for files or a directory.
        """
        this_format = self.currentFormat
        select_mode, format_name, ext_filter = SongFormat.get(this_format, u'selectMode',
            u'name', u'filter')
        filepathEdit = self.formatWidgets[this_format][u'filepathEdit']
        if select_mode == SongFormatSelect.SingleFile:
            self.getFileName(WizardStrings.OpenTypeFile % format_name, filepathEdit,
                u'last directory import', ext_filter)
        elif select_mode == SongFormatSelect.SingleFolder:
            self.getFolder(WizardStrings.OpenTypeFolder % format_name, filepathEdit, u'last directory import')

    def onAddButtonClicked(self):
        """
        Add a file or directory.
        """
        this_format = self.currentFormat
        select_mode, format_name, ext_filter, custom_title = \
            SongFormat.get(this_format, u'selectMode', u'name', u'filter', u'getFilesTitle')
        title = custom_title if custom_title else WizardStrings.OpenTypeFile % format_name
        if select_mode == SongFormatSelect.MultipleFiles:
            self.getFiles(title, self.formatWidgets[this_format][u'fileListWidget'], ext_filter)
            self.sourcePage.emit(QtCore.SIGNAL(u'completeChanged()'))

    def onRemoveButtonClicked(self):
        """
        Remove a file from the list.
        """
        self.removeSelectedItems(
            self.formatWidgets[self.currentFormat][u'fileListWidget'])
        self.sourcePage.emit(QtCore.SIGNAL(u'completeChanged()'))

    def onFilepathEditTextChanged(self):
        """
        Called when the content of the Filename/Folder edit box changes.
        """
        self.sourcePage.emit(QtCore.SIGNAL(u'completeChanged()'))

    def setDefaults(self):
        """
        Set default form values for the song import wizard.
        """
        self.restart()
        self.finishButton.setVisible(False)
        self.cancelButton.setVisible(True)
        last_import_type = Settings().value(u'songs/last import type')
        if last_import_type < 0 or last_import_type >= self.formatComboBox.count():
            last_import_type = 0
        self.formatComboBox.setCurrentIndex(last_import_type)
        for format in SongFormat.get_format_list():
            select_mode = SongFormat.get(format, u'selectMode')
            if select_mode == SongFormatSelect.MultipleFiles:
                self.formatWidgets[format][u'fileListWidget'].clear()
            else:
                self.formatWidgets[format][u'filepathEdit'].setText(u'')
        self.errorReportTextEdit.clear()
        self.errorReportTextEdit.setHidden(True)
        self.errorCopyToButton.setHidden(True)
        self.errorSaveToButton.setHidden(True)

    def preWizard(self):
        """
        Perform pre import tasks
        """
        OpenLPWizard.preWizard(self)
        self.progressLabel.setText(WizardStrings.StartingImport)
        self.application.process_events()

    def performWizard(self):
        """
        Perform the actual import. This method pulls in the correct importer
        class, and then runs the ``doImport`` method of the importer to do
        the actual importing.
        """
        source_format = self.currentFormat
        select_mode = SongFormat.get(source_format, u'selectMode')
        if select_mode == SongFormatSelect.SingleFile:
            importer = self.plugin.importSongs(source_format,
                filename=self.formatWidgets[source_format][u'filepathEdit'].text())
        elif select_mode == SongFormatSelect.SingleFolder:
            importer = self.plugin.importSongs(source_format,
                folder=self.formatWidgets[source_format][u'filepathEdit'].text())
        else:
            importer = self.plugin.importSongs(source_format,
                filenames=self.getListOfFiles(self.formatWidgets[source_format][u'fileListWidget']))
        importer.doImport()
        self.progressLabel.setText(WizardStrings.FinishedImport)

    def onErrorCopyToButtonClicked(self):
        """
        Copy the error report to the clipboard.
        """
        self.clipboard.setText(self.errorReportTextEdit.toPlainText())

    def onErrorSaveToButtonClicked(self):
        """
        Save the error report to a file.
        """
        filename = QtGui.QFileDialog.getSaveFileName(self,
            Settings().value(self.plugin.settingsSection + u'last directory import'))
        if not filename:
            return
        report_file = codecs.open(filename, u'w', u'utf-8')
        report_file.write(self.errorReportTextEdit.toPlainText())
        report_file.close()

    def addFileSelectItem(self):
        """
        Add a file selection page.
        """
        this_format = self.currentFormat
        prefix, can_disable, description_text, select_mode = \
            SongFormat.get(this_format, u'prefix', u'canDisable', u'descriptionText', u'selectMode')
        page = QtGui.QWidget()
        page.setObjectName(prefix + u'Page')
        if can_disable:
            importWidget = self.disablableWidget(page, prefix)
        else:
            importWidget = page
        importLayout = QtGui.QVBoxLayout(importWidget)
        importLayout.setMargin(0)
        importLayout.setObjectName(prefix + u'ImportLayout')
        if description_text is not None:
            descriptionLayout = QtGui.QHBoxLayout()
            descriptionLayout.setObjectName(prefix + u'DescriptionLayout')
            descriptionSpacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            descriptionLayout.addSpacerItem(descriptionSpacer)
            descriptionLabel = QtGui.QLabel(importWidget)
            descriptionLabel.setWordWrap(True)
            descriptionLabel.setOpenExternalLinks(True)
            descriptionLabel.setObjectName(prefix + u'DescriptionLabel')
            descriptionLayout.addWidget(descriptionLabel)
            importLayout.addLayout(descriptionLayout)
            self.formatWidgets[this_format][u'descriptionLabel'] = descriptionLabel
            self.formatWidgets[this_format][u'descriptionSpacer'] = descriptionSpacer
        if select_mode == SongFormatSelect.SingleFile or select_mode == SongFormatSelect.SingleFolder:
            filepathLayout = QtGui.QHBoxLayout()
            filepathLayout.setObjectName(prefix + u'FilepathLayout')
            filepathLayout.setContentsMargins(0, self.formatVSpacing, 0, 0)
            filepathLabel = QtGui.QLabel(importWidget)
            filepathLabel.setObjectName(prefix + u'FilepathLabel')
            filepathLayout.addWidget(filepathLabel)
            filepathSpacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            filepathLayout.addSpacerItem(filepathSpacer)
            filepathEdit = QtGui.QLineEdit(importWidget)
            filepathEdit.setObjectName(prefix + u'FilepathEdit')
            filepathLayout.addWidget(filepathEdit)
            browseButton = QtGui.QToolButton(importWidget)
            browseButton.setIcon(self.openIcon)
            browseButton.setObjectName(prefix + u'BrowseButton')
            filepathLayout.addWidget(browseButton)
            importLayout.addLayout(filepathLayout)
            importLayout.addSpacerItem(self.stackSpacer)
            self.formatWidgets[this_format][u'filepathLabel'] = filepathLabel
            self.formatWidgets[this_format][u'filepathSpacer'] = filepathSpacer
            self.formatWidgets[this_format][u'filepathLayout'] = filepathLayout
            self.formatWidgets[this_format][u'filepathEdit'] = filepathEdit
            self.formatWidgets[this_format][u'browseButton'] = browseButton
        elif select_mode == SongFormatSelect.MultipleFiles:
            fileListWidget = QtGui.QListWidget(importWidget)
            fileListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
            fileListWidget.setObjectName(prefix + u'FileListWidget')
            importLayout.addWidget(fileListWidget)
            buttonLayout = QtGui.QHBoxLayout()
            buttonLayout.setObjectName(prefix + u'ButtonLayout')
            addButton = QtGui.QPushButton(importWidget)
            addButton.setIcon(self.openIcon)
            addButton.setObjectName(prefix + u'AddButton')
            buttonLayout.addWidget(addButton)
            buttonLayout.addStretch()
            removeButton = QtGui.QPushButton(importWidget)
            removeButton.setIcon(self.deleteIcon)
            removeButton.setObjectName(prefix + u'RemoveButton')
            buttonLayout.addWidget(removeButton)
            importLayout.addLayout(buttonLayout)
            self.formatWidgets[this_format][u'fileListWidget'] = fileListWidget
            self.formatWidgets[this_format][u'buttonLayout'] = buttonLayout
            self.formatWidgets[this_format][u'addButton'] = addButton
            self.formatWidgets[this_format][u'removeButton'] = removeButton
        self.formatStack.addWidget(page)
        self.formatWidgets[this_format][u'page'] = page
        self.formatWidgets[this_format][u'importLayout'] = importLayout
        self.formatComboBox.addItem(u'')

    def disablableWidget(self, page, prefix):
        """
        Disable a widget.
        """
        this_format = self.currentFormat
        self.disablableFormats.append(this_format)
        layout = QtGui.QVBoxLayout(page)
        layout.setMargin(0)
        layout.setSpacing(0)
        layout.setObjectName(prefix + u'Layout')
        disabledWidget = QtGui.QWidget(page)
        disabledWidget.setVisible(False)
        disabledWidget.setObjectName(prefix + u'DisabledWidget')
        disabledLayout = QtGui.QVBoxLayout(disabledWidget)
        disabledLayout.setMargin(0)
        disabledLayout.setObjectName(prefix + u'DisabledLayout')
        disabledLabel = QtGui.QLabel(disabledWidget)
        disabledLabel.setWordWrap(True)
        disabledLabel.setObjectName(prefix + u'DisabledLabel')
        disabledLayout.addWidget(disabledLabel)
        disabledLayout.addSpacerItem(self.stackSpacer)
        layout.addWidget(disabledWidget)
        importWidget = QtGui.QWidget(page)
        importWidget.setObjectName(prefix + u'ImportWidget')
        layout.addWidget(importWidget)
        self.formatWidgets[this_format][u'layout'] = layout
        self.formatWidgets[this_format][u'disabledWidget'] = disabledWidget
        self.formatWidgets[this_format][u'disabledLayout'] = disabledLayout
        self.formatWidgets[this_format][u'disabledLabel'] = disabledLabel
        self.formatWidgets[this_format][u'importWidget'] = importWidget
        return importWidget


class SongImportSourcePage(QtGui.QWizardPage):
    """
    Subclass of QtGui.QWizardPage to override isComplete() for Source Page.
    """
    def isComplete(self):
        """
        Return True if:

        * an available format is selected, and
        * if MultipleFiles mode, at least one file is selected
        * or if SingleFile mode, the specified file exists
        * or if SingleFolder mode, the specified folder exists

        When this method returns True, the wizard's Next button is enabled.
        """
        wizard = self.wizard()
        this_format = wizard.currentFormat
        select_mode, format_available = SongFormat.get(this_format, u'selectMode', u'availability')
        if format_available:
            if select_mode == SongFormatSelect.MultipleFiles:
                if wizard.formatWidgets[this_format][u'fileListWidget'].count() > 0:
                    return True
            else:
                filepath = unicode(wizard.formatWidgets[this_format][u'filepathEdit'].text())
                if filepath:
                    if select_mode == SongFormatSelect.SingleFile and os.path.isfile(filepath):
                        return True
                    elif select_mode == SongFormatSelect.SingleFolder and os.path.isdir(filepath):
                        return True
        return False
