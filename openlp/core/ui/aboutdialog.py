# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from PyQt4 import QtCore, QtGui
from openlp.core.lib import translate

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName(u'AboutDialog')
        AboutDialog.resize(516, 481)
        LogoIcon = QtGui.QIcon()
        LogoIcon.addPixmap(QtGui.QPixmap(u':/icon/openlp-logo-16x16.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutDialog.setWindowIcon(LogoIcon)
        self.AboutDialogLayout = QtGui.QVBoxLayout(AboutDialog)
        self.AboutDialogLayout.setSpacing(8)
        self.AboutDialogLayout.setMargin(8)
        self.AboutDialogLayout.setObjectName(u'AboutDialogLayout')
        self.LogoLabel = QtGui.QLabel(AboutDialog)
        self.LogoLabel.setPixmap(
            QtGui.QPixmap(u':/graphics/openlp-about-logo.png'))
        self.LogoLabel.setScaledContents(False)
        self.LogoLabel.setIndent(0)
        self.LogoLabel.setObjectName(u'LogoLabel')
        self.AboutDialogLayout.addWidget(self.LogoLabel)
        self.AboutNotebook = QtGui.QTabWidget(AboutDialog)
        self.AboutNotebook.setObjectName(u'AboutNotebook')
        self.AboutTab = QtGui.QWidget()
        self.AboutTab.setObjectName(u'AboutTab')
        self.AboutTabLayout = QtGui.QVBoxLayout(self.AboutTab)
        self.AboutTabLayout.setSpacing(0)
        self.AboutTabLayout.setMargin(8)
        self.AboutTabLayout.setObjectName(u'AboutTabLayout')
        self.AboutTextEdit = QtGui.QPlainTextEdit(self.AboutTab)
        self.AboutTextEdit.setReadOnly(True)
        self.AboutTextEdit.setObjectName(u'AboutTextEdit')
        self.AboutTabLayout.addWidget(self.AboutTextEdit)
        self.AboutNotebook.addTab(self.AboutTab, '')
        self.CreditsTab = QtGui.QWidget()
        self.CreditsTab.setObjectName(u'CreditsTab')
        self.CreditsTabLayout = QtGui.QVBoxLayout(self.CreditsTab)
        self.CreditsTabLayout.setSpacing(0)
        self.CreditsTabLayout.setMargin(8)
        self.CreditsTabLayout.setObjectName(u'CreditsTabLayout')
        self.CreditsTextEdit = QtGui.QPlainTextEdit(self.CreditsTab)
        self.CreditsTextEdit.setReadOnly(True)
        self.CreditsTextEdit.setObjectName(u'CreditsTextEdit')
        self.CreditsTabLayout.addWidget(self.CreditsTextEdit)
        self.AboutNotebook.addTab(self.CreditsTab, '')
        self.LicenseTab = QtGui.QWidget()
        self.LicenseTab.setObjectName(u'LicenseTab')
        self.LicenseTabLayout = QtGui.QVBoxLayout(self.LicenseTab)
        self.LicenseTabLayout.setSpacing(8)
        self.LicenseTabLayout.setMargin(8)
        self.LicenseTabLayout.setObjectName(u'LicenseTabLayout')
        self.LicenseTextEdit = QtGui.QPlainTextEdit(self.LicenseTab)
        self.LicenseTextEdit.setReadOnly(True)
        self.LicenseTextEdit.setObjectName(u'LicenseTextEdit')
        self.LicenseTabLayout.addWidget(self.LicenseTextEdit)
        self.AboutNotebook.addTab(self.LicenseTab, '')
        self.AboutDialogLayout.addWidget(self.AboutNotebook)
        self.ButtonWidget = QtGui.QWidget(AboutDialog)
        self.ButtonWidget.setObjectName(u'ButtonWidget')
        self.ButtonWidgetLayout = QtGui.QHBoxLayout(self.ButtonWidget)
        self.ButtonWidgetLayout.setSpacing(8)
        self.ButtonWidgetLayout.setMargin(0)
        self.ButtonWidgetLayout.setObjectName(u'ButtonWidgetLayout')
        ButtonSpacer = QtGui.QSpacerItem(275, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ButtonWidgetLayout.addItem(ButtonSpacer)
        self.ContributeButton = QtGui.QPushButton(self.ButtonWidget)
        ContributeIcon = QtGui.QIcon()
        ContributeIcon.addPixmap(
            QtGui.QPixmap(u':/system/system_contribute.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ContributeButton.setIcon(ContributeIcon)
        self.ContributeButton.setObjectName(u'ContributeButton')
        self.ButtonWidgetLayout.addWidget(self.ContributeButton)
        self.CloseButton = QtGui.QPushButton(self.ButtonWidget)
        CloseIcon = QtGui.QIcon()
        CloseIcon.addPixmap(QtGui.QPixmap(u':/system/system_close.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(CloseIcon)
        self.CloseButton.setObjectName(u'CloseButton')
        self.ButtonWidgetLayout.addWidget(self.CloseButton)
        self.AboutDialogLayout.addWidget(self.ButtonWidget)

        self.retranslateUi(AboutDialog)
        self.AboutNotebook.setCurrentIndex(0)
        QtCore.QObject.connect(self.CloseButton, QtCore.SIGNAL(u'clicked()'),
            AboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(translate(u'AboutForm', u'About OpenLP'))
        self.AboutTextEdit.setPlainText(translate(u'AboutForm',
            u'OpenLP <version><revision> - Open Source Lyrics '
            u'Projection\n'
            u'\n'
            u'OpenLP is free church presentation software, or lyrics '
            u'projection software, used to display slides of songs, Bible '
            u'verses, videos, images, and even presentations (if '
            u'OpenOffice.org, PowerPoint or PowerPoint Viewer is installed) '
            u'for church worship using a computer and a data projector.\n'
            u'\n'
            u'Find out more about OpenLP: http://openlp.org/\n'
            u'\n'
            u'OpenLP is written and maintained by volunteers. If you would '
            u'like to see more free Christian software being written, please '
            u'consider contributing by using the button below.'
        ))
        self.AboutNotebook.setTabText(

            self.AboutNotebook.indexOf(self.AboutTab),
            translate(u'AboutForm', u'About'))
        self.CreditsTextEdit.setPlainText(translate(u'AboutForm', 
            u'Project Lead\n'
            u'    Raoul "superfly" Snyman\n'
            u'\n'
            u'Developers\n'
            u'    Tim "TRB143" Bentley\n'
            u'    Jonathan "gushie" Corwin\n'
            u'    Michael "cocooncrash" Gorven\n'
            u'    Scott "sguerrieri" Guerrieri\n'
            u'    Raoul "superfly" Snyman\n'
            u'    Martin "mijiti" Thompson\n'
            u'    Jon "Meths" Tibble\n'
            u'\n'
            u'Contributors\n'
            u'    Meinert "m2j" Jordan\n'
            u'    Christian "crichter" Richter\n'
            u'    Maikel Stuivenberg\n'
            u'    Carsten "catini" Tingaard\n'
            u'\n'
            u'Testers\n'
            u'    Philip "Phill" Ridout\n'
            u'    Wesley "wrst" Stout (lead)\n'
            u'\n'
            u'Packagers\n'
            u'    Thomas "tabthorpe" Abthorpe (FreeBSD)\n'
            u'    Tim "TRB143" Bentley (Fedora)\n'
            u'    Michael "cocooncrash" Gorven (Ubuntu)\n'
            u'    Matthias "matthub" Hub (Mac OS X)\n'
            u'    Raoul "superfly" Snyman (Windows)\n'
        ))
        self.AboutNotebook.setTabText(
            self.AboutNotebook.indexOf(self.CreditsTab),
            translate(u'AboutForm', u'Credits'))
        self.LicenseTextEdit.setPlainText(translate(u'AboutForm', 
            u'Copyright \xa9 2004-2010 Raoul Snyman\n'
            u'Portions copyright \xa9 2004-2010 '
            u'Tim Bentley, Jonathan Corwin, Michael Gorven, Scott Guerrieri, '
            u'Christian Richter, Maikel Stuivenberg, Martin Thompson, Jon '
            u'Tibble, Carsten Tinggaard\n'
            u'\n'
            u'This program is free software; you can redistribute it and/or '
            u'modify it under the terms of the GNU General Public License as '
            u'published by the Free Software Foundation; version 2 of the '
            u'License.\n'
            u'\n'
            u'This program is distributed in the hope that it will be useful, '
            u'but WITHOUT ANY WARRANTY; without even the implied warranty of '
            u'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See below '
            u'for more details.\n'
            u'\n'
            u'\n'
            u'GNU GENERAL PUBLIC LICENSE\n'
            u'Version 2, June 1991\n'
            u'\n'
            u'Copyright (C) 1989, 1991 Free Software Foundation, Inc., 51 '
            u'Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. '
            u'Everyone is permitted to copy and distribute verbatim copies of '
            u'this license document, but changing it is not allowed.\n'
            u'\n'
            u'Preamble\n'
            u'\n'
            u'The licenses for most software are designed to take away your '
            u'freedom to share and change it.  By contrast, the GNU General '
            u'Public License is intended to guarantee your freedom to share '
            u'and change free software--to make sure the software is free for '
            u'all its users.  This General Public License applies to most of '
            u'the Free Software Foundation\'s software and to any other '
            u'program whose authors commit to using it.  (Some other Free '
            u'Software Foundation software is covered by the GNU Lesser '
            u'General Public License instead.)  You can apply it to your '
            u'programs, too.\n'
            u'\n'
            u'When we speak of free software, we are referring to freedom, not '
            u'price.  Our General Public Licenses are designed to make sure '
            u'that you have the freedom to distribute copies of free software '
            u'(and charge for this service if you wish), that you receive '
            u'source code or can get it if you want it, that you can change '
            u'the software or use pieces of it in new free programs; and that '
            u'you know you can do these things.\n'
            u'\n'
            u'To protect your rights, we need to make restrictions that forbid '
            u'anyone to deny you these rights or to ask you to surrender the '
            u'rights. These restrictions translate to certain responsibilities '
            u'for you if you distribute copies of the software, or if you '
            u'modify it.\n'
            u'\n'
            u'For example, if you distribute copies of such a program, whether '
            u'gratis or for a fee, you must give the recipients all the rights '
            u'that you have.  You must make sure that they, too, receive or '
            u'can get the source code.  And you must show them these terms so '
            u'they know their rights.\n'
            u'\n'
            u'We protect your rights with two steps: (1) copyright the '
            u'software, and (2) offer you this license which gives you legal '
            u'permission to copy, distribute and/or modify the software.\n'
            u'\n'
            u'Also, for each author\'s protection and ours, we want to make '
            u'certain that everyone understands that there is no warranty for '
            u'this free software.  If the software is modified by someone else '
            u'and passed on, we want its recipients to know that what they '
            u'have is not the original, so that any problems introduced by '
            u'others will not reflect on the original authors\' reputations.\n'
            u'\n'
            u'Finally, any free program is threatened constantly by software '
            u'patents.  We wish to avoid the danger that redistributors of a '
            u'free program will individually obtain patent licenses, in effect '
            u'making the program proprietary.  To prevent this, we have made '
            u'it clear that any patent must be licensed for everyone\'s free '
            u'use or not licensed at all.\n'
            u'\n'
            u'The precise terms and conditions for copying, distribution and '
            u'modification follow.\n'
            u'\n'
            u'GNU GENERAL PUBLIC LICENSE\n'
            u'TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION\n'
            u'\n'
            u'0. This License applies to any program or other work which '
            u'contains a notice placed by the copyright holder saying it may '
            u'be distributed under the terms of this General Public License.  '
            u'The "Program", below, refers to any such program or work, and a '
            u'"work based on the Program" means either the Program or any '
            u'derivative work under copyright law: that is to say, a work '
            u'containing the Program or a portion of it, either verbatim or '
            u'with modifications and/or translated into another language.  '
            u'(Hereinafter, translation is included without limitation in the '
            u'term "modification".)  Each licensee is addressed as "you".\n'
            u'\n'
            u'Activities other than copying, distribution and modification are '
            u'not covered by this License; they are outside its scope.  The '
            u'act of running the Program is not restricted, and the output '
            u'from the Program is covered only if its contents constitute a '
            u'work based on the Program (independent of having been made by '
            u'running the Program). Whether that is true depends on what the '
            u'Program does.\n'
            u'\n'
            u'1. You may copy and distribute verbatim copies of the Program\'s '
            u'source code as you receive it, in any medium, provided that you '
            u'conspicuously and appropriately publish on each copy an '
            u'appropriate copyright notice and disclaimer of warranty; keep '
            u'intact all the notices that refer to this License and to the '
            u'absence of any warranty; and give any other recipients of the '
            u'Program a copy of this License along with the Program.\n'
            u'\n'
            u'You may charge a fee for the physical act of transferring a '
            u'copy, and you may at your option offer warranty protection in '
            u'exchange for a fee.\n'
            u'\n'
            u'2. You may modify your copy or copies of the Program or any '
            u'portion of it, thus forming a work based on the Program, and '
            u'copy and distribute such modifications or work under the terms '
            u'of Section 1 above, provided that you also meet all of these '
            u'conditions:\n'
            u'\n'
            u'a) You must cause the modified files to carry prominent notices '
            u'stating that you changed the files and the date of any change.\n'
            u'\n'
            u'b) You must cause any work that you distribute or publish, that '
            u'in whole or in part contains or is derived from the Program or '
            u'any part thereof, to be licensed as a whole at no charge to all '
            u'third parties under the terms of this License.\n'
            u'\n'
            u'c) If the modified program normally reads commands interactively '
            u'when run, you must cause it, when started running for such '
            u'interactive use in the most ordinary way, to print or display an '
            u'announcement including an appropriate copyright notice and a '
            u'notice that there is no warranty (or else, saying that you '
            u'provide a warranty) and that users may redistribute the program '
            u'under these conditions, and telling the user how to view a copy '
            u'of this License.  (Exception: if the Program itself is '
            u'interactive but does not normally print such an announcement, '
            u'your work based on the Program is not required to print an '
            u'announcement.)\n'
            u'\n'
            u'These requirements apply to the modified work as a whole.  If '
            u'identifiable sections of that work are not derived from the '
            u'Program, and can be reasonably considered independent and '
            u'separate works in themselves, then this License, and its terms, '
            u'do not apply to those sections when you distribute them as '
            u'separate works.  But when you distribute the same sections as '
            u'part of a whole which is a work based on the Program, the '
            u'distribution of the whole must be on the terms of this License, '
            u'whose permissions for other licensees extend to the entire '
            u'whole, and thus to each and every part regardless of who wrote '
            u'it.\n'
            u'\n'
            u'Thus, it is not the intent of this section to claim rights or '
            u'contest your rights to work written entirely by you; rather, the '
            u'intent is to exercise the right to control the distribution of '
            u'derivative or collective works based on the Program.\n'
            u'\n'
            u'In addition, mere aggregation of another work not based on the '
            u'Program with the Program (or with a work based on the Program) '
            u'on a volume of a storage or distribution medium does not bring '
            u'the other work under the scope of this License.\n'
            u'\n'
            u'3. You may copy and distribute the Program (or a work based on '
            u'it, under Section 2) in object code or executable form under the '
            u'terms of Sections 1 and 2 above provided that you also do one of '
            u'the following:\n'
            u'\n'
            u'a) Accompany it with the complete corresponding machine-readable '
            u'source code, which must be distributed under the terms of '
            u'Sections 1 and 2 above on a medium customarily used for software '
            u'interchange; or,\n'
            u'\n'
            u'b) Accompany it with a written offer, valid for at least three '
            u'years, to give any third party, for a charge no more than your '
            u'cost of physically performing source distribution, a complete '
            u'machine-readable copy of the corresponding source code, to be '
            u'distributed under the terms of Sections 1 and 2 above on a '
            u'medium customarily used for software interchange; or,\n'
            u'\n'
            u'c) Accompany it with the information you received as to the '
            u'offer to distribute corresponding source code.  (This '
            u'alternative is allowed only for noncommercial distribution and '
            u'only if you received the program in object code or executable '
            u'form with such an offer, in accord with Subsection b above.)\n'
            u'\n'
            u'The source code for a work means the preferred form of the work '
            u'for making modifications to it.  For an executable work, '
            u'complete source code means all the source code for all modules '
            u'it contains, plus any associated interface definition files, '
            u'plus the scripts used to control compilation and installation of '
            u'the executable.  However, as a special exception, the source '
            u'code distributed need not include anything that is normally '
            u'distributed (in either source or binary form) with the major '
            u'components (compiler, kernel, and so on) of the operating system '
            u'on which the executable runs, unless that component itself '
            u'accompanies the executable.\n'
            u'\n'
            u'If distribution of executable or object code is made by offering '
            u'access to copy from a designated place, then offering equivalent '
            u'access to copy the source code from the same place counts as '
            u'distribution of the source code, even though third parties are '
            u'not compelled to copy the source along with the object code.\n'
            u'\n'
            u'4. You may not copy, modify, sublicense, or distribute the '
            u'Program except as expressly provided under this License.  Any '
            u'attempt otherwise to copy, modify, sublicense or distribute the '
            u'Program is void, and will automatically terminate your rights '
            u'under this License. However, parties who have received copies, '
            u'or rights, from you under this License will not have their '
            u'licenses terminated so long as such parties remain in full '
            u'compliance.\n'
            u'\n'
            u'5. You are not required to accept this License, since you have '
            u'not signed it.  However, nothing else grants you permission to '
            u'modify or distribute the Program or its derivative works.  These '
            u'actions are prohibited by law if you do not accept this '
            u'License.  Therefore, by modifying or distributing the Program '
            u'(or any work based on the Program), you indicate your acceptance '
            u'of this License to do so, and all its terms and conditions for '
            u'copying, distributing or modifying the Program or works based on '
            u'it.\n'
            u'\n'
            u'6. Each time you redistribute the Program (or any work based on '
            u'the Program), the recipient automatically receives a license '
            u'from the original licensor to copy, distribute or modify the '
            u'Program subject to these terms and conditions.  You may not '
            u'impose any further restrictions on the recipients\' exercise of '
            u'the rights granted herein. You are not responsible for enforcing '
            u'compliance by third parties to this License.\n'
            u'\n'
            u'7. If, as a consequence of a court judgment or allegation of '
            u'patent infringement or for any other reason (not limited to '
            u'patent issues), conditions are imposed on you (whether by court '
            u'order, agreement or otherwise) that contradict the conditions of '
            u'this License, they do not excuse you from the conditions of this '
            u'License.  If you cannot distribute so as to satisfy '
            u'simultaneously your obligations under this License and any other '
            u'pertinent obligations, then as a consequence you may not '
            u'distribute the Program at all.  For example, if a patent license '
            u'would not permit royalty-free redistribution of the Program by '
            u'all those who receive copies directly or indirectly through you, '
            u'then the only way you could satisfy both it and this License '
            u'would be to refrain entirely from distribution of the Program.\n'
            u'\n'
            u'If any portion of this section is held invalid or unenforceable '
            u'under any particular circumstance, the balance of the section is '
            u'intended to apply and the section as a whole is intended to '
            u'apply in other circumstances.\n'
            u'\n'
            u'It is not the purpose of this section to induce you to infringe '
            u'any patents or other property right claims or to contest '
            u'validity of any such claims; this section has the sole purpose '
            u'of protecting the integrity of the free software distribution '
            u'system, which is implemented by public license practices.  Many '
            u'people have made generous contributions to the wide range of '
            u'software distributed through that system in reliance on '
            u'consistent application of that system; it is up to the '
            u'author/donor to decide if he or she is willing to distribute '
            u'software through any other system and a licensee cannot impose '
            u'that choice.\n'
            u'\n'
            u'This section is intended to make thoroughly clear what is '
            u'believed to be a consequence of the rest of this License.\n'
            u'\n'
            u'8. If the distribution and/or use of the Program is restricted '
            u'in certain countries either by patents or by copyrighted '
            u'interfaces, the original copyright holder who places the Program '
            u'under this License may add an explicit geographical distribution '
            u'limitation excluding those countries, so that distribution is '
            u'permitted only in or among countries not thus excluded.  In such '
            u'case, this License incorporates the limitation as if written in '
            u'the body of this License.\n'
            u'\n'
            u'9. The Free Software Foundation may publish revised and/or new '
            u'versions of the General Public License from time to time.  Such '
            u'new versions will be similar in spirit to the present version, '
            u'but may differ in detail to address new problems or concerns.\n'
            u'\n'
            u'Each version is given a distinguishing version number.  If the '
            u'Program specifies a version number of this License which applies '
            u'to it and \"any later version\', you have the option of '
            u'following the terms and conditions either of that version or of '
            u'any later version published by the Free Software Foundation.  If '
            u'the Program does not specify a version number of this License, '
            u'you may choose any version ever published by the Free Software '
            u'Foundation.\n'
            u'\n'
            u'10. If you wish to incorporate parts of the Program into other '
            u'free programs whose distribution conditions are different, write '
            u'to the author to ask for permission.  For software which is '
            u'copyrighted by the Free Software Foundation, write to the Free '
            u'Software Foundation; we sometimes make exceptions for this.  Our '
            u'decision will be guided by the two goals of preserving the free '
            u'status of all derivatives of our free software and of promoting '
            u'the sharing and reuse of software generally.\n'
            u'\n'
            u'NO WARRANTY\n'
            u'\n'
            u'11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO '
            u'WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE '
            u'LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT '
            u'HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT '
            u'WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, '
            u'BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY '
            u'AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS TO THE '
            u'QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE '
            u'PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY '
            u'SERVICING, REPAIR OR CORRECTION.\n'
            u'\n'
            u'12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO '
            u'IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY '
            u'MODIFY AND/OR REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE '
            u'LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, '
            u'INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR '
            u'INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS '
            u'OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY '
            u'YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH '
            u'ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN '
            u'ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n'
            u'\n'
            u'END OF TERMS AND CONDITIONS\n'
            u'\n'
            u'How to Apply These Terms to Your New Programs\n'
            u'\n'
            u'If you develop a new program, and you want it to be of the '
            u'greatest possible use to the public, the best way to achieve '
            u'this is to make it free software which everyone can redistribute '
            u'and change under these terms.\n'
            u'\n'
            u'To do so, attach the following notices to the program.  It is '
            u'safest to attach them to the start of each source file to most '
            u'effectively convey the exclusion of warranty; and each file '
            u'should have at least the "copyright" line and a pointer to where '
            u'the full notice is found.\n'
            u'\n'
            u'<one line to give the program\'s name and a brief idea of what '
            u'it does.>\n'
            u'Copyright (C) <year>  <name of author>\n'
            u'\n'
            u'This program is free software; you can redistribute it and/or '
            u'modify it under the terms of the GNU General Public License as '
            u'published by the Free Software Foundation; either version 2 of '
            u'the License, or (at your option) any later version.\n'
            u'\n'
            u'This program is distributed in the hope that it will be useful, '
            u'but WITHOUT ANY WARRANTY; without even the implied warranty of '
            u'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the '
            u'GNU General Public License for more details.\n'
            u'\n'
            u'You should have received a copy of the GNU General Public '
            u'License along with this program; if not, write to the Free '
            u'Software Foundation, Inc., 51 Franklin Street, Fifth Floor, '
            u'Boston, MA 02110-1301 USA.\n'
            u'\n'
            u'Also add information on how to contact you by electronic and '
            u'paper mail.\n'
            u'\n'
            u'If the program is interactive, make it output a short notice '
            u'like this when it starts in an interactive mode:\n'
            u'\n'
            u'Gnomovision version 69, Copyright (C) year name of author\n'
            u'Gnomovision comes with ABSOLUTELY NO WARRANTY; for details type '
            u'"show w".\n'
            u'This is free software, and you are welcome to redistribute it '
            u'under certain conditions; type "show c" for details.\n'
            u'\n'
            u'The hypothetical commands "show w" and "show c" should show '
            u'the appropriate parts of the General Public License.  Of course, '
            u'the commands you use may be called something other than "show '
            u'w" and "show c"; they could even be mouse-clicks or menu items--'
            u'whatever suits your program.\n'
            u'\n'
            u'You should also get your employer (if you work as a programmer) '
            u'or your school, if any, to sign a "copyright disclaimer" for the '
            u'program, if necessary.  Here is a sample; alter the names:\n'
            u'\n'
            u'Yoyodyne, Inc., hereby disclaims all copyright interest in the '
            u'program "Gnomovision" (which makes passes at compilers) written '
            u'by James Hacker.\n'
            u'\n'
            u'<signature of Ty Coon>, 1 April 1989\n'
            u'Ty Coon, President of Vice\n'
            u'\n'
            u'This General Public License does not permit incorporating your '
            u'program into proprietary programs.  If your program is a '
            u'subroutine library, you may consider it more useful to permit '
            u'linking proprietary applications with the library.  If this is '
            u'what you want to do, use the GNU Lesser General Public License '
            u'instead of this License.'))
        self.AboutNotebook.setTabText(
            self.AboutNotebook.indexOf(self.LicenseTab),
            translate(u'AboutForm', u'License'))
        self.ContributeButton.setText(translate(u'AboutForm', u'Contribute'))
        self.CloseButton.setText(translate(u'AboutForm', u'Close'))
