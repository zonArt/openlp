# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Ken Roberts, Simon Scudder,               #
# Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon Tibble,             #
# Dave Warnock, Frode Woldsund, Martin Zibricky, Patrick Zimmermann           #
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
The :mod:`projector.pjlink1` module provides the necessary functions
        for connecting to a PJLink-capable projector.

    See PJLink Specifications for Class 1 for details.

    NOTE:
      Function names follow  the following syntax:
            def process_CCCC(...):
      WHERE:
            CCCC = PJLink command being processed.

      See PJLINK_FUNC(...) for command returned from projector.

"""

import logging
log = logging.getLogger(__name__)

log.debug('projectorpjlink1 loaded')

__all__ = ['PJLink1']

from time import sleep
from codecs import decode, encode

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt4.QtNetwork import QAbstractSocket, QTcpSocket

from openlp.core.common import translate, qmd5_hash
from openlp.core.lib.projector.constants import *

# Shortcuts
SocketError = QAbstractSocket.SocketError
SocketSTate = QAbstractSocket.SocketState

PJLINK_PREFIX = '%'
PJLINK_CLASS = '1'
PJLINK_HEADER = '%s%s' % (PJLINK_PREFIX, PJLINK_CLASS)
PJLINK_SUFFIX = CR


class PJLink1(QTcpSocket):
    """
    Socket service for connecting to a PJLink-capable projector.
    """
    changeStatus = pyqtSignal(str, int, str)
    projectorNetwork = pyqtSignal(int)  # Projector network activity
    projectorStatus = pyqtSignal(int)

    def __init__(self, name=None, ip=None, port=PJLINK_PORT, pin=None, *args, **kwargs):
        """
        Setup for instance.

        :param name: Display name
        :param ip: IP address to connect to
        :param port: Port to use. Default to PJLINK_PORT
        :param pin: Access pin (if needed)

        Optional parameters
        :param dbid: Database ID number
        :param location: Location where projector is physically located
        :param notes: Extra notes about the projector
        """
        log.debug('PJlink(args="%s" kwargs="%s")' % (args, kwargs))
        self.name = name
        self.ip = ip
        self.port = port
        self.pin = pin
        super(PJLink1, self).__init__()
        self.dbid = None
        self.location = None
        self.notes = None
        # Allowances for Projector Wizard option
        if 'dbid' in kwargs:
            self.dbid = kwargs['dbid']
        else:
            self.dbid = None
        if 'location' in kwargs:
            self.location = kwargs['location']
        else:
            self.location = None
        if 'notes' in kwargs:
            self.notes = kwargs['notes']
        else:
            self.notes = None
        if 'wizard' in kwargs:
            self.new_wizard = True
        else:
            self.new_wizard = False
        self.i_am_running = False
        self.status_connect = S_NOT_CONNECTED
        self.last_command = ''
        self.projector_status = S_NOT_CONNECTED
        self.error_status = S_OK
        # Socket information
        # Account for self.readLine appending \0 and/or exraneous \r
        self.maxSize = PJLINK_MAX_PACKET + 2
        self.setReadBufferSize(self.maxSize)
        # PJLink projector information
        self.pjlink_class = '1'  # Default class
        self.power = S_OFF
        self.pjlink_name = None
        self.manufacturer = None
        self.model = None
        self.shutter = None
        self.mute = None
        self.lamp = None
        self.fan = None
        self.source_available = None
        self.source = None
        self.projector_errors = None
        # Set from ProjectorManager.add_projector()
        self.widget = None  # QListBox entry
        self.timer = None  # Timer that calls the poll_loop
        # Map command returned to function
        self.PJLINK1_FUNC = {'AVMT': self.process_avmt,
                             'CLSS': self.process_clss,
                             'ERST': self.process_erst,
                             'INFO': self.process_info,
                             'INF1': self.process_inf1,
                             'INF2': self.process_inf2,
                             'INPT': self.process_inpt,
                             'INST': self.process_inst,
                             'LAMP': self.process_lamp,
                             'NAME': self.process_name,
                             'POWR': self.process_powr
                             }

    def thread_started(self):
        """
        Connects signals to methods when thread is started.
        """
        log.debug('(%s) Thread starting' % self.ip)
        self.i_am_running = True
        self.connected.connect(self.check_login)
        self.disconnected.connect(self.disconnect_from_host)
        self.error.connect(self.get_error)

    def thread_stopped(self):
        """
        Cleanups when thread is stopped.
        """
        log.debug('(%s) Thread stopped' % self.ip)
        self.connected.disconnect(self.check_login)
        self.disconnected.disconnect(self.disconnect_from_host)
        self.error.disconnect(self.get_error)
        self.disconnect_from_host()
        self.deleteLater()
        self.i_am_running = False

    def poll_loop(self):
        """
        Called by QTimer in ProjectorManager.ProjectorItem.
        Retrieves status information.
        """
        if self.state() != self.ConnectedState:
            return
        log.debug('(%s) Updating projector status' % self.ip)
        # Reset timer in case we were called from a set command
        self.timer.start()
        for i in ['POWR', 'ERST', 'LAMP', 'AVMT', 'INPT']:
            self.send_command(i)
            self.waitForReadyRead()
        if self.source_available is None:
            self.send_command('INST')

    def _get_status(self, status):
        """
        Helper to retrieve status/error codes and convert to strings.
        """
        # Return the status code as a string
        if status in ERROR_STRING:
            return (ERROR_STRING[status], ERROR_MSG[status])
        elif status in STATUS_STRING:
            return (STATUS_STRING[status], ERROR_MSG[status])
        else:
            return (status, 'Unknown status')

    def change_status(self, status, msg=None):
        """
        Check connection/error status, set status for projector, then emit status change signal
        for gui to allow changing the icons.
        """
        message = 'No message' if msg is None else msg
        (code, message) = self._get_status(status)
        if msg is not None:
            message = msg
        if status in CONNECTION_ERRORS:
            # Projector, connection state
            self.projector_status = self.error_status = self.status_connect = E_NOT_CONNECTED
        elif status >= S_NOT_CONNECTED and status < S_STATUS:
            self.status_connect = status
            self.projector_status = S_NOT_CONNECTED
        elif status < S_NETWORK_SENDING:
            self.status_connect = S_CONNECTED
            self.projector_status = status
        (status_code, status_message) = self._get_status(self.status_connect)
        log.debug('(%s) status_connect: %s: %s' % (self.ip, status_code, status_message if msg is None else msg))
        (status_code, status_message) = self._get_status(self.projector_status)
        log.debug('(%s) projector_status: %s: %s' % (self.ip, status_code, status_message if msg is None else msg))
        (status_code, status_message) = self._get_status(self.error_status)
        log.debug('(%s) error_status: %s: %s' % (self.ip, status_code, status_message if msg is None else msg))
        self.changeStatus.emit(self.ip, status, message)

    def check_command(self, cmd):
        """
        Verifies command is valid based on PJLink class.
        """
        return self.pjlink_class in PJLINK_VALID_CMD and \
            cmd in PJLINK_VALID_CMD[self.pjlink_class]

    def check_login(self):
        """
        Processes the initial connection and authentication (if needed).
        """
        self.waitForReadyRead(5000)  # 5 seconds should be more than enough
        read = self.readLine(self.maxSize)
        dontcare = self.readLine(self.maxSize)  # Clean out the trailing \r\n
        if len(read) < 8:
            log.warn('(%s) Not enough data read)' % self.ip)
            return
        data = decode(read, 'ascii')
        # Possibility of extraneous data on input when reading.
        # Clean out extraneous characters in buffer.
        dontcare = self.readLine(self.maxSize)
        log.debug('(%s) check_login() read "%s"' % (self.ip, data))
        # At this point, we should only have the initial login prompt with
        # possible authentication
        if not data.upper().startswith('PJLINK'):
            # Invalid response
            return self.disconnect_from_host()
        data_check = data.strip().split(' ')
        log.debug('(%s) data_check="%s"' % (self.ip, data_check))
        salt = None
        # PJLink initial login will be:
        # 'PJLink 0' - Unauthenticated login - no extra steps required.
        # 'PJLink 1 XXXXXX' Authenticated login - extra processing required.
        if data_check[1] == '1':
            # Authenticated login with salt
            salt = qmd5_hash(salt=data_check[2], data=self.pin)
        # We're connected at this point, so go ahead and do regular I/O
        self.readyRead.connect(self.get_data)
        # Initial data we should know about
        self.send_command(cmd='CLSS', salt=salt)
        self.waitForReadyRead()
        # These should never change once we get this information
        if self.manufacturer is None:
            for i in ['INF1', 'INF2', 'INFO', 'NAME', 'INST']:
                self.send_command(cmd=i)
                self.waitForReadyRead()
        self.change_status(S_CONNECTED)
        if not self.new_wizard:
            self.timer.start()
            self.poll_loop()

    def get_data(self):
        """
        Socket interface to retrieve data.
        """
        log.debug('(%s) Reading data' % self.ip)
        if self.state() != self.ConnectedState:
            log.debug('(%s) get_data(): Not connected - returning' % self.ip)
            return
        read = self.readLine(self.maxSize)
        if read == -1:
            # No data available
            log.debug('(%s) get_data(): No data available (-1)' % self.ip)
            return
        self.projectorNetwork.emit(S_NETWORK_RECEIVED)
        data_in = decode(read, 'ascii')
        data = data_in.strip()
        if len(data) < 8:
            # Not enough data for a packet
            log.debug('(%s) get_data(): Packet length < 8: "%s"' % (self.ip, data))
            return
        log.debug('(%s) Checking new data "%s"' % (self.ip, data))
        if '=' in data:
            pass
        else:
            log.warn('(%s) Invalid packet received')
            return
        data_split = data.split('=')
        try:
            (prefix, class_, cmd, data) = (data_split[0][0], data_split[0][1], data_split[0][2:], data_split[1])
        except ValueError as e:
            log.warn('(%s) Invalid packet - expected header + command + data' % self.ip)
            log.warn('(%s) Received data: "%s"' % (self.ip, read))
            self.change_status(E_INVALID_DATA)
            return

        if not self.check_command(cmd):
            log.warn('(%s) Invalid packet - unknown command "%s"' % self.ip, cmd)
            return
        return self.process_command(cmd, data)

    @pyqtSlot(int)
    def get_error(self, err):
        """
        Process error from SocketError signal
        """
        log.debug('(%s) get_error(err=%s): %s' % (self.ip, err, self.errorString()))
        if err <= 18:
            # QSocket errors. Redefined in projectorconstants so we don't mistake
            # them for system errors
            check = err + E_CONNECTION_REFUSED
            self.timer.stop()
        else:
            check = err
        if check < E_GENERAL:
            # Some system error?
            self.change_status(err, self.errorString())
        else:
            self.change_status(E_NETWORK, self.errorString())
        return

    def send_command(self, cmd, opts='?', salt=None):
        """
        Socket interface to send commands to projector.
        """
        if self.state() != self.ConnectedState:
            log.warn('(%s) send_command(): Not connected - returning' % self.ip)
            return
        self.projectorNetwork.emit(S_NETWORK_SENDING)
        log.debug('(%s) Sending cmd="%s" opts="%s" %s' % (self.ip,
                                                          cmd,
                                                          opts,
                                                          '' if salt is None else 'with hash'))
        if salt is None:
            out = '%s%s %s%s' % (PJLINK_HEADER, cmd, opts, CR)
        else:
            out = '%s%s %s%s' % (salt, cmd, opts, CR)
        sent = self.write(out)
        self.waitForBytesWritten(5000)  # 5 seconds should be enough
        if sent == -1:
            # Network error?
            self.projectorNetwork.emit(S_NETWORK_RECEIVED)
            self.change_status(E_NETWORK, 'Error while sending data to projector')

    def process_command(self, cmd, data):
        """
        Verifies any return error code. Calls the appropriate command handler.
        """
        log.debug('(%s) Processing command "%s"' % (self.ip, cmd))
        if data in PJLINK_ERRORS:
            # Oops - projector error
            if data.upper() == 'ERRA':
                # Authentication error
                self.change_status(E_AUTHENTICATION)
                return
            elif data.upper() == 'ERR1':
                # Undefined command
                self.change_status(E_UNDEFINED, 'Undefined command: "%s"' % cmd)
                return
            elif data.upper() == 'ERR2':
                # Invalid parameter
                self.change_status(E_PARAMETER)
                return
            elif data.upper() == 'ERR3':
                # Projector busy
                self.change_status(E_UNAVAILABLE)
                return
            elif data.upper() == 'ERR4':
                # Projector/display error
                self.change_status(E_PROJECTOR)
                return

        # Command succeeded - no extra information
        if data.upper() == 'OK':
            log.debug('(%s) Command returned OK' % self.ip)
            return

        if cmd in self.PJLINK1_FUNC:
            return self.PJLINK1_FUNC[cmd](data)
        else:
            log.warn('(%s) Invalid command %s' % (self.ip, cmd))

    def process_lamp(self, data):
        """
        Lamp(s) status. See PJLink Specifications for format.
        """
        lamps = []
        data_dict = data.split()
        while data_dict:
            fill = {'Hours': int(data_dict[0]), 'On': False if data_dict[1] == '0' else True}
            lamps.append(fill)
            data_dict.pop(0)  # Remove lamp hours
            data_dict.pop(0)  # Remove lamp on/off
        self.lamp = lamps
        return

    def process_powr(self, data):
        """
        Power status. See PJLink specification for format.
        """
        if data in PJLINK_POWR_STATUS:
            self.power = PJLINK_POWR_STATUS[data]
            self.change_status(PJLINK_POWR_STATUS[data])
        else:
            # Log unknown status response
            log.warn('Unknown power response: %s' % data)
        return

    def process_avmt(self, data):
        """
        Shutter open/closed. See PJLink specification for format.
        """
        if data == '11':
            self.shutter = True
            self.mute = False
        elif data == '21':
            self.shutter = False
            self.mute = True
        elif data == '30':
            self.shutter = False
            self.mute = False
        elif data == '31':
            self.shutter = True
            self.mute = True
        else:
            log.warn('Unknown shutter response: %s' % data)
        return

    def process_inpt(self, data):
        """
        Current source input selected. See PJLink specification for format.
        """
        self.source = data
        return

    def process_clss(self, data):
        """
        PJLink class that this projector supports. See PJLink specification for format.
        """
        self.pjlink_class = data
        log.debug('(%s) Setting pjlink_class for this projector to "%s"' % (self.ip, self.pjlink_class))
        return

    def process_name(self, data):
        """
        Projector name set by customer.
        """
        self.pjlink_name = data
        return

    def process_inf1(self, data):
        """
        Manufacturer name set by manufacturer.
        """
        self.manufacturer = data
        return

    def process_inf2(self, data):
        """
        Projector Model set by manufacturer.
        """
        self.model = data
        return

    def process_info(self, data):
        """
        Any extra info set by manufacturer.
        """
        self.other_info = data
        return

    def process_inst(self, data):
        """
        Available source inputs. See PJLink specification for format.
        """
        sources = []
        check = data.split()
        for source in check:
            sources.append(source)
        self.source_available = sources
        return

    def process_erst(self, data):
        """
        Error status. See PJLink Specifications for format.
        """
        if int(data) == 0:
            self.projector_errors = None
        else:
            self.projector_errors = {}
            # Fan
            if data[0] != '0':
                self.projector_errors[translate('OpenLP.ProjectorPJLink', 'Fan')] = \
                    PJLINK_ERST_STATUS[data[0]]
            # Lamp
            if data[1] != '0':
                self.projector_errors[translate('OpenLP.ProjectorPJLink', 'Lamp')] =  \
                    PJLINK_ERST_STATUS[data[1]]
            # Temp
            if data[2] != '0':
                self.projector_errors[translate('OpenLP.ProjectorPJLink', 'Temperature')] =  \
                    PJLINK_ERST_STATUS[data[2]]
            # Cover
            if data[3] != '0':
                self.projector_errors[translate('OpenLP.ProjectorPJLink', 'Cover')] =  \
                    PJLINK_ERST_STATUS[data[3]]
            # Filter
            if data[4] != '0':
                self.projector_errors[translate('OpenLP.ProjectorPJLink', 'Filter')] =  \
                    PJLINK_ERST_STATUS[data[4]]
            # Other
            if data[5] != '0':
                self.projector_errors[translate('OpenLP.ProjectorPJLink', 'Other')] =  \
                    PJLINK_ERST_STATUS[data[5]]
        return

    def connect_to_host(self):
        """
        Initiate connection.
        """
        if self.state() == self.ConnectedState:
            log.warn('(%s) connect_to_host(): Already connected - returning' % self.ip)
            return
        self.change_status(S_CONNECTING)
        self.connectToHost(self.ip, self.port if type(self.port) is int else int(self.port))

    @pyqtSlot()
    def disconnect_from_host(self):
        """
        Close socket and cleanup.
        """
        if self.state() != self.ConnectedState:
            log.warn('(%s) disconnect_from_host(): Not connected - returning' % self.ip)
            return
        self.disconnectFromHost()
        try:
            self.readyRead.disconnect(self.get_data)
        except TypeError:
            pass
        self.change_status(S_NOT_CONNECTED)
        self.timer.stop()

    def get_available_inputs(self):
        """
        Send command to retrieve available source inputs.
        """
        return self.send_command(cmd='INST')

    def get_error_status(self):
        """
        Send command to retrieve currently known errors.
        """
        return self.send_command(cmd='ERST')

    def get_input_source(self):
        """
        Send command to retrieve currently selected source input.
        """
        return self.send_command(cmd='INPT')

    def get_lamp_status(self):
        """
        Send command to return the lap status.
        """
        return self.send_command(cmd='LAMP')

    def get_manufacturer(self):
        """
        Send command to retrieve manufacturer name.
        """
        return self.send_command(cmd='INF1')

    def get_model(self):
        """
        Send command to retrieve the model name.
        """
        return self.send_command(cmd='INF2')

    def get_name(self):
        """
        Send command to retrieve name as set by end-user (if set).
        """
        return self.send_command(cmd='NAME')

    def get_other_info(self):
        """
        Send command to retrieve extra info set by manufacturer.
        """
        return self.send_command(cmd='INFO')

    def get_power_status(self):
        """
        Send command to retrieve power status.
        """
        return self.send_command(cmd='POWR')

    def get_shutter_status(self):
        """
        Send command to retrive shutter status.
        """
        return self.send_command(cmd='AVMT')

    def set_input_source(self, src=None):
        """
        Verify input source available as listed in 'INST' command,
        then send the command to select the input source.
        """
        if self.source_available is None:
            return
        elif src not in self.source_available:
            return
        self.send_command(cmd='INPT', opts=src)
        self.waitForReadyRead()
        self.poll_loop()

    def set_power_on(self):
        """
        Send command to turn power to on.
        """
        self.send_command(cmd='POWR', opts='1')
        self.waitForReadyRead()
        self.poll_loop()

    def set_power_off(self):
        """
        Send command to turn power to standby.
        """
        self.send_command(cmd='POWR', opts='0')
        self.waitForReadyRead()
        self.poll_loop()

    def set_shutter_closed(self):
        """
        Send command to set shutter to closed position.
        """
        self.send_command(cmd='AVMT', opts='11')
        self.waitForReadyRead()
        self.poll_loop()

    def set_shutter_open(self):
        """
        Send command to set shutter to open position.
        """
        self.send_command(cmd='AVMT', opts='10')
        self.waitForReadyRead()
        self.poll_loop()
