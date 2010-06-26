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

# OOo API documentation:
# http://api.openoffice.org/docs/common/ref/com/sun/star/presentation/XSlideShowController.html
# http://wiki.services.openoffice.org/wiki/Documentation/DevGuide/ProUNO/Basic/Getting_Information_about_UNO_Objects#Inspecting_interfaces_during_debugging
# http://docs.go-oo.org/sd/html/classsd_1_1SlideShow.html
# http://www.oooforum.org/forum/viewtopic.phtml?t=5252
# http://wiki.services.openoffice.org/wiki/Documentation/DevGuide/Working_with_Presentations
# http://mail.python.org/pipermail/python-win32/2008-January/006676.html
# http://www.linuxjournal.com/content/starting-stopping-and-connecting-openoffice-python
# http://nxsy.org/comparing-documents-with-openoffice-and-python

import logging
import os
import time

from openlp.core.lib import resize_image

if os.name == u'nt':
    from win32com.client import Dispatch
else:
    try:
        import uno
        from com.sun.star.beans import PropertyValue
        uno_available = True
    except ImportError:
        uno_available = False
        
from PyQt4 import QtCore

from presentationcontroller import PresentationController, PresentationDocument

log = logging.getLogger(__name__)

class ImpressController(PresentationController):
    """
    Class to control interactions with Impress presentations.
    It creates the runtime environment, loads and closes the presentation as
    well as triggering the correct activities based on the users input
    """
    log.info(u'ImpressController loaded')

    def __init__(self, plugin):
        """
        Initialise the class
        """
        log.debug(u'Initialising')
        PresentationController.__init__(self, plugin, u'Impress')
        self.supports = [u'.odp']
        self.alsosupports = [u'.ppt', u'.pps', u'.pptx', u'.ppsx']
        self.process = None
        self.desktop = None

    def check_available(self):
        """
        Impress is able to run on this machine
        """
        log.debug(u'check_available')
        if os.name == u'nt':
            return self.get_com_servicemanager() is not None
        else:
            return uno_available

    def start_process(self):
        """
        Loads a running version of OpenOffice in the background.
        It is not displayed to the user but is available to the UNO interface
        when required.
        """
        log.debug(u'start process Openoffice')
        if os.name == u'nt':
            self.manager = self.get_com_servicemanager()
            self.manager._FlagAsMethod(u'Bridge_GetStruct')
            self.manager._FlagAsMethod(u'Bridge_GetValueObject')
        else:
            # -headless
            cmd = u'openoffice.org -nologo -norestore -minimized -invisible -nofirststartwizard -accept="socket,host=localhost,port=2002;urp;"'
            self.process = QtCore.QProcess()
            self.process.startDetached(cmd)
            self.process.waitForStarted()

    def get_uno_desktop(self):
        log.debug(u'get UNO Desktop Openoffice')
        ctx = None
        loop = 0
        log.debug(u'get UNO Desktop Openoffice - getComponentContext')
        context = uno.getComponentContext()
        log.debug(u'get UNO Desktop Openoffice - createInstaneWithContext - '
            u'UnoUrlResolver')
        resolver = context.ServiceManager.createInstanceWithContext(
            u'com.sun.star.bridge.UnoUrlResolver', context)
        while ctx is None and loop < 3:
            try:
                log.debug(u'get UNO Desktop Openoffice - resolve')
                ctx = resolver.resolve(u'uno:socket,host=localhost,port=2002;'
                    u'urp;StarOffice.ComponentContext')
            except:
                log.exception(u'Unable to find running instance ')
                self.start_process()
                loop += 1
        try:
            self.manager = ctx.ServiceManager
            log.debug(u'get UNO Desktop Openoffice - createInstanceWithContext'
                u' - Desktop')
            desktop = self.manager.createInstanceWithContext(
                "com.sun.star.frame.Desktop", ctx )
            return desktop
        except:
            log.exception(u'Failed to get UNO desktop')
            return None

    def get_com_desktop(self):
        log.debug(u'get COM Desktop OpenOffice')
        return self.manager.createInstance(u'com.sun.star.frame.Desktop')

    def get_com_servicemanager(self):
        log.debug(u'get_com_servicemanager openoffice')
        try:
            return Dispatch(u'com.sun.star.ServiceManager')
        except pywintypes.com_error:
            log.exception(u'Failed to get COM service manager')
            return None

    def kill(self):
        """
        Called at system exit to clean up any running presentations
        """
        log.debug(u'Kill OpenOffice')
        while self.docs:
            self.docs[0].close_presentation()
        if os.name != u'nt':
            desktop = self.get_uno_desktop()
        else:
            desktop = self.get_com_desktop()
        #Sometimes we get a failure and desktop is None
        if not desktop:
            log.exception(u'Failed to terminate OpenOffice')
            return
        docs = desktop.getComponents()
        if docs.hasElements():
            log.debug(u'OpenOffice not terminated')
        else:
            try:
                desktop.terminate()
                log.debug(u'OpenOffice killed')
            except:
                log.exception(u'Failed to terminate OpenOffice')

    def add_doc(self, name):
        log.debug(u'Add Doc OpenOffice')
        doc = ImpressDocument(self, name)
        self.docs.append(doc)
        return doc

class ImpressDocument(PresentationDocument):
    def __init__(self, controller, presentation):
        log.debug(u'Init Presentation OpenOffice')
        PresentationDocument.__init__(self, controller, presentation)
        self.document = None
        self.presentation = None
        self.control = None

    def load_presentation(self):
        """
        Called when a presentation is added to the SlideController.
        It builds the environment, starts communcations with the background
        OpenOffice task started earlier.  If OpenOffice is not present is is
        started.  Once the environment is available the presentation is loaded
        and started.

        ``presentation``
        The file name of the presentatios to the run.
        """
        log.debug(u'Load Presentation OpenOffice')
        #print "s.dsk1 ", self.desktop
        if os.name == u'nt':
            desktop = self.controller.get_com_desktop()
            if desktop is None:
                self.controller.start_process()
                desktop = self.controller.get_com_desktop()
            url = u'file:///' + self.filepath.replace(u'\\', u'/').replace(
                u':', u'|').replace(u' ', u'%20')
        else:
            desktop = self.controller.get_uno_desktop()
            url = uno.systemPathToFileUrl(self.filepath)
        if desktop is None:
            return
        self.desktop = desktop
        #print "s.dsk2 ", self.desktop
        properties = []
        properties.append(self.create_property(u'Minimized', True))
        properties = tuple(properties)
        try:
            self.document = desktop.loadComponentFromURL(url, u'_blank',
                0, properties)
        except:
            log.exception(u'Failed to load presentation')
            return
        self.presentation = self.document.getPresentation()
        self.presentation.Display = \
            self.controller.plugin.render_manager.screens.current_display + 1
        self.control = None
        self.create_thumbnails()

    def create_thumbnails(self):
        """
        Create thumbnail images for presentation
        """
        log.debug(u'create thumbnails OpenOffice')
        if self.check_thumbnails():
            return
        if os.name == u'nt':
            thumbdir = u'file:///' + self.thumbnailpath.replace(
                u'\\', u'/').replace(u':', u'|').replace(u' ', u'%20')
        else:
            thumbdir = uno.systemPathToFileUrl(self.thumbnailpath)
        props = []
        props.append(self.create_property(u'FilterName', u'impress_png_Export'))
        props = tuple(props)
        doc = self.document
        pages = doc.getDrawPages()
        for idx in range(pages.getCount()):
            page = pages.getByIndex(idx)
            doc.getCurrentController().setCurrentPage(page)
            path = u'%s/%s%s.png' % (thumbdir, self.controller.thumbnailprefix,
                    unicode(idx + 1))
            try:
                doc.storeToURL(path , props)
                preview = resize_image(path, 640, 480)
                if os.path.exists(path):
                    os.remove(path)
                preview.save(path, u'png')
            except:
                log.exception(u'%s - Unable to store openoffice preview' % path)

    def create_property(self, name, value):
        log.debug(u'create property OpenOffice')
        if os.name == u'nt':
            prop = self.controller.manager.\
                Bridge_GetStruct(u'com.sun.star.beans.PropertyValue')
        else:
            prop = PropertyValue()
        prop.Name = name
        prop.Value = value
        return prop

    def close_presentation(self):
        """
        Close presentation and clean up objects
        Triggered by new object being added to SlideController or OpenLP
        being shutdown
        """
        log.debug(u'close Presentation OpenOffice')
        if self.document:
            if self.presentation:
                try:
                    self.presentation.end()
                    self.presentation = None
                    self.document.dispose()
                except:
                    #We tried!
                    pass
            self.document = None
        self.controller.remove_doc(self)

    def is_loaded(self):
        log.debug(u'is loaded OpenOffice')
        #print "is_loaded "
        if self.presentation is None or self.document is None:
            #print "no present or document"
            return False
        try:
            if self.document.getPresentation() is None:
                #print "no getPresentation"
                return False
        except:
            return False
        return True

    def is_active(self):
        log.debug(u'is active OpenOffice')
        #print "is_active "
        if not self.is_loaded():
            #print "False "
            return False
        #print "self.con ", self.control
        if self.control is None:
            return False
        return True

    def unblank_screen(self):
        log.debug(u'unblank screen OpenOffice')
        return self.control.resume()

    def blank_screen(self):
        log.debug(u'blank screen OpenOffice')
        self.control.blankScreen(0)

    def is_blank(self):
        """
        Returns true if screen is blank
        """
        log.debug(u'is blank OpenOffice')
        if self.control:
            return self.control.isPaused()
        else:
            return False

    def stop_presentation(self):
        log.debug(u'stop presentation OpenOffice')
        # deactivate should hide the screen according to docs, but doesn't
        #self.control.deactivate()
        self.presentation.end()
        self.control = None

    def start_presentation(self):
        log.debug(u'start presentation OpenOffice')
        if self.control is None or not self.control.isRunning():
            self.presentation.start()
            # start() returns before the getCurrentComponent is ready.
            # Try for 5 seconds
            i = 1
            while self.desktop.getCurrentComponent() is None and i < 50:
                time.sleep(0.1)
                i = i + 1
            self.control = \
                self.desktop.getCurrentComponent().Presentation.getController()
        else:
            self.control.activate()
            self.goto_slide(1)

    def get_slide_number(self):
        return self.control.getCurrentSlideIndex() + 1

    def get_slide_count(self):
        return self.document.getDrawPages().getCount()

    def goto_slide(self, slideno):
        self.control.gotoSlideIndex(slideno-1)

    def next_step(self):
        """
        Triggers the next effect of slide on the running presentation
        """
        self.control.gotoNextEffect()

    def previous_step(self):
        """
        Triggers the previous slide on the running presentation
        """
        self.control.gotoPreviousSlide()

    def get_slide_text(self, slide_no):
        """
        Returns the text on the slide

        ``slide_no``
        The slide the text is required for, starting at 1
        """
        doc = self.document
        pages = doc.getDrawPages()
        text = ''
        page = pages.getByIndex(slide_no - 1)
        for idx in range(page.getCount()):
            shape = page.getByIndex(idx)
            if shape.supportsService("com.sun.star.drawing.Text"):
                text += shape.getString() + '\n'
        return text

    def get_slide_notes(self, slide_no):
        """
        Returns the text on the slide

        ``slide_no``
        The slide the notes are required for, starting at 1
        """
        doc = self.document
        pages = doc.getDrawPages()
        text = ''
        page = pages.getByIndex(slide_no - 1)
        notes = page.getNotesPage()
        for idx in range(notes.getCount()):
            shape = notes.getByIndex(idx)
            if shape.supportsService("com.sun.star.drawing.Text"):
                text += shape.getString() + '\n'
        return text

