# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
The UI widgets for the first time wizard.
"""
from PyQt5 import QtCore, QtGui, QtWidgets

from openlp.core.common import translate, is_macosx, clean_button_text, Settings
from openlp.core.lib import build_icon
from openlp.core.lib.ui import add_welcome_page


class FirstTimePage(object):
    """
    An enumeration class with each of the pages of the wizard.
    """
    Welcome = 0
    Download = 1
    NoInternet = 2
    Plugins = 3
    Songs = 4
    Bibles = 5
    Themes = 6
    Defaults = 7
    Progress = 8


class UiFirstTimeWizard(object):
    """
    The UI widgets for the first time wizard.
    """
    def setup_ui(self, first_time_wizard):
        """
        Set up the UI.

        :param first_time_wizard: The wizard form
        """
        first_time_wizard.setObjectName('first_time_wizard')
        first_time_wizard.setWindowIcon(build_icon(u':/icon/openlp-logo.svg'))
        first_time_wizard.resize(550, 386)
        first_time_wizard.setModal(True)
        first_time_wizard.setOptions(QtWidgets.QWizard.IndependentPages | QtWidgets.QWizard.NoBackButtonOnStartPage |
                                     QtWidgets.QWizard.NoBackButtonOnLastPage | QtWidgets.QWizard.HaveCustomButton1 |
                                     QtWidgets.QWizard.HaveCustomButton2)
        if is_macosx():
            first_time_wizard.setPixmap(QtWidgets.QWizard.BackgroundPixmap,
                                        QtGui.QPixmap(':/wizards/openlp-osx-wizard.png'))
            first_time_wizard.resize(634, 386)
        else:
            first_time_wizard.setWizardStyle(QtWidgets.QWizard.ModernStyle)
        self.finish_button = self.button(QtWidgets.QWizard.FinishButton)
        self.no_internet_finish_button = self.button(QtWidgets.QWizard.CustomButton1)
        self.cancel_button = self.button(QtWidgets.QWizard.CancelButton)
        self.no_internet_cancel_button = self.button(QtWidgets.QWizard.CustomButton2)
        self.next_button = self.button(QtWidgets.QWizard.NextButton)
        self.back_button = self.button(QtWidgets.QWizard.BackButton)
        add_welcome_page(first_time_wizard, ':/wizards/wizard_firsttime.bmp')
        # The download page
        self.download_page = QtWidgets.QWizardPage()
        self.download_page.setObjectName('download_page')
        self.download_layout = QtWidgets.QVBoxLayout(self.download_page)
        self.download_layout.setContentsMargins(48, 48, 48, 48)
        self.download_layout.setObjectName('download_layout')
        self.download_label = QtWidgets.QLabel(self.download_page)
        self.download_label.setObjectName('download_label')
        self.download_layout.addWidget(self.download_label)
        first_time_wizard.setPage(FirstTimePage.Download, self.download_page)
        # The "you don't have an internet connection" page.
        self.no_internet_page = QtWidgets.QWizardPage()
        self.no_internet_page.setObjectName('no_internet_page')
        self.no_internet_layout = QtWidgets.QVBoxLayout(self.no_internet_page)
        self.no_internet_layout.setContentsMargins(50, 30, 50, 40)
        self.no_internet_layout.setObjectName('no_internet_layout')
        self.no_internet_label = QtWidgets.QLabel(self.no_internet_page)
        self.no_internet_label.setWordWrap(True)
        self.no_internet_label.setObjectName('no_internet_label')
        self.no_internet_layout.addWidget(self.no_internet_label)
        first_time_wizard.setPage(FirstTimePage.NoInternet, self.no_internet_page)
        # The plugins page
        self.plugin_page = QtWidgets.QWizardPage()
        self.plugin_page.setObjectName('plugin_page')
        self.plugin_layout = QtWidgets.QVBoxLayout(self.plugin_page)
        self.plugin_layout.setContentsMargins(40, 15, 40, 0)
        self.plugin_layout.setObjectName('plugin_layout')
        self.songs_check_box = QtWidgets.QCheckBox(self.plugin_page)
        self.songs_check_box.setChecked(True)
        self.songs_check_box.setObjectName('songs_check_box')
        self.plugin_layout.addWidget(self.songs_check_box)
        self.custom_check_box = QtWidgets.QCheckBox(self.plugin_page)
        self.custom_check_box.setChecked(True)
        self.custom_check_box.setObjectName('custom_check_box')
        self.plugin_layout.addWidget(self.custom_check_box)
        self.bible_check_box = QtWidgets.QCheckBox(self.plugin_page)
        self.bible_check_box.setChecked(True)
        self.bible_check_box.setObjectName('bible_check_box')
        self.plugin_layout.addWidget(self.bible_check_box)
        self.image_check_box = QtWidgets.QCheckBox(self.plugin_page)
        self.image_check_box.setChecked(True)
        self.image_check_box.setObjectName('image_check_box')
        self.plugin_layout.addWidget(self.image_check_box)
        self.presentation_check_box = QtWidgets.QCheckBox(self.plugin_page)
        self.presentation_check_box.setChecked(True)
        self.presentation_check_box.setObjectName('presentation_check_box')
        self.plugin_layout.addWidget(self.presentation_check_box)
        self.media_check_box = QtWidgets.QCheckBox(self.plugin_page)
        self.media_check_box.setChecked(True)
        self.media_check_box.setObjectName('media_check_box')
        self.plugin_layout.addWidget(self.media_check_box)
        self.remote_check_box = QtWidgets.QCheckBox(self.plugin_page)
        self.remote_check_box.setObjectName('remote_check_box')
        self.plugin_layout.addWidget(self.remote_check_box)
        self.song_usage_check_box = QtWidgets.QCheckBox(self.plugin_page)
        self.song_usage_check_box.setChecked(True)
        self.song_usage_check_box.setObjectName('song_usage_check_box')
        self.plugin_layout.addWidget(self.song_usage_check_box)
        self.alert_check_box = QtWidgets.QCheckBox(self.plugin_page)
        self.alert_check_box.setChecked(True)
        self.alert_check_box.setObjectName('alert_check_box')
        self.plugin_layout.addWidget(self.alert_check_box)
        self.projectors_check_box = QtWidgets.QCheckBox(self.plugin_page)
        # If visibility setting for projector panel is True, check the box.
        if Settings().value('projector/show after wizard'):
            self.projectors_check_box.setChecked(True)
        self.projectors_check_box.setObjectName('projectors_check_box')
        self.projectors_check_box.clicked.connect(self.on_projectors_check_box_clicked)
        self.plugin_layout.addWidget(self.projectors_check_box)
        first_time_wizard.setPage(FirstTimePage.Plugins, self.plugin_page)
        # The song samples page
        self.songs_page = QtWidgets.QWizardPage()
        self.songs_page.setObjectName('songs_page')
        self.songs_layout = QtWidgets.QVBoxLayout(self.songs_page)
        self.songs_layout.setContentsMargins(50, 20, 50, 20)
        self.songs_layout.setObjectName('songs_layout')
        self.songs_list_widget = QtWidgets.QListWidget(self.songs_page)
        self.songs_list_widget.setAlternatingRowColors(True)
        self.songs_list_widget.setObjectName('songs_list_widget')
        self.songs_layout.addWidget(self.songs_list_widget)
        first_time_wizard.setPage(FirstTimePage.Songs, self.songs_page)
        # The Bible samples page
        self.bibles_page = QtWidgets.QWizardPage()
        self.bibles_page.setObjectName('bibles_page')
        self.bibles_layout = QtWidgets.QVBoxLayout(self.bibles_page)
        self.bibles_layout.setContentsMargins(50, 20, 50, 20)
        self.bibles_layout.setObjectName('bibles_layout')
        self.bibles_tree_widget = QtWidgets.QTreeWidget(self.bibles_page)
        self.bibles_tree_widget.setAlternatingRowColors(True)
        self.bibles_tree_widget.header().setVisible(False)
        self.bibles_tree_widget.setObjectName('bibles_tree_widget')
        self.bibles_layout.addWidget(self.bibles_tree_widget)
        first_time_wizard.setPage(FirstTimePage.Bibles, self.bibles_page)
        # The theme samples page
        self.themes_page = QtWidgets.QWizardPage()
        self.themes_page.setObjectName('themes_page')
        self.themes_layout = QtWidgets.QVBoxLayout(self.themes_page)
        self.themes_layout.setContentsMargins(20, 50, 20, 60)
        self.themes_layout.setObjectName('themes_layout')
        self.themes_list_widget = QtWidgets.QListWidget(self.themes_page)
        self.themes_list_widget.setViewMode(QtWidgets.QListView.IconMode)
        self.themes_list_widget.setMovement(QtWidgets.QListView.Static)
        self.themes_list_widget.setFlow(QtWidgets.QListView.LeftToRight)
        self.themes_list_widget.setSpacing(4)
        self.themes_list_widget.setUniformItemSizes(True)
        self.themes_list_widget.setIconSize(QtCore.QSize(133, 100))
        self.themes_list_widget.setWrapping(False)
        self.themes_list_widget.setObjectName('themes_list_widget')
        self.themes_layout.addWidget(self.themes_list_widget)
        first_time_wizard.setPage(FirstTimePage.Themes, self.themes_page)
        # the default settings page
        self.defaults_page = QtWidgets.QWizardPage()
        self.defaults_page.setObjectName('defaults_page')
        self.defaults_layout = QtWidgets.QFormLayout(self.defaults_page)
        self.defaults_layout.setContentsMargins(50, 20, 50, 20)
        self.defaults_layout.setObjectName('defaults_layout')
        self.display_label = QtWidgets.QLabel(self.defaults_page)
        self.display_label.setObjectName('display_label')
        self.display_combo_box = QtWidgets.QComboBox(self.defaults_page)
        self.display_combo_box.setEditable(False)
        self.display_combo_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.display_combo_box.setObjectName('display_combo_box')
        self.defaults_layout.addRow(self.display_label, self.display_combo_box)
        self.theme_label = QtWidgets.QLabel(self.defaults_page)
        self.theme_label.setObjectName('theme_label')
        self.theme_combo_box = QtWidgets.QComboBox(self.defaults_page)
        self.theme_combo_box.setEditable(False)
        self.theme_combo_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.theme_combo_box.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.theme_combo_box.setObjectName('theme_combo_box')
        self.defaults_layout.addRow(self.theme_label, self.theme_combo_box)
        first_time_wizard.setPage(FirstTimePage.Defaults, self.defaults_page)
        # Progress page
        self.progress_page = QtWidgets.QWizardPage()
        self.progress_page.setObjectName('progress_page')
        self.progress_layout = QtWidgets.QVBoxLayout(self.progress_page)
        self.progress_layout.setContentsMargins(48, 48, 48, 48)
        self.progress_layout.setObjectName('progress_layout')
        self.progress_label = QtWidgets.QLabel(self.progress_page)
        self.progress_label.setObjectName('progress_label')
        self.progress_layout.addWidget(self.progress_label)
        self.progress_bar = QtWidgets.QProgressBar(self.progress_page)
        self.progress_bar.setObjectName('progress_bar')
        self.progress_layout.addWidget(self.progress_bar)
        first_time_wizard.setPage(FirstTimePage.Progress, self.progress_page)
        self.retranslate_ui(first_time_wizard)

    def retranslate_ui(self, first_time_wizard):
        """
        Translate the UI on the fly

        :param first_time_wizard: The wizard form
        """
        first_time_wizard.setWindowTitle(translate('OpenLP.FirstTimeWizard', 'First Time Wizard'))
        text = translate('OpenLP.FirstTimeWizard', 'Welcome to the First Time Wizard')
        first_time_wizard.title_label.setText('<span style="font-size:14pt; font-weight:600;">{text}'
                                              '</span>'.format(text=text))
        button = clean_button_text(first_time_wizard.buttonText(QtWidgets.QWizard.NextButton))
        first_time_wizard.information_label.setText(
            translate('OpenLP.FirstTimeWizard', 'This wizard will help you to configure OpenLP for initial use. '
                                                'Click the {button} button below to start.').format(button=button))
        self.download_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Downloading Resource Index'))
        self.download_page.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Please wait while the resource index is '
                                                                           'downloaded.'))
        self.download_label.setText(translate('OpenLP.FirstTimeWizard', 'Please wait while OpenLP downloads the '
                                                                        'resource index file...'))
        self.plugin_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Select parts of the program you wish to use'))
        self.plugin_page.setSubTitle(translate('OpenLP.FirstTimeWizard',
                                               'You can also change these settings after the Wizard.'))
        self.songs_check_box.setText(translate('OpenLP.FirstTimeWizard', 'Songs'))
        self.custom_check_box.setText(translate('OpenLP.FirstTimeWizard',
                                                'Custom Slides – Easier to manage than songs and they have their own'
                                                ' list of slides'))
        self.bible_check_box.setText(translate('OpenLP.FirstTimeWizard',
                                               'Bibles – Import and show Bibles'))
        self.image_check_box.setText(translate('OpenLP.FirstTimeWizard',
                                               'Images – Show images or replace background with them'))
        self.presentation_check_box.setText(translate('OpenLP.FirstTimeWizard',
                                                      'Presentations – Show .ppt, .odp and .pdf files'))
        self.media_check_box.setText(translate('OpenLP.FirstTimeWizard', 'Media – Playback of Audio and Video files'))
        self.remote_check_box.setText(translate('OpenLP.FirstTimeWizard', 'Remote – Control OpenLP via browser or smart'
                                                                          'phone app'))
        self.song_usage_check_box.setText(translate('OpenLP.FirstTimeWizard', 'Song Usage Monitor'))
        self.alert_check_box.setText(translate('OpenLP.FirstTimeWizard',
                                               'Alerts – Display informative messages while showing other slides'))
        self.projectors_check_box.setText(translate('OpenLP.FirstTimeWizard',
                                                    'Projectors – Control PJLink compatible projects on your network'
                                                    ' from OpenLP'))
        self.no_internet_page.setTitle(translate('OpenLP.FirstTimeWizard', 'No Internet Connection'))
        self.no_internet_page.setSubTitle(
            translate('OpenLP.FirstTimeWizard', 'Unable to detect an Internet connection.'))
        button = clean_button_text(first_time_wizard.buttonText(QtWidgets.QWizard.FinishButton))
        self.no_internet_text = translate('OpenLP.FirstTimeWizard',
                                          'No Internet connection was found. The First Time Wizard needs an Internet '
                                          'connection in order to be able to download sample songs, Bibles and themes.'
                                          '  Click the {button} button now to start OpenLP with initial settings and '
                                          'no sample data.\n\nTo re-run the First Time Wizard and import this sample '
                                          'data at a later time, check your Internet connection and re-run this '
                                          'wizard by selecting "Tools/Re-run First Time Wizard" from OpenLP.'
                                          ).format(button=button)
        button = clean_button_text(first_time_wizard.buttonText(QtWidgets.QWizard.CancelButton))
        self.cancel_wizard_text = translate('OpenLP.FirstTimeWizard',
                                            '\n\nTo cancel the First Time Wizard completely (and not start OpenLP), '
                                            'click the {button} button now.').format(button=button)
        self.songs_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Sample Songs'))
        self.songs_page.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Select and download public domain songs.'))
        self.bibles_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Sample Bibles'))
        self.bibles_page.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Select and download free Bibles.'))
        self.themes_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Sample Themes'))
        self.themes_page.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Select and download sample themes.'))
        self.defaults_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Default Settings'))
        self.defaults_page.setSubTitle(translate('OpenLP.FirstTimeWizard',
                                                 'Set up default settings to be used by OpenLP.'))
        self.display_label.setText(translate('OpenLP.FirstTimeWizard', 'Default output display:'))
        self.theme_label.setText(translate('OpenLP.FirstTimeWizard', 'Select default theme:'))
        self.progress_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Downloading and Configuring'))
        self.progress_page.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Please wait while resources are downloaded '
                                                                           'and OpenLP is configured.'))
        self.progress_label.setText(translate('OpenLP.FirstTimeWizard', 'Starting configuration process...'))
        first_time_wizard.setButtonText(QtWidgets.QWizard.CustomButton1,
                                        clean_button_text(first_time_wizard.buttonText(QtWidgets.QWizard.FinishButton)))
        first_time_wizard.setButtonText(QtWidgets.QWizard.CustomButton2,
                                        clean_button_text(first_time_wizard.buttonText(QtWidgets.QWizard.CancelButton)))

    def on_projectors_check_box_clicked(self):
        # When clicking projectors_check box, change the visibility setting for Projectors panel.
        if Settings().value('projector/show after wizard'):
            Settings().setValue('projector/show after wizard', False)
        else:
            Settings().setValue('projector/show after wizard', True)
