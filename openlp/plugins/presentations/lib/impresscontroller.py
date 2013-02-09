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

if os.name == u'nt':
    from win32com.client import Dispatch
    import pywintypes
    # Declare an empty exception to match the exception imported from UNO
    class ErrorCodeIOException(Exception):
        pass
else:
    try:
        import uno
        from com.sun.star.beans import PropertyValue
        from com.sun.star.task import ErrorCodeIOException
        uno_available = True
    except ImportError:
        uno_available = False

from PyQt4 import QtCore

from openlp.core.utils import delete_file, get_uno_command, get_uno_instance
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
        PresentationController.__init__(self, plugin, u'Impress', ImpressDocument)
        self.supports = [u'odp']
        self.alsosupports = [u'ppt', u'pps', u'pptx', u'ppsx']
        self.process = None
        self.desktop = None
        self.manager = None

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
            cmd = get_uno_command()
            self.process = QtCore.QProcess()
            self.process.startDetached(cmd)

    def get_uno_desktop(self):
        """
        On non-Windows platforms, use Uno. Get the OpenOffice desktop
        which will be used to manage impress
        """
        log.debug(u'get UNO Desktop Openoffice')
        uno_instance = None
        loop = 0
        log.debug(u'get UNO Desktop Openoffice - getComponentContext')
        context = uno.getComponentContext()
        log.debug(u'get UNO Desktop Openoffice - createInstaneWithContext - UnoUrlResolver')
        resolver = context.ServiceManager.createInstanceWithContext(u'com.sun.star.bridge.UnoUrlResolver', context)
        while uno_instance is None and loop < 3:
            try:
                uno_instance = get_uno_instance(resolver)
            except:
                log.warn(u'Unable to find running instance ')
                self.start_process()
                loop += 1
        try:
            self.manager = uno_instance.ServiceManager
            log.debug(u'get UNO Desktop Openoffice - createInstanceWithContext'
                u' - Desktop')
            desktop = self.manager.createInstanceWithContext("com.sun.star.frame.Desktop", uno_instance)
            return desktop
        except:
            log.warn(u'Failed to get UNO desktop')
            return None

    def get_com_desktop(self):
        """
        On Windows platforms, use COM. Return the desktop object which
        will be used to manage Impress
        """
        log.debug(u'get COM Desktop OpenOffice')
        if not self.manager:
            return None
        desktop = None
        try:
            desktop = self.manager.createInstance(u'com.sun.star.frame.Desktop')
        except (AttributeError, pywintypes.com_error):
            log.warn(u'Failure to find desktop - Impress may have closed')
        return desktop if desktop else None

    def get_com_servicemanager(self):
        """
        Return the OOo service manager for windows
        """
        log.debug(u'get_com_servicemanager openoffice')
        try:
            return Dispatch(u'com.sun.star.ServiceManager')
        except pywintypes.com_error:
            log.warn(u'Failed to get COM service manager. Impress Controller has been disabled')
            return None

    def kill(self):
        """
        Called at system exit to clean up any running presentations
        """
        log.debug(u'Kill OpenOffice')
        while self.docs:
            self.docs[0].close_presentation()
        desktop = None
        try:
            if os.name != u'nt':
                desktop = self.get_uno_desktop()
            else:
                desktop = self.get_com_desktop()
        except:
            log.warn(u'Failed to find an OpenOffice desktop to terminate')
        if not desktop:
            return
        docs = desktop.getComponents()
        cnt = 0
        if docs.hasElements():
            list = docs.createEnumeration()
            while list.hasMoreElements():
                doc = list.nextElement()
                if doc.getImplementationName() != u'com.sun.star.comp.framework.BackingComp':
                    cnt += 1
        if cnt > 0:
            log.debug(u'OpenOffice not terminated as docs are still open')
        else:
            try:
                desktop.terminate()
                log.debug(u'OpenOffice killed')
            except:
                log.warn(u'Failed to terminate OpenOffice')


class ImpressDocument(PresentationDocument):
    """
    Class which holds information and controls a single presentation
    """

    def __init__(self, controller, presentation):
        """
        Constructor, store information about the file and initialise
        """
        log.debug(u'Init Presentation OpenOffice')
        PresentationDocument.__init__(self, controller, presentation)
        self.document = None
        self.presentation = None
        self.control = None

    def load_presentation(self):
        """
        Called when a presentation is added to the SlideController.
        It builds the environment, starts communcations with the background
        OpenOffice task started earlier. If OpenOffice is not present is is
        started. Once the environment is available the presentation is loaded
        and started.
        """
        log.debug(u'Load Presentation OpenOffice')
        if os.name == u'nt':
            desktop = self.controller.get_com_desktop()
            if desktop is None:
                self.controller.start_process()
                desktop = self.controller.get_com_desktop()
            url = u'file:///' + self.filepath.replace(u'\\', u'/').replace(u':', u'|').replace(u' ', u'%20')
        else:
            desktop = self.controller.get_uno_desktop()
            url = uno.systemPathToFileUrl(self.filepath)
        if desktop is None:
            return False
        self.desktop = desktop
        properties = []
        if os.name != u'nt':
            # Recent versions of Impress on Windows won't start the presentation
            # if it starts as minimized. It seems OK on Linux though.
            properties.append(self.create_property(u'Minimized', True))
        properties = tuple(properties)
        try:
            self.document = desktop.loadComponentFromURL(url, u'_blank',
                0, properties)
        except:
            log.warn(u'Failed to load presentation %s' % url)
            return False
        if os.name == u'nt':
            # As we can't start minimized the Impress window gets in the way.
            # Either window.setPosSize(0, 0, 200, 400, 12) or .setVisible(False)
            window = self.document.getCurrentController().getFrame().getContainerWindow()
            window.setVisible(False)
        self.presentation = self.document.getPresentation()
        self.presentation.Display = self.controller.plugin.renderer.screens.current[u'number'] + 1
        self.control = None
        self.create_thumbnails()
        return True

    def create_thumbnails(self):
        """
        Create thumbnail images for presentation
        """
        log.debug(u'create thumbnails OpenOffice')
        if self.check_thumbnails():
            return
        if os.name == u'nt':
            thumbdirurl = u'file:///' + self.get_temp_folder().replace(u'\\', u'/') \
                .replace(u':', u'|').replace(u' ', u'%20')
        else:
            thumbdirurl = uno.systemPathToFileUrl(self.get_temp_folder())
        props = []
        props.append(self.create_property(u'FilterName', u'impress_png_Export'))
        props = tuple(props)
        doc = self.document
        pages = doc.getDrawPages()
        if not pages:
            return
        if not os.path.isdir(self.get_temp_folder()):
            os.makedirs(self.get_temp_folder())
        for idx in range(pages.getCount()):
            page = pages.getByIndex(idx)
            doc.getCurrentController().setCurrentPage(page)
            urlpath = u'%s/%s.png' % (thumbdirurl, unicode(idx + 1))
            path = os.path.join(self.get_temp_folder(), unicode(idx + 1) + u'.png')
            try:
                doc.storeToURL(urlpath, props)
                self.convert_thumbnail(path, idx + 1)
                delete_file(path)
            except ErrorCodeIOException, exception:
                log.exception(u'ERROR! ErrorCodeIOException %d' % exception.ErrCode)
            except:
                log.exception(u'%s - Unable to store openoffice preview' % path)

    def create_property(self, name, value):
        """
        Create an OOo style property object which are passed into some
        Uno methods
        """
        log.debug(u'create property OpenOffice')
        if os.name == u'nt':
            prop = self.controller.manager.Bridge_GetStruct(u'com.sun.star.beans.PropertyValue')
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
                    log.warn("Closing presentation failed")
            self.document = None
        self.controller.remove_doc(self)

    def is_loaded(self):
        """
        Returns true if a presentation is loaded
        """
        log.debug(u'is loaded OpenOffice')
        if self.presentation is None or self.document is None:
            log.debug("is_loaded: no presentation or document")
            return False
        try:
            if self.document.getPresentation() is None:
                log.debug("getPresentation failed to find a presentation")
                return False
        except:
            log.warn("getPresentation failed to find a presentation")
            return False
        return True

    def is_active(self):
        """
        Returns true if a presentation is active and running
        """
        log.debug(u'is active OpenOffice')
        if not self.is_loaded():
            return False
        return self.control.isRunning() if self.control else False

    def unblank_screen(self):
        """
        Unblanks the screen
        """
        log.debug(u'unblank screen OpenOffice')
        return self.control.resume()

    def blank_screen(self):
        """
        Blanks the screen
        """
        log.debug(u'blank screen OpenOffice')
        self.control.blankScreen(0)

    def is_blank(self):
        """
        Returns true if screen is blank
        """
        log.debug(u'is blank OpenOffice')
        if self.control and self.control.isRunning():
            return self.control.isPaused()
        else:
            return False

    def stop_presentation(self):
        """
        Stop the presentation, remove from screen
        """
        log.debug(u'stop presentation OpenOffice')
        # deactivate should hide the screen according to docs, but doesn't
        #self.control.deactivate()
        self.presentation.end()
        self.control = None

    def start_presentation(self):
        """
        Start the presentation from the beginning
        """
        log.debug(u'start presentation OpenOffice')
        if self.control is None or not self.control.isRunning():
            self.presentation.start()
            self.control = self.presentation.getController()
            # start() returns before the Component is ready.
            # Try for 15 seconds
            i = 1
            while not self.control and i < 150:
                time.sleep(0.1)
                i += 1
                self.control = self.presentation.getController()
        else:
            self.control.activate()
            self.goto_slide(1)

    def get_slide_number(self):
        """
        Return the current slide number on the screen, from 1
        """
        return self.control.getCurrentSlideIndex() + 1

    def get_slide_count(self):
        """
        Return the total number of slides
        """
        return self.document.getDrawPages().getCount()

    def goto_slide(self, slideno):
        """
        Go to a specific slide (from 1)
        """
        self.control.gotoSlideIndex(slideno-1)

    def next_step(self):
        """
        Triggers the next effect of slide on the running presentation
        """
        is_paused = self.control.isPaused()
        self.control.gotoNextEffect()
        time.sleep(0.1)
        if not is_paused and self.control.isPaused():
            self.control.gotoPreviousEffect()

    def previous_step(self):
        """
        Triggers the previous slide on the running presentation
        """
        self.control.gotoPreviousSlide()

    def get_slide_text(self, slide_no):
        """
        Returns the text on the slide.

        ``slide_no``
            The slide the text is required for, starting at 1
        """
        return self.__get_text_from_page(slide_no)

    def get_slide_notes(self, slide_no):
        """
        Returns the text in the slide notes.

        ``slide_no``
            The slide the notes are required for, starting at 1
        """
        return self.__get_text_from_page(slide_no, True)

    def __get_text_from_page(self, slide_no, notes=False):
        """
        Return any text extracted from the presentation page.

        ``notes``
            A boolean. If set the method searches the notes of the slide.
        """
        text = ''
        pages = self.document.getDrawPages()
        page = pages.getByIndex(slide_no - 1)
        if notes:
            page = page.getNotesPage()
        for idx in range(page.getCount()):
            shape = page.getByIndex(idx)
            if shape.supportsService("com.sun.star.drawing.Text"):
                text += shape.getString() + '\n'
        return text
