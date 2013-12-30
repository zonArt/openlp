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
These declarations have been extracted from the interface file created by makepy
"""
class constants:
    ppPlaceholderBody             =2          # from enum PpPlaceholderType

import os
if os.name=='nt':
    import pythoncom, pywintypes
    from win32com.client import Dispatch,DispatchBaseClass,CoClassBaseClass, \
        CLSIDToClass
    from pywintypes import IID
    import win32com


    # The following 3 lines may need tweaking for the particular server
    # Candidates are pythoncom.Missing, .Empty and .ArgNotFound
    defaultNamedOptArg=pythoncom.Empty
    defaultNamedNotOptArg=pythoncom.Empty
    defaultUnnamedArg=pythoncom.Empty


    CLSID = IID('{91493440-5A91-11CF-8700-00AA0060263B}')
    MajorVersion = 2
    MinorVersion = 11
    LibraryFlags = 8
    LCID = 0x0

    class EApplication:
        CLSID = CLSID_Sink = IID('{914934C2-5A91-11CF-8700-00AA0060263B}')
        coclass_clsid = IID('{91493441-5A91-11CF-8700-00AA0060263B}')
        _public_methods_ = [] # For COM Server support
        _dispid_to_func_ = {
                 2029 : "OnProtectedViewWindowActivate",
                 2015 : "OnPresentationPrint",
                 2013 : "OnSlideShowNextSlide",
                 2011 : "OnSlideShowBegin",
                 2001 : "OnWindowSelectionChange",
                 2005 : "OnPresentationSave",
                 2020 : "OnAfterNewPresentation",
                 2014 : "OnSlideShowEnd",
                 2028 : "OnProtectedViewWindowBeforeClose",
                 2025 : "OnPresentationBeforeClose",
                 2018 : "OnPresentationBeforeSave",
                 2010 : "OnWindowDeactivate",
                 2021 : "OnAfterPresentationOpen",
                 2027 : "OnProtectedViewWindowBeforeEdit",
                 2026 : "OnProtectedViewWindowOpen",
                 2023 : "OnSlideShowOnNext",
                 2012 : "OnSlideShowNextBuild",
                 2002 : "OnWindowBeforeRightClick",
                 2030 : "OnProtectedViewWindowDeactivate",
                 2016 : "OnSlideSelectionChanged",
                 2004 : "OnPresentationClose",
                 2017 : "OnColorSchemeChanged",
                 2019 : "OnSlideShowNextClick",
                 2006 : "OnPresentationOpen",
                 2003 : "OnWindowBeforeDoubleClick",
                 2031 : "OnPresentationCloseFinal",
                 2032 : "OnAfterDragDropOnSlide",
                 2033 : "OnAfterShapeSizeChange",
                 2009 : "OnWindowActivate",
                 2022 : "OnPresentationSync",
                 2007 : "OnNewPresentation",
                 2024 : "OnSlideShowOnPrevious",
                 2008 : "OnPresentationNewSlide",
            }

        def __init__(self, oobj = None):
            if oobj is None:
                self._olecp = None
            else:
                import win32com.server.util
                from win32com.server.policy import EventHandlerPolicy
                cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
                cp=cpc.FindConnectionPoint(self.CLSID_Sink)
                cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
                self._olecp,self._olecp_cookie = cp,cookie
        def __del__(self):
            try:
                self.close()
            except pythoncom.com_error:
                pass
        def close(self):
            if self._olecp is not None:
                cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
                cp.Unadvise(cookie)
        def _query_interface_(self, iid):
            import win32com.server.util
            if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

    class _Application(DispatchBaseClass):
        CLSID = IID('{91493442-5A91-11CF-8700-00AA0060263B}')
        coclass_clsid = IID('{91493441-5A91-11CF-8700-00AA0060263B}')

        def Activate(self):
            return self._oleobj_.InvokeTypes(2033, LCID, 1, (24, 0), (),)

        # Result is of type FileDialog
        # The method FileDialog is actually a property, but must be used as a method to correctly pass the arguments
        def FileDialog(self, Type=defaultNamedNotOptArg):
            ret = self._oleobj_.InvokeTypes(2045, LCID, 2, (9, 0), ((3, 1),),Type
                )
            if ret is not None:
                ret = Dispatch(ret, 'FileDialog', '{000C0362-0000-0000-C000-000000000046}')
            return ret

        def GetOptionFlag(self, Option=defaultNamedNotOptArg, Persist=False):
            return self._oleobj_.InvokeTypes(2043, LCID, 1, (11, 0), ((3, 1), (11, 49)),Option
                , Persist)

        def Help(self, HelpFile='vbapp10.chm', ContextID=0):
            return self._ApplyTypes_(2020, 1, (24, 32), ((8, 49), (3, 49)), 'Help', None,HelpFile
                , ContextID)

        def LaunchPublishSlidesDialog(self, SlideLibraryUrl=defaultNamedNotOptArg):
            return self._oleobj_.InvokeTypes(2054, LCID, 1, (24, 0), ((8, 1),),SlideLibraryUrl
                )

        def LaunchSendToPPTDialog(self, SlideUrls=defaultNamedNotOptArg):
            return self._oleobj_.InvokeTypes(2055, LCID, 1, (24, 0), ((16396, 1),),SlideUrls
                )

        # Result is of type Theme
        def OpenThemeFile(self, themeFileName=defaultNamedNotOptArg):
            ret = self._oleobj_.InvokeTypes(2069, LCID, 1, (9, 0), ((8, 1),),themeFileName
                )
            if ret is not None:
                ret = Dispatch(ret, 'OpenThemeFile', '{D9D60EB3-D4B4-4991-9C16-75585B3346BB}')
            return ret

        def PPFileDialog(self, Type=defaultNamedNotOptArg):
            ret = self._oleobj_.InvokeTypes(2023, LCID, 1, (13, 0), ((3, 1),),Type
                )
            if ret is not None:
                # See if this IUnknown is really an IDispatch
                try:
                    ret = ret.QueryInterface(pythoncom.IID_IDispatch)
                except pythoncom.error:
                    return ret
                ret = Dispatch(ret, 'PPFileDialog', None)
            return ret

        def Quit(self):
            return self._oleobj_.InvokeTypes(2021, LCID, 1, (24, 0), (),)

        def Run(self, *args):
            return self._get_good_object_(self._oleobj_.Invoke(*((2022,0,1,1)+args)),'Run')

        def SetOptionFlag(self, Option=defaultNamedNotOptArg, State=defaultNamedNotOptArg, Persist=False):
            return self._oleobj_.InvokeTypes(2044, LCID, 1, (24, 0), ((3, 1), (11, 1), (11, 49)),Option
                , State, Persist)

        def SetPerfMarker(self, Marker=defaultNamedNotOptArg):
            return self._oleobj_.InvokeTypes(2051, LCID, 1, (24, 0), ((3, 1),),Marker
                )

        def StartNewUndoEntry(self):
            return self._oleobj_.InvokeTypes(2067, LCID, 1, (24, 0), (),)

        _prop_map_get_ = {
            "Active": (2032, 2, (3, 0), (), "Active", None),
            "ActiveEncryptionSession": (2058, 2, (3, 0), (), "ActiveEncryptionSession", None),
            # Method 'ActivePresentation' returns object of type 'Presentation'
            "ActivePresentation": (2005, 2, (13, 0), (), "ActivePresentation", '{91493444-5A91-11CF-8700-00AA0060263B}'),
            "ActivePrinter": (2016, 2, (8, 0), (), "ActivePrinter", None),
            # Method 'ActiveProtectedViewWindow' returns object of type 'ProtectedViewWindow'
            "ActiveProtectedViewWindow": (2064, 2, (9, 0), (), "ActiveProtectedViewWindow", '{BA72E55A-4FF5-48F4-8215-5505F990966F}'),
            # Method 'ActiveWindow' returns object of type 'DocumentWindow'
            "ActiveWindow": (2004, 2, (9, 0), (), "ActiveWindow", '{91493457-5A91-11CF-8700-00AA0060263B}'),
            # Method 'AddIns' returns object of type 'AddIns'
            "AddIns": (2018, 2, (9, 0), (), "AddIns", '{91493460-5A91-11CF-8700-00AA0060263B}'),
            # Method 'AnswerWizard' returns object of type 'AnswerWizard'
            "AnswerWizard": (2034, 2, (9, 0), (), "AnswerWizard", '{000C0360-0000-0000-C000-000000000046}'),
            # Method 'Assistance' returns object of type 'IAssistance'
            "Assistance": (2057, 2, (9, 0), (), "Assistance", '{4291224C-DEFE-485B-8E69-6CF8AA85CB76}'),
            # Method 'Assistant' returns object of type 'Assistant'
            "Assistant": (2010, 2, (9, 0), (), "Assistant", '{000C0322-0000-0000-C000-000000000046}'),
            # Method 'AutoCorrect' returns object of type 'AutoCorrect'
            "AutoCorrect": (2052, 2, (9, 0), (), "AutoCorrect", '{914934ED-5A91-11CF-8700-00AA0060263B}'),
            "AutomationSecurity": (2047, 2, (3, 0), (), "AutomationSecurity", None),
            "Build": (2013, 2, (8, 0), (), "Build", None),
            # Method 'COMAddIns' returns object of type 'COMAddIns'
            "COMAddIns": (2035, 2, (9, 0), (), "COMAddIns", '{000C0339-0000-0000-C000-000000000046}'),
            "Caption": (2009, 2, (8, 0), (), "Caption", None),
            "ChartDataPointTrack": (2070, 2, (11, 0), (), "ChartDataPointTrack", None),
            # Method 'CommandBars' returns object of type 'CommandBars'
            "CommandBars": (2007, 2, (13, 0), (), "CommandBars", '{55F88893-7708-11D1-ACEB-006008961DA5}'),
            "Creator": (2017, 2, (3, 0), (), "Creator", None),
            # Method 'DefaultWebOptions' returns object of type 'DefaultWebOptions'
            "DefaultWebOptions": (2037, 2, (9, 0), (), "DefaultWebOptions", '{914934CD-5A91-11CF-8700-00AA0060263B}'),
            "Dialogs": (2003, 2, (13, 0), (), "Dialogs", None),
            "DisplayAlerts": (2049, 2, (3, 0), (), "DisplayAlerts", None),
            "DisplayDocumentInformationPanel": (2056, 2, (11, 0), (), "DisplayDocumentInformationPanel", None),
            "DisplayGridLines": (2046, 2, (3, 0), (), "DisplayGridLines", None),
            "DisplayGuides": (2071, 2, (3, 0), (), "DisplayGuides", None),
            "FeatureInstall": (2042, 2, (3, 0), (), "FeatureInstall", None),
            # Method 'FileConverters' returns object of type 'FileConverters'
            "FileConverters": (2059, 2, (9, 0), (), "FileConverters", '{92D41A50-F07E-4CA4-AF6F-BEF486AA4E6F}'),
            # Method 'FileFind' returns object of type 'IFind'
            "FileFind": (2012, 2, (9, 0), (), "FileFind", '{000C0337-0000-0000-C000-000000000046}'),
            # Method 'FileSearch' returns object of type 'FileSearch'
            "FileSearch": (2011, 2, (9, 0), (), "FileSearch", '{000C0332-0000-0000-C000-000000000046}'),
            "FileValidation": (2068, 2, (3, 0), (), "FileValidation", None),
            "HWND": (2031, 2, (3, 0), (), "HWND", None),
            "Height": (2028, 2, (4, 0), (), "Height", None),
            "IsSandboxed": (2065, 2, (11, 0), (), "IsSandboxed", None),
            # Method 'LanguageSettings' returns object of type 'LanguageSettings'
            "LanguageSettings": (2038, 2, (9, 0), (), "LanguageSettings", '{000C0353-0000-0000-C000-000000000046}'),
            "Left": (2025, 2, (4, 0), (), "Left", None),
            "Marker": (2041, 2, (13, 0), (), "Marker", None),
            # Method 'MsoDebugOptions' returns object of type 'MsoDebugOptions'
            "MsoDebugOptions": (2039, 2, (9, 0), (), "MsoDebugOptions", '{000C035A-0000-0000-C000-000000000046}'),
            "Name": (0, 2, (8, 0), (), "Name", None),
            # Method 'NewPresentation' returns object of type 'NewFile'
            "NewPresentation": (2048, 2, (9, 0), (), "NewPresentation", '{000C0936-0000-0000-C000-000000000046}'),
            "OperatingSystem": (2015, 2, (8, 0), (), "OperatingSystem", None),
            # Method 'Options' returns object of type 'Options'
            "Options": (2053, 2, (9, 0), (), "Options", '{914934EE-5A91-11CF-8700-00AA0060263B}'),
            "Path": (2008, 2, (8, 0), (), "Path", None),
            # Method 'Presentations' returns object of type 'Presentations'
            "Presentations": (2001, 2, (9, 0), (), "Presentations", '{91493462-5A91-11CF-8700-00AA0060263B}'),
            "ProductCode": (2036, 2, (8, 0), (), "ProductCode", None),
            # Method 'ProtectedViewWindows' returns object of type 'ProtectedViewWindows'
            "ProtectedViewWindows": (2063, 2, (9, 0), (), "ProtectedViewWindows", '{BA72E559-4FF5-48F4-8215-5505F990966F}'),
            # Method 'ResampleMediaTasks' returns object of type 'ResampleMediaTasks'
            "ResampleMediaTasks": (2066, 2, (9, 0), (), "ResampleMediaTasks", '{BA72E554-4FF5-48F4-8215-5505F990966F}'),
            "ShowStartupDialog": (2050, 2, (3, 0), (), "ShowStartupDialog", None),
            "ShowWindowsInTaskbar": (2040, 2, (3, 0), (), "ShowWindowsInTaskbar", None),
            # Method 'SlideShowWindows' returns object of type 'SlideShowWindows'
            "SlideShowWindows": (2006, 2, (9, 0), (), "SlideShowWindows", '{91493456-5A91-11CF-8700-00AA0060263B}'),
            # Method 'SmartArtColors' returns object of type 'SmartArtColors'
            "SmartArtColors": (2062, 2, (9, 0), (), "SmartArtColors", '{000C03CD-0000-0000-C000-000000000046}'),
            # Method 'SmartArtLayouts' returns object of type 'SmartArtLayouts'
            "SmartArtLayouts": (2060, 2, (9, 0), (), "SmartArtLayouts", '{000C03C9-0000-0000-C000-000000000046}'),
            # Method 'SmartArtQuickStyles' returns object of type 'SmartArtQuickStyles'
            "SmartArtQuickStyles": (2061, 2, (9, 0), (), "SmartArtQuickStyles", '{000C03CB-0000-0000-C000-000000000046}'),
            "Top": (2026, 2, (4, 0), (), "Top", None),
            # Method 'VBE' returns object of type 'VBE'
            "VBE": (2019, 2, (9, 0), (), "VBE", '{0002E166-0000-0000-C000-000000000046}'),
            "Version": (2014, 2, (8, 0), (), "Version", None),
            "Visible": (2030, 2, (3, 0), (), "Visible", None),
            "Width": (2027, 2, (4, 0), (), "Width", None),
            "WindowState": (2029, 2, (3, 0), (), "WindowState", None),
            # Method 'Windows' returns object of type 'DocumentWindows'
            "Windows": (2002, 2, (9, 0), (), "Windows", '{91493455-5A91-11CF-8700-00AA0060263B}'),
        }
        _prop_map_put_ = {
            "AutomationSecurity": ((2047, LCID, 4, 0),()),
            "Caption": ((2009, LCID, 4, 0),()),
            "ChartDataPointTrack": ((2070, LCID, 4, 0),()),
            "DisplayAlerts": ((2049, LCID, 4, 0),()),
            "DisplayDocumentInformationPanel": ((2056, LCID, 4, 0),()),
            "DisplayGridLines": ((2046, LCID, 4, 0),()),
            "DisplayGuides": ((2071, LCID, 4, 0),()),
            "FeatureInstall": ((2042, LCID, 4, 0),()),
            "FileValidation": ((2068, LCID, 4, 0),()),
            "Height": ((2028, LCID, 4, 0),()),
            "Left": ((2025, LCID, 4, 0),()),
            "ShowStartupDialog": ((2050, LCID, 4, 0),()),
            "ShowWindowsInTaskbar": ((2040, LCID, 4, 0),()),
            "Top": ((2026, LCID, 4, 0),()),
            "Visible": ((2030, LCID, 4, 0),()),
            "Width": ((2027, LCID, 4, 0),()),
            "WindowState": ((2029, LCID, 4, 0),()),
        }
        # Default property for this class is 'Name'
        def __call__(self):
            return self._ApplyTypes_(*(0, 2, (8, 0), (), "Name", None))
        def __str__(self, *args):
            return str(self.__call__(*args))
        def __int__(self, *args):
            return int(self.__call__(*args))
        def __iter__(self):
            "Return a Python iterator for this object"
            try:
                ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
            except pythoncom.error:
                raise TypeError("This object does not support enumeration")
            return win32com.client.util.Iterator(ob, None)

    # This CoClass is known by the name 'PowerPoint.Application.15'
    class Application(CoClassBaseClass): # A CoClass
        CLSID = IID('{91493441-5A91-11CF-8700-00AA0060263B}')
        coclass_sources = [
            EApplication,
        ]
        default_source = EApplication
        coclass_interfaces = [
            _Application,
        ]
        default_interface = _Application


    CLSIDToClassMap = {
        '{91493441-5A91-11CF-8700-00AA0060263B}' : Application,
        '{91493442-5A91-11CF-8700-00AA0060263B}' : _Application,
        '{914934C2-5A91-11CF-8700-00AA0060263B}' : EApplication,
    }

    CLSIDToPackageMap = {}
    win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
