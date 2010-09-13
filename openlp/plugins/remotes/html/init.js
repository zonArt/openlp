/*****************************************************************************
 * OpenLP - Open Source Lyrics Projection                                    *
 * ------------------------------------------------------------------------- *
 * Copyright (c) 2008-2010 Raoul Snyman                                      *
 * Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael    *
 * Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin    *
 * Thompson, Jon Tibble, Carsten Tinggaard                                   *
 * ------------------------------------------------------------------------- *
 * This program is free software; you can redistribute it and/or modify it   *
 * under the terms of the GNU General Public License as published by the     *
 * Free Software Foundation; version 2 of the License.                       *
 *                                                                           *
 * This program is distributed in the hope that it will be useful, but       *
 * WITHOUT ANY WARRANTY; without even the implied warranty of                *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General  *
 * Public License for more details.                                          *
 *                                                                           *
 * You should have received a copy of the GNU General Public License along   *
 * with this program; if not, write to the Free Software Foundation, Inc.,   *
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA                     *
 *****************************************************************************/

/**
 * init.js - In certain browsers (yes, IE, I'm looking at you!), DocumentReady
 * JavaScript functions can only be run very last on the page. This file is the
 * last JavaScript file to be included on the page, and provides a work-around
 * for this bug in certain browsers.
 */

$(document).ready(function () {
  OpenLP.Events.init();
});