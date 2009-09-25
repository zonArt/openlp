# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from sqlalchemy import Column, Table, types

from openlp.plugins.audit.lib.meta import metadata

# Definition of the "songs" table
audit_table = Table(u'audit_data', metadata,
    Column(u'id', types.Integer(), primary_key=True),
    Column(u'auditdate', types.Date, index=True, nullable=False),
    Column(u'audittime', types.Time, index=True, nullable=False),
    Column(u'title', types.Unicode(255), nullable=False),
    Column(u'authors', types.Unicode(255), nullable=False),
    Column(u'copyright', types.Unicode(255)),
    Column(u'ccl_number', types.Unicode(65))
)
